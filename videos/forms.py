from django import forms

from videos.models import Video


class VideoForm(forms.ModelForm):
    # order   = forms.IntegerField(widget=forms.TextInput())
    class Meta:
        model = Video
        fields = [
            'title',
            'embed_code',
        ]
