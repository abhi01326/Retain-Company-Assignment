from flask import Flask, request, jsonify
import sqlite3
import json

app = Flask(__name__)

conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()


@app.route('/')
def home():
    return "User Management System"


@app.route('/users', methods=['GET'])
#added try except block for error handling and converted raw data to json data using jsonify
def get_all_users():
    try:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        #convert user data
        users_data = []
        for user in users:
            users_data.append(
                {
                    'id': user[0],
                    'name': user[1],
                    'email': user[2]
                }
            )
        conn.close()
        return jsonify(users_data),200
    except Exception as e:
        return jsonify({'error': str(e)}),500


#added try except block for error handling and converted raw data to json data using jsonify
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        query = "SELECT * FROM users WHERE id = ?"
        cursor.execute(query, [user_id])
        user = cursor.fetchone()

        if user:
            user_data = {
                'id': user[0],
                'name': user[1],
                'email': user[2]
            }
            return jsonify(user_data), 200
        else:
            return jsonify({'error': 'User not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


#added try except block for error handling and converted raw data to json data using jsonify also changed parameters passing method
@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()

        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if not all [name,email,password]:
            return jsonify({'error': 'Missing required fields'}),400

        cursor.execute(f"INSERT INTO users (name, email, password) VALUES (?,?,?)",(name,email,password))
        conn.commit()
        return jsonify({'message': '"User created successfully!"'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


#added try except block for error handling and converted raw data to json data using jsonify
@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        name, email = data.get('name'), data.get('email')
        if not name or not email:
            return jsonify({'error': 'Name and Email are required'}), 400
        cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
        if cursor.rowcount == 0:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'message': 'User updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#added try except block for error handling and converted raw data to json data using jsonify also added status code for every response
@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        cursor.execute(f"DELETE FROM users WHERE id = ?" , [user_id])
        conn.commit()
        if cursor.rowcount==0:
            return jsonify({'error': 'User not found'}),404
        return jsonify({'message': f'User {user_id} deleted successfully'}),200
    except Exception as e:
        return jsonify({'error': str(e)}),500


@app.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name')

    if not name:
        return jsonify({'error': 'Please provide a name to search'})

    try:
        cursor.execute(f"SELECT * FROM users WHERE name LIKE '%{name}%'")
        users = cursor.fetchall()
        if not users:
            return jsonify({'erorr': 'No users found'}),404
        users_data = [{'id': user[0],'name': user[1],'email': user[2]} for user in users]
        return jsonify(users_data),200
    except Exception as e:
        return jsonify({'error': str(e)}),500


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'status': 'failed', 'message': 'Email and password are required'})

        cursor.execute(f"SELECT * FROM users WHERE email = '{email}' AND password = '{password}'")
        user = cursor.fetchone()

        if user:
            return jsonify({"status": "success", 'user': {
                'id': user[0],
                'name': user[1],
                'email': user[2]
            }}), 200
        else:
            return jsonify({"status": "failed", 'message': 'Invalid email or password'}), 401
    except Exception as e:
        return jsonify({'message': str(e)}),500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)
