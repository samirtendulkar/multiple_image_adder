from django.conf.urls import url
from . import views


app_name = 'posts'

urlpatterns = [
    url(r'^$', views.Postlist.as_view(), name='all'),
    url(r'^new/$', views.post_create, name='new'),
    url(r'^(?P<username>[-\w]+)/(?P<slug>[-\w]+)/$', views.PostDetail.as_view(), name='single'),

    ]
