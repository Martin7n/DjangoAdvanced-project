from django.urls import path, include
from workoutApp.nutrition.views import CreateMeal, ViewMeals, MealDetailView


urlpatterns = [
    path('create-meal/', CreateMeal.as_view(), name='create-meal'),
    path('user-nutrition/', ViewMeals.as_view(), name='user_meal_list'),
    path("<int:pk>/",
             include(
            [path('edit/', MealDetailView.as_view(), name="edit-meal"),
             ])
             )
    ]

