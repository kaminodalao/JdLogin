from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_cors import CORS

import uuid
import json
import docker
import subprocess
import json

configs = {}

with open("config.json", "r", encoding="utf8") as f:
    configs = json.loads(f.read())

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://%s:%s@%s:%s/%s' % (
    configs['database']['username'],
    configs['database']['password'],
    configs['database']['host'],
    configs['database']['port'],
    configs['database']['dbname']
)

db = SQLAlchemy(app)
Migrate(app, db)
CORS(app)

docker_client = docker.from_env()
docker_api = docker.APIClient()

websockify = None


def restart_websockify():
    global websockify
    config = ""
    for task in Task.query.filter_by(running=1).all():
        config += "%s: %s:%s\n" % (task.uuid, task.container_ip, 5901)
    with open("novnc.conf", "w") as f:
        f.write(config)
    if websockify is not None:
        websockify.terminate()
    websockify = subprocess.Popen(
        ["websockify", "--target-config", "./novnc.conf", "6666"])


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(255), unique=True)
    status = db.Column(db.String(255))
    container_id = db.Column(db.String(255))
    container_ip = db.Column(db.String(255))
    runtime = db.Column(db.Integer, default=0)
    cookie = db.Column(db.Text, nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    finish_time = db.Column(db.DateTime, nullable=True)
    client_ip = db.Column(db.String(255), nullable=True)
    client_ua = db.Column(db.String(255), nullable=True)
    running = db.Column(db.Integer, default=0)
    sendkey = db.Column(db.String(255), nullable=True)


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    message = db.Column(db.String(255), nullable=True)
    time = db.Column(db.DateTime, default=datetime.now)


@app.route('/api/report', methods=['POST'])
def report():
    print(request.json)
    data = request.json['data']
    taskid = request.json['taskid']

    task = Task.query.filter_by(uuid=taskid).filter_by(running=1).first()
    if task is None:
        print("未找到该任务")
        return {"message": "未找到该任务"}, 404

    report = Report(
        task_id=task.id,
        message=json.dumps(data)[0:255],
    )
    db.session.add(report)
    db.session.commit()

    task.status = data['name']

    if data['code'] == -1:
        task.running = 0
        print("任务出错%s" % taskid)
    elif data['code'] == 0:
        task.running = 0
        print("任务完成%s" % taskid)
        task.cookie = data['cookie']
    else:
        pass

    sendkey = None

    if task.sendkey is not None:
        sendkey = task.sendkey
        task.sendkey = None

    db.session.commit()

    return {"sendkeys": sendkey}


@app.route('/api/sendkeys', methods=['POST'])
def sendkey():
    taskid = request.json['task']
    keys = request.json['keys']
    task = Task.query.filter_by(uuid=taskid).filter_by(running=1).first()
    if task is None:
        print("未找到该任务")
        return {"message": "未找到该任务"}, 404

    task.sendkey = keys
    db.session.commit()

    return {"message": "ok"}


@app.route('/api/status', methods=['GET'])
def status():
    taskid = request.args.get("task")
    if taskid is None:

        return {'message': 'No Task Id'}, 403
    task = Task.query.filter_by(uuid=taskid).first()

    if task is None:
        return {'message': 'Task Not Found'}, 404

    data = {
        'status': task.status,
        'cookie': None,
        'running': task.running,
    }

    return data


@app.route('/api/create', methods=['POST'])
def create():
    taskid = str(uuid.uuid1())

    container = docker_client.containers.run("jdlogin:debug", None, environment=[
        'TASKID=%s' % taskid,
        'REPORTURL=%s/api/report' % configs['server']
    ], detach=True, remove=True)

    inspect = docker_api.inspect_container(container.id)

    task = Task(
        uuid=taskid,
        status="created",
        container_id=container.id,
        container_ip=inspect['NetworkSettings']['IPAddress'],
        runtime=0,
        create_time=datetime.now(),
        client_ua=request.headers.get('User-Agent'),
        client_ip=request.remote_addr,
        running=1
    )

    db.session.add(task)
    db.session.commit()

    restart_websockify()

    return json.dumps({
        'task': taskid
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
