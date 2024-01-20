from django.shortcuts import render
from .models import CategoryModel
from rest_framework import generics

from .serializer import CategoryCreateSerializer, CategoryUpdateSerializer


class CategoryCreateView(generics.CreateAPIView):
    serializer_class = CategoryCreateSerializer
    queryset = CategoryModel.objects.all()

    def perform_create(self, serializer):
        data = serializer.validated_data

        instance = CategoryModel(**data)

        instance.add_child()

        instance.save()


class CategoryEditView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategoryUpdateSerializer
    queryset = CategoryModel.objects.all()

    def perform_update(self, serializer):
        instance = self.get_object()
        destination = self.request.data.get('destination')
        instance.move(destination=destination)
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()



