# post_service.py

from flask import Flask, jsonify, request
import requests

app = Flask(__name__)
comments = {
        '1': {'user_id': '1', 'post_id': '2', 'comment':'Hello, world!'},
        '2': {'user_id': '2', 'post_id': '2', 'comment':'Hello, world! Amazing port'},
}
@app.route('/')
def hello():
    return "i am live now"

@app.route('/comment/<id>')
def comment(id):
   
    comment_info = comments.get(id, {})
    print(comment_info)
    try:
        # Get user info from User Service
        if comment_info:
            response = requests.get(f'http://localhost:5000/user/{comment_info["user_id"]}')
            print(comment_info)
            print(response)
            if response.status_code == 200:
                comment_info['user'] = response.json()

            response = requests.get(f'http://localhost:5001/post/{comment_info["post_id"]}')
            
            if response.status_code == 200:
                comment_info['post'] = response.json()
    except Exception as e:
        # Handle the exception, you can log the error or return an error response
        return jsonify({'error': str(e)}), 500  # Return an error response with status code 500 for example

    return jsonify(comment_info)

@app.route('/comment', methods=['POST'])
def create_comment():
    new_comment = request.get_json()
    
    # Define a list of required keys
    required_keys = ['user_id', 'post_id', 'comment']

    # Check if all required keys exist in the request data
    if all(key in new_comment for key in required_keys):
        comments[str(len(comments.keys()) + 1)] = new_comment
        print(comments)
        return jsonify({"success":True})
    else:
        return jsonify({"success":False, "msg": "Please pass all the data"})

if __name__ == '__main__':
    app.run()