from flask import jsonify
import json

class UserController:

    def __init__(self):
        # Define the user data structure
        self.user_schema = {
            "id": str,
            "username": str,
            "dob":str,
            "email": str,
            "aadhar":str,
            "mobile":str,
            "plan_id":str,
            "active":str
        }

    def load_users(self):
        """Loads user data from the JSON file."""
        try:
            with open("db.json", "r") as f:
                data = json.load(f)
            return data
        except (FileNotFoundError, json.JSONDecodeError):
            return []  # Return empty list if file not found or invalid JSON

    def save_users(self, data):
        """Saves user data to the JSON file."""
        with open("db.json", "w") as f:
            json.dump(data, f, indent=4)

    def generate_next_id(self, users):
        """Generates the next available user ID."""
        if not users:
            return 1
        return max(user["id"] for user in users) + 1

    def get_users(self):
        users = self.load_users()
        return jsonify({"data":users}), 200  # OK

    def create_user(self, new_user):
        try:
            if not new_user or not all(key in new_user for key in self.user_schema):
                return jsonify({"error": "Invalid user data"}), 400  # Bad Request

            users = self.load_users()
            new_user["id"] = self.generate_next_id(users)
            users.append(new_user)
            self.save_users(users)
            return jsonify(new_user), 201  # Created

        except (json.JSONDecodeError, KeyError):
            return jsonify({"error": "Invalid JSON data"}), 400  # Bad Request

    def get_user(self, user_id):
        users = self.load_users()
        user = [u for u in users if u["id"] == user_id]
        if not user:
            return jsonify({"error": "User not found"}), 404  # Not Found
        return jsonify({"data":user[0]}), 200  # OK

    def update_user(self, user_id, updated_user):
        try:
            if not updated_user or not all(key in updated_user for key in self.user_schema):
                return jsonify({"error": "Invalid user data"}), 400  # Bad Request

            users = self.load_users()
            for i, user in enumerate(users):
                if user["id"] == user_id:
                    users[i] = updated_user  # Update user data
                    self.save_users(users)
                    return jsonify(updated_user), 200  # OK
            return jsonify({"error": "User not found"}), 404  # Not Found

        except (json.JSONDecodeError, KeyError):
            return jsonify({"error": "Invalid JSON data"}), 400  # Bad Request
    
