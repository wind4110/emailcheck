import imaplib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

imap_server = "imap.zju.edu.cn"  # Zju邮箱smtp服务器
smtp_server = "smtp.zju.edu.cn"
username = "3210100658@zju.edu.cn"  # 发件人邮箱
password = "Q6GSkesgcngZvKy8"  # 专用密码
receiver = ["wind4110@qq.com"]

mail_title = "教育邮箱新邮件通知"  # 邮件标题

# 邮件正文内容
mail_content = """
<div style="text-indent:2em;">
<p>有新邮件，请及时登录查看。</p>
</div>
"""

msg = MIMEMultipart()
msg["Subject"] = Header(mail_title, "utf-8")
msg["From"] = username
msg["To"] = Header("host", "utf-8")  # 对收件人的描述

msg.attach(MIMEText(mail_content, "html"))


def check_inbox():
    """
    检查收件箱是否有未读邮件
    """
    try:
        # 连接到Gmail的IMAP服务器
        mail = imaplib.IMAP4_SSL(imap_server, 993)
        # 登录
        mail.login(username, password)
        # 选择收件箱
        mail.select("inbox")

        # 搜索所有未读邮件
        status, messages = mail.search(None, "(UNSEEN)")

        # 如果没有未读邮件，messages将是一个空字符串
        if messages[0] == b"":
            print("No new emails")
            return False
        else:
            print("You have new emails")
            return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def send_note():
    try:
        # 连接到Gmail的IMAP服务器
        mail = smtplib.SMTP_SSL(smtp_server, 994)
        # 登录
        mail.login(username, password)
        mail.set_debuglevel(0)  # 0是关闭，1是开启debug
        mail.ehlo(imap_server)  # 跟服务器打招呼，告诉它我们准备连接，最好加上这行代码
        mail.login(username, password)
        mail.sendmail(username, receiver, msg.as_string())
        mail.quit()
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


# 执行检查
if check_inbox():
    send_note()
    print("send.")
