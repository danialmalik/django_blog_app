from django.conf import settings
from django.forms import model_to_dict
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (CreateView,
                                  ListView,
                                  UpdateView,
                                  DeleteView,
                                  TemplateView,
                                  DetailView)

from base.utils import get_reverse_url, get_template_path

from .models import Post
from . import constants


DEFAULT_DATE_TIME_FORMAT = getattr(settings, 'DATETIME_FORMAT')


class Index(TemplateView):
    template_name = get_template_path(constants.APP_NAME,
                                      constants.INDEX_TEMPLATE)


class PostCreate(CreateView):
    template_name = get_template_path(constants.APP_NAME,
                                      constants.POST_CREATE_TEMPLATE)
    model = Post
    fields = ('title', 'content')

    # reverse_lazy is used to avoid circular imports and 'no urls' error .
    # "reverse" is called when view is loaded and at that
    # time urls are not loaded.
    # or we can override get_success_url method.
    success_url = reverse_lazy(
        get_reverse_url(constants.APP_NAME, constants.MY_POSTS_VIEW_NAME)
    )

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.posted_by = self.request.user
        return super(PostCreate, self).form_valid(form)


class PostsList(ListView):
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.all()
        if self.request.GET.get('filter', None) == 'mine':
            if self.request.user.is_authenticated:
                queryset = queryset.filter(
                    posted_by=self.request.user
                ).order_by(constants.ORDER_BY)
        return queryset.order_by(constants.ORDER_BY)

    def get(self, request, *args, **kwargs):
        response = super().get(PostsList, self, *args, **kwargs)
        response_data = [model_to_dict(post, fields=('posted_by.username',
                                                     'posted_on',
                                                     'id',
                                                     'content',
                                                     'title'))
                         for post in response.context_data['posts']]

        return JsonResponse({
            'posts': response_data
        })


class MyPosts(TemplateView):
    template_name = get_template_path(constants.APP_NAME,
                                      constants.MY_POSTS_TEMPLATE)


class PostEdit(UpdateView):
    template_name = get_template_path(constants.APP_NAME,
                                      constants.POST_EDIT_TEMPLATE)
    success_url = reverse_lazy(
        get_reverse_url(constants.APP_NAME, constants.MY_POSTS_VIEW_NAME)
    )
    model = Post
    fields = ('content', 'id',)
    context_object_name = 'post'

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        if post.posted_by != self.request.user:
            raise Http404
        return post


class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy(
        get_reverse_url(constants.APP_NAME, constants.MY_POSTS_VIEW_NAME)
    )


class PostDetailsView(DetailView):
    model = Post
    template_name = get_template_path(constants.APP_NAME,
                                      constants.POST_DETAILS_TEMPLATE)
    context_object_name = 'post'
