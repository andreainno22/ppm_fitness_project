from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.validators import MinValueValidator

from .models import CustomUser, Workout, Exercise, UserWorkout
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "age",
            "email",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "age",
            "email",
        )


class WorkoutForm(forms.Form):
    workouts = forms.ModelMultipleChoiceField(
        queryset=Workout.objects.filter(is_standard=True),
        widget=forms.CheckboxSelectMultiple
    )


class CreateWorkoutForm(forms.Form):
    exercises = forms.ModelMultipleChoiceField(queryset=Exercise.objects.all()
                                               , widget=forms.CheckboxSelectMultiple)
    reps = forms.IntegerField(validators=[MinValueValidator(1)])
    sets = forms.IntegerField(validators=[MinValueValidator(1)])
    rest_time = forms.FloatField(validators=[MinValueValidator(0.0)])
    workout = forms.CharField(max_length=255)
    description = forms.CharField(max_length=255, required=False)


class DeleteWorkoutForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(DeleteWorkoutForm, self).__init__(*args, **kwargs)
        self.fields['workout'] = forms.ModelMultipleChoiceField(
            queryset=UserWorkout.objects.filter(user=user),
            widget=forms.CheckboxSelectMultiple
        )


class GoalForm(forms.Form):
    goal_kilocalories = forms.IntegerField(validators=[MinValueValidator(1)])
    goal_date = forms.DateTimeField()


class ResetGoalForm(forms.Form):
    reset_kilocalories = forms.CharField(widget=forms.HiddenInput(), initial='reset')


class ChangeTrainingWeightForm(forms.Form):
    training_weight = forms.IntegerField(validators=[MinValueValidator(1)])
