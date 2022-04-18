import smtplib, re
from random import randint


def send_otp(receiver_mail: str):

    otp_data = {
        'mail_address': receiver_mail,
        'valid_mail': False,
        'otp': None
    }

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if re.fullmatch(regex, receiver_mail):
        otp_data['valid_mail'] = True
    else:
        print("invalid email address")
        return otp_data

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
EWU University
"""

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login('onlineadvisingportal@gmail.com', '123456Seven')
        smtp_server.sendmail('onlineadvisingportal@gmail.com', receiver_mail, email_text)
        smtp_server.close()
        otp_data['otp'] = otp
        print("Email sent successfully!")
    except Exception as ex:
        print("Something went wrong….", ex)

    return otp_data


print(send_otp('mdtanvirmobasshir@gmail.com'))
