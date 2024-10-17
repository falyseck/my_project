from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder='public')

comments = []
next_comment_id = 1

@app.route('/')
def index():
    print(f"Static folder: {app.static_folder}")
    print(f"Index.html exists: {os.path.exists(os.path.join(app.static_folder, 'index.html'))}")
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/comments', methods=['GET'])
def get_comments():
    print("Fetching comments:", comments)  # Debug print
    return jsonify(comments)

@app.route('/api/comments', methods=['POST'])
def add_comment():
    global next_comment_id
    data = request.json
    print("Received data:", data)  # Debug print
    if 'text' in data and isinstance(data['text'], str):
        new_comment = {'id': next_comment_id, 'text': data['text']}
        comments.append(new_comment)
        next_comment_id += 1
        print("Added new comment:", new_comment)  # Debug print
        return jsonify(new_comment), 201
    return jsonify({'error': 'Invalid comment text'}), 400

@app.route('/api/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    global comments
    original_length = len(comments)
    comments = [c for c in comments if c['id'] != comment_id]
    if len(comments) < original_length:
        print(f"Deleted comment with id {comment_id}")  # Debug print
        return '', 204
    else:
        print(f"Comment with id {comment_id} not found")  # Debug print
        return jsonify({'error': 'Comment not found'}), 404

@app.route('/script.js')
def serve_script():
    print(f"Attempting to serve script.js from {app.static_folder}")
    print(f"Does file exist? {os.path.exists(os.path.join(app.static_folder, 'script.js'))}")
    return send_from_directory(app.static_folder, 'script.js')

@app.route('/styles.css')
def serve_css():
    print(f"Attempting to serve styles.css from {app.static_folder}")
    print(f"Does file exist? {os.path.exists(os.path.join(app.static_folder, 'styles.css'))}")
    return send_from_directory(app.static_folder, 'styles.css')

if __name__ == '__main__':
    app.run(debug=True)
