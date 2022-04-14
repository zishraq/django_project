import smtplib
from random import randint


def send_otp(receiver_mail: str):

    otp = randint(10000, 999999)
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

    otp_data = {
        'mail_address': receiver_mail,
        'otp': otp
    }

    return otp_data


send_otp('mdtanvirmobasshir@gmail.com')
