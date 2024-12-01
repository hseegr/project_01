from django import forms
from .models import Article, Comment

class ArticleForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        ('MOVIE', '영화'),
        ('TICKET', '티켓 거래'),
        ('CHAT', '잡담'),
    ]
    
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, label='카테고리')

    class Meta:
        model = Article
        fields = ['title', 'content', 'image', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['content'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']