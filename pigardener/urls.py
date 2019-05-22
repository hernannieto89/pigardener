"""pigardener URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import logging

from django.contrib import admin
from django.urls import path, include

from dashboard.models import SimpleTimer
from core.runner import start_job

logger = logging.getLogger(__name__)

urlpatterns = [
    path('dashboard/', include('dashboard.urls')),
    path('admin/', admin.site.urls),
]


def one_time_startup():
    timers_list = SimpleTimer.objects.all()

    try:
        for timer in timers_list:
            if timer.activated:
                logger.info('Startup - Activating Timer {}'.format(timer.name))
                process_id = start_job(timer)
                timer.process_id = process_id
                timer.save()
                logger.info('Startup - Timer {} activated at Process {}'.format(timer.name, timer.process_id))
    except Exception as err:
        print(err)  #  Add OperationalError instead of Exception. Leave explanation.
one_time_startup()
