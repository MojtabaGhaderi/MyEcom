from django.shortcuts import render
from django.utils.text import slugify
from rest_framework.response import Response
from rest_framework.views import APIView
from UserManagement.models import UserManageModel
from UserManagement.serializers import UserProfileSerializer
from .models import CategoryModel, ProductModel, ProductComment, NotificationModel, DiscountCodeModel
from rest_framework import generics, viewsets, status
from .serializer import CategorySerializer, ProductAddEditSerializer, CommentSerializer, \
    NotificationSerializer, DiscountCodeSerializer, ImageSerializer, ProductBatchUpdateItemSerializer
from core.permissions import IsAdmin


#  ///////////  Category related views  ///////////

class CategoryTestView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = CategoryModel.objects.all()


# // for creating a new category. //
class CategoryCreateView(generics.CreateAPIView):
    permission_classes = [IsAdmin]
    serializer_class = CategorySerializer
    queryset = CategoryModel.objects.all()


# // for editing categories. //
class CategoryEditView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin]
    serializer_class = CategorySerializer
    queryset = CategoryModel.objects.all()

    # // if a category was going to be deleted, its children would take its
    # parent(s) as a new parent. //
    def perform_destroy(self, instance):
        parents = instance.parent.all()
        children = CategoryModel.objects.filter(parent=instance)
        products = ProductModel.objects.filter(category=instance)

        for child in children:
            child.parent.set(parents)

        for product in products:
            product.category.set(parents)

        instance.delete()

#  /////  ^^^^^  ///////


# //////////    Product related views    //////////

class ProductView(viewsets.ModelViewSet):
    permission_classes = IsAdmin
    serializer_class = ProductAddEditSerializer
    queryset = ProductModel.objects.all()
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            valid_data = []
            errors = []
            for item in request.data:
                serializer = self.get_serializer(data=item)
                if serializer.is_valid():
                    valid_data.append(serializer)
                else:
                    errors.append({
                        'data': item,
                        'errors': serializer.errors
                    })
            for serializer in valid_data:
                self.perform_create(serializer)

            if errors:
                return Response(errors, status=status.HTTP_207_MULTI_STATUS)
            else:
                return Response(
                    [serializer.data for serializer in valid_data],
                    status=status.HTTP_201_CREATED
                )

        else:
            serializer = self.get_serializer(data=request.data)

            serializer.is_valid(raise_exception=True)

            self.perform_create(serializer)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())

        return Response(status=status.HTTP_204_NO_CONTENT)


# // admins can delete a comment. //
class ProductCommentDelete(generics.DestroyAPIView):
    permission_classes = [IsAdmin]
    queryset = ProductComment.objects.all()
    serializer_class = CommentSerializer


# // batch update for changing special_offer and discount fields for products easier. //
class ProductBatchUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAdmin]
    serializer_class = ProductBatchUpdateItemSerializer

    def update(self, request, *args, **kwargs):
        valid_data = []
        invalid_data = []

        for item in request.data:
            serializer = self.get_serializer(data=item)
            if serializer.is_valid:
                serializer.is_valid(raise_exception=True)
                valid_data.append(serializer.validated_data)
            else:
                invalid_data.append({
                    'data': item,
                    'error': serializer.errors
                })

        queryset = ProductModel.objects.filter(id__in=[item['id'] for item in valid_data])

        for instance in queryset:
            for i in range(len(valid_data)):
                for field, value in valid_data[i].items():
                    setattr(instance, field, value)
                instance.save()

        if invalid_data:
            return Response(invalid_data, status=status.HTTP_207_MULTI_STATUS)
        else:
            return Response(
                [serializer.data for serializer in valid_data],
                status=status.HTTP_201_CREATED
            )

# //////////    User related views    //////////


# // admins can see a list of users. //
class UserListView(generics.ListAPIView):
    permission_classes = [IsAdmin]
    queryset = UserManageModel.objects.all()
    serializer_class = UserProfileSerializer


# // admins can see a specific user. //
class UserRetrieveView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdmin]
    queryset = UserManageModel.objects.all()
    serializer_class = UserProfileSerializer


# //////////    Discount Code related views    //////////
class DiscountCodeCreate(generics.CreateAPIView):
    permission_classes = [IsAdmin]
    serializer_class = DiscountCodeSerializer
    queryset = DiscountCodeModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class DiscountCodeUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin]
    serializer_class = DiscountCodeSerializer
    queryset = DiscountCodeModel.objects.all()


# //////////    Notification related views    //////////

class NotificationCreate(generics.CreateAPIView):
    permission_classes = [IsAdmin]
    serializer_class = NotificationSerializer
    queryset = NotificationModel.objects.all()


class NotificationEdit(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin]
    serializer_class = NotificationSerializer
    queryset = NotificationModel.objects.all()

