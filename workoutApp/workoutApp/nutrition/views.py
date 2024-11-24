from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, DeleteView
from workoutApp.nutrition.forms import MealCreateForm, MealFilterForm
from workoutApp.nutrition.models import Meal


class CreateMeal(LoginRequiredMixin, CreateView):
    model = Meal
    form_class = MealCreateForm
    template_name = 'nutrition/nutrition_create_meal.html'
    success_url = reverse_lazy('user_meal_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ViewMeals(LoginRequiredMixin, ListView):
    model = Meal
    template_name = 'nutrition/meals_list.html'
    context_object_name = 'meals'
    paginate_by = 10  # Number of meals per page
    success_url = reverse_lazy('user_meal_list')

    def get_queryset(self):
        user = self.request.user
        queryset = Meal.objects.filter(user=user).order_by("-id")

        form = MealFilterForm(self.request.GET)
        #forms to id-s, id's to start_date/end_date

        start_date = self.request.GET.get('start_date', None)
        end_date = self.request.GET.get('end_date', None)

        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        if form.is_valid():
            meal_type = form.cleaned_data.get('meal_type')
            if meal_type:
                queryset = queryset.filter(type=meal_type)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = MealFilterForm(self.request.GET)
        return context


class MealDetailView(LoginRequiredMixin,DetailView):
    model = Meal
    template_name = 'nutrition/meal_detail.html'
    context_object_name = 'meal'
    success_url = reverse_lazy('user_meal_list')


    def post(self, request, *args, **kwargs):
        meal = self.get_object()
        if request.user == meal.user:
            # Direct deletion of the workout if the user is the auth.
            meal.delete()
            return redirect('user_meal_list')
        return redirect('login')



