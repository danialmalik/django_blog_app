from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from rest_framework.authtoken import views as rest_framework_views

from users import urls as users_urls
from blogs import urls as blogs_urls

from api.v1.users_api import urls as users_api_urls
from api.v1.blogs_api import urls as blogs_api_urls


urlpatterns = [
    path('admin/', admin.site.urls),

    path('users/', include(users_urls, namespace='users')),
    path('blogs/', include(blogs_urls, namespace='blogs')),

    # to get token for any registered user

    path('auth_token/get_auth_token/',
         rest_framework_views.obtain_auth_token,
         name='get_auth_token'),

    path('api/v1/users/', include(users_api_urls, namespace='users_api')),
    path('api/v1/blogs/', include(blogs_api_urls, namespace='blogs_api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
