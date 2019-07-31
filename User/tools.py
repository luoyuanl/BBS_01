from flask import render_template
from flask_mail import Message
from ext import mail


def send_mail(subject, towhom, templatename, sender, **kwargs):
    """
    功能：发送邮件
    :param subject: 邮件标题
    :param towhom: 接受者，可以是列表、元组
    :param templatename: 邮件正文的模板文件名
    :param sender: 发送者
    :param kwargs: 模板参数
    :return:
    """
    if isinstance(towhom, (list, tuple)):
        recipients = towhom
    elif isinstance(towhom, str):
        recipients = towhom.split(',')
    else:
        raise Exception('接收者类型错误')
    msg = Message(subject, recipients=recipients, sender=sender)
    msg.html = render_template(templatename, **kwargs)
    mail.send(msg)
