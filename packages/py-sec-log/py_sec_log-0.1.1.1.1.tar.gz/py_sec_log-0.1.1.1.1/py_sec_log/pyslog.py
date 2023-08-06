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
    def user_id(text):
       print(text+Helpers.GetMachineCode())
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
    def verify(auth_id, mail, subject, mail_text, notlogin):
        global code
        login=requests.get('https://pastebin.com/'+auth_id)
        email=mail.encode('utf-8')
        gmail=hashlib.md5(email)
        logmail=gmail.hexdigest()
        if logmail in login.text:
            pass
        else:
            print(notlogin)
            sys.exit()
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
        message = 'Subject: '+subject+'\n\n'+mail_text+" "+code

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
    class getotp:
        def otp(mail, otp, alert_mail, alert_text, warn_mail, warn_text, warn_subject, alert_subject):
            if otp==code:
                if warn_mail=='on':
                    get_ip=requests.get('https://get.geojs.io/v1/ip.json')
                    ip=(get_ip.json()['ip'])
                    get_info='https://get.geojs.io/v1/ip/geo/'+ip+'.json'
                    data=requests.get(get_info)
                    get_data=data.json()
                    #print(get_data)
                    all_info=(f'\nIP: {ip}\n\nCity: '+get_data['city']+'\n\nCountry: '+get_data['country']+'\n\nRegion: '+get_data['region'])
                    port = 587  # For starttls
                    smtp_server = "smtp.gmail.com"
                    sender_email = "sendotpnoreply@gmail.com"
                    receiver_email = mail
                    password = "otp@send"
                    message = 'Subject: '+warn_subject+'\n\n'+warn_text+' '+str(all_info)
                    context = ssl.create_default_context()
                    with smtplib.SMTP(smtp_server, port) as server:
                        server.ehlo()  # Can be omitted
                        server.starttls(context=context)
                        server.ehlo()  # Can be omitted
                        server.login(sender_email, password)
                        server.sendmail(sender_email, receiver_email, message)
                elif warn_mail=='off':
                    pass
                else:
                    sys.exit()
            else:
                if alert_mail=='on':
                    get_ip=requests.get('https://get.geojs.io/v1/ip.json')
                    ip=(get_ip.json()['ip'])
                    get_info='https://get.geojs.io/v1/ip/geo/'+ip+'.json'
                    data=requests.get(get_info)
                    get_data=data.json()
                    #print(get_data)
                    all_info=(f'\nIP: {ip}\n\nCity: '+get_data['city']+'\n\nCountry: '+get_data['country']+'\n\nRegion: '+get_data['region'])
                    port = 587  # For starttls
                    smtp_server = "smtp.gmail.com"
                    sender_email = "sendotpnoreply@gmail.com"
                    receiver_email = mail
                    password = "otp@send"
                    message = 'Subject: '+alert_subject+'\n\n'+alert_text+' '+str(all_info)
                    context = ssl.create_default_context()
                    with smtplib.SMTP(smtp_server, port) as server:
                        server.ehlo()  # Can be omitted
                        server.starttls(context=context)
                        server.ehlo()  # Can be omitted
                        server.login(sender_email, password)
                        server.sendmail(sender_email, receiver_email, message)

                elif alert_mail=='off':
                    print('Invalid Conformation Code')
                    sys.exit()
                else:
                    sys.exit()
