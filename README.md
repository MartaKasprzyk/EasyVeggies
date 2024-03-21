# EasyVeggies

Final project made at the Python Developer course at CodersLab – IT School. This user-friendly web application was prepared in Django and has been tested using pytest unit tests.

Application helps gardeners to keep their veggie gardens organized and plan their crops according to the crop rotation rule. Home page is available to all users, but the further functionalities can be accessed only by the registered and logged users. 

![EasyVeggies_01](https://github.com/MartaKasprzyk/EasyVeggies/assets/154241273/7167e4a8-5298-4acb-a0b7-b69d4f7dcd23)

**PLAN**– in this section users easily plan their veggie crops, several options are available:
1. First time planning of veggie beds – application dynamically displays available veggies for the veggie family of choice
2. Planning based on last year – user can either choose to use the last year plan as the base or input manually veggie families that has been growing in veggie beds, based on the provided veggie families application dynamically displays what families can be grown next
3. View all saved plans, search for the plan of interest, CRUD operations available to each plan as well as RUD operations available for each bed in the given plan (beds are created automatically when plan is saved), 
    so the gardener can specify what conditions each of the beds had, application counts and displays the saved plans, details of each plan can be downloaded in pdf (ReportLab)

![EasyVeggies_02](https://github.com/MartaKasprzyk/EasyVeggies/assets/154241273/f568633a-57af-43d3-8d2c-f7766f294437)

**SEEDS** – in this section gardeners can store their collection of seeds, for each seed all CRUD operations are available, seed list can be downloaded in pdf and filtered on several parameters, applications counts and displays the total number of seeds for the given logged gardener

![EasyVeggies_03](https://github.com/MartaKasprzyk/EasyVeggies/assets/154241273/0536f67e-f797-43eb-ac18-49bed00a17c3)

**GROW** – in this section gardeners can store information regarding the growing conditions for their veggies, for each record all CRUD operations are available, list of conditions can be downloaded in pdf and filtered on several parameters, applications counts and displays the total number of all growing condition for a logged gardener

![EasyVeggies_04](https://github.com/MartaKasprzyk/EasyVeggies/assets/154241273/1a7cced6-2220-4c3f-a1af-37d1e706f0fa)

Project involves the use of Django-forms as well as custom made forms. Application styling is prepared in CSS and for some parts Bootstrap was applied. Application logo was prepared in Canva. Pictures used in this project are of my authorship and can be freely used. 

## Requirements

- Django==5.0.3
- psycopg2==2.9.9
- pytest==8.1.1
- pytest-django==4.8.0
- reportlab==4.1.0
