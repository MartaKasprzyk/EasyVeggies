from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from GrowVeggies.models import Seed, Veggie, Company, GrowVeggie, Plan, Bed, VeggieBed, VeggieFamily
from GrowVeggies.forms import SeedCreateForm, VeggieCreateForm, CompanyCreateForm, GrowVeggieCreateForm
from GrowVeggies.forms import VeggieUpdateForm, CompanyUpdateForm, SeedUpdateForm, GrowVeggieUpdateForm
# from GrowVeggies.forms import PlanOption1CreateForm
from GrowVeggies.models import PROGRESS

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


class GrowVeggieCreateView(LoginRequiredMixin, View):

    def get(self, request):
        form = GrowVeggieCreateForm()
        return render(request, 'grow_veggie_add.html', {'form': form})

    def post(self, request):
        user = request.user
        form = GrowVeggieCreateForm(request.POST)
        if form.is_valid():
            veggie = form.cleaned_data['veggie']
            sun = form.cleaned_data.get('sun')
            water = form.cleaned_data.get('water')
            soil = form.cleaned_data.get('soil')
            sow = form.cleaned_data.get('sow')
            comment = form.cleaned_data['comment']
            grow_veggie = GrowVeggie.objects.create(owner=user, veggie=veggie, comment=comment)
            grow_veggie.sun.set(sun)
            grow_veggie.water.set(water)
            grow_veggie.soil.set(soil)
            grow_veggie.sow.set(sow)
            return redirect('grow_veggie_add')
        return render(request, 'grow_veggie_add.html', {'form': form})


class GrowVeggieUpdateView(LoginRequiredMixin, View):

    def get(self, request, pk):
        grow_veggie = GrowVeggie.objects.get(pk=pk)
        form = GrowVeggieUpdateForm(instance=grow_veggie)
        return render(request, 'form.html', {'form': form})

    def post(self, request, pk):
        grow_veggie = GrowVeggie.objects.get(pk=pk)
        form = GrowVeggieUpdateForm(request.POST, instance=grow_veggie)
        if form.is_valid():
            form.save()
            return redirect('grow_veggie_add', grow_veggie.pk)
        return render(request, 'form.html', {'form': form})


class GrowVeggieDeleteView(UserPassesTestMixin, View):

    def test_func(self):
        user = self.request.user
        grow_veggie = GrowVeggie.objects.get(pk=self.kwargs['pk'])
        return grow_veggie.owner == user

    def get(self, request, pk):
        grow_veggie = GrowVeggie.objects.get(pk=pk)
        return render(request, 'grow_veggie_delete.html', {"grow_veggie": grow_veggie})

    def post(self, request, pk):
        delete = request.POST.get('delete')
        if delete == 'YES':
            grow_veggie = GrowVeggie.objects.get(pk=pk)
            grow_veggie.delete()
        return redirect('grow_veggies')


class GrowVeggieListView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        grow_veggies = GrowVeggie.objects.filter(owner=user)
        return render(request, 'grow_veggies.html', {'grow_veggies': grow_veggies})


class PlanView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'plan.html')


class PlanCreateFirstView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'plan_option1.html')

    def post(self, request):
        beds_amount = int(request.POST.get('beds_amount'))
        beds = []
        for bed in range(beds_amount):
            bed = 'name'
            beds.append(bed)

        veggies = Veggie.objects.all()
        families = VeggieFamily.objects.all()
        progress = PROGRESS
        # if beds_amount > 0:
        #     user = request.user
        #     for bed in range(beds_amount):
        #         Bed.objects.create(owner=user)
        #
        # beds = Bed.objects.all()

        return render(request, 'plan_option1.html', {'beds_amount': beds_amount, 'beds': beds,
                                                     'veggies': veggies, 'families': families, 'progress':progress})


class PlanCreateBasedOnLastView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'plan_option2.html')


class PlanListView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        plans = Plan.objects.filter(owner=user)
        return render(request, 'plan_list.html', {'plans': plans})
