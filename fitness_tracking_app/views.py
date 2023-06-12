from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, CreateWorkoutForm, DeleteWorkoutForm, GoalForm, \
    ResetGoalForm, ChangeTrainingWeightForm
from .models import Workout, UserWorkout, WorkoutExercise, Goal, CustomUser, UserExercise
from django.shortcuts import render
from .forms import WorkoutForm
from datetime import datetime


def home(request):
    return render(request, 'home.html', {'user': request.user})


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "Registration/signUp.html"


def workout_delete_view(request):
    if request.method == 'POST':
        form = DeleteWorkoutForm(request.user, request.POST)
        if form.is_valid():
            workout_id = form.cleaned_data['workout']
            for workout in workout_id:
                if request.user.is_superuser:
                    Workout.objects.filter(name=workout.workout.name).delete()
                elif workout.workout.is_standard:
                    UserWorkout.objects.filter(user=request.user, id=workout.id).delete()
                else:
                    Workout.objects.filter(name=workout.workout.name).delete()

            return redirect('workouts_list')
    else:
        form = DeleteWorkoutForm(user=request.user)
    return render(request, 'workouts_delete.html', {'form': form})


def workout_view(request):
    workouts = Workout.objects.all()
    return render(request, 'workouts_list.html', {'workouts': workouts})


def workout_add_view(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            selected_workouts = form.cleaned_data['workouts']
            for workout in selected_workouts:
                user_workouts = UserWorkout.objects.filter(user=request.user, workout=workout)
                if not user_workouts:
                    UserWorkout.objects.create(user=request.user, workout=workout)
            return redirect('workouts_list')
        else:
            return render(request, 'workouts_invalid_form.html', {'form': form})
    else:
        form = WorkoutForm()
        return render(request, 'workouts_add.html', {'form': form})


def workout_list_and_create_view(request):
    workouts = Workout.objects.filter(is_standard=True)
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CreateWorkoutForm(request.POST)
            if form.is_valid():
                exercises = form.cleaned_data['exercises']
                reps = form.cleaned_data['reps']
                sets = form.cleaned_data['sets']
                new_workout = form.cleaned_data['workout']
                description = form.cleaned_data['description']
                rest_time = form.cleaned_data['rest_time']
                calories = 0
                duration = 0
                for e in exercises:
                    calories += 1
                    duration += 1
                calories = calories * reps * sets * 3
                duration = duration * (rest_time * sets + reps * 0.2 * sets)
                for w in Workout.objects.values('name'):
                    if new_workout == w['name']:
                        return render(request, 'workout_form_invalid_input.html', {'form': form})
                if request.user.is_superuser:
                    workout_id = Workout.objects.create(name=new_workout, description=description, calories=calories,
                                                        duration=duration, is_standard=True)
                else:
                    workout_id = Workout.objects.create(name=new_workout, description=description, calories=calories,
                                                        duration=duration)

                UserWorkout.objects.create(user=request.user, workout=workout_id)
                for exercise in exercises:
                    user_exercise = UserExercise.objects.create(exercise=exercise, user=request.user, training_weight=0)
                    WorkoutExercise.objects.create(workout=workout_id, reps=reps, sets=sets,
                                                   exercise=exercise, rest_time=rest_time, user=request.user,
                                                   user_exercise=user_exercise)
        else:
            form = CreateWorkoutForm()

        user_workouts = UserWorkout.objects.filter(user=request.user)

        return render(request, 'workouts_list.html',
                      {'user_workouts': user_workouts, 'workouts': workouts, 'form': form})
    else:
        return render(request, 'workouts_list.html', {'workouts': workouts})


def change_training_weight_view(request, id):
    if request.method == 'POST':
        form = ChangeTrainingWeightForm(request.POST)
        if form.is_valid():
            training_weight = form.cleaned_data['training_weight']
            UserExercise.objects.filter(exercise=id, user=request.user.id).update(training_weight=training_weight)
            return redirect('workouts_list')
    else:
        form = ChangeTrainingWeightForm()
    return render(request, 'change_training_weight.html', {'form': form})


def workout_selection_view(request, id):
    workout = Workout.objects.get(id=id)
    exercises = WorkoutExercise.objects.filter(workout=workout)
    if request.method == 'POST':
        a = UserWorkout.objects.get(user=request.user, workout=workout)
        a.number_of_workouts_done += 1
        a.save()
        CustomUser.objects.filter(id=request.user.id).update(
            calories_burned=CustomUser.objects.get(id=request.user.id).calories_burned + workout.calories)
        return redirect('workout_start', rest_time=exercises[0].rest_time)

    return render(request, 'workouts_selection.html',
                  {'workout': workout, 'exercises': exercises})


def workout_start_view(request, rest_time):
    return render(request, 'workout_start.html', {'rest_time': rest_time})


def workout_start_rest_view(request, rest_time):
    return render(request, 'workout_start_rest.html', {'rest_time': rest_time})


def goals_view(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        reset_form = ResetGoalForm(request.POST)
        if reset_form.is_valid():
            CustomUser.objects.filter(id=request.user.id).update(calories_burned=0)
            return redirect('goals')
        if form.is_valid():
            calories = form.cleaned_data['goal_kilocalories']
            date = form.cleaned_data['goal_date']
            if date.date() > datetime.now().date():
                if Goal.objects.filter(user=request.user).exists():
                    Goal.objects.filter(user=request.user).update(goal_calories=calories, goal_date=date)
                else:
                    Goal.objects.create(user=request.user, goal_calories=calories, goal_date=date)
                return redirect('goals')
            else:
                return render(request, 'goals_invalid_form.html', {'form': form})
    else:
        form = GoalForm()
        reset_form = ResetGoalForm()
    if Goal.objects.filter(user=request.user).exists():
        goal_calories = Goal.objects.get(user=request.user).goal_calories
    else:
        goal_calories = 0
    return render(request, 'goals.html',
                  {'form': form, 'reset_form': reset_form, 'goals': Goal.objects.filter(user=request.user),
                   'user': CustomUser.objects.get(id=request.user.id), 'date': datetime.now(),
                   'calories_to_burn': goal_calories - CustomUser.objects.get(
                       id=request.user.id).calories_burned})

