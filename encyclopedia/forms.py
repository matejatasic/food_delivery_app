from django import forms

class PageCreateForm(forms.Form):
    title = forms.CharField(
        label="Title", 
        widget=forms.TextInput(attrs={"style": "width: 300px; display: block;"}), 
        required=True
    )
    content = forms.CharField(
        label="Page Content", 
        widget=forms.Textarea(attrs={"style": "width: 300px; display: block"}), 
        required=True
    )

class PageEditForm(forms.Form):
    content = forms.CharField(
        label="Page Content", 
        widget=forms.Textarea(attrs={"style": "width: 300px; display: block"}), 
        required=True
    )