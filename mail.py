import smtplib
import os
import getpass
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.header import Header
from email.mime.application import MIMEApplication

emailContent=""
recipientDict={}
subject=''
credentials=[]
attachment_files=[]

## Read credentials.
file = open('credentials.txt','r')
for line in file:
    credentials.append(line.strip())
file.close()

## Read subject.
file = open('subject.txt','r')
for line in file:
    subject +=line.strip()
file.close()

## Read email body.
file = open('body.txt','r')
for line in file:
    emailContent+=line
    emailContent+='<br>'
file.close()

## Read recipient info.
file = open('recipients.txt','r')
for line in file:
    data = line.split(";");
    if(len(data) > 0 ):
        recipientDict[data[0].strip()] = ""
    if(len(data) > 1 ):
        recipientDict[data[0].strip()] = data[1].strip()
file.close()

## Read attachments.
for dir_entry in os.listdir('./attachments'):
    dir_entry_path = os.path.join('./attachments', dir_entry)
    if os.path.isfile(dir_entry_path) and dir_entry != '.DS_Store' and dir_entry != 'read_me.help':
        attachment_files.append(dir_entry_path)

#Initialize mail server
s = smtplib.SMTP('smtp.gmail.com')
s.starttls()

print('Recipient List:\n{0}'.format(recipientDict))
print('Subject shall be : {0}\n '.format(subject))
print('Attachments shall be :\n{0}\n\n '.format(attachment_files))

goForward = raw_input('Continue (y/n) : ')

if goForward == 'y' or goForward == 'Y':

    userName = credentials[0]
    gmalId = credentials[1]
    password = getpass.getpass('Password : ')
    s.login(gmalId,password)

    for k, v in recipientDict.items():
        print('Emailing {0}'.format(k))
        body = '<html><head></head><body><div>{0},<br><br></div><div>{1}</div></p></body></html>'.format(v, emailContent)
        msg = MIMEMultipart()
        msg.attach(MIMEText(body,'html','utf-8'))
        msg['Subject'] = Header(subject,'utf-8')
        msg['From'] = userName
        msg['To'] = k
        ## Add attachments
        for dir_entry_path in attachment_files:
            with open(dir_entry_path, 'rb') as fil:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(fil.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition','attachment; filename="%s"' % basename(dir_entry))
                msg.attach(part)

        s.ehlo()
        s.sendmail(gmalId, k, msg.as_string())

s.close()
print('Done')
