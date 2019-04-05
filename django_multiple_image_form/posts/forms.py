from django import forms
from .models import Post, Prep
from django.forms import inlineformset_factory


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'message', 'post_image',)

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['post_image'].widget = forms.FileInput(attrs={
            'id': 'main_image'})
        self.fields['post_image'].label = "Image of dish (An image of the actual dish made by you)"
        self.fields['message'].label = "Recipe"
        self.fields['message'].widget.attrs['placeholder'] = "Recipe in detail"

    # widgets = {
    #     'post_image': forms.FileInput(attrs={'class': 'form-control', 'id': 'main_input'})
    # }


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'message', 'post_image', )

    def __init__(self, *args, **kwargs):
        super(PostEditForm, self).__init__(*args, **kwargs)
        self.fields['post_image'].widget = forms.FileInput(attrs={
            'id': 'main_image'})
        self.fields['post_image'].label = "Image of dish (An image of the actual dish made by you)"
        self.fields['message'].label = "Recipe"
        self.fields['message'].widget.attrs['placeholder'] = "Recipe in detail"


class PrepForm(forms.ModelForm):
    class Meta:
        model = Prep
        fields = ('image', 'image_title', 'image_description')


class PrepEditForm(forms.ModelForm):
    class Meta:
        model = Prep
        fields = ('image', 'image_title', 'image_description', 'sequence')

    def __init__(self, *args, **kwargs):
        super(PrepEditForm, self).__init__(*args, **kwargs)
        self.fields['sequence'].required = True


PrepFormSet = inlineformset_factory(Post, Prep, form=PrepForm, extra=12, max_num=12, min_num=2)

PrepEditFormSet = inlineformset_factory(Post, Prep, form=PrepEditForm, extra=12, max_num=12, min_num=2)