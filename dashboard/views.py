import requests

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import UpdateView
from django.urls import reverse

from dashboard.forms import SimpleTimerForm
from dashboard.models import SimpleTimer
from core.runner import start_job, stop_job


def index(request):
    timers_list = SimpleTimer.objects.all()
    context = {
        'timers_list': timers_list,
        'url': reverse('index'),
        'th_message': get_th()
        }
    return render(request, 'index.html', context)


def switch_status(request, id):
    simple_timer = SimpleTimer.objects.get(id=id)
    if simple_timer.activated:
        stop_job(simple_timer)
        simple_timer.process_id = -1
        simple_timer.activated = False
    else:
        pid = start_job(simple_timer)
        if pid:
            simple_timer.process_id = pid
            simple_timer.activated = True
    simple_timer.save()
    return HttpResponseRedirect(reverse('index'))


def get_th():
    try:
        msg = requests.get("localhost:8080/get_weather")
    except:
        msg = "Please retry"
    return msg


class EditSimpleTimer(UpdateView):
    template_name = 'edit.html'
    form_class = SimpleTimerForm
    model = SimpleTimer

    def get_initial(self):
        pass

    def form_valid(self, form):
        form.save()
        return super(EditSimpleTimer, self).form_valid(form)

    def get_success_url(self):
        return reverse('index')
