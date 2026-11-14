# Cookie & Session Security Lab

교육용 쿠키/세션 데모입니다. 실제 계정 인증정보나 다른 사이트의 쿠키를 읽거나 전송하지 않습니다.

## Run locally
```bash
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## Deploy on Render
1. Render에서 **New + → Web Service**를 선택합니다.
2. GitHub 저장소 `meifactory1-png/cookie-session-lab`를 연결합니다.
3. Runtime: Python, Build Command: `pip install -r requirements.txt`, Start Command: `gunicorn app:app`
4. Free 플랜으로 생성하고 배포가 끝나면 Render가 제공하는 `.onrender.com` 주소를 공유합니다.

The demo issues only a synthetic random cookie named `demo_session`, with HttpOnly and SameSite=Lax. It never reads cookies belonging to other websites.
