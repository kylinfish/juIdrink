from django.conf.urls import patterns, url
from info import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),

    # url(r'^ta/feedback/', include('teacher_apps.feedback.urls', namespace="index")),
)
