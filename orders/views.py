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
from sslcommerz_lib import SSLCOMMERZ
from django.shortcuts import redirect
from accounts.models import CustomUser
import random
import string
import os
from dotenv import load_dotenv
load_dotenv()

base_url = os.getenv("VITE_BASE_URL")
base_api_url = os.getenv("BASE_API_URL")

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

class PaymentAPI(APIView):
    
    def post(self, request, user_id):
        
        settings = {
            "store_id": "test671f2ed69a42f",
            "store_pass": "test671f2ed69a42f@ssl",
            "issandbox": True,
        }
        
        sslcz = SSLCOMMERZ(settings)
        
        total_amount = request.data.get("total_amount")
        
        tran_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        
        post_body = {
            "total_amount": total_amount,
            "currency": "BDT",
            "tran_id": tran_id,
            "success_url": f"{base_api_url}/api/payment-success/{user_id}/{tran_id}/", 
            "fail_url": f"{base_api_url}/api/payment-fail/", 
            "cancel_url": f"{base_api_url}/api/payment-cancel/",  
            "emi_option": 0,
            "cus_name": "test",
            "cus_email": "test@test.com",
            "cus_phone": "01700000000",
            "cus_add1": "customer address",
            "cus_city": "Dhaka",
            "cus_country": "Bangladesh",
            "shipping_method": "NO",
            "multi_card_name": "",
            "num_of_item": 1,
            "product_name": "Test",
            "product_category": "Test Category",
            "product_profile": "general",
        }

        response = sslcz.createSession(post_body)
       
        return Response({"redirect_url": response["GatewayPageURL"]})
        
        
class PaymentSuccessAPI(APIView):
    
    def post(self, request, user_id, tran_id):
        
        user = CustomUser.objects.get(id=user_id)
        
        cart_items = CartItem.objects.filter(cart__user=user)
        
        if not cart_items:
            return Response(
                {"error": "cart item empty"}, status=status.HTTP_404_NOT_FOUND
            )

        subtotal = sum(item.quantity * item.food_item.price for item in cart_items)
        shipping_cost = 60.00
        total = subtotal + int(shipping_cost)

        order = Order.objects.create(
            user=user,
            phone=request.data.get("phone"),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            payment_method="online_payment",
            address=request.data.get("address"),
            status="Paid",
            payment_id=tran_id,
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
        
        return redirect(f"{base_url}/order-history/")

class PaymentFailedAPI(APIView):
    def post(self, request):
        return redirect(f"{base_url}/checkout/")
        

