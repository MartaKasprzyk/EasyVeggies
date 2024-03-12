from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from GrowVeggies.models import Seed, Veggie, Company
from GrowVeggies.forms import SeedCreateForm, VeggieCreateForm, CompanyCreateForm
from GrowVeggies.forms import VeggieUpdateForm, CompanyUpdateForm, SeedUpdateForm


class BaseView(View):

    def get(self, request):
        return render(request, 'base.html')


class VeggieCreateView(LoginRequiredMixin, View):

    def get(self, request):
        form = VeggieCreateForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = VeggieCreateForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            family = form.cleaned_data['family']
            Veggie.objects.create(name=name, family=family)
            return redirect('seed_add')
        return render(request, 'form.html', {'form': form})


# This functionality will not be allowed
# class VeggieUpdateView(LoginRequiredMixin, View):
#
#     def get(self, request, pk):
#         veggie = Veggie.objects.get(pk=pk)
#         form = VeggieUpdateForm(instance=veggie)
#         return render(request, 'form.html', {'form': form})
#
#     def post(self, request, pk):
#         veggie = Veggie.objects.get(pk=pk)
#         form = VeggieUpdateForm(request.POST, instance=veggie)
#         if form.is_valid():
#             form.save()
#             return redirect('seed_add', veggie.pk)
#         return render(request, 'form.html', {'form': form})


class CompanyCreateView(LoginRequiredMixin, View):

    def get(self, request):
        form = CompanyCreateForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = CompanyCreateForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            Company.objects.create(name=name)
            return redirect('seed_add')
        return render(request, 'form.html', {'form': form})


# This functionality will not be allowed
# class CompanyUpdateView(LoginRequiredMixin, View):
#
#     def get(self, request, pk):
#         company = Company.objects.get(pk=pk)
#         form = CompanyUpdateForm(instance=company)
#         return render(request, 'form.html', {'form': form})
#
#     def post(self, request, pk):
#         company = Company.objects.get(pk=pk)
#         form = CompanyUpdateForm(request.POST, instance=company)
#         if form.is_valid():
#             form.save()
#             return redirect('seed_add', company.pk)
#         return render(request, 'form.html', {'form': form})


class SeedCreateView(LoginRequiredMixin, View):

    def get(self, request):
        form = SeedCreateForm()
        return render(request, 'seed_add.html', {'form': form})

    def post(self, request):
        user = request.user
        form = SeedCreateForm(request.POST)
        if form.is_valid():
            veggie = form.cleaned_data['veggie']
            variety = form.cleaned_data['variety']
            company = form.cleaned_data['company']
            comment = form.cleaned_data['comment']
            Seed.objects.create(owner=user, veggie=veggie, variety=variety, company=company, comment=comment)
            return redirect('seed_add')
        return render(request, 'seed_add.html', {'form': form})


class SeedUpdateView(LoginRequiredMixin, View):

    def get(self, request, pk):
        seed = Seed.objects.get(pk=pk)
        form = SeedUpdateForm(instance=seed)
        return render(request, 'form.html', {'form': form})

    def post(self, request, pk):
        seed = Seed.objects.get(pk=pk)
        form = SeedUpdateForm(request.POST, instance=seed)
        if form.is_valid():
            form.save()
            return redirect('seed_add', seed.pk)
        return render(request, 'form.html', {'form': form})


class SeedDeleteView(UserPassesTestMixin, View):

    def test_func(self):
        user = self.request.user
        seed = Seed.objects.get(pk=self.kwargs['pk'])
        return seed.owner == user

    def get(self, request, pk):
        seed = Seed.objects.get(pk=pk)
        return render(request, 'seed_delete.html', {"seed": seed})

    def post(self, request, pk):
        delete = request.POST.get('delete')
        if delete == 'YES':
            seed = Seed.objects.get(pk=pk)
            seed.delete()
        return redirect('seeds')


class SeedsListView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        seeds = Seed.objects.filter(owner=user)
        return render(request, 'seeds.html', {'seeds': seeds})
