from django.urls import path
from .views import get_data, ComplexListView, ComplexCreateView, ComplexGenerateView


urlpatterns = [
    path('', get_data,),
    path('list/', ComplexListView.as_view(), name='complex-list'),
    path('create/', ComplexCreateView.as_view(), name='complex-create'),
    path('generate/', ComplexGenerateView.as_view(), name='complex-generate'),
]
