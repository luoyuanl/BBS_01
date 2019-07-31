from flask import Blueprint, redirect, session, url_for
us = Blueprint('us', __name__, '/user/')


def check_login(func):
    def inner(*args, **kwargs):
        if 'uid' not in session:
            return redirect(url_for('bbs.login'))
        return func(*args, **kwargs)
    return inner
