from apps.relationship.models import *

from rest_framework import serializers

class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        exclude = ('createdDate', )

class RelationshipFollowersSerializer(serializers.ModelSerializer):

    numberFollowers = serializers.SerializerMethodField()

    def get_numberFollowers(self, relationship: Relationship):
        return Relationship.objects.filter(followedId=relationship.followedId).filter(blocked = False).count()

    class Meta:
        model = Relationship
        fields = ['numberFollowers']

class RelationshipFollowingSerializer(serializers.ModelSerializer):

    numberFollowing = serializers.SerializerMethodField()

    def get_numberFollowing(self, relationship: Relationship):
        return Relationship.objects.filter(followerId=relationship.followerId).filter(blocked = False).count()

    class Meta:
        model = Relationship
        fields = ['numberFollowing']


class RelationshipBlockedSerializer(serializers.ModelSerializer):

    numberBlocked = serializers.SerializerMethodField()

    def get_numberBlocked(self, relationship: Relationship):
        return Relationship.objects.filter(followedId=relationship.followedId).filter(blocked = True).count()

    class Meta:
        model = Relationship
        fields = ['numberBlocked']
