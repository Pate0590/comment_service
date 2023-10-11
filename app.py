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
       
        if comment_info:
            response = requests.get(f'https://ankituserservice.azurewebsites.net/user/{comment_info["user_id"]}')
            print(comment_info)
            print(response)
            if response.status_code == 200:
                comment_info['user'] = response.json()

            response = requests.get(f'https://ankitpostservice.azurewebsites.net/post/{comment_info["post_id"]}')
            
            if response.status_code == 200:
                comment_info['post'] = response.json()
    except Exception as e:
        
        return jsonify({'error': str(e)}), 500  

    return jsonify(comment_info)

@app.route('/comment', methods=['POST'])
def create_comment():
    new_comment = request.get_json()
    required_keys = ['user_id', 'post_id', 'comment']
    if all(key in new_comment for key in required_keys):
        comments[str(len(comments.keys()) + 1)] = new_comment
        print(comments)
        return jsonify({"success":True})
    else:
        return jsonify({"success":False, "msg": "Please pass all the data"})
    
@app.route('/comment/<id>', methods=['PUT'])
def update_comment(id):
    
    if id in comments:
        updated_comment = request.get_json()
        required_keys = ['user_id', 'post_id', 'comment']
        if all(key in updated_comment for key in required_keys):
            comments[id] = updated_comment
            print(comments)
            return jsonify({"success": True, "msg": "Comment updated successfully"})
        else:
            return jsonify({"success": False, "msg": "Please pass all the required data for update"}), 400
    else:
        return jsonify({"success": False, "msg": "Comment not found"}), 404
    
@app.route('/comment/<id>', methods=['DELETE'])
def delete_comment(id):
    if id in comments:
        del comments[id]
        return jsonify({"success": True, "msg": "Comment deleted successfully"})
    else:
        return jsonify({"success": False, "msg": "Comment not found"}), 404



if __name__ == '__main__':
    app.run('0.0.0.0',port=5003)