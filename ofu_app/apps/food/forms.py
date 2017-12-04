from django import forms
from apps.food.models import UserFoodImage


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserFoodImage
        fields = ['image']
