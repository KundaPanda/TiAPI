"""TiAPI_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import rest_framework_simplejwt.views as jwt_views
from django.contrib import admin
from django.urls import path, re_path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from TiAPI.router import router
from TiAPI.views import *

schema_view = get_schema_view(
    openapi.Info(
        title="Ticket Scanning API",
        default_version='v1',
        description="API for creating and scanning tickets.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="vojdoh@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticated,),
)

urlpatterns = [
    path('admin', admin.site.urls),
    path('admin/database', DatabaseView.as_view(), name='database'),
    path('admin/database/list', BackupView.as_view(), name='database-backups'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('tiapi/', include(router.urls)),
    # path('auth/', include('django.contrib.auth.urls')),
    path('tiapi/test_login', TestLogin.as_view()),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='home'),
    path('tiapi/token/new', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('tiapi/token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('tiapi/token/validate', jwt_views.TokenVerifyView.as_view(), name='token_validate'),
    path('auth/login', JWTLoginView.as_view(), name='login'),
    path('auth/logout', JWTLogoutView.as_view(), name='logout'),
    # path('auth/', include(auth_urls))

    # path('add/code', AddCode.as_view()),
    # path('add/user', AddUser.as_view()),
    # path('get/users', GetUsers.as_view()),
    # path('get/codes', GetCodes.as_view()),
    # path('get/user_codes', GetUserCodes.as_view()),
]
