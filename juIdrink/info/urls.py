from django.conf.urls import patterns, url
from student_apps.course import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^quiz/(?P<activity_id>\d+)$', views.quiz, name='quiz'),
    url(r'ajax_up', views.ajax_up, name='ajax_up'),
    url(r'log', views.log, name='log'),
    # url(r'^ta/feedback/', include('teacher_apps.feedback.urls', namespace="index")),
)
