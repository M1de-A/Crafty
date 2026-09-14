from django import forms
from .models import Shop
from marketplace.models import Product

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'slug', 'description', 'avatar', 'banner']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Например, Lumi Handmade'}),
            'slug': forms.TextInput(attrs={'placeholder': 'lumi-handmade'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Расскажите о магазине и своих работах...'}),
            'avatar': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'banner': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }
    def clean_name(self):
        name=' '.join(self.cleaned_data['name'].split())
        qs=Shop.objects.filter(name__iexact=name)
        if self.instance.pk: qs=qs.exclude(pk=self.instance.pk)
        if qs.exists(): raise forms.ValidationError('Магазин с таким названием уже существует. Придумайте другое название.')
        return name

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'category', 'description', 'price', 'stock', 'image', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Название товара'}),
            'slug': forms.TextInput(attrs={'placeholder': 'unikalnaya-svecha'}),
            'description': forms.Textarea(attrs={'rows': 7, 'placeholder': 'Материалы, размеры, особенности и история товара...'}),
            'price': forms.NumberInput(attrs={'min': '0', 'step': '0.01', 'placeholder': '0.00'}),
            'stock': forms.NumberInput(attrs={'min': '0', 'step': '1'}),
        }
