from django.urls import path
from . import views
from .views import CustomPasswordChangeView

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('preference/', views.preference, name='preference'),
    path('delete/', views.delete, name='delete'),
    path('update/', views.update, name='update'),
    path('mypage/', views.mypage, name='mypage'),
    path('<int:user_pk>/password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('find_id/', views.find_id, name='find_id'),
]
