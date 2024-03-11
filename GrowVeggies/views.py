from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from GrowVeggies.models import Seed, Veggie, Company
from GrowVeggies.forms import SeedCreateForm, VeggieCreateForm, CompanyCreateForm


class BaseView(View):

    def get(self, request):
        return render(request, 'base.html')


class VeggieCreateView(LoginRequiredMixin, View):

    def get(self, request):
        form = VeggieCreateForm()
        return render(request, 'form.html', {'form': form})


class CompanyCreateView(LoginRequiredMixin, View):

    def get(self, request):
        form = CompanyCreateForm()
        return render(request, 'form.html', {'form': form})


class SeedCreateView(LoginRequiredMixin, View):

    def get(self, request):
        form = SeedCreateForm()
        return render(request, 'seed_add.html', {'form': form})

