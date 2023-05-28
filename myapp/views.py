
# Create your views here.
from django.shortcuts import render

from django.shortcuts import redirect
from django.http import JsonResponse
from django.views import View
from google.auth import credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from urllib.parse import urlencode
from django.conf import settings
from django.urls import reverse

class GoogleCalendarInitView(View):
    def get(self, request):
        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        flow = Flow.from_client_secrets_file(
            'D:\Python_backend_Assignment\myproject\credentials\client_secret.json',
            SCOPES,
            redirect_uri=request.build_absolute_uri(reverse('calendar-redirect'))
        )

        authorization_url, state = flow.authorization_url(
            access_type='offline',
            prompt='consent',
        )
        request.session['state'] = state

        return redirect(authorization_url)


class GoogleCalendarRedirectView(View):
    def get(self, request):
        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        flow = Flow.from_client_secrets_file(
            'D:\Python_backend_Assignment\myproject\credentials\client_secret.json',
            SCOPES,
            redirect_uri='https://127.0.0.1:8000/rest/v1/calendar/redirect/'
        )
        flow.fetch_token(authorization_response=request.build_absolute_uri())
        request.session['credentials'] = credentials_to_dict(flow.credentials)
        return redirect('/rest/v1/calendar/events/')





class GoogleCalendarEventsView(View):
    def get(self, request):
        credentials_data = request.session['credentials']
        credentials = credentials.Credentials.from_authorized_user_info({
            'token': credentials_data['token'],
            'refresh_token': credentials_data['refresh_token'],
            'token_uri': credentials_data['token_uri'],
            'client_id': credentials_data['client_id'],
            'client_secret': credentials_data['client_secret'],
            'scopes': credentials_data['scopes'],
        })
        service = build('calendar', 'v1', credentials=credentials)
        events_result = service.events().list(calendarId='primary', maxResults=10).execute()
        events = events_result.get('items', [])
        return JsonResponse(events, safe=False)

def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes,
    }




# Create your views here.
