from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    calories_burned = models.IntegerField(null=True, blank=True, default=0)


class Workout(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    duration = models.IntegerField(null=True)
    calories = models.IntegerField(null=True)
    is_standard = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"


class UserWorkout(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    number_of_workouts_done = models.PositiveIntegerField(null=True, default=0)

    def __str__(self):
        return f"{self.workout.name}"


class Exercise(models.Model):
    name = models.CharField(max_length=255)
    muscle_group = models.CharField(max_length=255)
    calories = models.PositiveIntegerField(null=True)
    MUSCLE_GROUP_CHOICES = (
        'chest', 'biceps', 'triceps', 'shoulders', 'back', 'legs', 'abdomen'
    )

    def __str__(self):
        return f"{self.name}"


class UserExercise(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    training_weight = models.PositiveIntegerField(null=True, default=1)

    def __str__(self):
        return f"{self.exercise.name}"


class Goal(models.Model):
    goal_calories = models.PositiveIntegerField(null=True, default=0)
    goal_date = models.DateTimeField(null=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    reps = models.PositiveIntegerField(null=True)
    sets = models.PositiveIntegerField(null=True)
    rest_time = models.FloatField(null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user_exercise = models.ForeignKey(UserExercise, on_delete=models.CASCADE, null=True)

