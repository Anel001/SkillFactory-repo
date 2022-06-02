from django.urls import path
from .views import PostList, PostDetail, PostCreate, SearchList, PostDelete, PostUpdate, CategoryList
from .views import subscribe_me

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='post.html'),
    path('search/', SearchList.as_view(), name='search.html'),
    path('add/', PostCreate.as_view(), name='create.html'),
    path('edit/<int:pk>', PostUpdate.as_view(), name='create.html'),
    path('delete/<int:pk>', PostDelete.as_view(), name='delete.html'),
    path('cat/', CategoryList.as_view(), name='category.html'),
    path('subscribe/<int:pk>', subscribe_me, name='subscribe'),
]
