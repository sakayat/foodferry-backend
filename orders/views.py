from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.response import Response
from .serializers import OrderSerializer, OrderDetailsSerializer
from .models import Order, OrderDetails
from carts.models import CartItem


# Create your views here.


class CreateOrderAPI(APIView):

    serializer_class = OrderSerializer

    def post(self, request):
        cart_items = CartItem.objects.filter(cart__user=request.user)

        if not cart_items:
            return Response({"error": "items not found"})

        subtotal = sum(item.quantity * item.food_item.price for item in cart_items)

        shipping_cost = 60.00

        total = subtotal + int(shipping_cost)

        order = Order.objects.create(
            user=request.user,
            phone=request.data.get("phone"),
            email=request.user.email,
            first_name=request.data.get("first_name"),
            last_name=request.data.get("last_name"),
            city=request.data.get("city"),
            postal_code=request.data.get("postal_code"),
            payment_method=request.data.get("payment_method", "Cash on delivery"),
            status="pending",
            subtotal=subtotal,
            total=total,
            shipping_cost=shipping_cost,
        )

        for item in cart_items:
            OrderDetails.objects.create(
                order=order,
                item_name=item.food_item.name,
                subtotal=item.quantity * item.food_item.price,
                total=item.quantity,
            )

        cart_items.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderListAPI(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            orders = OrderDetails.objects.filter(order__user=request.user)
            serializer = OrderDetailsSerializer(orders, many=True)
            return Response(serializer.data)
        except OrderDetails.DoesNotExist:
            return Response(serializer.errors)
