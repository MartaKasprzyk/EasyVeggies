from django import forms
from GrowVeggies.models import Seed, Veggie, Company, GrowVeggie, Plan, Bed, VeggieBed, VeggieFamily
from GrowVeggies.models import SunScale, WaterScale, SoilScale


class VeggieCreateForm(forms.ModelForm):
    class Meta:
        model = Veggie
        fields = "__all__"
        widgets = {
            'family': forms.Select(attrs={'class': 'select-styling'})
        }


class VeggieUpdateForm(forms.ModelForm):
    class Meta:
        model = Veggie
        fields = "__all__"
        widgets = {
            'family': forms.Select(attrs={'class': 'select-styling'}),
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
            'veggie': forms.Select(attrs={'class': 'select-styling'}),
            'company': forms.Select(attrs={'class': 'select-styling'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['veggie'].queryset = self.fields['veggie'].queryset.order_by('name')
        self.fields['company'].queryset = self.fields['company'].queryset.order_by('name')


class SeedUpdateForm(forms.ModelForm):
    class Meta:
        model = Seed
        fields = ['veggie', 'variety', 'company', 'comment']
        widgets = {
            'veggie': forms.Select(attrs={'class': 'select-styling'}),
            'company': forms.Select(attrs={'class': 'select-styling'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['veggie'].queryset = self.fields['veggie'].queryset.order_by('name')
        self.fields['company'].queryset = self.fields['company'].queryset.order_by('name')

class GrowVeggieCreateForm(forms.ModelForm):
    class Meta:
        model = GrowVeggie
        fields = ['veggie', 'sun', 'water', 'soil', 'sow', 'comment']
        widgets = {
            'veggie': forms.Select(attrs={'class': 'select-styling'}),
            'sun': forms.CheckboxSelectMultiple(),
            'water': forms.CheckboxSelectMultiple(),
            'soil': forms.CheckboxSelectMultiple(),
            'sow': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['veggie'].queryset = self.fields['veggie'].queryset.order_by('name')
        self.fields['sun'].queryset = self.fields['sun'].queryset.order_by('pk')
        self.fields['water'].queryset = self.fields['water'].queryset.order_by('pk')
        self.fields['soil'].queryset = self.fields['soil'].queryset.order_by('-pk')
        self.fields['sow'].queryset = self.fields['sow'].queryset.order_by('order')


class GrowVeggieUpdateForm(forms.ModelForm):
    class Meta:
        model = GrowVeggie
        fields = ['veggie', 'sun', 'water', 'soil', 'sow', 'comment']
        widgets = {
            'veggie': forms.Select(attrs={'class': 'select-styling'}),
            'sun': forms.CheckboxSelectMultiple(),
            'water': forms.CheckboxSelectMultiple(),
            'soil': forms.CheckboxSelectMultiple(),
            'sow': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['veggie'].queryset = self.fields['veggie'].queryset.order_by('name')
        self.fields['sun'].queryset = self.fields['sun'].queryset.order_by('pk')
        self.fields['water'].queryset = self.fields['water'].queryset.order_by('pk')
        self.fields['soil'].queryset = self.fields['soil'].queryset.order_by('-pk')
        self.fields['sow'].queryset = self.fields['sow'].queryset.order_by('order')


class BedUpdateForm(forms.ModelForm):
    class Meta:
        model = Bed
        fields = ['name', 'sun', 'water', 'soil']
        widgets = {
            'sun': forms.Select(attrs={'class': 'select-styling'}),
            'water': forms.Select(attrs={'class': 'select-styling'}),
            'soil': forms.Select(attrs={'class': 'select-styling'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sun'].queryset = self.fields['sun'].queryset.order_by('pk')
        self.fields['water'].queryset = self.fields['water'].queryset.order_by('pk')
        self.fields['soil'].queryset = self.fields['soil'].queryset.order_by('-pk')
