from django.conf.urls import url

from mysite.core import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.UsersListView.as_view(), name='users_list'),
    url(r'^generate/$', views.GenerateRandomUserView.as_view(), name='generate'),
    url(r'^generatesimulations/$', views.GenerateSimulation.as_view(), name='generatesimulations'),
    url(r'^viewsimulation/(?P<pk>\d+)$', views.ViewSimulation.as_view(), name='viewsimulation'),
    url(r'^viewsimulationlist/$', views.ViewSimulationList.as_view(), name='viewsimulationlist')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)