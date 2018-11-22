from django import forms

class CartGroupForm(forms.Form):
    group_name = forms.CharField(max_length=30)
    
