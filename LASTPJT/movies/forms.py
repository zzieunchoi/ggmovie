from django import forms
from .models import MovieComment

class MovieCommentForm(forms.ModelForm):

    content = forms.CharField(
        widget=forms.TextInput(
            attrs = {
                'placeholder':'영화 리뷰 작성하기',
                'class' : 'my-content form-control',
            }
        )
    )
    
    # 0~10까지 숫자 범위 제한을 두고 싶어!
    rank = forms.IntegerField(
        widget = forms.NumberInput(
            attrs = {
                'placeholder':'평가 점수(0~10)',
                'class': 'score my-rank form-control',
                'min':0,
                'max':10,
            }
        )
    )

    class Meta:
        model = MovieComment
        fields = ('content','rank',)