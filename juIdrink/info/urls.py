from django.conf.urls import patterns, url
from info import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'store', views.store, name='store'),
    url(r'main', views.search, name='main'),
    url(r'locate', views.locate, name='locate'),

    # url(r'^ta/feedback/', include('teacher_apps.feedback.urls', namespace="index")),
)
