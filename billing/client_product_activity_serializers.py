from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ReadOnlyField, PrimaryKeyRelatedField
from .models import Client, Product, Invoice, InvoiceItem, ActivityLog, Payment
from django.db import transaction
from django.contrib.auth.models import User
from .payment_invoice_serializers import PaymentSerializer


class ClientSerializer(ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True, source="client_payments")
    class Meta:
        model = Client
        fields = ["name", "email", "phone", "company", "address", "payments"]

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ActivityLogSerializer(ModelSerializer):
    user_name = ReadOnlyField(source='user.username')
    class Meta:
        model = ActivityLog
        fields = ["id", "user_name", "action", "timestamp"]

