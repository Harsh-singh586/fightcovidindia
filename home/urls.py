from django.contrib import admin
from django.urls import path
from django.urls import path,include
from django.conf.urls import url
from home import views
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',views.home,name = 'home'),
    path('state/<str:key>',views.state, name = 'state'),
    path('state/<str:state>/<str:district>',views.district, name = 'state'),
    path('hospital/<str:state>/<str:district>/<str:bedtype>/<str:hostype>/<str:lat>/<str:lon>/<str:distance>',views.hospital_update, name = 'filter hospital'),
    path('vaccine/pincode/<str:pincode>/<str:feetype>/<str:vaccinetype>/<str:availability>',views.vaccine_search, name = 'vaccine search'),
    path('emailalert/<str:pincode>/<str:email>/<str:feetype>/<str:vaccinetype>/<str:availability>',views.email_alert, name = 'email alert'),
    path('emailverify/<str:key>', views.verify_email, name = 'verify')
]
