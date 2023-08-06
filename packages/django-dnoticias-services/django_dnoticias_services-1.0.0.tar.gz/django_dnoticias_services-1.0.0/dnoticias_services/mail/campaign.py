import requests
from django.conf import settings
from dnoticias_services.mail.base import BaseMail


class BaseCampaign(BaseMail):
    def __call__(self, template_uuid, brand_group_uuid, newsletter_uuid, title, subject, context=dict(), from_email=None, from_name=None, track_opens=None, track_clicks=None, api_key=None):
        url = self.get_url()
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

    def get_url(self):
        return None

class SendCampaign(BaseCampaign):
    def get_url(self):
        return settings.SEND_CAMPAIGN_API_URL

class CreateCampaign(BaseCampaign):
    def get_url(self):
        return settings.CREATE_CAMPAIGN_API_URL

send_campaign = SendCampaign()
create_campaign = CreateCampaign()

__all__ = ("send_campaign", "create_campaign")
