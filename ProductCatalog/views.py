from django.shortcuts import render
from .models import CategoryModel
from rest_framework import generics

from .serializer import CategoryCreateSerializer, CategoryUpdateSerializer, CategoryTestSerializer


class CategoryTestView(generics.ListAPIView):
    serializer_class = CategoryTestSerializer
    queryset = CategoryModel.objects.all()


class CategoryCreateView(generics.CreateAPIView):
    serializer_class = CategoryCreateSerializer
    queryset = CategoryModel.objects.all()

    def perform_create(self, serializer):
        data = serializer.validated_data
        parent_id = self.request.data.get('parent_id')

        if parent_id:
            parent = CategoryModel.objects.get(id=parent_id)
            child = parent.add_child(data['name'])
            serializer.instance = child

        else:
            root = CategoryModel.create_root_category(data['name'])
            serializer.instance = root

        serializer.save()


class CategoryMoveView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategoryUpdateSerializer
    queryset = CategoryModel.objects.all()

    def perform_update(self, serializer):
        instance = self.get_object()
        destination_id = self.request.data.get('destination')
        instance.move(destination_id=destination_id)


class CategoryEditNameView(generics.RetrieveUpdateAPIView):
    serializer_class = CategoryUpdateSerializer
    queryset = CategoryModel.objects.all()
    def perform_update(self, serializer):
        instance = self.get_object()
        new_name = self.request.data.get('name')
        instance.edit_name(name=new_name)



