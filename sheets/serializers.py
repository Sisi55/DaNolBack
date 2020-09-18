from rest_framework import serializers

from sheets.models import Member, Content, SNS, Sponsor


class MemberSerializer(serializers.ModelSerializer):
    sns = serializers.SerializerMethodField()

    # contents =

    class Meta:
        model = Member
        # 'id', 'kind', 'email', 'name', 'introduction', 'sns', 'belongTo'
        fields = ['id', 'kind', 'email', 'image_url', 'name', 'introduction', 'sns', 'belongTo']
        read_only_fields = ['sns']  # 'team', 이렇게 하면 team 빠지나 ? oo

    def get_sns(self, obj):
        # print(obj)
        # if 'sns' in obj:
        # print(obj.sns)
        serializer = SnsSerializer(instance=obj.sns.all(), many=True)
        return serializer.data

    def create(self, validated_data):
        return Member.objects.create(**validated_data)

    def update(self, instance, validated_data):  # introduction, homepage_link, sponsorship_rating
        instance.introduction = validated_data.get('introduction', instance.introduction)  # 준비위: 소개
        instance.belongTo = validated_data.get('belongTo', instance.belongTo)  # 발표자: 소속
        # instance.sponsorship_rating = validated_data.get('sponsorship_rating', instance.sponsorship_rating)
        instance.save()
        return instance


class ContentSerializer(serializers.ModelSerializer):
    presenter = MemberSerializer(read_only=True)  # read_only=True

    class Meta:
        model = Content
        fields = ['id', 'year', 'track_num', 'order', 'presenter', 'title', 'source_link', 'introduction', 'kind']
        read_only_fields = []

    def create(self, validated_data):
        return Content.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Content: presenter, title, presentation_time, introduction, kind
        print('ContentSerializer:update', instance.presenter)
        instance.presenter = validated_data.get('presenter', instance.presenter)

        instance.title = validated_data.get('title', instance.title)
        instance.presentation_time = validated_data.get('presentation_time', instance.presentation_time)
        instance.introduction = validated_data.get('introduction', instance.introduction)
        instance.kind = validated_data.get('kind', instance.kind)
        instance.save()
        return instance


class SnsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SNS
        fields = ['id', 'kind', 'link']
        read_only_fields = []


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ['id', 'introduction', 'homepage_link', 'sponsorship_rating', 'name']
        read_only_fields = []

    def create(self, validated_data):
        return Sponsor.objects.create(**validated_data)

    def update(self, instance, validated_data):  # introduction, homepage_link, sponsorship_rating
        instance.introduction = validated_data.get('introduction', instance.introduction)
        instance.homepage_link = validated_data.get('homepage_link', instance.homepage_link)
        instance.sponsorship_rating = validated_data.get('sponsorship_rating', instance.sponsorship_rating)
        instance.save()
        return instance


class ContentToPresenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'kind', 'email', 'name', 'introduction', 'belongTo']
        read_only_fields = []  # 'team', 이렇게 하면 team 빠지나 ? oo
