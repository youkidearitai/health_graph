from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from .models import Question, SeatPressure
import datetime
import json
import pytz

class IndexView(generic.ListView):
    template_name = 'health_graph/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'health_graph/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'health_graph/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'health_graph/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('health_graph:results', args=(question.id,)))

def health_pressure_append(request, date):
    timestamp = datetime.datetime.strptime(date, "%Y-%m-%d")
    seat_pressure = None

    try:
        sp = SeatPressure.objects
        seat_pressure = sp \
            .filter(minutes__gte=(timestamp).strftime("%Y-%m-%d 00:00:00")) \
            .filter(minutes__lt=(timestamp).strftime("%Y-%m-%d 23:59:59"))
    except (KeyError, SeatPressure.DoesNotExist):
        pass

    pressure_output = []
    for seat in seat_pressure:
        pressure_output.append(
            {
                "time": seat.minutes.astimezone(pytz.timezone("Asia/Tokyo")).strftime("%Y/%m/%d %H:%M:%S"),
                "seat_count": seat.seat_count,
                "average": seat.average,
            }
        )

    return HttpResponse(
        json.dumps(pressure_output),
        content_type='application/json; charset=UTF-8',
        status=200
    )

# Create your views here.
