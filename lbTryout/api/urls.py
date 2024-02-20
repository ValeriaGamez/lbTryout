from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes, name='routes'),
    path('pars/', views.getPars, name='participant-list'),
    # path('pars/create/', views.createPar, name='create-participant' ),
    # path('pars/<str:an>/update', views.getPar, name='update-participant' ),
    # path('pars/<str:an>/delete', views.deletePar, name='delete-participant' ),
    #path('pars/export_rsr/', views.export_rsr, name="export-rsr"),
    path('pars/export_heats/', views.export_heats, name="export-heats"),
    path('pars/export_all/', views.export_all, name="export-all"),
    path('pars/export_rsr/', views.export_rsr, name="export_rsr"),
    path('pars/<str:an>/', views.getPar, name='participant-detail' ),

]