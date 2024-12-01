from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django import forms
from .models import Award, Director, Genre
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy
from movies.models import Genre
from datetime import date
from dateutil.relativedelta import relativedelta

User = get_user_model()
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        max_length=15,  # 유저네임 최대 길이 15자로 설정
        label="아이디",
        error_messages={ 
            'required': '아이디를 입력해주세요.',
            'unique': '이미 사용중인 아이디입니다.',
            'invalid': '올바른 아이디를 입력해주세요. 영문자, 숫자, @/./+/-/_ 만 사용 가능합니다.'
        },
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput,
        max_length=15,  # 비밀번호 최대 길이 15자로 설정
        label="비밀번호",
        error_messages={ 
            'required': '비밀번호를 입력해주세요.',
            'too_common': '너무 일반적인 비밀번호입니다.',
            'too_similar': '아이디와 비슷한 비밀번호는 사용할 수 없습니다.',
            'too_short': '비밀번호는 최소 8자 이상이어야 합니다.',
            'numeric': '비밀번호는 숫자로만 이루어질 수 없습니다.'
        },
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput,
        max_length=15,  # 비밀번호 확인 최대 길이 15자로 설정
        label="비밀번호 확인",
        error_messages={
            'required': '비밀번호 확인을 입력해주세요.',
            'password_mismatch': '비밀번호가 일치하지 않습니다.'
        },
    )
    birth_date = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date'}), 
        label="생년월일"
    )
    nickname = forms.CharField(
        required=True,
        max_length=50,
        label="닉네임",
        error_messages={
            'required': '닉네임을 입력해주세요.',
            'unique': '이미 사용중인 닉네임입니다.',
        },
    )
    email = forms.EmailField(
        required=True,
        label="이메일",
        error_messages={
            'required': '이메일을 입력해주세요.',
            'invalid': '올바른 이메일 주소를 입력해주세요.'
        }
    )

    name = forms.CharField(
        required=True,
        max_length=50,
        label="이름",
        error_messages={
            'required': '이름을 입력해주세요.',
            'max_length': '이름은 50자를 초과할 수 없습니다.'
        }
    )
    class Meta:
        model = User
        fields = [
            'username', 'password1', 'password2', 
            'name', 'email', 
            'birth_date', 'nickname'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'username': '아이디',
            'password1': '비밀번호',
            'password2': '비밀번호 확인',
            'name': '이름',
            'email': '이메일',
            'birth_date': '생년월일',
            'nickname' : '닉네임',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # username 필드 에러 메시지
        self.fields['username'].error_messages = {
            'required': '아이디를 입력해주세요.',
            'unique': '이미 사용중인 아이디입니다.',
            'invalid': '올바른 아이디를 입력해주세요. 영문자, 숫자, @/./+/-/_ 만 사용 가능합니다.'
        }

        # 비밀번호 필드 에러 메시지
        self.fields['password1'].error_messages = {
            'required': '비밀번호를 입력해주세요.',
            'too_common': '너무 일반적인 비밀번호입니다.',
            'too_similar': '아이디와 비슷한 비밀번호는 사용할 수 없습니다.',
            'too_short': '비밀번호는 최소 8자 이상이어야 합니다.',
            'numeric': '비밀번호는 숫자로만 이루어질 수 없습니다.'
        }
        
        self.fields['password2'].error_messages = {
            'required': '비밀번호 확인을 입력해주세요.',
            'password_mismatch': '비밀번호가 일치하지 않습니다.'
        }

        # email 필드 에러 메시지
        self.fields['email'].error_messages = {
            'required': '이메일을 입력해주세요.',
            'invalid': '올바른 이메일 주소를 입력해주세요.'
        }
        # birth_date 필드 에러 메시지
        self.fields['birth_date'].error_messages = {
            'invalid': '올바른 날짜 형식으로 입력해주세요.'
        }

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if not password:
            raise forms.ValidationError("비밀번호를 입력해주세요.")
        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("이메일을 입력해주세요.")
        return email
    
    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            today = date.today()
            if birth_date:
                if birth_date > date.today():
                    raise forms.ValidationError("당신은 미래에서 왔나요?")
            max_age = 120
            min_date = today - relativedelta(years=max_age)
            if birth_date < min_date:
                raise forms.ValidationError("올바른 생년월일을 입력해주세요.")
        return birth_date
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("이미 존재하는 이메일입니다.")
        return email
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("이름을 입력해주세요.")
        return name
    

class CustomUserChangeForm(UserChangeForm):
    name = forms.CharField(
        required=True,
        max_length=50,
        label="이름",
        error_messages={
            'required': '이름을 입력해주세요.',
            'max_length': '이름은 50자를 초과할 수 없습니다.'
        }
    )

    favorite_genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('name', 'nickname', 'email', 'birth_date', 'favorite_genres')

    def clean_favorite_genres(self):
        genres = self.cleaned_data.get('favorite_genres')
        if genres and len(genres) > 3:
            raise forms.ValidationError("장르는 최대 3개까지만 선택할 수 있습니다.")
        return genres
    
class PreferenceForm(forms.ModelForm):
    favorite_genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='선호하는 장르'
    )

    class Meta:
        model = get_user_model()
        fields = ['favorite_genres']

    def clean_favorite_genres(self):
        genres = self.cleaned_data.get('favorite_genres')
        if genres and len(genres) > 3:
            raise forms.ValidationError("장르는 최대 3개까지만 선택할 수 있습니다.")
        return genres
    
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 각 필드의 위젯에 클래스 추가
        self.fields['old_password'].widget.attrs.update({
            'class': 'password-change-input'
        })
        self.fields['new_password1'].widget.attrs.update({
            'class': 'password-change-input'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'password-change-input'
        })
        
        self.error_messages = {
            'password_incorrect': '기존 비밀번호가 일치하지 않습니다.',
            'password_mismatch': '두 비밀번호가 일치하지 않습니다.',
            'password_too_similar': '비밀번호가 사용자 이름과 너무 유사합니다.',
            'password_too_short': '비밀번호가 너무 짧습니다. 최소 8자 이상이어야 합니다.',
            'password_too_common': '비밀번호가 너무 일반적입니다.',
            'password_entirely_numeric': '비밀번호는 숫자로만 이루어질 수 없습니다.',
        }

        # 각 필드의 help_text 제거 (선택사항)
        self.fields['new_password1'].help_text = ''
        self.fields['new_password2'].help_text = ''

    def clean_new_password2(self):
        old_password = self.cleaned_data.get('old_password')
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')

        # 기본 유효성 검사 수행
        new_password2 = super().clean_new_password2()

        # 이전 비밀번호와 새 비밀번호가 같은지 확인
        if old_password and new_password1 and old_password == new_password1:
            raise ValidationError(
                gettext_lazy("새 비밀번호는 이전 비밀번호와 같을 수 없습니다."),
                code='password_unchanged'
            )

        return new_password2
