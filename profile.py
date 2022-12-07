from flask import Blueprint, render_template, jsonify, request, session

profile = Blueprint('profile', __name__)


@profile.route('/profile-data', methods=['GET', 'POST'])
def testfn():
    # GET request
    if request.method == 'GET':
        print(f"request from user {session['user_id']}")

        message = {'years': [2018, 2019, 2020, 2021, 2022]}
        return jsonify(message)  # serialize and use JSON headers
    # POST request
    if request.method == 'POST':
        print(request.get_json())  # parse as JSON
        return 'Sucesss', 200