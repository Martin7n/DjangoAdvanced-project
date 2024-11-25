from django.contrib import admin

from workoutApp.workouts.models import Exercise, Workout, WorkoutSet


# Register your models here.


from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Workout


# Custom filter class
class IsEmptyFilter(admin.SimpleListFilter):
    title = _('Is Empty')  # Label for the filter
    parameter_name = 'is_empty'  # URL query parameter for the filter

    def lookups(self, request, model_admin):
        # Define filter options
        return (
            ('True', _('Yes')),
            ('False', _('No')),
        )

    def queryset(self, request, queryset):
        # Filter the queryset based on the selected filter option
        value = self.value()
        if value == 'True':
            return queryset.filter(sets__isnull=True)  # No related sets
        if value == 'False':
            return queryset.exclude(sets__isnull=True)  # At least one related set
        return queryset  # No filter applied


# Register the Workout model with the custom admin
@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['user', "get_exercises", "get_all_sets_reps", "get_total_volume", "is_empty"]
    list_filter = ['user', IsEmptyFilter]
    ordering = ['user']

    def is_empty(self, obj):
        list = [p.exercise for p in obj.sets.all()]
        return not bool(list)  # Return True if list is empty, else False

    is_empty.boolean = True  # Display as a boolean icon (tick or cross)


    def get_exercises(self, obj):
        return  ", ".join([p.exercise.name for p in obj.sets.all()])

    def get_all_sets_reps(self, obj):
        listed = []
        for xrx in obj.sets.all():
            listed.append(f"{xrx.reps} - {xrx.weight}")
        return ', '.join(listed)

    def get_total_volume(self, obj):

        total = sum(xrx.reps * xrx.weight for xrx in obj.sets.all())
        return total



@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = [

        'name',
        'type',
        'category'
        # 'get_info',
        # 'get_author',

    ]

    # def get_created(self, obj):
    #     return obj.workout.created_at.strftime('%Y-%m-%d')

    # def get_info(self, obj):
    #     return  f'{obj.type} '

    # def get_author(self, obj):
    #     return obj.author


# @admin.register(ExerciseCategory)
# class ExerciseCategoryAdmin(admin.ModelAdmin):
#     list_display = ['category']
#
# @admin.register(ExerciseType)
# class ExerciseTypeAdmin(admin.ModelAdmin):
#     list_display = ['type', 'category']



@admin.register(WorkoutSet)
class WorkoutSetAdmin(admin.ModelAdmin):
    list_display = [
        "workout",
        "exercise",
        "reps",
        "weight",
        "order",
    ]




# @admin.register(SetExercise)
# class SetAdmin(admin.ModelAdmin):
#     list_display = [
#         "exercise",
#         "reps",
#         "weight",
#         "order",
#
#     ]


    # Workout
    # WorkoutTemplate
    # ExerciseCategory
    # ExerciseType
    # Exercise
    # Setw
    #
