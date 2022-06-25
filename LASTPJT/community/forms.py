from django import forms
from .models import Community, CommunityComment

class CommunityForm(forms.ModelForm):
    # 공지, 잡담, 후기, 베스트리뷰어, 극장/이벤트, 기타
    commu_1 = '공지',
    commu_2 = '잡담',
    commu_3 = '영화리뷰',
    commu_4 = '극장/이벤트',
    commu_5 = '기타',

    COMMU_CHOICES = [
        (commu_1 , '공지'),
        (commu_2 , '잡담'),
        (commu_3 , '영화리뷰'),
        (commu_4 , '극장/이벤트'),
        (commu_5 , '기타'),
    ]
    
    category = forms.ChoiceField(
        label ='카테고리',
        choices=COMMU_CHOICES,
        widget=forms.Select(
            attrs = {
                'class' : 'my-category form-control'
            }
        )
    )

    title = forms.CharField(
        widget=forms.TextInput(
            attrs = {
                'placeholder':'커뮤니티 글 제목 작성',
                'class' : 'my-title form-control',
            }
        )
    )

    content = forms.CharField(
        widget=forms.Textarea(
            attrs = {
                'placeholder':'커뮤니티 글 내용 작성',
                'class' : 'my-title form-control',
            }
        )
    )
    class Meta:
        model = Community
        fields = ('category','title','content','imgfile')


class CommunityCommentForm(forms.ModelForm):
    content = forms.CharField(
        label = 'content',
        widget= forms.TextInput(
            attrs = {
                'class':'my-content form-control',
            }
        )
    )
    
    class Meta:
        model = CommunityComment
        fields = ('content',)