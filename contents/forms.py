from django import forms


class ContentForm(forms.Form):
    title = forms.CharField(
        label='Title',
        required=False,
        max_length=100

    )
    author_name = forms.CharField(
        label='Author Name',
        required=False,
        max_length=100
        )
    