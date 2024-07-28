from django.urls import path
from blogapp.views import Home,Base,Audiovideo,Graphics,Posts,PostDetail,PostEdit,PostDelete,CommentDelete,ProfileView,ProfileEditView,AddFollower,RemoveFollower,AddLike,AddDislike,ListFollowers,CreateThread,ListThreads,ThreadView,CreateMessage
from . import views

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('base/', Base.as_view(), name='base'),
    path('audiovideo/', Audiovideo.as_view(), name='audiovideo'),
    
    path('graphics/', Graphics.as_view(), name='graphics'),

    path('signin/', views.signin,name='signin'),
    path('signup/', views.signup,name='signup'),
    path('signout/', views.signout,name='signout'),

    path('posts/', Posts.as_view(), name='posts'),
    path('post/<int:pk>/', PostDetail.as_view(), name ='postdetail'),
    path('post/edit/<int:pk>/',PostEdit.as_view(),name='postedit'),
    path('post/delete/<int:pk>/',PostDelete.as_view(),name='postdelete'),
    path('post/<int:post_pk>/comment/delete/<int:pk>/',CommentDelete.as_view(),name='commentdelete'),
    path('post/<int:pk>/like', AddLike.as_view(), name ='like'),
    path('post/<int:pk>/dislike', AddDislike.as_view(), name ='dislike'),
    path('profile/<int:pk>/', ProfileView.as_view(), name ='profile'),
    path('profile/edit/<int:pk>/', ProfileEditView.as_view(), name ='profile_edit'),
    path('profile/<int:pk>/followers/', ListFollowers.as_view(), name ='list-followers'),
    path('profile/<int:pk>/followers/add', AddFollower.as_view(), name ='add-folower'),
    path('profile/<int:pk>/followers/remove', RemoveFollower.as_view(), name ='remove-folower'),

    # chatting
    path('inbox/', ListThreads.as_view(), name='inbox'),
    path('inbox/create-thread/', CreateThread.as_view(), name='create-thread'),
    path('inbox/<int:pk>/', ThreadView.as_view(), name ='thread'),
    path('inbox/<int:pk>/create-message/', CreateMessage.as_view(), name ='create-message'),


    # trial
    path('create_article/', views.create_article,name='create_article'),
    path('article_list/', views.article_list,name='article_list'),
]
