# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     app
   Description :
   Author :       guodongqing
   date：          2019/11/11
-------------------------------------------------
"""

from flask import Flask, render_template, request, jsonify

from manager.manager import Manager
from util.Logger import Logger

logger = Logger.instance()
sysManager = Manager()
app = Flask(__name__)


def start_web_server(port=5000, debug=True):
    app.run(port=port, debug=debug)


@app.route('/meeting')
def meeting():
    meetingUsers = sysManager.getAllMeetingUsers()
    logger.info(request.remote_addr + " - meeting user's size:" + str(len(meetingUsers)))
    return render_template('meetingusers.html', meetingUsers=meetingUsers)


@app.route('/mis')
def mis():
    misUsers = sysManager.getAllMisUsers()
    logger.info(request.remote_addr + " - mis user's size:" + str(len(misUsers)))
    return render_template('misusers.html', misUsers=misUsers)


@app.route('/meeting/user', methods=['POST'])
def meetinguser():
    abled = request.form.get('abled')
    account = request.form.get('account')
    sysManager.updateMeetingUsers(account, (True if abled == 'true' else False))
    logger.info(request.remote_addr + " - update meeting user:" + account + "->" + abled)
    return jsonify(abled, account)


@app.route('/meeting/start', methods=['POST'])
def meetingstart():
    account = request.form.get('account')
    status, msg = sysManager.startMeetingReminder(account)
    if status:
        logger.info(msg)
    else:
        logger.error(msg)

    return jsonify(status, msg)


@app.route('/meeting/stop', methods=['POST'])
def meetingstop():
    status, msg = sysManager.stopMeetingReminder()
    if status:
        logger.info(msg)
    else:
        logger.error(msg)
    return jsonify(status, msg)


#########

@app.route('/mis/user', methods=['POST'])
def misuser():
    abled = request.form.get('abled')
    account = request.form.get('account')
    sysManager.updateMisUsers(account, (True if abled == 'true' else False))
    logger.info(request.remote_addr + "-update mis user:" + account + "->" + abled)
    return jsonify(abled, account)


@app.route('/mis/start', methods=['POST'])
def misstart():
    account = request.form.get('account')
    status, msg = sysManager.startMisReminder(account)
    if status:
        logger.info(msg)
    else:
        logger.error(msg)
    return jsonify(status, msg)


@app.route('/mis/stop', methods=['POST'])
def misstop():
    status, msg = sysManager.stopMisReminder()
    if status:
        logger.info(msg)
    else:
        logger.error(msg)
    return jsonify(status, msg)


#########

if __name__ == '__main__':
    app.run(debug=True)
