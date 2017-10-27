from django.conf.urls import include, url
from django.contrib import admin
from demo.views import index
from django.contrib.auth.views import login, logout

urlpatterns = [
    # Examples:
    # url(r'^$', 'chat.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),
    url(r'^$', index, name="home"),
    url(r'^admin/', include(admin.site.urls)),
]
