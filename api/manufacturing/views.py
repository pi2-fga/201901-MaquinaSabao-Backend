from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Manufacturing
from .serializers import ManufacturingSerializer


class ManufacturingCreateList(APIView):

    def get(self, request, format=None):
        fabrications = Manufacturing.objects.all()
        serializer = ManufacturingSerializer(fabrications, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ManufacturingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)
