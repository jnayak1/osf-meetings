from rest_framework.views import APIView
from rest_framework.response import Response
from allauth.socialaccount.models import SocialToken
from allauth.socialaccount.models import SocialAccount
from osf_oauth2_adapter.apps import OsfOauth2AdapterConfig
from rest_framework import status
import requests
import json


class CurrentUserView(APIView):
    base_url = '{}oauth2/{}'.format(
        OsfOauth2AdapterConfig.osf_accounts_url, '{}')
    access_token_url = base_url.format('token')
    authorize_url = base_url.format('authorize')
    profile_url = '{}v2/users/me/'.format(OsfOauth2AdapterConfig.osf_api_url)

    def get(self, request, **kwargs):
        if request.user.is_authenticated():
            curUser = request.user.username
            account = SocialAccount.objects.get(uid=curUser)
            token = SocialToken.objects.get(account=account)
            extra_data = requests.get(self.profile_url, headers={
                'Authorization': 'Bearer {}'.format(token)
            })
            data = json.loads(extra_data._content)['data']
            data['attributes']['token'] = str(token)
            return Response(data)
        else:
            return Response('User is not logged in', status=status.HTTP_401_UNAUTHORIZED)
