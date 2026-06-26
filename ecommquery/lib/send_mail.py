import smtplib

# Simple SMTP wrapper

class FakeSendMail:
    def __init__(self):
        pass

    def send(self, to_addr: [str], cc_addr: [str] = None, msg: str = "", subject: str = 'No Subject'):
        print("Mail TO: " + ", ".join(to_addr))
        print("Mail CC: " + ", ".join(cc_addr) )
        print("Mail Subject: " + subject)
        print("Mail Message: \n" + msg)

class SendMail:
    def __init__(self, from_email: str, hostname:str='localhost', port:int = 25):
        self._sendmail_from = from_email
        self._hostname = hostname
        self._port = port


    def send(self, to_addr: [str], cc_addr: [str] = None, msg: str = "", subject: str = 'No Subject'):

        if to_addr is None or len(to_addr) == 0:
            raise Exception("Internal Exception: no TO address provided")

        sendmail_to = []
        email_msg = ""

        server = smtplib.SMTP(self._hostname, self._port)

        # prepare an email message and send e-mail
        for addr in to_addr:
            sendmail_to.append(addr)
            email_msg += f"To: {addr}\n"

        if cc_addr:
            for addr in cc_addr:
                email_msg += f"Cc: {addr}\n"
                sendmail_to.append(addr)

        email_msg += f"Subject: {subject}\n"
        email_msg += "MIME-Version: 1.0\n"
        email_msg += "Content-Type: text/plain; charset = \"UTF-8\"\n"
        email_msg += "Content-Transfer-Encoding: 8bit\n"

        email_msg += f"\n{msg}"
        server.sendmail(from_addr=self._sendmail_from, to_addrs=sendmail_to,
                    msg=email_msg)
        server.quit()

