from django.http import HttpResponse
from django.shortcuts import render
import random
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from .models import Complex
from .serializers import ComplexSerializer, DataSerializer, ComplexCreateSerializer
from ..common_utils.workout_choices import Load, ComplexType
from ..workouts.models import Exercise


@api_view(['GET', 'POST'])
def getData(request):
    app = Complex.objects.all()
    serializer = DataSerializer(app, many=True)
    # return Response(serializer.data)
    return HttpResponse(20*"<h1>API</h1>")


class ComplexListView(APIView):
    def get(self, request):
        complexes = Complex.objects.all()
        serializer = ComplexSerializer(complexes, many=True)
        return Response(serializer.data)

class ComplexCreateView(APIView):
    def post(self, request):
        serializer = ComplexCreateSerializer(data=request.data)
        if serializer.is_valid():
            complex_instance = serializer.save()
            return Response(ComplexSerializer(complex_instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
test rq
POST /complexes/create/
Content-Type: application/json

{
  "name": "Morning Routine",
  "type": "AMRAP",
  "loading": "BW",
  "exercises": [1, 2, 3]
}
'''

class ComplexGenerateView(APIView):
    def post(self, request):

        # filtering by type and category...
        # complex_type = request.data.get('type', None)
        # category = request.data.get('category', None)
        # exercises = Exercise.objects.all()
        complex_type = random.choice([item[0] for item in ComplexType.choices])
        loading = random.choice([item[0] for item in Load.choices])

        # exercises = Exercise.objects.all()
        exercises = Exercise.objects.distinct('type')
        complex_name = request.data.get('name', 'Generated Complex')


        # if complex_type:
        #     exercises = exercises.filter(type=complex_type)
        #
        # if category:
        #     exercises = exercises.filter(category=category)
        #
        if len(exercises) < 3:
            return Response({"detail": "Not enough exercises available."}, status=status.HTTP_400_BAD_REQUEST)
        #
        selected_exercises = random.sample(list(exercises), 3)


        complex_instance = Complex.objects.create(
            name=complex_name,
            type=complex_type,
            loading=loading
        )

        complex_instance.exercises.set(selected_exercises)
        complex_instance.save()

        return Response(ComplexSerializer(complex_instance).data, status=status.HTTP_201_CREATED)