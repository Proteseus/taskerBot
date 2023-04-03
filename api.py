import json
from flask import Flask, Response, request
from db import Database

app = Flask(__name__)
db = Database()


@app.route('/', methods=['GET'])
def get_members():
    members = db.fetch_members()
    return json.dumps(members)


@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = db.fetch_task()
    return json.dumps(tasks)


@app.route('/assigned', methods=['GET'])
def get_assigned():
    assigned = db.fetch_task_assigned()
    return json.dumps(assigned)


@app.route('/roles', methods=['GET'])
def get_roles():
    roles = db.fetch_roles()
    return json.dumps(roles)


@app.route('/add_member/', methods=['POST'])
def add_member():
    user = request.args.to_dict()['user']
    role = request.args.to_dict()['role']

    res = db.add_member(user, role)
    if res == 0:
        return Response("Member Added", status=200)
    else:
        return Response("Member Already in Database", status=500)


@app.route('/add_role/', methods=['POST'])
def add_role():
    role = request.args.to_dict()['role']

    res = db.add_role(role)
    if res == 0:
        return Response("Role Added", status=200)
    else:
        return Response("Role Already in Database", status=500)


@app.route('/add_task/', methods=['POST'])
def add_task():
    task = request.args.to_dict()['task']
    due = request.args.to_dict()['due']

    res = db.add_task(task, due)
    if res == 0:
        return Response("Task Added", status=200)
    else:
        return Response("Task Already in Database", status=500)


@app.route('/assign_task/', methods=['POST'])
def assign_task():
    user = request.args.to_dict()['user']
    task = request.args.to_dict()['task']

    res = db.assign_task(user, task)
    if res == 0:
        return Response("Task Assigned", status=200)
    elif res == 1:
        return Response("Task Already Assigned", status=500)
    elif res == 2:
        return Response("Task Not Found", status=500)
    elif res == 3:
        return Response("User Not Found", status=500)
    elif res == 4:
        return Response("User and Task Not Found", status=500)


def runner():
    app.run()
