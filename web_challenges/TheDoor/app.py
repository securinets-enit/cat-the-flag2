from flask import Flask, request, jsonify, render_template_string
import jwt
import os
import hashlib
import json

app = Flask(__name__)

# JWT secret - this is what we need to leak!
JWT_SECRET = "d3bug_s3cr3t_k3y_f0r_d3v3l0pm3nt_0nly_d0_n0t_us3_in_pr0d"

# Simulated database
documents = {
    "lolo": {
        "doc_001": {"title": "CIA backlog", "content": "ken 3andek backlog ab3eth"},
        "doc_002": {"title": "F22 raptor designs", "content": "Jad 3lik sehla heyya"}
    },
    "Messi": {
        "doc_003": {"title": "How to be the Goat", "content": "I don't know ask CR7"},
        "doc_004": {"title": "Ballon d or robbery tricks", "content": "SecurinetsENIT{987b679bbeb4b5314f8297f4e8a63ed5}"}
    }
}

# HTML template with complete API documentation
INDEX_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Secure Document Vault API</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
        h1 { color: #2c3e50; }
        h2 { color: #34495e; margin-top: 30px; }
        .endpoint { background: #f8f9fa; padding: 15px; margin: 10px 0; border-left: 4px solid #3498db; }
        .method { display: inline-block; background: #e74c3c; color: white; padding: 2px 8px; border-radius: 3px; font-weight: bold; }
        .method.get { background: #27ae60; }
        .method.post { background: #2980b9; }
        code { background: #ecf0f1; padding: 2px 6px; border-radius: 3px; }
        .note { background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; margin: 10px 0; border-radius: 4px; }
    </style>
</head>
<body>
    <h1>Secure Document Vault API</h1>

    <p>Welcome to the Secure Document Vault API. This service allows authenticated users to manage their private documents.</p>

    <div class="note">
        <strong>Authentication:</strong> All protected endpoints require a Bearer token in the Authorization header:<br>
        <code>Authorization: Bearer <your_jwt_token></code>
    </div>

    <h2>Authentication Endpoints</h2>

    <div class="endpoint">
        <span class="method post">POST</span> <strong>/login</strong><br>
        <strong>Description:</strong> Authenticate a user and receive a JWT token<br>
        <strong>Request Body:</strong> <code>{"username": "string"}</code><br>
        <strong>Response:</strong> <code>{"token": "jwt_token_string"}</code><br>
        <strong>Valid Users:</strong> <code>lolo</code>, <code>Messi</code>
    </div>

    <h2>Document Management Endpoints</h2>

    <div class="endpoint">
        <span class="method get">GET</span> <strong>/documents</strong><br>
        <strong>Description:</strong> List all documents accessible to the authenticated user<br>
        <strong>Response:</strong> <code>{"documents": [{"id": "string", "title": "string"}]}</code>
    </div>

    <div class="endpoint">
        <span class="method get">GET</span> <strong>/document/<doc_id></strong><br>
        <strong>Description:</strong> Retrieve a specific document by ID<br>
        <strong>Path Parameter:</strong> <code>doc_id</code> (string)<br>
        <strong>Response:</strong> <code>{"id": "string", "title": "string", "content": "string"}</code>
    </div>

    <h2>Debug & Configuration Endpoints</h2>


    <div class="endpoint">
        <span class="method get">GET</span> <strong>/debug/logs</strong><br>
        <strong>Description:</strong> Debug logs endpoint with verbose error reporting<br>
        <strong>Query Parameter:</strong> <code>show_error=true</code> to trigger detailed error messages<br>
        <strong>Note:</strong> May contain sensitive information in error responses
    </div>

    <div class="note">
        <strong>Security Note:</strong> This API implements strict access controls. 
        Users can only access their own documents. Attempting to access another user's 
        documents will result in a 403 Forbidden error.
    </div>
</body>
</html>
"""


def require_auth(f):
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            request.user_id = payload['user_id']
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    decorated_function.__name__ = f.__name__
    return decorated_function


@app.route('/')
def index():
    """Main page with complete API documentation"""
    return render_template_string(INDEX_TEMPLATE)


@app.route('/login', methods=['POST'])
def login():
    """Login endpoint - returns JWT token"""
    data = request.get_json()
    username = data.get('username')

    if username not in documents:
        return jsonify({"error": "User not found"}), 404

    token = jwt.encode({'user_id': username}, JWT_SECRET, algorithm='HS256')
    return jsonify({"token": token})


@app.route('/documents', methods=['GET'])
@require_auth
def list_documents():
    """List documents accessible to user"""
    user_docs = documents.get(request.user_id, {})
    doc_list = []
    for doc_id, doc_info in user_docs.items():
        doc_list.append({
            "id": doc_id,
            "title": doc_info["title"]
        })
    return jsonify({"documents": doc_list})


@app.route('/document/<doc_id>', methods=['GET'])
@require_auth
def get_document(doc_id):
    """Get specific document - proper access control"""
    user_docs = documents.get(request.user_id, {})
    if doc_id not in user_docs:
        return jsonify({"error": "Document not found or access denied"}), 403

    return jsonify({
        "id": doc_id,
        "title": user_docs[doc_id]["title"],
        "content": user_docs[doc_id]["content"]
    })


# VULNERABLE ENDPOINT THAT LEAKS THE SECRET
@app.route('/config')
def get_config():
    """
    Debug endpoint that accidentally leaks configuration
    Only accessible with special User-Agent header
    """
    user_agent = request.headers.get('User-Agent', '')

    if 'Internal-Debug-Tool' in user_agent:
        # Return configuration including the JWT secret
        config = {
            "app_name": "Secure Document Vault",
            "version": "1.2.3",
            "debug_mode": True,
            "jwt_secret": JWT_SECRET,  # <-- SECRET LEAKED HERE!
            "database_type": "in-memory"
        }
        return jsonify(config)
    else:
        return jsonify({"error": "Access denied. Internal endpoint only."}), 403


# ALTERNATIVE LEAK METHOD - through error messages
@app.route('/debug/logs')
def debug_logs():
    """
    Debug endpoint that leaks secret through verbose error messages
    """
    if request.args.get('show_error') == 'true':
        try:
            # This will cause an error that includes the secret
            invalid_operation = JWT_SECRET + 123
        except Exception as e:
            # Insecure error handling - leaks secret in error message
            return jsonify({
                "error": f"Internal server error: cannot concatenate str and int: '{JWT_SECRET}' + 123",
                "traceback": "..."
            }), 500

    return jsonify({"message": "Debug logs endpoint. Add ?show_error=true to see error details."})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8010, debug=False)
