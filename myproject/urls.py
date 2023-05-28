from django.contrib import admin
from django.urls import path
from myapp.views import GoogleCalendarInitView, GoogleCalendarRedirectView, GoogleCalendarEventsView
from django.views.generic import RedirectView
from django.urls import include, path

urlpatterns = [
    path('', GoogleCalendarInitView.as_view(), name='home'),
    path('rest/v1/calendar/init/', GoogleCalendarInitView.as_view(), name='calendar-init'),
path('rest/v1/calendar/redirect/', GoogleCalendarRedirectView.as_view(), name='calendar-redirect'),
    path('rest/v1/calendar/events/', GoogleCalendarEventsView.as_view(), name='calendar-events'),
    path('admin/', admin.site.urls),
]

