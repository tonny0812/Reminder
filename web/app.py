# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     app
   Description :
   Author :       guodongqing
   date：          2019/11/11
-------------------------------------------------
"""
from random import choice

from flask import Flask, render_template, request, jsonify

from db.sqlitecli import SqliteUserDB
from manager.manager import Manager

app = Flask(__name__)

sysManager = Manager()


@app.route('/')
def index():
    meetingUsers = sysManager.getAllMeetingUsers()
    return render_template('index.html', meetingUsers=meetingUsers)


@app.route('/meeting/user', methods=['POST'])
def meetinguser():
    abled = request.form.get('abled')
    account = request.form.get('account')
    sysManager.updateMeetingUsers(account, (True if abled=='true' else False))
    return jsonify(abled, account)


@app.route('/meeting/start', methods=['POST'])
def meetingstart():
    account = request.form.get('account')
    status, msg = sysManager.startMeetingReminder(account)
    return jsonify(status, msg)


@app.route('/meeting/stop', methods=['POST'])
def meetingstop():
    status, msg = sysManager.stopMeetringReminder()
    return jsonify(status, msg)


if __name__ == '__main__':
    app.run(debug=True)
