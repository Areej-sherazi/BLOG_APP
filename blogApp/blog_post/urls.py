# app urls.py
from django.urls import path
from .views import (
    CreatePostView,
    RetrievePostsView,
    UpdatePostView,
    DeletePostView,
    CreateCommentView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path('create_post/', CreatePostView.as_view(), name='create_post_view'),  
    path('retrieve_post/', RetrievePostsView.as_view(), name='retrieve_post_view'),  
    path('update_post/<int:post_id>/',UpdatePostView.as_view(), name='update_post_view'),  
    path('delete_post/<int:post_id>/', DeletePostView.as_view(), name='delete-post'),
    path('create_comment/<int:post_id>/', CreateCommentView.as_view(), name='create_comment_view'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]


