from django.urls import path, include

from workoutApp.workouts.views import \
    create_workout, WorkoutDetailView, edit_workout,\
    WorkoutStatusView, ExerciseListView, ExerciseUpdateView, \
    ExerciseCreateView, ExerciseDeleteView

urlpatterns = [
    path('create-workout/', create_workout, name='create-workout'),
    path('status', WorkoutStatusView.as_view(), name='user_workouts'),
    path('<int:pk>/', include(
            [path('edit/', edit_workout, name='edit-workout'),
             path('detail/', WorkoutDetailView.as_view(), name='workout_detail'),
             ])),
    path('exercises/', include(
            [path('', ExerciseListView.as_view(), name='exercise-list'),
             path('create/', ExerciseCreateView.as_view(), name='exercise-create'),
             path('<int:pk>/edit/', ExerciseUpdateView.as_view(), name='exercise-edit'),
             path('delete/<int:pk>/', ExerciseDeleteView.as_view(), name='exercise-delete'), ]))
    ]
