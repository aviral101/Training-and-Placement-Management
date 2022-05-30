from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings
from . import views

urlpatterns=[
    path('', views.companyindex, name='companyindex'),
    path('update_company_details/', views.update_company_details, name='update_company_details'),
    path('save_company_details/', views.save_company_details, name='save_company_details'),
    path('stats/', views.stats, name='stats'),
    path('download/(?P<path>.*)$', serve,{'document_root':settings.MEDIA_ROOT}),
    path('recieved_applications/', views.recieved_applications, name='recieved_applications'),
    path('logout/', views.logout, name='logout'),
    path('upload_result', views.upload_result, name='upload_result'),
    path('save_result', views.save_result, name='save_result'),
    path('delete', views.delete, name='delete'),
    path('confirm_delete', views.confirm_delete, name='confirm_delete'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)