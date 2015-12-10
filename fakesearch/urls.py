from django.conf.urls import patterns, url
from fakesearch import views

app_name = 'fakesearch'
urlpatterns = [ url(r'^$', views.index, name='index'),
                       url(r'^about/$', views.about, name='about'),

                       # Login related functions:
                       url(r'^register/$', views.register, name='register'),
                       url(r'^login/$', views.user_login, name='login'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^profile/$', views.user_profile, name='profile'),

                       # Experiment related functions:
                       url(r'^experiments/$', views.experiments, name='experiments'),
                       url(r'^run_experiment/(?P<exp_pk>[\w]+)/', views.run_experiment, name='run_experiment'),
              ]

