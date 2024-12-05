from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('perfil/', views.profile, name='profile'),
    path('diretorios/', views.main_directories, name='main_directories'),
    path('diretorios/<int:diretorio_id>/subdiretorios/', views.subdirectories, name='subdirectories'),
    path('subdiretorios/<int:subdiretorio_id>/arquivos/', views.files, name='files'),
    path('registro/', views.register, name='register'), 
    path('arquivos/<int:arquivo_id>/', views.file_details, name='file_details'),
]
