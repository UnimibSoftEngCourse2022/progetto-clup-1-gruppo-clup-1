class NotifyEnabledAccounts:
    def __init__(self, email_service_provider):
        self.email_service_provider = email_service_provider
        self.subject = 'Your reservation has been enabled'
        self.content = 'You can go shopping now!'

    def execute(self, accounts):
        for account in accounts:
            self.email_service_provider.send(account.username, self.subject, self.content)
