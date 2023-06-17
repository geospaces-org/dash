from django.urls import path
from . import views

app_name = 'dash'

urlpatterns = [
    path('LINK/',  views.index , name='dash urls1'),
]
