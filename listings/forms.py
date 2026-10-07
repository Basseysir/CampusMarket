from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'category', 'price', 'condition', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-md'}),
            'category': forms.Select(attrs={'class': 'w-full p-2 border rounded-md'}),
            'price': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-md', 'step': '0.01'}),
            'condition': forms.Select(attrs={'class': 'w-full p-2 border rounded-md'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-2 border rounded-md', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'w-full p-2 border rounded-md'}),
        }