from django import forms
from .models import MovieComment

class MovieCommentForm(forms.ModelForm):
    class Meta:
        model = MovieComment
        fields = ('content',)

class CityForm(forms.Form):
    city = forms.CharField(
        max_length=50, 
        label="City Name",
        widget=forms.TextInput(attrs={
            'placeholder': '도시명을 입력해주세요'
        })
    )