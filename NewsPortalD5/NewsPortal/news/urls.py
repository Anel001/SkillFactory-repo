from django.urls import path
from .views import PostList, PostDetail, SearchList, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='post.html'),
    path('search/', SearchList.as_view(), name='searchposts.html'),
    path('add/', PostCreateView.as_view(), name='create.html'),
    path('edit/<int:pk>', PostUpdateView.as_view(), name='create.html'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='delete.html'),
]
