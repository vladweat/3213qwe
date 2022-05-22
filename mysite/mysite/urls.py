"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path, re_path


from users import views as users_views
from web3app import views as web3app_views

# extra_patterns = [
#     path('reports/', credit_views.report),
#     path('reports/<int:id>/', credit_views.report),
#     path('charge/', credit_views.charge),
# ]

urlpatterns = [
    ###
    # re_path(r'^accounts/register/$', users_views.SignUpView.as_view(), name='signup'),
    # re_path("^$", users_views.HomePageView.as_view(), name="home"),
    # path('cr_proposal/', web3app_views.cr_proposal, name='cr_proposal'),
    # path("forma/", web3app_views.forma, name='forma'),

    # users views
    path("accounts/", include("django.contrib.auth.urls")),
    path("registr/", users_views.registr, name="registr"),
    path("login/", users_views.login, name="login"),
    path("logout/", users_views.logout, name="logout"),
    # web3app views
    
    re_path(r'^view_proposal/(?P<proposal_id>\d+)/', web3app_views.view_proposal, name="view_proposal"),
    path("creating_proposal/", web3app_views.creating_proposal, name="creating_proposal"),
    # path("view_proposal/", web3app_views.view_proposal, name="view_proposal"),
    path("", users_views.index),
    path("admin/", admin.site.urls),
]
