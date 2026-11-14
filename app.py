import json
import os
import secrets
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, make_response, render_template, request

app = Flask(__name__)
COOKIE_NAME = "demo_session"
STORE = Path(os.environ.get("EVENT_STORE", "/tmp/cookie-lab-events.json"))


def record_event(event, marker=""):
    try:
        rows = json.loads(STORE.read_text("utf-8")) if STORE.exists() else []
    except (OSError, json.JSONDecodeError):
        rows = []
    rows.append({
        "time": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "marker": marker[:8] + "..." if marker else ""
    })
    STORE.parent.mkdir(parents=True, exist_ok=True)
    STORE.write_text(json.dumps(rows[-100:], ensure_ascii=False, indent=2), "utf-8")


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/login-demo")
def login_demo():
    # This is a randomly generated teaching token, not a real account credential.
    token = secrets.token_urlsafe(24)
    record_event("demo_session_created", token)
    response = make_response(jsonify({"ok": True, "message": "가짜 세션 쿠키를 발급했어요."}))
    response.set_cookie(
        COOKIE_NAME,
        token,
        httponly=True,
        secure=request.is_secure,
        samesite="Lax",
        max_age=1800,
    )
    return response


@app.get("/check")
def check():
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        return jsonify({"ok": False, "message": "세션 쿠키가 없어요. 먼저 체험 시작을 눌러 주세요."}), 401
    record_event("demo_session_checked", token)
    return jsonify({
        "ok": True,
        "message": "가짜 세션 쿠키가 확인됐어요.",
        "cookie": "HttpOnly로 보호됨 (페이지 JavaScript에서 읽을 수 없음)"
    })


@app.post("/logout")
def logout():
    response = make_response(jsonify({"ok": True, "message": "체험 세션을 종료했어요."}))
    response.delete_cookie(COOKIE_NAME, httponly=True, secure=request.is_secure, samesite="Lax")
    record_event("demo_session_deleted")
    return response


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=False)
