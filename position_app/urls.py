from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),

    # Positions
    path('positions/', views.position_list_view, name='position_list'),
    path('positions/create/', views.position_create_view, name='position_create'),
    path('positions/<int:pk>/', views.position_detail_view, name='position_detail'),

    # Applicants
    path('applicants/', views.applicant_list_view, name='applicant_list'),
    path('applicants/create/', views.applicant_create_view, name='applicant_create'),
    path('applicants/<int:pk>/', views.applicant_detail_view, name='applicant_detail'),

    # Contracts
    path('contracts/', views.contract_list_view, name='contract_list'),
    path('contracts/create/', views.contract_create_view, name='contract_create'),
    path('contracts/<int:pk>/', views.contract_detail_view, name='contract_detail'),

    # Activity Logs
    path('logs/', views.activity_logs_view, name='activity_logs'),

    # Reports
    path('reports/', views.reports_view, name='reports'),
    path('reports/data/', views.reports_data_view, name='reports_data'),
]
