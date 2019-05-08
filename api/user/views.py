from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import RealUser
from .serializers import RealUserSerializer

# Create your views here.

class UserCreateList(APIView):
    
    def get(self, request, format=None):
        users = RealUser.objects.all()
        serializer = RealUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RealUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)