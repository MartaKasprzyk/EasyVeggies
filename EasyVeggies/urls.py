"""
URL configuration for EasyVeggies project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from GrowVeggies import views
from Users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    path('register/', user_views.RegisterUserView.as_view(), name='registration'),
    path('login/', user_views.LoginView.as_view(), name='login'),
    path('logout/', user_views.LogoutView.as_view(), name='logout'),
    path('veggie/add/', views.VeggieCreateView.as_view(), name='veggie_add'),
    # path('veggie/update/<int:pk>/', views.VeggieUpdateView.as_view(), name='veggie_update'),
    path('company/add/', views.CompanyCreateView.as_view(), name='company_add'),
    # path('company/update/<int:pk>/', views.CompanyUpdateView.as_view(), name='company_update'),
    path('seed/add/', views.SeedCreateView.as_view(), name='seed_add'),
    path('seed/update/<int:pk>/', views.SeedUpdateView.as_view(), name='seed_update'),
    path('seed/delete/<int:pk>/', views.SeedDeleteView.as_view(), name='seed_delete'),
    path('seeds/', views.SeedsListView.as_view(), name='seeds'),
    path('growveggie/add/', views.GrowVeggieCreateView.as_view(), name='grow_veggie_add'),
    path('growveggie/update/<int:pk>/', views.GrowVeggieUpdateView.as_view(), name='grow_veggie_update'),
    path('growveggie/delete/<int:pk>/', views.GrowVeggieDeleteView.as_view(), name='grow_veggie_delete'),
    path('growveggies/', views.GrowVeggieListView.as_view(), name='grow_veggies'),
    path('plan/', views.PlanView.as_view(), name='plan'),
    path('plan/option1/', views.PlanCreateOption1View.as_view(), name='plan_option1'),
    path('plan/option2/', views.PlanCreateOption2View.as_view(), name='plan_option2'),
    path('plan/option2/upload_plan/', views.PlanCreateOption2UploadView.as_view(), name='plan_option2_upload_plan'),
    path('plan/option2/choose/', views.PlanCreateOption2ChooseView.as_view(), name='plan_option2_choose'),
    path('plan/list/', views.PlanListView.as_view(), name='plan_list'),
    path('plan/details/<int:pk>/', views.PlanDetailsView.as_view(), name='plan_details'),
    path('plan/update/<int:pk>/', views.PlanUpdateView.as_view(), name='plan_update'),
    path('plan/delete/<int:pk>/', views.PlanDeleteView.as_view(), name='plan_delete'),
    path('bed/details/<int:pk>/', views.BedDetailsView.as_view(), name='bed_details'),
    path('bed/update/<int:pk>/', views.BedUpdateView.as_view(), name='bed_update'),
    path('bed/delete/<int:pk>/', views.BedDeleteView.as_view(), name='bed_delete'),
    path('filter_veggies/', views.FilterVeggiesView.as_view(), name='filter_veggies'),
    path('seeds/pdf/', views.SeedsPdfView.as_view(), name='seeds_pdf'),
    path('growveggies/pdf/', views.GrowVeggiesPdfView.as_view(), name='grow_veggies_pdf'),
    path('plan/details/pdf/<int:pk>/', views.PlanDetailsPdfView.as_view(), name='plan_details_pdf'),
    ]
