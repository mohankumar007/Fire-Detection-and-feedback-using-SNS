# helloworld/urls.py
from django.conf.urls import url
from django.conf.urls.static import static
from app1 import views
from django.urls import path
from django.conf import settings



urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    path("img",views.upload_process,name='home'),
    # path("vid",views.upload_process1,name='home1'),
    path("cam",views.upload_process2,name='home2'),
    path("process",views.process,name='process'),
    path("success",views.success,name='success'),
    path("fail",views.fail,name='fail'),
    path("proc",views.upload_process,name='hotel'),
    # path("proc1",views.upload_process1,name='hotel1'),
]

if settings.DEBUG: 
        urlpatterns += static(settings.MEDIA_URL, 
                              document_root=settings.MEDIA_ROOT) 