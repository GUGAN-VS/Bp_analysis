from django.urls import path
from .views import *

urlpatterns = [
    path('', base, name='base'),
    path('bp/', create_bp_record),
    path('delete_bp_record/<int:pk>/', delete_record, name='delete'),
    path('login/', login_view, name='login'),
    path('login/', logoutuser, name='logout'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('caretaker_dashboard/<str:patient_id>/', caretaker_dashboard, name='caretaker_dashboard'),
    path('analyze/', analyze_patient_data, name='analyze'),
]

# from django.urls import path
# from .views import login_view, admin_dashboard, caretaker_dashboard

# urlpatterns = [
#     path('login/', login_view, name='login'),
#     path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
#     path('caretaker_dashboard/<str:patient_id>/', caretaker_dashboard, name='caretaker_dashboard'),
# ]