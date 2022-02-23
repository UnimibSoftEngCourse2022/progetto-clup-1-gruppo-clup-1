import smtplib, ssl

from src.clup.providers.email_service_provider_abc import EmailServiceProvider


class GmailServiceProvider(EmailServiceProvider):
    def __init__(self, mail, password):
        self.smtp_domain_name = 'smtp.gmail.com'
        self.port = 465
        self.sender = mail
        self.password = password

    def send(self, to, subject, content):
        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(self.server_domain_name, self.port, context=ssl_context)
        service.login(self.sender, self.password)

        service.sendmail(self.sender, to, f'Subject: {subject}\n{content}'

        service.quit()