from django import forms
from apps.food.models import FoodImage


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = FoodImage
        fields = ['image']
