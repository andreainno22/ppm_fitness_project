from django.urls import path, include
from . import views
from .views import SignUpView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("signUp/", SignUpView.as_view(), name="signUp"),
    #path('login/', auth_views.LoginView.as_view(template_name="registration/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password_reset_confirm/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_change_form/', auth_views.PasswordChangeView.as_view(), name='password_change_form'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('workouts_add/', views.workout_add_view, name='workouts_add'),
    path('workouts_list/workouts_selection/<int:id>', views.workout_selection_view, name='workouts_selection'),
    path('workouts_delete/', views.workout_delete_view, name='workouts_delete'),
    path('workouts_list/', views.workout_list_and_create_view, name='workouts_list'),
    path('workout_start/<str:rest_time>/', views.workout_start_view, name='workout_start'),
    path('workout_start_rest/<str:rest_time>/', views.workout_start_rest_view, name='workout_start_rest'),
    path('goals/', views.goals_view, name='goals'),
    path('workouts_list/workouts_selection/change_training_weight/<int:id>/', views.change_training_weight_view,
         name='change_training_weight'),
]
