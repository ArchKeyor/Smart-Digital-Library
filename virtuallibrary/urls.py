from django.urls import path
from . import views

app_name = 'virtuallibrary'

urlpatterns = [
 path('', views.book_list, name='book_list'),
 # path('', views.BookListView.as_view(), name='book_list'),
 path('<int:id>/', views.book_detail, name='book_detail'),
 path('tag/<slug:tag_slug>/', views.book_list, name='book_list_by_tag'),

path('login/', views.login_view, name='login'),

]
