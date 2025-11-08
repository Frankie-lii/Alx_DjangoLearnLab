from django.urls import path
from . import views

urlpatterns = [
    # previous URLs (login, logout, register, etc.)

    path('admin-view/', views.admin_view, name='admin_view'),
    path('librarian-view/', views.librarian_view, name='librarian_view'),
    path('member-view/', views.member_view, name='member_view'),
]

