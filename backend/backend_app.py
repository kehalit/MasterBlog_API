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
    """
        Error handler for 404 Not Found.

        This function is called when a 404 error occurs, returning a JSON response with an
        error message. If a custom error message is provided, it will be used; otherwise,
        a generic "Not Found" message is returned.

        Args:
        - error (Exception): The error that caused the 404 response.

        Returns:
        - JSON response with an error message and 404 status code.
        """
    message = error.description if error.description else "Not Found"
    return jsonify({"error": message}), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    """
        Error handler for 405 Method Not Allowed.

        This function is called when a 405 error occurs, returning a JSON response with
        a message indicating that the method is not allowed.

        Args:
        - error (Exception): The error that caused the 405 response.

        Returns:
        - JSON response with an error message and 405 status code.
        """
    return jsonify({"error": "Method Not Allowed"}), 405


def validate_posts_data(data):
    """
        Validate the data for creating or updating a blog post.

        This function checks whether the provided data contains both 'title' and 'content'
        keys, which are required for a valid blog post.

        Args:
        - data (dict): The data to be validated.

        Returns:
        - bool: True if the data is valid, otherwise False.
        """
    if "title" not in data or "content" not in data:
        return False
    return True


def find_post_by_id(post_id):
    """
        Find a post by its ID.

        This function searches through the list of posts and returns the post that matches
        the given ID. If no post is found, it returns None.

        Args:
        - post_id (int): The ID of the post to be searched.

        Returns:
        - dict or None: The post with the specified ID, or None if not found.
        """
    for post in POSTS:
        if post['id'] == post_id:
            return post

    return None


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
        Retrieve all blog posts, optionally sorted by title or content.

        This endpoint returns a list of all blog posts, which can be optionally sorted by
        either 'title' or 'content' in ascending or descending order. If no sorting parameters
        are provided, the posts are returned in their original order.

        Query Parameters:
        - sort (str): The field by which to sort the posts. Can be 'title' or 'content'.
        - direction (str): The direction of sorting. Can be 'asc' or 'desc'.

        Returns:
        - JSON response containing the list of posts.
        """
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
    """
       Add a new blog post.

       This endpoint allows the creation of a new blog post. The post data must contain
       both a 'title' and 'content' field. A new post ID is automatically assigned, and
       the post is added to the list of posts.

       Request Body:
       - title (str): The title of the blog post.
       - content (str): The content of the blog post.

       Returns:
       - JSON response with the list of all posts and a 201 status code if successful.
       """
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
    """
        Delete a blog post by its ID.

        This endpoint deletes a post with the given ID. If the post with the specified ID
        is not found, a 404 error is raised. On successful deletion, a success message is returned.

        Args:
        - id (int): The ID of the post to be deleted.

        Returns:
        - JSON response with a success message and 200 status code if successful.
        """
    post = find_post_by_id(id)
        # If the post wasn't found, return a 404 error
    if post is None:
        abort(404, description=f'post with id {id} is not found.')

    POSTS.remove(post)
    return jsonify({'message': f'post with id {id} has been deleted successfully.'}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    """
        Update a blog post by its ID.

        This endpoint allows the updating of an existing blog post. The post with the given
        ID is updated with the new data provided in the request body. If the post is not found,
        a 404 error is raised.

        Args:
        - id (int): The ID of the post to be updated.

        Request Body:
        - title (str): The new title of the blog post.
        - content (str): The new content of the blog post.

        Returns:
        - JSON response with a success message and 200 status code if successful.
        """
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
    """
        Search for blog posts by title.

        This endpoint allows searching for blog posts based on the provided title. If a 'title'
        query parameter is specified, it returns all posts that match the given title.

        Query Parameters:
        - title (str): The title of the post to search for.

        Returns:
        - JSON response containing a list of posts that match the search criteria.
        """
    title = request.args.get('title')
    if title:
        filtered_post = [post for post in POSTS if post.get('title') == title]
        return  jsonify(filtered_post)
    else:
        return jsonify(POSTS)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005, debug=True)
