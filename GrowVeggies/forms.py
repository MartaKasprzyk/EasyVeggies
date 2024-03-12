from django import forms
from GrowVeggies.models import Seed, Veggie, Company


class VeggieCreateForm(forms.ModelForm):
    class Meta:
        model = Veggie
        fields = "__all__"
        widgets = {
            'family': forms.Select(),
        }


class VeggieFlowUpdateForm(forms.ModelForm):
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


class CompanyFlowUpdateForm(forms.ModelForm):
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


class SeedFlowUpdateForm(forms.ModelForm):
    class Meta:
    model = Seed
    fields = ['veggie', 'variety', 'company', 'comment']
    widgets = {
        'veggie': forms.Select(),
        'company': forms.Select(),
    }