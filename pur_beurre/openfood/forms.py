from django import forms

class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, label="Je veux remplacer ")
