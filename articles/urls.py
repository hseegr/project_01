from django.urls import path
from . import views

app_name="articles"
urlpatterns = [
    path('', views.MainPageView.as_view(), name='main_page'),
    path("articles_list/", views.articles_list, name="articles_list"),
    path("create/", views.create, name="create"),
    path("<int:article_pk>/articles_detail/", views.articles_detail, name="articles_detail"),
    path("<int:article_pk>/articles_delete/", views.articles_delete, name="articles_delete"),
    path("<int:article_pk>/articles_update/", views.articles_update, name="articles_update"),
    path("comment/<int:comment_id>/delete/", views.comment_delete, name="comment_delete"),
    path("toggle_like/", views.toggle_like, name="toggle_like"),
    path('<category>/', views.CategoryListView.as_view(), name='category_list'),
]

