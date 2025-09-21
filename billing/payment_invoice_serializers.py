from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ReadOnlyField, PrimaryKeyRelatedField
from .models import Client, Product, Invoice, InvoiceItem, ActivityLog, Payment
from django.db import transaction
from django.contrib.auth.models import User



class InvoiceItemSerializer(ModelSerializer):
    product_name = ReadOnlyField(source='product.name')
    class Meta:
        model = InvoiceItem
        fields = ["id", "product", "product_name", "quantity", "line_total"]
        read_only_fields = ["id", "product_name", "line_total"]


class PaymentSerializer(ModelSerializer):
    client_name = ReadOnlyField(source='client.name')
    client = PrimaryKeyRelatedField(queryset=Client.objects.all())
    invoice = PrimaryKeyRelatedField(queryset=Invoice.objects.all())
    invoice_number = ReadOnlyField(source='invoice.invoice_number')
    created_by = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Payment
        fields = ["client", "client_name", "invoice", "invoice_number", "amount", "payment_date", "payment_method", "created_by"]
        
    @transaction.atomic
    def create(self, validated_data):
        request = self.context.get('request')
        invoice = validated_data.get('invoice')
        amount = validated_data.get('amount', 0)

        if amount <= 0:
            raise serializers.ValidationError("Payment amount must be greater than zero.")
        if invoice.status == "paid":
            raise serializers.ValidationError("Invoice is already fully paid.")
        if invoice.remaining_amount == 0 and amount > invoice.total:
            raise serializers.ValidationError("Payment amount cannot exceed total invoice amount.")
        if invoice.remaining_amount > 0 and amount > invoice.remaining_amount:
            raise serializers.ValidationError("Payment amount cannot exceed remaining invoice amount.")
        

        payment = Payment.objects.create(**validated_data)

        # For Unpaid Invoices
        if invoice.remaining_amount == 0 and invoice.status == "unpaid":
            if amount == invoice.total:
                invoice.remaining_amount = 0
                invoice.status = "paid"
            else:
                invoice.remaining_amount = invoice.total - amount
                invoice.status = "partially_paid"

        # For Partially Paid Invoices
        else:
            invoice.remaining_amount -= amount
            if invoice.remaining_amount == 0:
                invoice.status = "paid"
            else:
                invoice.status = "partially_paid"

        invoice.save()

        ActivityLog.objects.create(
            user=request.user if request else None,
            action=f"Recorded payment of {amount} for invoice #{invoice.invoice_number}",
        )
        
        return payment



class InvoiceSerializer(ModelSerializer):
    items = InvoiceItemSerializer(many=True, write_only=True)
    items_details = InvoiceItemSerializer(many=True, read_only=True, source='items')
    payments_details = PaymentSerializer(many=True, read_only=True, source='invoice_payments')
    client = PrimaryKeyRelatedField(queryset=Client.objects.all())
    client_name = ReadOnlyField(source='client.name')
    
    class Meta:
        model = Invoice
        fields = [
            "id", "invoice_number", "client", "client_name",
            "issue_date", "status",
            "sub_total", "tax", "discount", "total", "remaining_amount",
            "items", "created_at", "updated_at", "items_details", "payments_details"
        ]
        read_only_fields = [
            "id", "invoice_number", "client_name",
            "issue_date", "status", "sub_total", "total", "remaining_amount", 
            "created_at", "updated_at"
        ]

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop('items', [])

        request = self.context.get('request')
        tax = validated_data.get('tax', 0)
        discount = validated_data.get('discount', 0)

        invoice = Invoice.objects.create(**validated_data)

        sub_total = 0
        for item_data in items_data:
            product = item_data['product']
            qty = item_data['quantity']
            line_total = product.unit_price * qty
            sub_total += line_total

            InvoiceItem.objects.create(
                invoice=invoice,
                product=product,
                quantity=qty,
                line_total=line_total
            )

        invoice.sub_total = sub_total
        tax_amount = (tax / 100) * sub_total
        discount_amount = (discount / 100) * sub_total
        invoice.total = sub_total + tax_amount - discount_amount
        invoice.save()

        ActivityLog.objects.create(
            user=request.user if request else None,
            action=f"Created invoice #{invoice.invoice_number}",
        )
        
        return invoice
