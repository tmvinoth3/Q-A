"""QandA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from accounts import views as acc_view
from forum import views as for_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login$', auth_views.LoginView.as_view(template_name='login.html',redirect_authenticated_user=True), name='login'),
    url(r'^signup/$', acc_view.signup, name='signup'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),

    url(r'^$', for_views.home, name='home'),
    url(r'^follow/$', for_views.follow, name='follow'),
    url(r'^unfollow/$', for_views.unfollow, name='unfollow'),
    url(r'^getQuestions/$', for_views.getQuestions, name='getQuestions'),
    url(r'^getSearchQuesions/(?P<ques_id>\d+)/$', for_views.getSearchQuesions, name='getSearchQuesions'),
    url(r'^upvote/$', for_views.upvote, name='upvote'),
    url(r'^comment/$', for_views.comment, name='comment'),
    url(r'^askQues/$', for_views.createQuestion, name='askQues'),

    url(r'^settings/account/$', for_views.UserUpdateView.as_view(), name='my_account'),
    url(r'^tinymce/', include('tinymce.urls')),

    url(r'^undoUpvote/$', for_views.undo_upvote, name='undo_upvote'),
    url(r'^userProfile/(?P<user_id>\d+)/$', for_views.userProfile, name='user_profile'),
    url(r'^topicDetail/(?P<topic_id>\d+)/$', for_views.topicDetail, name='topic_detail'),

    url(r'^pwd_reset/$', auth_views.password_reset, {'template_name':'registration/password_reset_form.html'}, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    #or url('^', include('django.contrib.auth.urls')),

    url(r'^settings/password/$', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
    name='password_change'),

    url(r'^settings/password/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
    name='password_change_done'),

]