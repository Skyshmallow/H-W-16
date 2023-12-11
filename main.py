import random
from flask import Flask, request, jsonify, render_template,redirect,url_for
from functions import jsonify_request, get_profiles_from_file, set_profiles_to_file


app = Flask(__name__)

@app.route("/")
def main():
    profiles = get_profiles_from_file()
    return render_template('users.html', profiles=profiles)


@app.route("/profiles")
def get_profiles():
    result = get_profiles_from_file()
    return jsonify_request(result)


@app.route("/profiles/<int:id>")
def get_profile_by_id(id):
    profiles = get_profiles_from_file()
    for profile in profiles:
        if profile.get("id") == id:
            return jsonify_request(profile)
    return jsonify_request(None, message=f"There is no such profile with that ID --> {id}")


@app.route("/profiles/create", methods=["GET", "POST"])
def create_profile():
    if request.method=="POST":
        profiles = get_profiles_from_file()
        login = request.form["login"]
        for profile in profiles:
            if profile.get("login") == login:
                return jsonify_request(None, message="This login already exists")

        age = request.form["age"]
        email = request.form["email"]

        created_profile = {
            "id": random.randrange(1, 100_000),
            "login": login,
            "age": age,
            "email": email 
        }

        profiles.append(created_profile)
        set_profiles_to_file(profiles)
        return redirect(url_for('main'))

    return render_template('create_profile.html')

@app.route("/profiles/update/<int:id>", methods=["POST"])
def update_profile_by_id(id):
    profiles = get_profiles_from_file()
    for profile in profiles:
        if profile.get("id") == id:
            for key in request.form:
                profile[key] = request.form[key]
            set_profiles_to_file(profiles)
            return redirect(url_for('profile_details', id=id))
    return jsonify_request(None, message=f"There is no such id: {id}")


@app.route("/profiles/delete/<int:id>", methods = ["POST"])
def delete_profile_by_id(id):
    profiles = get_profiles_from_file()

    for i in range(len(profiles)):
        if profiles[i].get("id") == id:
            profiles.pop(i)
            set_profiles_to_file(profiles)
            return redirect(url_for('main'))
        
    
    return jsonify_request(False, message=f"There is no such id to delete: {id}")


@app.route("/profiles/details/<int:id>")
def profile_details(id):
    profiles = get_profiles_from_file()
    for profile in profiles:
        if profile.get("id") == id:
            return render_template('profile_details.html', profile=profile)
    return render_template('profile_details.html', profile=None, message=f"There is no such profile with that ID --> {id}")


if __name__ == '__main__':
    app.run(debug=True)

    