from django import forms

from webapp.models import Product, Review


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'category', 'description', 'picture')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('review_text', 'rate', )


class ModerForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('review_text', 'rate', 'is_moderated')