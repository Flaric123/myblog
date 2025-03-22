from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    guest_name = forms.CharField(
        required=False,
        label="Ваше имя",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Comment
        fields = ['content', 'guest_name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user and self.user.is_authenticated:
            del self.fields['guest_name']

    def clean(self):
        cleaned_data = super().clean()
        if not self.user.is_authenticated and not cleaned_data.get('guest_name'):
            raise forms.ValidationError("Пожалуйста, укажите ваше имя")
        return cleaned_data
