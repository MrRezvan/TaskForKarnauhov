#Django
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

#Local
from currency.views import MainView

urlpatterns = [
    path('', MainView.as_view())
]
