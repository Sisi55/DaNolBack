from rest_framework import serializers

from sheets.models import Member, Content


class MemberSerializer(serializers.ModelSerializer):
    sns = serializers.SerializerMethodField()
    # contents =

    class Meta:
        model = Member
        fields = ['id', 'kind', 'email', 'image_url', 'name', 'introduction', 'sns']
        read_only_fields = []  # 'team', 이렇게 하면 team 빠지나 ? oo

    def get_sns(self, obj):
        serializer = SnsSerializer(instance=obj.sns.all(), many=True)
        return serializer.data


class ContentSerializer(serializers.ModelSerializer):
    presenter = MemberSerializer()

    class Meta:
        model = Content
        fields = ['id', 'year', 'track_num', 'order', 'presenter', 'title', 'source_link']
        read_only_fields = []


class SnsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Content
        fields = ['id', 'kind', 'link']
        read_only_fields = []
