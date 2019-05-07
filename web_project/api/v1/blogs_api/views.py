from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from blogs.models import Post, Comment

from .permissions import IsCommentOwner, IsPostOwner
from .serializers import CommentSerializer, PostSerializer

POSTS_ORDER_BY = '-last_modified_on'
COMMENTS_ORDER_BY = '-commented_on'


class PostViewSet(ModelViewSet):
    """Operations for posts:-
        list
        create

        retrieve
        update
        destroy
    """
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)
    filter_backends = (SearchFilter,)
    search_fields = ('title', 'content')

    def get_permissions(self):
        permissions = []
        if self.action in ('list', 'retrieve'):
            permissions = [AllowAny]
        elif self.action == 'create':
            permissions = [IsAuthenticated]
        elif self.action in ('update', 'destroy'):
            permissions = [IsAuthenticated, IsPostOwner]
        return [permission() for permission in permissions]

    def get_queryset(self):
        query_set = Post.objects.all()
        if self.request.query_params.get('filter') == 'mine':  # to get logged in user's posts
            query_set = query_set.filter(posted_by=self.request.user.id)
        return query_set.order_by(POSTS_ORDER_BY)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    authentication_classes = (TokenAuthentication,)
    pagination_class = None

    def get_permissions(self):
        permissions = []
        if self.action in ('list', 'retrieve'):
            permissions = [AllowAny]
        elif self.action == 'create':
            permissions = [IsAuthenticated]
        elif self.action in ('update', 'destroy'):
            permissions = [IsAuthenticated, IsCommentOwner]
        return [permission() for permission in permissions]

    def get_queryset(self):
        queryset = Comment.objects.all()
        if self.action in ('list', 'retrieve'):
            post_id = self.kwargs['post_id']
            queryset = queryset.filter(post__id=post_id)

        elif self.action in ('update', 'destroy'):
            user = self.request.user
            queryset = user.comments.all()

        return queryset.order_by(COMMENTS_ORDER_BY)
