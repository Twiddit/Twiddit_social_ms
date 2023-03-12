from django.urls import path
from apps.relationship.api.views import *

urlpatterns = [
    path('followers/<int:id>/', FollowersList.as_view()),
    path('following/<int:id>/', FollowingList.as_view()),
    path('blocked/<int:id>/', BlockedList.as_view()),
    path('numberFollowers/<int:id>/', NumberFollowers.as_view()),
    path('numberFollowing/<int:id>/', NumberFollowing.as_view()),
    path('numberBlocked/<int:id>/', NumberBlocked.as_view()),
    path('disblock/<int:followedId>/<int:followerId>/', Disblock.as_view()),
    path('unfollow/<int:followedId>/<int:followerId>/', Unfollow.as_view()),
    path('createRelationship/', CreateRelationship.as_view()),

]