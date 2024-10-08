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
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        quantity = request.data.get("quantity")

        if not quantity:
            return Response(status=status.HTTP_404_NOT_FOUND)

        food_item = get_object_or_404(FoodItem, slug=slug)

        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, food_item=food_item
        )

        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateCartItem(APIView):

    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        try:
            cart_item = CartItem.objects.get(id=id, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Item not found in your cart."},
                status=status.HTTP_404_NOT_FOUND,
            )

        quantity = request.data.get("quantity")

        if quantity is not None and quantity == 0:
            cart_item.delete()
            cart = Cart.objects.get(user=request.user)
            return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteCartItem(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        cart_item = request.user.cart.items.get(id=id)
        cart_item.delete()
        return Response(
                {"details": "Cart item removed successfully"}, status=status.HTTP_200_OK
            )
            
        


class ClearCartItemsAPI(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items:
            return Response("Cart is already empty", status=status.HTTP_200_OK)
        cart_items.delete()
        return Response(
            {"details": "Cart items removed successfully"}, status=status.HTTP_200_OK
        )


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
