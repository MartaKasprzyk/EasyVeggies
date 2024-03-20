from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib  import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View

from GrowVeggies.forms import BedUpdateForm
from GrowVeggies.forms import SeedCreateForm, VeggieCreateForm, CompanyCreateForm, GrowVeggieCreateForm
from GrowVeggies.forms import SeedUpdateForm, GrowVeggieUpdateForm
from GrowVeggies.models import PROGRESS, SunScale, WaterScale, SoilScale, Month
from GrowVeggies.models import Seed, Veggie, Company, GrowVeggie, Plan, Bed, VeggieBed, VeggieFamily

import reportlab
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from datetime import datetime


class HomeView(View):

    def get(self, request):
        return render(request, 'home.html')


class VeggieCreateView(LoginRequiredMixin, View):

    def get(self, request):
        form = VeggieCreateForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = VeggieCreateForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            family = form.cleaned_data['family']
            if Veggie.objects.filter(name__iexact=name).exists():
                messages.info(request, "Veggie with this name already exists.")
                return redirect('veggie_add')
            else:
                Veggie.objects.create(name=name, family=family)
                return redirect('seed_add')

        return render(request, 'form.html', {'form': form})


class CompanyCreateView(LoginRequiredMixin, View):

    def get(self, request):
        form = CompanyCreateForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = CompanyCreateForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            if Company.objects.filter(name__iexact=name).exists():
                messages.info(request, "Company with this name already exists.")
                return redirect('company_add')
            else:
                Company.objects.create(name=name)
                return redirect('seed_add')

        return render(request, 'form.html', {'form': form})


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
            if Seed.objects.filter(owner=user, veggie=veggie,
                                   variety__iexact=variety, company=company).exists():
                messages.info(request, "This seed record already exists.")
                return redirect('seed_add')
            else:
                Seed.objects.create(owner=user, veggie=veggie, variety=variety, company=company, comment=comment)
                return redirect('seeds')

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
            return redirect('seeds')
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
        seeds_list = Seed.objects.filter(owner=user).order_by('veggie__name')
        number_of_seeds = seeds_list.count()
        seeds_per_page = 3

        veggies = Veggie.objects.all()
        companies = Company.objects.all()

        veggie = request.GET.get('veggie', '')
        company = request.GET.get('company', '')
        variety = request.GET.get('variety')

        if variety:
            seeds_list = seeds_list.filter(variety__icontains=variety)
        if veggie:
            seeds_list = seeds_list.filter(veggie=veggie)
        if company:
            seeds_list = seeds_list.filter(company=company)

        paginator = Paginator(seeds_list, seeds_per_page)
        page = request.GET.get('page')
        seeds = paginator.get_page(page)

        start_index = (seeds.number - 1) * seeds_per_page + 1

        context = {
            'seeds': seeds,
            'number_of_seeds': number_of_seeds,
            'start_index': start_index,
            'veggies': veggies,
            'companies': companies,
        }

        return render(request, 'seeds_list.html', context)



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
            return redirect('grow_veggies')
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
            return redirect('grow_veggies')
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
        grow_veggies_list = GrowVeggie.objects.filter(owner=user).order_by('veggie__name')
        number_of_conditions = grow_veggies_list.count()
        conditions_per_page = 3

        veggies = Veggie.objects.all().order_by('name')
        sun_scale = SunScale.objects.all().order_by('pk')
        water_scale = WaterScale.objects.all().order_by('pk')
        soil_scale = SoilScale.objects.all().order_by('-pk')
        months = Month.objects.all().order_by('order')

        veggie = request.GET.get('veggie', '')
        sun = request.GET.get('sun', '')
        water = request.GET.get('water')
        soil = request.GET.get('soil', '')
        sow = request.GET.get('sow', '')

        if veggie:
            grow_veggies_list = grow_veggies_list.filter(veggie=veggie)
        if sun:
            grow_veggies_list = grow_veggies_list.filter(sun=sun)
        if water:
            grow_veggies_list = grow_veggies_list.filter(water=water)
        if soil:
            grow_veggies_list = grow_veggies_list.filter(soil=soil)
        if sow:
            grow_veggies_list = grow_veggies_list.filter(sow=sow)

        paginator = Paginator(grow_veggies_list, conditions_per_page)
        page = request.GET.get('page')
        grow_veggies = paginator.get_page(page)

        start_index = (grow_veggies.number - 1) * conditions_per_page + 1

        context = {
            'grow_veggies': grow_veggies,
            'number_of_conditions': number_of_conditions,
            'start_index': start_index,
            'veggies': veggies,
            'sun_scale': sun_scale,
            'water_scale': water_scale,
            'soil_scale': soil_scale,
            'months': months,
        }

        return render(request, 'grow_veggies_list.html', context)


class PlanView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'plan.html')


class PlanCommonFunctionsMixin:
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

    def create_veggie_bed_objects(self, request, amount, bed_objs_pks, plan_id):

        veggie = request.POST.getlist('veggie')
        bed = bed_objs_pks
        progress = request.POST.getlist('progress')
        plan = plan_id

        vb_objs = []
        for i in range(amount):
            vb = VeggieBed.objects.create(veggie_id=veggie[i], bed_id=bed[i], progress=progress[i], plan_id=plan)
            vb_objs.append(vb)

        return vb_objs


class PlanCreateOption1View(PlanCommonFunctionsMixin, LoginRequiredMixin, View):

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
            self.create_veggie_bed_objects(request, amount, bed_objs_pks, plan_id)

            return redirect('plan_list')

        return render(request, 'plan_option1.html', {'beds_amount': beds_amount, 'beds': beds,
                                                     'veggies': veggies, 'families': families, 'progress': progress})


class PlanCreateOption2ChooseView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'plan_option2_choose.html')


class PlanCreateOption2View(PlanCommonFunctionsMixin, LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'plan_option2.html')

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
            self.create_veggie_bed_objects(request, amount, bed_objs_pks, plan_id)

            return redirect('plan_list')

        return render(request, 'plan_option2.html', {'beds_amount': beds_amount, 'beds': beds,
                                                     'veggies': veggies, 'families': families, 'progress': progress})


class PlanCreateOption2UploadView(PlanCommonFunctionsMixin, LoginRequiredMixin, View):
    def get(self, request):
        plan = request.GET.get('prev_plan')
        plans = Plan.objects.all()
        veggie_beds = VeggieBed.objects.all()
        amount = veggie_beds.count()
        families = VeggieFamily.objects.all().order_by('order')
        veggies = Veggie.objects.all().order_by('name')
        progress = sorted(PROGRESS, key=lambda x: x[0])
        if plan:
            veggie_beds = VeggieBed.objects.filter(plan=plan)
            amount = veggie_beds.count()

        return render(request, 'plan_option2_upload.html', {'plans': plans,
                                                            'veggie_beds': veggie_beds, 'families': families,
                                                            'veggies': veggies, 'progress': progress,
                                                            'amount': amount})

    def post(self, request):
        plan = request.POST.get('save_plan')
        if plan == "SAVE PLAN":
            amount = int(request.POST.get('amount'))

            bed_objs_pks = self.create_bed_objects(request)
            plan_id = self.create_plan_object(request)
            self.create_veggie_bed_objects(request, amount, bed_objs_pks, plan_id)

            return redirect('plan_list')


class PlanListView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        plan_list = Plan.objects.filter(owner=user).order_by('name')
        number_of_plans = plan_list.count()
        plans_per_page = 5

        plan = request.GET.get('plan')
        if plan:
            plan_list = plan_list.filter(name__icontains=plan)

        paginator = Paginator(plan_list, plans_per_page)
        page = request.GET.get('page')
        plans = paginator.get_page(page)

        start_index = (plans.number - 1) * plans_per_page + 1

        context = {
            'plans': plans,
            'number_of_plans': number_of_plans,
            'start_index': start_index,
            'plan': plan
        }

        return render(request, 'plan_list.html', context)


class FilterVeggiesView(LoginRequiredMixin, View):
    def get(self, request):
        family = request.GET.get('family', '')
        families = VeggieFamily.objects.all().order_by("order")
        family_name = ''
        veggies = Veggie.objects.all().order_by("name")
        if family:
            veggies = veggies.filter(family=family).order_by("name")
            family_name = VeggieFamily.objects.filter(pk=family)

        return render(request, "filter_veggies.html", {'families': families, 'veggies': veggies,
                                                       'family': family_name})


class PlanDetailsView(LoginRequiredMixin, View):
    def get(self, request, pk):
        plan = Plan.objects.get(pk=pk)
        veggie_beds = VeggieBed.objects.filter(plan_id=pk)
        return render(request, "plan_details.html", {'plan': plan, 'veggie_beds': veggie_beds})


class PlanUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        plan = Plan.objects.get(pk=pk)
        veggie_beds = VeggieBed.objects.filter(plan_id=plan)
        families = VeggieFamily.objects.all().order_by('order')
        veggies = Veggie.objects.all().order_by('name')
        progress = sorted(PROGRESS, key=lambda x: x[0])
        return render(request, "plan_update.html", {'plan': plan, 'veggie_beds': veggie_beds,
                                                    'families': families, 'veggies': veggies, 'progress': progress})

    def post(self, request, pk):
        plan = Plan.objects.get(pk=pk)
        plan_veggie_beds = VeggieBed.objects.filter(plan_id=plan)

        plan_name = request.POST.get('plan_name')
        bed_name = request.POST.getlist('bed_name')
        veggie = request.POST.getlist('veggie')
        progress = request.POST.getlist('progress')

        plan.name = plan_name
        plan.save()

        index = 0
        for veggie_bed in plan_veggie_beds:
            veggie_bed.bed.name = bed_name[index]
            veggie_bed.veggie_id = veggie[index]
            veggie_bed.progress = progress[index]
            veggie_bed.bed.save()
            veggie_bed.veggie.save()
            veggie_bed.save()
            index += 1

        return redirect('plan_details', pk=plan.pk)


class PlanDeleteView(UserPassesTestMixin, View):
    def test_func(self):
        user = self.request.user
        plan = Plan.objects.get(pk=self.kwargs['pk'])
        return plan.owner == user

    def get(self, request, pk):
        plan = Plan.objects.get(pk=pk)
        return render(request, "plan_delete.html", {'plan': plan})

    def post(self, request, pk):
        delete = request.POST.get('delete')
        if delete == 'YES':
            plan = Plan.objects.get(pk=pk)
            plan.delete()
        return redirect('plan_list')


class BedDetailsView(LoginRequiredMixin, View):
    def get(self, request, pk):
        bed = Bed.objects.get(pk=pk)
        return render(request, "bed_details.html", {'bed': bed})


class BedUpdateView(LoginRequiredMixin, View):

    def get(self, request, pk):
        bed = Bed.objects.get(pk=pk)
        form = BedUpdateForm(instance=bed)
        return render(request, 'form.html', {'form': form, 'bed': bed})

    def post(self, request, pk):
        bed = Bed.objects.get(pk=pk)
        form = BedUpdateForm(request.POST, instance=bed)
        if form.is_valid():
            form.save()
            return redirect('bed_details', bed.pk)
        return render(request, 'form.html', {'form': form, 'bed': bed})


class BedDeleteView(UserPassesTestMixin, View):

    def test_func(self):
        user = self.request.user
        bed = Bed.objects.get(pk=self.kwargs['pk'])
        return bed.owner == user

    def get(self, request, pk):
        bed = Bed.objects.get(pk=pk)
        return render(request, 'bed_delete.html', {"bed": bed})

    def post(self, request, pk):
        delete = request.POST.get('delete')
        if delete == 'YES':
            bed = Bed.objects.get(pk=pk)
            bed.delete()
        return redirect('plan_list')


class PdfGeneratorMixin:
    def generate_pdf(self, request, lines):
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter, bottomup=0)
        text = p.beginText()
        text.setTextOrigin(inch, inch)
        text.setFont('Helvetica', 12)

        for line in lines:
            text.textLine(line)

        p.drawText(text)
        p.showPage()
        p.save()
        buffer.seek(0)

        return buffer


class SeedsPdfView(LoginRequiredMixin, PdfGeneratorMixin, View):
    def get(self, request):
        user = request.user
        seeds = Seed.objects.filter(owner=user).order_by('veggie__name')

        lines = []

        for seed in seeds:
            lines.append(
                f'{seed.veggie.name} - {seed.variety} ({seed.company.name})'
            )
            lines.append(f'Comments: {seed.comment}')
            lines.append(" ")

        buffer = self.generate_pdf(request, lines)

        return FileResponse(buffer, as_attachment=True, filename='Seeds.pdf')


class GrowVeggiesPdfView(LoginRequiredMixin, PdfGeneratorMixin, View):
    def get(self, request):
        user = request.user
        grow_veggies_conditions = GrowVeggie.objects.filter(owner=user).order_by('veggie__name')

        lines = []

        for condition in grow_veggies_conditions:
            lines.append(f'{condition.veggie.name}')

            sun = [sun.name for sun in condition.sun.all().order_by('pk')]
            formatted_sun = ', '.join(sun)
            lines.append(f'sun: {formatted_sun}')

            water = [water.name for water in condition.water.all().order_by('pk')]
            formatted_water = ', '.join(water)
            lines.append(f'water: {formatted_water}')

            soil = [soil.name for soil in condition.soil.all().order_by('pk')]
            formatted_soil = ', '.join(soil)
            lines.append(f'soil: {formatted_soil}')

            sow = [sow.name for sow in condition.sow.all().order_by('order')]
            formatted_sow = ', '.join(sow)
            lines.append(f'Sowing: {formatted_sow}')

            lines.append(f'Comments: {condition.comment}')
            lines.append(" ")

        buffer = self.generate_pdf(request, lines)

        return FileResponse(buffer, as_attachment=True, filename='Growing_conditions.pdf')


class PlanDetailsPdfView(LoginRequiredMixin, PdfGeneratorMixin, View):

    def get(self, request, pk):
        plan = Plan.objects.get(pk=pk)
        veggie_beds = VeggieBed.objects.filter(plan=plan)

        lines = []
        lines.append(f'PDF generated: {datetime.today().date()}')
        lines.append(" ")
        lines.append(f'Plan name: {plan.name}')
        lines.append(" ")

        for veggie_bed in veggie_beds:
            lines.append(f'Bed: {veggie_bed.bed.name}')
            lines.append(f'Family: {veggie_bed.veggie.family.name} Veggie: {veggie_bed.veggie.name} '
                         f'Status: {veggie_bed.get_progress_display()}')
            lines.append(" ")

        buffer = self.generate_pdf(request, lines)

        return FileResponse(buffer, as_attachment=True, filename=f'{plan.name}_Details.pdf')
