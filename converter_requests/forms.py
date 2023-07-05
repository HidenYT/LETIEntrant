from django import forms

class TextSendForm(forms.Form):
    FILE_FORMATS = (
        ('XML', 'xml'),
        ('JSON', 'json')
    )
    text = forms.CharField(widget=forms.Textarea())
    file_format_choice = forms.ChoiceField(choices=FILE_FORMATS)