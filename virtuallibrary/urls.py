from django.urls import path
from . import views

app_name = 'virtuallibrary'

urlpatterns = [
 path('', views.book_list, name='book_list'),
 # path('', views.BookListView.as_view(), name='book_list'),
 path('<int:id>/', views.book_detail, name='book_detail'),
 path('tag/<slug:tag_slug>/', views.book_list, name='book_list_by_tag'),
 path('home/', views.home_view, name='home'),   # /home/ -> home
 path('login/', views.login_view, name='login'),
 path('logout/', views.logout_view, name='logout'),
 path('profile/', views.profile_view, name='profile'),
 path('emprestar/<int:book_id>/', views.emprestar_livro, name='emprestar_livro'),
 path('devolver/<int:emprestimo_id>/', views.devolver_livro, name='devolver_livro'),


]
