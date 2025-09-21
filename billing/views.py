from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from .permissions import IsManagerOrReadOnly
from .client_product_activity_serializers import ClientSerializer, ProductSerializer, ActivityLogSerializer
from .payment_invoice_serializers import InvoiceSerializer, PaymentSerializer
from .models import Client, Product, Invoice, ActivityLog, Payment
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse

# Create your views here.

@extend_schema(tags=["Billing"])
class BillingView(APIView):
    def get(self, request):
        return Response(
            {
                "message": "Billing endpoint",
                "endpoints": ["/clients/", "/invoices/", "/payments/"],
            }
        )
    

@extend_schema(tags=["Clients"])
class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsManagerOrReadOnly]


@extend_schema(
    tags=["Products"],
    examples=[
        OpenApiExample(
            "Product Create Example",
            value={
                "name": "string",
                "description": "string",
                "unit_price": 500,
            }
        )
    ]
)
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsManagerOrReadOnly]


@extend_schema(
    tags=["Invoices"],
    examples=[
        OpenApiExample(
            "Invoice Create Example",
            value={
                "client": 1,
                "tax": 5,
                "discount": 10,
                "items": [
                    {"product": 2, "quantity": 10},
                    {"product": 5, "quantity": 15}
                ]
            }
        )
    ]
)
class InvoiceViewSet(ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsManagerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


@extend_schema(
    tags=["payments"],
    examples=[
        OpenApiExample(
            "Payment Example",
            value={
                "client": 1,
                "invoice": 1,
                "amount": "150.00",
                "payment_method": "credit_card",
            },
        )
    ]
)
class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsManagerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


@extend_schema(
    tags=["Activity Logs"],
    summary="List all activity logs",
    description="Retrieve a list of activity logs for the authenticated user. Each log contains details such as the user, action performed, and timestamp.",
    responses={
        200: ActivityLogSerializer(many=True),
        403: OpenApiResponse(description="Not authenticated or no permission."),
    },
    examples=[
        OpenApiExample(
            "Activity Log Example",
            value=[
                {
                    "id": 1,
                    "user": "huraira",
                    "action": "Created a new product",
                    "timestamp": "2025-09-19T10:15:30Z"
                },
                {
                    "id": 2,
                    "user": "huraira",
                    "action": "Updated an invoice",
                    "timestamp": "2025-09-19T10:25:10Z"
                }
            ],
        )
    ],
)
class ActivityLogAPIView(generics.ListAPIView):
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAuthenticated]
