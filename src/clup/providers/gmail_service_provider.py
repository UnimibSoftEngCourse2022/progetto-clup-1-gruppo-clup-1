import smtplib
import ssl

from src.clup.providers.abc.email_service_provider import EmailServiceProvider


class GmailServiceProvider(EmailServiceProvider):
    def __init__(self, mail, password):
        self.smtp_server_domain_name = 'smtp.gmail.com'
        self.port = 465
        self.sender = mail
        self.password = password

    def send(self, to, msg):
        msg['From'] = self.sender
        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context)
        service.login(self.sender, self.password)

        service.sendmail(self.sender, to, msg.as_string())

        service.quit()
