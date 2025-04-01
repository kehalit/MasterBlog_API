# Master Blog API

This is a simple REST API built using Flask to manage blog posts. It supports common operations like creating, reading, updating, deleting, and searching posts. It also includes error handling for 404 and 405 HTTP status codes.

## Features

- **CRUD Operations**: Create, Read, Update, Delete blog posts.
- **Search**: Search posts by title and content.
- **Sorting**: Sort posts by title or content in ascending or descending order.
- **Error Handling**: Custom error messages for 404 Not Found and 405 Method Not Allowed.
- **CORS Support**: Cross-Origin Resource Sharing (CORS) enabled for all routes.

## Endpoints

### `GET /api/posts`
Retrieve all blog posts. You can optionally sort the posts by title or content.

- **Query Parameters**:
  - `sort`: Sort by either `title` or `content`.
  - `direction`: Sort direction: `asc` or `desc`.

#### Example:
GET /api/posts?sort=title&direction=asc
### `POST /api/posts`
Add a new blog post. The request body must include `title` and `content`.

- **Request Body**:
  ```json
  {
    "title": "Your Post Title",
    "content": "The content of your post"
  }
## Error Handling
- 404 Not Found: When the requested resource is not found.

- 405 Method Not Allowed: When a method is not allowed for the requested route.

## Installation
To run the project locally, follow these steps:

1.Clone this repository:
    git clone https://github.com/kehalit/MasterBlog_API.git
2. Install the required dependencies:
  pip install -r requirements.txt
3. Run the application:
  backend app.py
  
## Dependencies
  - Flask
  - Flask-Cors












