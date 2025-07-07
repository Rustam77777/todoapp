from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # for signup

urlpatterns = [
    # login: renders ‘registration/login.html’ by default
    path('login/',
         auth_views.LoginView.as_view(template_name='manage/login.html'),
         name='login'),

    # logout: redirects to LOGOUT_REDIRECT_URL
    path('logout/',
         auth_views.LogoutView.as_view(),
         name='logout'),

    # optional: simple signup view
    path('signup/',
         views.signup,
         name='signup'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/list/', views.project_list, name='project_list'),
    path('task/<int:pk>/status/', views.task_update_status, name='task_update_status'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/<int:project_id>/tasks/create/', views.task_create, name='task_create'),
    path('projects/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('tasks/<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('profile/', views.profile_edit, name='profile_edit'),
]