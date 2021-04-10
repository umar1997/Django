from .views import PostList, PostDetail, PostListDetailfilter, CreatePost, EditPost, AdminPostDetail, DeletePost
from django.urls import path

app_name = 'blog_api'

# FOR TYPE VIEWSET FOR ROUTES
#------------------------
# from .views import Posts
# from rest_framework.routers import DefaultRouter
# router = DefaultRouter()
# router.register('', Posts, basename='post')
# urlpatterns = router.urls

urlpatterns = [

    # FOR TYPE VIEWSET MODEL
    # ------------------------
    # path('<int:pk>/', PostDetail.as_view(), name='detailcreate'),
    # path('', PostList.as_view(), name='listcreate'),



    # FOR TPE GENERICS
    # ------------------------
    path('', PostList.as_view(), name='listpost'),
    path('post/<str:pk>/', PostDetail.as_view(), name='detailpost'),
    path('search/', PostListDetailfilter.as_view(), name='searchpost'),

    # Post Admin URLs
    path('admin/create/', CreatePost.as_view(), name='createpost'),
    path('admin/edit/postdetail/<int:pk>/', AdminPostDetail.as_view(), name='admindetailpost'),
    path('admin/edit/<int:pk>/', EditPost.as_view(), name='editpost'),
    path('admin/delete/<int:pk>/', DeletePost.as_view(), name='deletepost'),
]
