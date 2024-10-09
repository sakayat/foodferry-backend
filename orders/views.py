from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.response import Response
from .serializers import (
    OrderSerializer,
    OrderDetailsSerializer,
    UserOrderSerializer,
    UserOrderStatusSerializer,
)
from .models import Order, OrderDetails
from carts.models import CartItem
from restaurant.models import Restaurant

# Create your views here.


class CreateOrderAPI(APIView):

    serializer_class = OrderSerializer

    def post(self, request):
        cart_items = CartItem.objects.filter(cart__user=request.user)

        if not cart_items:
            return Response(
                {"error": "cart item empty"}, status=status.HTTP_404_NOT_FOUND
            )

        subtotal = sum(item.quantity * item.food_item.price for item in cart_items)

        shipping_cost = 60.00

        total = subtotal + int(shipping_cost)

        order = Order.objects.create(
            user=request.user,
            phone=request.data.get("phone"),
            email=request.user.email,
            first_name=request.data.get("first_name"),
            last_name=request.data.get("last_name"),
            payment_method=request.data.get("payment_method"),
            address=request.data.get("address"),
            status="pending",
            subtotal=subtotal,
            total=total,
            shipping_cost=shipping_cost,
        )

        for item in cart_items:
            OrderDetails.objects.create(
                order=order,
                item_name=item.food_item.name,
                item_price=item.food_item.price,
                quantity=item.quantity,
                item_image=item.food_item.image,
                restaurant=item.food_item.restaurant.slug,
                status=order.status,
                subtotal=item.quantity * item.food_item.price,
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


class UserOrderListAPI(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            restaurant = Restaurant.objects.get(owner=request.user)
        except Restaurant.DoesNotExist:
            return Response({"error": "restaurant owner not found"})
        orders = OrderDetails.objects.filter(restaurant=restaurant.slug)
        serializer = UserOrderSerializer(orders, many=True)
        return Response(serializer.data)


class UserOrderStatusAPI(APIView):

    serializer_class = UserOrderStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        try:
            restaurant = Restaurant.objects.get(owner=request.user)
            order = OrderDetails.objects.get(restaurant=restaurant.slug, id=id)
        except OrderDetails.DoesNotExist:
            return Response({"error": "not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserOrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id):
        try:
            restaurant = Restaurant.objects.get(owner=request.user)
            order = OrderDetails.objects.get(restaurant=restaurant.slug, id=id)
        except OrderDetails.DoesNotExist:
            return Response({"error": "not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserOrderStatusSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
