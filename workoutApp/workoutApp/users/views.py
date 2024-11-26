from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Count
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from .forms import CustomLoginForm, CustomUserCreationForm, CustomUserChangeForm, UserProfileForm, ExerciseFilterForm
from .models import CustomUser, RepMax, UserProfile
from ..workouts.models import Workout


def custom_login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            next_url = request.GET.get('next', '/')
            # print(f"REDIRECT =>>>>>>>>>>>> {next_url}")
            return redirect(next_url)
    else:
        form = CustomLoginForm()

    context = {'form': form}

    return render(request, 'users/login.html', context)


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return redirect(self.success_url)


def custom_logout(request):
    if request.user.is_authenticated:
        logout(request)
    else:
        return HttpResponseRedirect('/')

    return redirect('index')


class CustomUserEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('user-profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the UserProfileForm with the user's profile instance
        context['profile_form'] = UserProfileForm()
        return context

    def form_valid(self, form):
        profile_form = UserProfileForm(self.request.POST, self.request.FILES, instance=self.request.user.profile)

        if profile_form.is_valid():
            profile_form.save()

        password = form.cleaned_data.get('password')
        if password:
            self.object.set_password(password)

        self.object.save()

        if password:
            update_session_auth_hash(self.request, self.object)

        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


@login_required
def user_profile_view(request):
    user = request.user
    profile_picture = user.profile.profile_picture if user.profile else None

    context = {
        'user': user,
        'profile_picture': profile_picture
    }
    return render(request, 'users/profile.html', context)


def staff_required(view_func):
    return user_passes_test(lambda u: u.is_staff)(view_func)


@staff_required
def view_all_profile(request):
    users = CustomUser.objects.annotate(workout_count=Count('workouts'))
    # users = CustomUser.objects.all()
    context = {'users': users}

    return render(request, 'users/manage_all_profiles.html', context)


@staff_required
def view_profile(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    workout_count = Workout.objects.filter(user=user).count()
    profile_picture = user.profile.profile_picture
    context = {
        'user': user,
        'profile_picture': profile_picture,
        'workout_count': workout_count}
    return render(request, 'users/manage_profile.html', context)


@staff_required
def delete_profile(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)

    if user == request.user:
        messages.error(request, "You cannot delete your own profile.")
        return redirect('all-profiles')

    user.delete()
    messages.success(request, f"The profile of {user.username} has been deleted.")

    return redirect('all-profiles')




class PublicUserProfileListView(ListView):
    model = UserProfile
    template_name = 'users/public_profiles_list.html'  # Adjust path if needed
    context_object_name = 'user_profiles'
    paginate_by = 5
    def get_queryset(self):
        return UserProfile.objects.filter(is_public=True)



class RepMaxStatusView(LoginRequiredMixin, ListView):
    model = RepMax
    template_name = 'users/repmax_details.html'
    context_object_name = 'repmaxes'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
        user_profile = get_object_or_404(UserProfile, user=user)

        if user != self.request.user and not user_profile.is_public:
            raise Http404("This profile is private.")


        queryset = RepMax.objects.filter(user=user).order_by("-max_weight", "-reps")

        form = ExerciseFilterForm(self.request.GET)
        if form.is_valid():
            category = form.cleaned_data.get('exercise_category')
            exercise_type = form.cleaned_data.get('exercise_type')
            exercise_name = form.cleaned_data.get('exercise_names')

            if category:
                queryset = queryset.filter(exercise__category=category)

            if exercise_type:
                queryset = queryset.filter(exercise__type=exercise_type)

            if exercise_name:
                queryset = queryset.filter(exercise__name=exercise_name)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['filter_form'] = ExerciseFilterForm(self.request.GET)

        return context