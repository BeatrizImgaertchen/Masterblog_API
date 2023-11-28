from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    sort_by = request.args.get('sort')
    direction = request.args.get('direction')

    # Perform sorting based on the provided parameters
    if sort_by and direction:
        if sort_by == 'title':
            POSTS.sort(key=lambda x: x['title'], reverse=(direction == 'desc'))
        elif sort_by == 'content':
            POSTS.sort(key=lambda x: x['content'], reverse=(direction == 'desc'))
        else:
            response = {
                "error": "Invalid sort field. Please use 'title' or 'content'."
            }
            return jsonify(response), 400

    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()

    if 'title' not in data or 'content' not in data:
        response = {
            "error": "Title and content are required fields."
        }
        return jsonify(response), 400

    new_post = {
        "id": len(POSTS) + 1,
        "title": data['title'],
        "content": data['content']
    }

    POSTS.append(new_post)

    response = {
        "id": new_post['id'],
        "title": new_post['title'],
        "content": new_post['content']
    }
    return jsonify(response), 201


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()

    for post in POSTS:
        if post['id'] == post_id:
            if 'title' in data:
                post['title'] = data['title']
            if 'content' in data:
                post['content'] = data['content']

            response = {
                "id": post['id'],
                "title": post['title'],
                "content": post['content']
            }
            return jsonify(response), 200

    response = {
        "error": "Post not found."
    }
    return jsonify(response), 404


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    for post in POSTS:
        if post['id'] == post_id:
            POSTS.remove(post)
            response = {
                "message": f"Post with id {post_id} has been deleted successfully."
            }
            return jsonify(response), 200

    response = {
        "error": "Post not found."
    }
    return jsonify(response), 404


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title = request.args.get('title')
    content = request.args.get('content')

    results = []
    for post in POSTS:
        if title and title.lower() in post['title'].lower():
            results.append(post)
        elif content and content.lower() in post['content'].lower():
            results.append(post)

    return jsonify(results)


@app.route('/', methods=['GET'])
def home():
    return "Welcome to the MasterBlog API"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
