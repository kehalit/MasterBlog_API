
from flask import Flask, jsonify, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
    {"id": 3, "title": "Post 3", "content": "This is the third post."}
]

@app.errorhandler(404)
def not_found_error(error):
    message = error.description if error.description else "Not Found"
    return jsonify({"error": message}), 404

@app.errorhandler(405)
def method_not_allowed_error(error):
    return jsonify({"error": "Method Not Allowed"}), 405

def validate_posts_data(data):
    if "title" not in data or "content" not in data:
        return False
    return True


def find_post_by_id(post_id):

    for post in POSTS:
        if post['id'] == post_id:
            return post

    return None

@app.route('/api/posts', methods=['GET'])
def get_posts():

    # Get the sort and direction from the query string
    sort_by = request.args.get('sort')
    direction = request.args.get('direction')

    if sort_by and direction:

        if sort_by not in ['title', 'content']:
            return jsonify({"error": "Invalid sort field"}), 400
        if direction not in ['asc', 'desc']:
            return jsonify({"error": "Invalid sort direction"}), 400

        reverse = direction == 'desc'
        POSTS.sort(key=lambda post: post.get(sort_by, ''), reverse=reverse)

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


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
        # Find the post with the given ID
    post = find_post_by_id(id)
        # If the post wasn't found, return a 404 error
    if post is None:
        abort(404, description=f'post with id {id} is not found.')

    POSTS.remove(post)
    return jsonify({'message': f'post with id {id} has been deleted successfully.'}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    # Find the post with the given ID
    post = find_post_by_id(id)

    # If the post wasn't found, return a 404 error
    if post is None:
        abort(404, description=f'post with id {id} is not found.')

    # Update the post with the new data
    new_data = request.get_json()
    post.update(new_data)

    # Return the updated post
    return jsonify({'message': f'post with id {id} has been updated successfully. '}), 200

@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title = request.args.get('title')
    if title:
        filtered_post = [post for post in POSTS if post.get('title') == title]
        return  jsonify(filtered_post)
    else:

        return jsonify(POSTS)




    # Return the posts (sorted or unsorted)
    return jsonify(POSTS)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005, debug=True)
