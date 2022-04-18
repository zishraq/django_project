import smtplib
import re
import uuid
import datetime
from random import randint
from .models import OTPmodel


def generate_otp():
    otp = randint(10000, 999999)
    return str(otp)


def store_otp(student_id, current_time):
    otp = generate_otp()
    receiver_mail = f'{student_id}@std.ewubd.edu'

    otp_id = str(uuid.uuid4())
    otp_data = {
        'otp_id': otp_id,
        'otp': otp,
        'student_id': student_id,
        'created_at': current_time,
        'expired_at': current_time + datetime.timedelta(minutes=2),
    }

    otp_store = OTPmodel(**otp_data)
    otp_store.save()

    store_otp_return = {
        'receiver_mail': receiver_mail,
        'otp': otp,
        'otp_id': otp_id
    }

    return store_otp_return


def send_otp(receiver_mail: str, otp: str, reset_password: bool):
    if reset_password:
        subject = 'Reset Password: Online Advising Portal'
        body = '''Your Reset password request has been processed successfully.
Please use this ONE TIME PASSWORD to reset your password:'''
    else:
        subject = 'OTP For Activation: Online Advising Portal'
        body = '''Your Account activation request has been processed successfully.
Please use this ONE TIME PASSWORD to activate your account:'''
    result = {
        'success': False
    }
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if not re.fullmatch(regex, receiver_mail):
        result['error'] = 'invalid email address'
        return result

    email_text = f"""\
Subject: {subject}

Dear User,

{body}

**Please note that this OTP will remain valid for 120 SECONDS**
------------------------------
User email: {receiver_mail}
Token: {otp}
------------------------------

Thank You
ABCD University
"""

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login('onlineadvisingportal@gmail.com', '123456Seven')
        smtp_server.sendmail('onlineadvisingportal@gmail.com', receiver_mail, email_text)
        smtp_server.close()
        print("Email sent successfully!")
    except Exception as ex:
        print("Something went wrong….", ex)
        result['error'] = 'Something went wrong….'
        return result

    result['success'] = True
    result['otp'] = otp
    return result
