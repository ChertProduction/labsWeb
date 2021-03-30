from django.shortcuts import render

from json import loads

from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from calculate.models import CalculateResponse, CalculateRequest
from calculate.serializers import CalculationResponseSerializer, CalculationRequestSerializer
from calculate.utils import Calculator


def index(request):
    return render(request, 'index.html', {
        'foo': 'bar',
    })


"""
Клас, що описує точку доступа до API застосунку. Має наслідуватись від
APIView.
"""
class ExampleView(APIView):

    def post(self, request: HttpRequest):
        parsed_request = loads(request.body)

        request_data_serializer = CalculationRequestSerializer(data=parsed_request)
        if not request_data_serializer.is_valid():

            return Response(status=400)

        request_data = CalculateRequest(**request_data_serializer.validated_data)

        calculation_result = Calculator.calculate(request_data.input_value)

        response_data = CalculateResponse(calculation_result)

        response_data_serializer = CalculationResponseSerializer(response_data)

        response = Response(response_data_serializer.data)

        return response

@api_view(['GET', 'POST'])
def another_example(request: HttpRequest):
    """
    Приклад створення точки доступу на основі python-функції із застосуванням декоратору api_view
    """
    if request.method == 'POST':
        return Response({'message': f'[POST] Another example also works!: {request.body}]'})
    return Response({'message': f'[GET] Another example also works!: no body'})

