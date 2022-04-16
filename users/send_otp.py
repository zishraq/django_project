import smtplib
import re
from random import randint


def generate_otp():
    otp = randint(10000, 999999)
    return str(otp)


def send_otp(receiver_mail: str, otp: str):
    result = {
        'success': False
    }
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if not re.fullmatch(regex, receiver_mail):
        result['error'] = 'invalid email address'
        return result

    email_text = f"""\
Subject: OTP For Online Advising Portal

Dear User,

Your Account activation request has been processed successfully.

Please use this ONE TIME PASSWORD to activate your account:

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
