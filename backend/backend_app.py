from certifi import contents
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not Found"}), 404

@app.errorhandler(405)
def method_not_allowed_error(error):
    return jsonify({"error": "Method Not Allowed"}), 405

def validate_posts_data(data):
    if "title" not in data or "content" not in data:
        return False
    return True

@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_new_blog_post():

    new_post = request.get_json()
    if not validate_posts_data(new_post):
        return jsonify({"error": "Invalid book data"}), 400

        # Generate a new ID for the post
    new_id = max(post['id'] for post in POSTS) + 1
    new_post['id'] = new_id

    POSTS.append(new_post)
    return jsonify(POSTS), 201



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005, debug=True)
