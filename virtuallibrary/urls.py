from django.urls import path
from . import views
app_name = 'virtuallibrary'
urlpatterns = [
 # post views
 path('', views.book_list, name='book_list'),
 # path('', views.PostListView.as_view(), name='post_list'),
 path('<int:id>/', views.book_detail, name='book_detail'),
 path('tag/<slug:tag_slug>/', views.book_list, name='book_list_by_tag'),
 path(
 '<int:year>/<int:month>/<int:day>/<slug:post>/',
 views.book_detail,
 name='book_detail'
 ),
# path('<int:book_id>/share/', views.book_share, name='book_share'),
# path(
# '<int:book_id>/comment/', views.book_comment, name='book'
#),


]
