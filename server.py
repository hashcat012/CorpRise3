import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, auth

# Sabit key ve path (frontend ile uyumlu)
SECRET_KEY = "AAA6C4A1227CBE4FFC5589E38BD64AA7303E3070B522D1BA47375643B8FB9781"
FIREBASE_CREDENTIALS_PATH = "C:/Users/Acer/Desktop/emergent-titanos-original - Kopya/backend/titanos-19c4d-firebase-adminsdk-fbsvc-5d5341bbf8.json"

# Firebase admin başlat
cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
firebase_admin.initialize_app(cred)

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Health check
@app.route("/api/health")
def health():
    return jsonify({"status": "ok"}), 200

# Session oluşturma
@app.route("/api/auth/session", methods=["POST"])
def create_session():
    data = request.get_json()
    id_token = data.get("session_id")
    if not id_token:
        return jsonify({"error": "No token provided"}), 400

    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token["uid"]
        user_record = auth.get_user(uid)
        user_info = {
            "uid": user_record.uid,
            "email": user_record.email,
            "displayName": user_record.display_name,
        }
        return jsonify(user_info), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

# Kullanıcı bilgisi
@app.route("/api/auth/me", methods=["GET"])
def me():
    id_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not id_token:
        return jsonify({"error": "No token provided"}), 401
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token["uid"]
        user_record = auth.get_user(uid)
        user_info = {
            "uid": user_record.uid,
            "email": user_record.email,
            "displayName": user_record.display_name,
        }
        return jsonify(user_info), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)