from django.conf.urls import url

from . import views

# using namespace
app_name = 'colors'

urlpatterns = [
    url(r'^$', views.index, name='index'),
]