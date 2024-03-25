from flask import Flask, request
from flask_cors import CORS
from controllers.Usercontroller import UserController


app = Flask(__name__)
CORS(app)
user_controller = UserController()  
@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        return user_controller.get_users()
    elif request.method == "POST":
        new_user = request.get_json()
        return user_controller.create_user(new_user)

@app.route("/users/<int:user_id>", methods=["GET", "PUT"])
def user(user_id):
    if request.method == "GET":
        return user_controller.get_user(user_id)
    elif request.method == "PUT":
        updated_user = request.get_json()
        return user_controller.update_user(user_id, updated_user)

if __name__ == "__main__":
    app.run(debug=True)
