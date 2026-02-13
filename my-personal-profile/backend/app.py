import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client

app = Flask(__name__)
# Allow Vercel frontend to access this API
CORS(app) 

# Initialize Supabase
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# --- NEW ROOT ROUTE (Fixes the 404 error on the main page) ---
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "Online",
        "message": "Guestbook API is running successfully!",
        "endpoints": {
            "GET_all": "/guestbook",
            "POST_new": "/guestbook"
        }
    }), 200

# --- GUESTBOOK ROUTES ---

@app.route('/guestbook', methods=['GET'])
def get_entries():
    try:
        response = supabase.table("guestbook").select("*").order("created_at", desc=True).execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/guestbook', methods=['POST'])
def add_entry():
    try:
        data = request.json
        response = supabase.table("guestbook").insert(data).execute()
        return jsonify(response.data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/guestbook/<id>', methods=['PUT'])
def update_entry(id):
    try:
        data = request.json
        response = supabase.table("guestbook").update(data).eq("id", id).execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/guestbook/<id>', methods=['DELETE'])
def delete_entry(id):
    try:
        supabase.table("guestbook").delete().eq("id", id).execute()
        return jsonify({"message": "Deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    # Use the PORT variable provided by Render (default 10000)
    port = int(os.environ.get("PORT", 5000))
    # Bind to 0.0.0.0 so Render can route external traffic to the app
    app.run(host='0.0.0.0', port=port)