from django.urls import path

from app.views import PostList, rate_post, UserRegistrationAPIView

urlpatterns = [
    path('posts/', PostList.as_view(), name='post-list'),
    path('posts/<int:post_id>/rate', rate_post, name='post-rate'),
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),

]
