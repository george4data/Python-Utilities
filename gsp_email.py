#!/usr/bin/python
import os
smtp_server = "relay.datanation.com"
email_from = "oracle@datanation.com"
email_to = ["sysadmins@datanation.com"]
subject = "SUBJECT OF EMAIL - George Email Testing"
message = "MESSAGE OF EMAIL - Ignore this"
file_To_Send = "/home/oracle/ENV_DBA/SCRIPTS/test_log.txt"

def gsp_email(email_from,email_to,subject,message,file_To_Send,smtp_server):
    import smtplib
    import mimetypes
    from email.MIMEMultipart import MIMEMultipart
    from email import Encoders
    from email.Message import Message
    from email.MIMEAudio import MIMEAudio
    from email.MIMEBase import MIMEBase
    from email.MIMEImage import MIMEImage
    from email.MIMEText import MIMEText
    emailfrom = email_from
    emailto = email_to
    fileToSend = file_To_Send
    head, tail = os.path.split(fileToSend)
    email_server = smtp_server
    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = ",".join(emailto)
    msg["Subject"] = subject
    msg.attach(MIMEText(message, 'plain'))
    ##Only needed for any preamble##msg.preamble = "YOUR EMAIL PREAMBLE"
    if fileToSend:
        ctype, encoding = mimetypes.guess_type(fileToSend)
        print(ctype)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"
        maintype, subtype = ctype.split("/", 1)
        print (maintype)
        print (subtype)
        if maintype == "text":
            print 'text'
            fp = open(fileToSend)
            # Note: we should handle calculating the charset
            attachment = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "image":
            print 'image'
            fp = open(fileToSend, "rb")
            attachment = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "audio":
            print 'audio'
            fp = open(fileToSend, "rb")
            attachment = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
        else:
            print 'else'
            fp = open(fileToSend, "rb")
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            fp.close()
            Encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment", filename=tail)
        msg.attach(attachment)
    server = smtplib.SMTP(email_server)
    server.set_debuglevel(0)
    server.sendmail(emailfrom, emailto, msg.as_string())
    server.quit()


gsp_email(email_from,email_to,subject,message,file_To_Send,smtp_server)
