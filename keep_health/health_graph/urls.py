from django.conf.urls import url
from . import views

app_name = 'health_graph'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^api/sensor/pressure/view/(?P<date>[0-9]{4}-[0-1][0-9]-[0-3][0-9])$', views.health_pressure_append, name='pressure'),
    url(r'^api/sensor/pressure/append/$', views.seat_pressure_append, name='pressure_append')
]
