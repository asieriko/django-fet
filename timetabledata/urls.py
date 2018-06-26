from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^data/', views.drivedata, name='drivedata'),
    url(r'^driveteachers/', views.driveTeachers, name='driveteachers'),
    url(r'^teachers/', views.showTeachers, name='teachers'),
    url(r'^ConexionTypeForm/', views.editConexion, name='econ'),
    url(r'^MultiConexionTypeForm/', views.editMultiConexion, name='emcon'),
    url(r'^MultiTeacherForm/', views.editMultiTeacher, name='emteachers'),
    url(r'^ajax/', views.ajax, name='ajax'),
    url(r'^SettingsForm/', views.editSettings, name='settings'),
    url(r'^', views.index, name='index'),
]