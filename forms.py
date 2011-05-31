from django import forms

class UrlForm(forms.Form):
    url = forms.URLField(label='Shorten this URL', verify_exists=True, max_length=1000)
