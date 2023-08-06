import requests
from django.conf import settings
from dnoticias_services.mail.base import BaseMail


class SendEmail(BaseMail):
    def __call__(self, email, template_uuid, brand_group_uuid, subject, context=dict(), from_email=None, from_name=None, track_opens=True, track_clicks=True, api_key=None):
        url = settings.SEND_EMAIL_API_URL
        _api_key = api_key or self.api_key
        
        response = requests.post(
            url,
            headers={
                "Authorization" : "Api-Key {}".format(_api_key)
            },
            data={
                "email" : email,
                "template_uuid" : template_uuid,
                "brand_group_uuid" : brand_group_uuid,
                "subject" : subject,
                "context" : context,
                "from_email" : from_email,
                "from_name" : from_name,
                "track_opens" : track_opens,
                "track_clicks" : track_clicks,
            }
        )
        response.raise_for_status()
        return response

send_email = SendEmail()

__all__ = ("send_email",)
