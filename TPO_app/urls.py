from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings


urlpatterns = [
    path('', views.index, name= "index"),
    # Authentication
    path('register/', views.register_page, name= "register_page"),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    
    path('TPO_app/', views.register_student, name= "register_student"),
    path('register_job/', views.register_job, name= "register_job"),
    path('register_student_submit/', views.register_student_submit, name= "register_student_submit"),
    path('companies/', views.companies, name= "companies"),
    path('upcoming_events/', views.upcoming_events, name= "upcoming_events"),
    path('upcoming_events_submit/', views.upcoming_events_submit, name= "upcoming_events_submit"),
    path('Statistics/', views.Statistics, name= "Statistics"),
    path('update_details/', views.update_details, name= "update_details"),
    path('update_user_details/', views.update_user_details, name= "update_user_details"),
    path('fill_details/', views.fill_details, name= "fill_details"),
    path('download/(?P<path>.*)$', serve,{'document_root':settings.MEDIA_ROOT}),
    
]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)