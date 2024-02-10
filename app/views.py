from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from app.models import Post
from app.serializers import PostSerializer, UserRegistrationSerializer
from app.utils import rate


class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AllowAny,)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def rate_post(request, post_id):
    """
    Rate a post.

    Parameters:
        post_id: int - The ID of the post to rate.
        rate: int (0-5) - The rating to assign to the post.

    Returns:
        Response - Empty response indicating success or error message if rating failed.
    """
    post = get_object_or_404(Post, id=post_id)

    # Get rate from request data
    rate_num = request.data.get('rate', None)

    if rate_num is not None:  # User has sent a rating
        try:
            rate_num = int(rate_num)
        except ValueError as err:
            # Return error response if rate number is not an integer
            return Response({"detail": 'Failed, the rate number should be an integer.'},
                            status=HTTP_400_BAD_REQUEST)

        rated, rate_obj = rate(request.user, post, rate_num)

        if not rated:
            # Return error response if rate number is not between 1 and 5
            return Response({"detail": "Failed, the rate number should be between 1 and 5."},
                            status=HTTP_400_BAD_REQUEST)

    return Response()


class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
