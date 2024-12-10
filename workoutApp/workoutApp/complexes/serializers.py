from rest_framework import serializers
from workoutApp.workouts.models import Exercise
from workoutApp.complexes.models import Complex


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complex
        fields = ['id', 'name', 'exercises', 'type', 'loading']


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'category', 'type']


class ComplexSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = Complex
        fields = ['id', 'name', 'type', 'loading', 'exercises']


class ComplexCreateSerializer(serializers.ModelSerializer):
    exercises = serializers.PrimaryKeyRelatedField(queryset=Exercise.objects.all(), many=True)

    class Meta:
        model = Complex
        fields = ['name', 'type', 'loading', 'exercises']

    def validate_exercises(self, value):
        if len(value) != 3:
            raise serializers.ValidationError("You must provide exactly 3 exercises.")
        return value
