from django.conf.urls import include, url
from mytestapp import views


urlpatterns = [
    url(r'^first_form/$',views.FirstForm.as_view(),name="firt_form")
]