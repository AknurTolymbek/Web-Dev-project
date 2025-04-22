from rest_framework import serializers
from .models import Drink, Pizza, Order, OrderItem, Sauce
from django.contrib.auth.models import User

class PizzaSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Pizza
        fields = ['id', 'name', 'description', 'price', 'image']

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url)
        return None
class DrinkSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Drink
        fields = ['id', 'name', 'price', 'image', 'image_url']

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url)
        return obj.image_url or None

class SauceSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Sauce
        fields = ['id', 'name', 'price', 'image', 'image_url']

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url)
        return obj.image_url or None
    

class OrderItemSerializer(serializers.ModelSerializer):
    pizza = PizzaSerializer(required=False)
    drink = DrinkSerializer(required=False)
    sauce = SauceSerializer(required=False)

    class Meta:
        model = OrderItem
        fields = ['pizza', 'drink', 'sauce', 'quantity']

    
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'status', 'items']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']