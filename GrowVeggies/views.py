from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from GrowVeggies.models import Seed, Veggie, Company, GrowVeggie, Plan, Bed, VeggieBed, VeggieFamily
from GrowVeggies.forms import SeedCreateForm, VeggieCreateForm, CompanyCreateForm, GrowVeggieCreateForm
from GrowVeggies.forms import VeggieUpdateForm, CompanyUpdateForm, SeedUpdateForm, GrowVeggieUpdateForm
# from GrowVeggies.forms import PlanOption1CreateForm
from GrowVeggies.models import PROGRESS
from bs4 import BeautifulSoup


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
    def create_bed_objects(self, request):
        user = request.user

        user_beds = request.POST.getlist('bed_name')

        bed_objs_pks = []
        for user_bed in user_beds:
            bed_obj = Bed.objects.create(owner=user, name=user_bed)
            bed_objs_pks.append(bed_obj.pk)

        return bed_objs_pks

    def create_plan_object(self, request):
        user = request.user

        plan_name = request.POST.get('plan_name')
        plan = Plan.objects.create(owner=user, name=plan_name)
        plan_id = plan.pk

        return plan_id

    def create_grow_veggies_objects(self, request, amount, bed_objs_pks, plan_id):

        veggie = request.POST.getlist('veggie')
        bed = bed_objs_pks
        progress = request.POST.getlist('progress')
        plan = plan_id

        vb_objs = []
        for i in range(amount):
            vb = VeggieBed.objects.create(veggie_id=veggie[i], bed_id=bed[i], progress=progress[i], plan_id=plan)
            vb_objs.append(vb)

        return vb_objs


    def get(self, request):
        return render(request, 'plan_option1.html')

    def post(self, request):
        beds_amount = int(request.POST.get('beds_amount'))
        beds = [bed for bed in range(beds_amount)]

        veggies = Veggie.objects.all().order_by('name')
        families = VeggieFamily.objects.all().order_by('order')
        progress = sorted(PROGRESS, key=lambda x: x[0])

        plan = request.POST.get('save_plan')
        if plan == "SAVE PLAN":
            amount = int(request.POST.get('beds_amount'))

            bed_objs_pks = self.create_bed_objects(request)
            plan_id = self.create_plan_object(request)
            self.create_grow_veggies_objects(request, amount, bed_objs_pks, plan_id)

            return redirect('plan_list')

        return render(request, 'plan_option1.html', {'beds_amount': beds_amount, 'beds': beds,
                                                     'veggies': veggies, 'families': families, 'progress': progress})


class PlanCreateBasedOnLastView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'plan_option2.html')


class PlanListView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        plans = Plan.objects.filter(owner=user)
        return render(request, 'plan_list.html', {'plans': plans})
