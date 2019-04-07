from django.conf.urls import url
from . import views


app_name = 'posts'

urlpatterns = [
    url(r'^$', views.Postlist.as_view(), name='all'),
    url(r'^drafts/$', views.PostDraftlist.as_view(), name='drafts'),
    url(r'^new/$', views.post_create, name='new'),
    url(r'^delete/(?P<slug>[-\w]+)/$', views.PostDelete.as_view(), name='delete'),
    url(r'^edit/(?P<slug>[-\w]+)/$', views.PostPrepUpdate.as_view(), name='edit'),
    url(r'^(?P<username>[-\w]+)/(?P<slug>[-\w]+)/$', views.PostDetail.as_view(), name='single'),


    ]
