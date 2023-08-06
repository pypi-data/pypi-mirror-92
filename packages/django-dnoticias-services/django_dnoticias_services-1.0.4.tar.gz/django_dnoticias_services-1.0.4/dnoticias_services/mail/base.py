from django.conf import settings


class BaseMail:
    def __init__(self):
        self.api_key = getattr(settings, "MAIL_SERVICE_ACCOUNT_API_KEY", None)
