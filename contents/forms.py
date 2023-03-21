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
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ContentForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['author_name'].widget.attrs['class'] = 'form-control'
    