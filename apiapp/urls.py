from django.contrib import admin
from django.urls import path
from django.urls import path,include
from django.conf.urls import url
from apiapp import views
urlpatterns = [
    url(r'^$', views.landing),
    path('district/<str:state>',views.districtapi,name='api'),
    path('details/<str:state>',views.details,name='api'),
    path('hospitals/<str:state>/<str:district>',views.hospitalapi,name='api'),
    path('nearhospitals/<str:state>/<str:lat>/<str:lon>/<str:distance>',views.hospitalnear,name='api'),
    path('state',views.stateapi,name='api'),
    path('availablebedtype/<str:state>/<str:districtcode>/<str:bedtype>',views.availablebedtype,name = 'available bedtype'),
    path('vaccine/pincode/<str:pincode>/<str:feetype>/<str:vaccinetype>/<str:avail>', views.vaccinecenters, name = 'vaccine'),
    path('covidstate/<str:state>',views.covid_state, name = 'covid_state'),
]