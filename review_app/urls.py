from django.urls import path,re_path as url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls,name='admin'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/login.html'),name='logout'),
    path('',views.home,name='home'),
    url(r'^project/(\d+)/$',views.project,name='project'),
    url(r'^accounts/profile/(\d+)/$',views.profile,name='profile'),
    url(r'^profile/(\d+)/bio/add-update/$',views.bio,name='bio'),
    url(r'^profile/(\d+)/contact/add-update/$',views.contact,name='contact'),
    path('add/project/',views.new_project,name='new-project'),
    path('search/term/',views.search_results,name='search_results'),
    path('api/projects/',views.ProjectList.as_view()),
    path('api/profiles/',views.ProfileList.as_view()),
    path('api/',views.api,name='api'),
    # path('projects/<int:project_id>/vote/', views.vote, name ='vote'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
