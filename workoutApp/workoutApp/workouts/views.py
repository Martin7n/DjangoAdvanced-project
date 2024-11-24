from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.forms import modelformset_factory
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from workoutApp.workouts.forms import WorkoutSetFormSet, ExerciseFormSet, WorkoutForm, ExerciseForm, WorkoutFilterForm, \
    ExercisesForm, ExerciseCreateForm
from workoutApp.workouts.models import Workout, WorkoutSet, Exercise


# 'static' non...functional views for non-logged users

def about(request):
    return render(request, 'common/about.html')

def what_we_do(request):
    return render(request, 'common/mission.html')

def contacts(request):
    return render(request, 'common/contact.html')



# Main functionalities FBV i CBV
# FIXME - change FBV to CVB for details view
#FIXME - add login user and user logic.


def login(request):

    return render(request, "common/login.html")

def index(request):

    # workouts = Workout.objects.all()

    # for x in workouts:
    #     print(x.get_tot_volume())
    #     print(x.get_exercises())

    # vs = Workout.objects.prefetch_related('exercise').all()
    #not needed for now

    # context = {
    #     "workouts": workouts
    # }
    '''todo:
    not needed for now. Potential upgrade for other users public stat.'''

    context = {}

    return render(request, 'common/index.html', context)



'''creating an <empty> workout, as a functional requirement for the app'''

@login_required
def create_workout(request):

    form =  WorkoutForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout = form.save()
            return redirect("edit-workout", pk=workout.pk)

    context = {
                "form": form,
            }

    return render(request, 'workouts/workout_create.html', context)

    # return HttpResponse('ok')


''' 
    some interesting issues/feature below. The idea is to take
    all the valid reps´-sets and save them
    and even if there are blank cells(model fields),
    just to skip that data without Exception.
    the part of skipping blanks is in the model save method. 
'''

def edit_workout(request, pk):
    workout = get_object_or_404(Workout, id=pk)
    # all = WorkoutSet.objects.filter(workout=workout) not needed.

    print(workout.get_exercises())

    if 'cancel' in request.POST:
        return redirect('index')

    if request.method == 'POST':

        exercise_form = ExerciseForm(request.POST)
        reps_formset = WorkoutSetFormSet(request.POST)
        print(exercise_form)

        if exercise_form.is_valid() and reps_formset.is_valid():

            selected_exercise = exercise_form.cleaned_data['name']
            exercise = get_object_or_404(Exercise, name=selected_exercise)


            # Saving sets each set (reps, weight) for the exercise
            for form in reps_formset:
                workout_set = form.save(commit=False)
                workout_set.exercise = exercise
                workout_set.workout = workout
                workout_set.save()


            if 'save' in request.POST:
                return redirect('user_workouts')

            elif 'save_and_add' in request.POST:
                 return redirect('edit-workout', pk=workout.pk)
                #continue with adding another exercise and etc.

    else:
        exercise_form = ExerciseForm()
        reps_formset = WorkoutSetFormSet(queryset=WorkoutSet.objects.none())
        # Empty formset for reps and weight

    context ={
        'exercise_form': exercise_form,
        'reps_formset': reps_formset,
        'workout': workout,
        # 'xrx': workout.get_all_sets_reps(),
        # 'all': all,
        'get_all': workout.get_all(),

    }

    return render(request, 'workouts/workout_manager.html', context)



'''WorkoutDetailView  used for full view of the workout.
Also implements an immediate deletion without additional template.
Separation of concerns isn't the best here,
but following the data in the app i think it's Ok from user perspective.'''

class WorkoutDetailView(LoginRequiredMixin , DetailView):
    model = Workout
    template_name = 'workouts/workout_details.html'
    context_object_name = 'workout'

    # dispach auth check
    def dispatch(self, request, *args, **kwargs):
        workout = self.get_object()

        if not request.user.is_authenticated or request.user != workout.user:
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        workout = self.get_object()

        context['is_author'] = self.request.user == workout.user
        return context

    def post(self, request, *args, **kwargs):
        workout = self.get_object()
        if request.user == workout.user:
            # Direct deletion of the workout if the user is the auth.
            workout.delete()
            return redirect('user_workouts')
        return redirect('login')


class WorkoutStatusView(LoginRequiredMixin, ListView):
    model = Workout
    template_name = 'workouts/workout-status.html'  # Adjust the template name
    context_object_name = 'workouts'
    paginate_by = 6
    success_url = reverse_lazy('user_workouts')


    def get_queryset(self):
        user = self.request.user
        queryset = Workout.objects.filter(user=user).order_by("-id")

        # Get the form data from the request
        form = WorkoutFilterForm(self.request.GET)

        start_date = self.request.GET.get('start_date', None)
        end_date = self.request.GET.get('end_date', None)
        # workout_type = self.request.GET.get('workout_type', None)


        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)

        if form.is_valid():
            workout_type = form.cleaned_data.get('workout_type')
            if workout_type:
                queryset = queryset.filter(workout_type=workout_type)

        return queryset
    #
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = WorkoutFilterForm(self.request.GET)
        return context



# class ExerciseCreateForm(LoginRequiredMixin, CreateView):
#     model = Workout
#     template_name = 'workouts/staff_create_xrx.html'  # Adjust the template name
#     context_object_name = 'exercise'  # This is the context variable for paginated results
#     success_url = reverse_lazy('user_workouts')





class ExerciseListView(ListView):
    model = Exercise
    template_name = 'workouts/exercise_list.html'  # Adjust the template path as needed
    context_object_name = 'exercises'


    def get_queryset(self):
        return Exercise.objects.all()


class ExerciseCreateView(UserPassesTestMixin, CreateView):
    model = Exercise
    form_class = ExercisesForm
    template_name = 'workouts/create_exercise_form.html'
    success_url = reverse_lazy('exercise-list')

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
         return HttpResponseForbidden("You do not have permission to that function")


    def form_valid(self, form):
        # Optionally, set additional fields here
        form.instance.user = self.request.user  # If you want to assign the current user
        return super().form_valid(form)



class ExerciseUpdateView(UserPassesTestMixin, UpdateView):
    model = Exercise
    form_class = ExercisesForm
    template_name = 'workouts/exercise_form.html'
    success_url = reverse_lazy('exercise-list')  # Redirect to the exercise list after successful update

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return HttpResponseForbidden("You do not have permission to that function.")

    def form_valid(self, form):
        return super().form_valid(form)



class ExerciseDeleteView(UserPassesTestMixin, DeleteView):
    model = Exercise
    success_url = reverse_lazy('exercise-list')  # Redirect to the exercise list after successful deletion

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        # If the user doesn't have permission, return a forbidden response
        return HttpResponseForbidden("You do not have permission to delete")


# TODO: delete. Already upgraded.
#  Working filter with types only
#
# class WorkoutStatusView(LoginRequiredMixin, ListView):
#     model = Workout
#     template_name = 'common/_off_workout-status.html'  # Adjust the template name
#     context_object_name = 'workouts'  # This is the context variable for paginated results
#     paginate_by = 6  # Number of workouts per page
#     success_url = reverse_lazy('user_workouts')
#
#     def get_queryset(self):
#
#         user = self.request.user
#         # Start with a base queryset filtered by the current user
#         queryset = Workout.objects.filter(user=user)
#
#         # Optional: Filter by workout_type if provided in the request
#         workout_type = self.request.GET.get('workout_type', None)
#         if workout_type:
#             queryset = queryset.filter(workout_type=workout_type)
#
#         return queryset
#
#
#     def get_context_data(self, **kwargs):
#
#         context = super().get_context_data(**kwargs)
#
#         #if no workout...add some.
#         context['no_workouts'] = self.get_queryset().count() == 0
#
#         # Filter enhancement
#         context['workout_types'] = Workout.objects.values_list('workout_type', flat=True).distinct()
#
#         return context

