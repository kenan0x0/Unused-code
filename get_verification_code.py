# Required libraries
import imaplib
import email
from email.header import decode_header

def get_verification_code(email_addr, pswd):
    needed_body = ""

    # account credentials (Credentials needed to login to your mail account)
    username = email_addr
    password = pswd

    # username = "sgtdopeaf@gmail.com"
    # password = "Kankan@Isra1996"

    # Mail provider can be changed (https://www.systoolsgroup.com/imap/)
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(username, password)


    status, messages = imap.select("INBOX")

    # number of top emails to fetch
    N = 1

    # total number of emails
    messages = int(messages[0])


    for i in range(messages, messages-N, -1):
        # fetch the email message by ID
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    subject = subject.decode(encoding)
                # decode email sender
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)

                # print("Subject:", subject)
                # print("From:", From)

                # extract content type of email
                content_type = msg.get_content_type()
                # get the email body
                body = msg.get_payload(decode=True).decode()

            
            if content_type == "text/html":
                needed_body = body
    # close the connection and logout
    imap.close()
    imap.logout()
    x = needed_body.find('<span class="validate-code-number">') + 35
    needed_code = int(needed_body[x:x+6])
    return needed_code
