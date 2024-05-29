from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
import markdown


host = "smtp.gmail.com"
port = "587"


def sendMain(from_addr, passwd, to_addr, title, msgtext, img=None):
    msg = MIMEBase('multipart', 'mixed')
    msg['Subject'] = title
    msg['From'] = from_addr
    msg['To'] = to_addr

    msg.attach(MIMEText(markdown.Markdown().convert(msgtext), 'html'))

    if img:
        imagePart = MIMEImage(img)
        imagePart.add_header('Content-ID', '<image1>')
        msg.attach(MIMEText("<img src='cid:image1'>", 'html'))
        msg.attach(imagePart)

    s=smtplib.SMTP(host,port)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(from_addr, passwd)
    s.sendmail(from_addr, [to_addr], msg.as_string())
    s.close()

