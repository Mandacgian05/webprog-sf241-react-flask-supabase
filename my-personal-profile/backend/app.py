import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client

app = Flask(__name__)

# Allow all origins so your Vercel frontend can connect
CORS(app, resources={r"/*": {"origins": "*"}})

# Supabase setup
# Ensure these names match your Render Environment Variables EXACTLY
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

@app.route('/', methods=['GET'])
def home():
    """Root route to confirm the API is live."""
    return jsonify({
        "status": "online",
        "message": "Flask Guestbook API is active",
        "usage": "Send GET or POST requests to /guestbook"
    }), 200

@app.route('/guestbook', methods=['GET'])
def get_entries():
    """Fetch all entries from Supabase."""
    try:
        # Note: 'guestbook' must match your table name in Supabase exactly
        response = supabase.table("guestbook").select("*").order("created_at", desc=True).execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/guestbook', methods=['POST'])
def add_entry():
    """Add a new entry to Supabase."""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        response = supabase.table("guestbook").insert(data).execute()
        return jsonify(response.data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/guestbook/<id>', methods=['PUT'])
def update_entry(id):
    try:
        data = request.json
        response = supabase.table("guestbook").update(data).eq("id", id).execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/guestbook/<id>', methods=['DELETE'])
def delete_entry(id):
    try:
        supabase.table("guestbook").delete().eq("id", id).execute()
        return jsonify({"message": "Deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Render uses the PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)