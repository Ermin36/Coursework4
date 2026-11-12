from django.urls import path

from send_track.apps import SendTrackConfig
from .views import (Home, MailingList, MailingDelete, MailingCreate, MailingDetail, MailingUpdate,
    MailingAttemptList, MailingAttemptDelete, MailingAttemptDetail,
    MailingSend, MailingSendAll)

app_name = SendTrackConfig.name

urlpatterns = [
    #Mailings
    path('', Home.as_view(), name='home'),
    path('mailings/', MailingList.as_view(), name='mailing_list'),
    path('mailings/create/', MailingCreate.as_view(), name='mailing_create'),
    path('mailings/<int:pk>/', MailingDetail.as_view(), name='mailing_detail'),
    path('mailings/<int:pk>/update/', MailingUpdate.as_view(), name='mailing_update'),
    path('mailings/<int:pk>/delete/', MailingDelete.as_view(), name='mailing_delete'),
    path('mailings/<int:pk>/send/', MailingSend.as_view(), name='mailing_send'),
    path('mailings/send-all/', MailingSendAll.as_view(), name='mailing_send_all'),

    #MailingAttempts
    path('mailing_attempts/', MailingAttemptList.as_view(), name='mailing_attempt_list'),
    path('mailing_attempts/<int:pk>/', MailingAttemptDetail.as_view(), name='mailing_attempt_detail'),
    path('mailing_attempts/<int:pk>/delete/', MailingAttemptDelete.as_view(), name='mailing_attempt_delete'),
]