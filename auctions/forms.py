from django import forms

from .models import Category

class ListingCreateForm(forms.Form):
    title = forms.CharField(label="Title", required=True, max_length=64)
    description = forms.CharField(label="Description", widget=forms.Textarea(), required=True)
    starting_price = forms.IntegerField(label="Starting price", required=True)
    category = forms.ModelChoiceField(label="Categories", queryset=Category.objects.all(), required=False)
    image = forms.CharField(label="Image", required=False)
    

    def __init__(self, *args, **kwargs):
        super(ListingCreateForm, self).__init__(*args, **kwargs)
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'