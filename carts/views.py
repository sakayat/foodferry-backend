from django.shortcuts import render
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from restaurant.models import FoodItem
from .models import Cart, CartItem
from .serializers import CartItemSerializer, CartSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class AddToCartAPI(APIView):

    serializer_class = CartItemSerializer

    def post(self, request, id):
        quantity = request.data.get("quantity")

        if not quantity:
            return Response(status=status.HTTP_404_NOT_FOUND)

        food_item = get_object_or_404(FoodItem, id=id)

        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, food_item=food_item
        )

        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartItemsAPI(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response(
                {"error": "Cart is empty"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
