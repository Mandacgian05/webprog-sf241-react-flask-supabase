import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client

app = Flask(__name__)
CORS(app) # Crucial for allowing Vercel to talk to Render

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

@app.route('/guestbook', methods=['GET'])
def get_entries():
    response = supabase.table("guestbook").select("*").order("created_at", desc=True).execute()
    return jsonify(response.data)

@app.route('/guestbook', methods=['POST'])
def add_entry():
    data = request.json
    response = supabase.table("guestbook").insert(data).execute()
    return jsonify(response.data), 201

@app.route('/guestbook/<id>', methods=['PUT'])
def update_entry(id):
    data = request.json
    response = supabase.table("guestbook").update(data).eq("id", id).execute()
    return jsonify(response.data)

@app.route('/guestbook/<id>', methods=['DELETE'])
def delete_entry(id):
    supabase.table("guestbook").delete().eq("id", id).execute()
    return jsonify({"message": "Deleted successfully"}), 200

if __name__ == '__main__':
    # Use the PORT variable provided by Render, default to 5000 for local dev
    port = int(os.environ.get("PORT", 5000))
    # Must bind to 0.0.0.0 for Render to detect the port
    app.run(host='0.0.0.0', port=port)