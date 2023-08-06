import requests, os, sys
from licensing import methods
from licensing.methods import Helpers
import hashlib
import smtplib, ssl
import random, string
class login:
    k=Helpers.GetMachineCode()
    ke=k.encode('utf-8')
    ey=hashlib.md5(ke)
    global key
    key=ey.hexdigest()
    def user_id():
       Helpers.GetMachineCode()
    def auth(auth_id):
        if auth_id=='':
            print('Please Enter auth_id')
            sys.exit()
        else:
            global r
        r=requests.get('https://pastebin.com/'+auth_id)
    def verify(username, password):
        if username=='' and password=='' or username=='' or password=='':
            print('Need Username And Password For Login!')
            sys.exit()
        else:
            pass
        ins=username+password
        sec=ins.encode('utf-8')
        secu=hashlib.md5(sec)
        info=secu.hexdigest()
        if info in r.text:
            if key in r.text:
                pass
            else:
                print('Unexpected Error!')
                sys.exit()
        else:
            print('Invalid Username Or Password!')
            sys.exit()
class verify:
    def verify(auth_id, mail):
        global code
        sec="1234567890"
        cod = []
        for x in range(6):
            cod.append(random.choice(sec))
        code=''.join(cod)
        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"
        sender_email = "sendotpnoreply@gmail.com"
        receiver_email = mail
        password = "otp@send"
        message = """\
        No Reply

        


        Hi, Your Conformation Code Is """+code

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
    class getotp:
        def otp(otp):
            if otp==code:
                pass
            else:
                print('Invalid Conformation Code')
                sys.exit()
