from django import forms
from GrowVeggies.models import Seed, Veggie, Company, GrowVeggie, Plan, Bed, VeggieBed, VeggieFamily


class VeggieCreateForm(forms.ModelForm):
    class Meta:
        model = Veggie
        fields = "__all__"
        widgets = {
            'family': forms.Select(),
        }


class VeggieUpdateForm(forms.ModelForm):
    class Meta:
        model = Veggie
        fields = "__all__"
        widgets = {
            'family': forms.Select(),
        }


class CompanyCreateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"


class CompanyUpdateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"


class SeedCreateForm(forms.ModelForm):
    class Meta:
        model = Seed
        fields = ['veggie', 'variety', 'company', 'comment']
        widgets = {
            'veggie': forms.Select(),
            'company': forms.Select(),
        }


class SeedUpdateForm(forms.ModelForm):
    class Meta:
        model = Seed
        fields = ['veggie', 'variety', 'company', 'comment']
        widgets = {
            'veggie': forms.Select(),
            'company': forms.Select(),
        }


class GrowVeggieCreateForm(forms.ModelForm):
    class Meta:
        model = GrowVeggie
        fields = ['veggie', 'sun', 'water', 'soil', 'sow', 'comment']
        widgets = {
            'veggie': forms.Select(),
            'sun': forms.CheckboxSelectMultiple(),
            'water': forms.CheckboxSelectMultiple(),
            'soil': forms.CheckboxSelectMultiple(),
            'sow': forms.CheckboxSelectMultiple(),
        }


class GrowVeggieUpdateForm(forms.ModelForm):
    class Meta:
        model = GrowVeggie
        fields = ['veggie', 'sun', 'water', 'soil', 'sow', 'comment']
        widgets = {
            'veggie': forms.Select(),
            'sun': forms.CheckboxSelectMultiple(),
            'water': forms.CheckboxSelectMultiple(),
            'soil': forms.CheckboxSelectMultiple(),
            'sow': forms.CheckboxSelectMultiple(),
        }
