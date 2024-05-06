from django.shortcuts import render
from rest_framework import generics
from rest_framework.filters import SearchFilter

from OrderManagement.models import OrdersModel
from OrderManagement.serializers import OrderSerializer
from PayManagement.models import InvoiceModel
from core.permissions import IsAdmin


def filter_order(queryset, params):
    progressing = params.get('Progressing')
    user = params.get('user')
    date = params.get('order_date')
    invoice_number = params.get('invoice_number')

    if progressing:
        queryset = queryset.filter(status='Progressing')

    if user:
        queryset = queryset.filter(user=user)

    if date:
        queryset = queryset.filter(order_date=date)

    if invoice_number:
        invoice = InvoiceModel.filter(invoice_number=invoice_number)
        queryset = queryset.filter(invoice=invoice)

    return queryset


def sort_orders(queryset, params):
    sort_by = params.get('sort_by')
    # Add the `-` prefix for descending order
    queryset.order_by('order_date')
    if sort_by.startswith('-'):
        queryset = queryset.reverse()
    return queryset


class OrderListView(generics.ListAPIView):
    permission_classes = IsAdmin
    filter_backends = [SearchFilter]
    search_fields = ['user']
    serializer_class = OrderSerializer
    queryset = OrdersModel.objects.all()


class OrderDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = IsAdmin
    serializer_class = OrderSerializer
    queryset = OrdersModel.objects.all()

