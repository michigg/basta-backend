from rest_framework import generics
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.parsers import FormParser, MultiPartParser

from apps.food.models import UserFoodRating, UserFoodImage, UserFoodComment, FoodImage
from apps.food.api.v1_2.serializers.user_serializers import UserFoodRatingSerializer, UserFoodImageSerializer, \
    UserFoodCommentSerializer


@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
class ApiFoodRatingUpload(generics.CreateAPIView):
    serializer_class = UserFoodRatingSerializer
    queryset = UserFoodRating.objects.all()

    def get_serializer_context(self):
        context = super(ApiFoodRatingUpload, self).get_serializer_context()
        context.update({
            "food_id": self.kwargs['pk'],
        })
        return context


@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
class ApiUserFoodCommentUpload(generics.CreateAPIView):
    serializer_class = UserFoodCommentSerializer
    queryset = UserFoodComment.objects.all()

    def get_serializer_context(self):
        context = super(ApiUserFoodCommentUpload, self).get_serializer_context()
        context.update({
            "food_id": self.kwargs['pk'],
        })
        return context


@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
class ApiFoodImageUpload(generics.CreateAPIView):
    serializer_class = UserFoodImageSerializer
    queryset = FoodImage.objects.all()

    def get_serializer_context(self):
        context = super(ApiFoodImageUpload, self).get_serializer_context()
        context.update({
            "food_id": self.kwargs['pk'],
        })
        return context
#
# @authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
# class ApiFoodImageUpload(generics.CreateAPIView):
#     serializer_class = UserFoodImageSerializer
#     queryset = UserFoodImage.objects.all()
#
#
