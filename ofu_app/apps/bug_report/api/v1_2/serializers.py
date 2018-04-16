from apps.bug_report.models import BugMsg
from rest_framework import serializers


class BugMsgCategoriesSerializer(serializers.Serializer):
    """Your data serializer, define your fields here."""

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    id = serializers.CharField()
    short = serializers.CharField()
    name = serializers.CharField()


class BugMsgStatesSerializer(serializers.Serializer):
    """Your data serializer, define your fields here."""

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    id = serializers.CharField()
    name = serializers.CharField()


class BugMsgPrioritiesSerializer(serializers.Serializer):
    """Your data serializer, define your fields here."""

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    id = serializers.CharField()
    name = serializers.CharField()


class BugMsgSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.ChoiceField(choices=BugMsg.CATEGORY_CHOICES)
    status = serializers.ChoiceField(choices=BugMsg.STATE_CHOICES)

    # def create(self, validated_data):
    #     title = validated_data.pop('title')
    #     description = validated_data.pop('description')
    #     category = validated_data.pop('category')
    #     if 'status' in validated_data:
    #         status = validated_data.pop('status')
    #     else:
    #         status = BugMsg.REGISTERED
    #     bugMsg, _ = BugMsg.objects.get_or_create(title=title, description=description, category=category, status=status)
    #     return bugMsg

    class Meta:
        model = BugMsg
        fields = ('id', 'title', 'status', 'description', 'category')


class BugMsgDetailSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.ChoiceField(choices=BugMsg.CATEGORY_CHOICES)
    priority = serializers.ChoiceField(choices=BugMsg.PRIORITY_CHOICES)
    status = serializers.ChoiceField(choices=BugMsg.STATE_CHOICES)
    registration_date = serializers.DateField(format='iso-8601')

    class Meta:
        model = BugMsg
        fields = ('id', 'registration_date', 'title', 'description', 'category', 'priority', 'status')
