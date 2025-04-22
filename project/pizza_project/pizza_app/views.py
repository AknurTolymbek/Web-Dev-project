from rest_framework import generics, response, status
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Pizza, Drink, Sauce, Order, OrderItem
from .serializers import PizzaSerializer, DrinkSerializer, OrderSerializer, OrderItemSerializer, UserSerializer, SauceSerializer
import logging
from rest_framework_simplejwt.tokens import RefreshToken
logger = logging.getLogger(__name__)

# CRUD for Pizza
class PizzaListView(generics.ListAPIView):
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['price', 'name']
    pagination_class = PageNumberPagination

class PizzaCreateView(generics.CreateAPIView):
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer
    permission_classes = [IsAdminUser]

class PizzaDetailView(generics.RetrieveAPIView):
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer
    lookup_field = 'id'

class PizzaUpdateView(generics.UpdateAPIView):
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminUser]

class PizzaDeleteView(generics.DestroyAPIView):
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminUser]

# CRUD for Drink
class DrinkListView(generics.ListAPIView):
    queryset = Drink.objects.all()
    serializer_class = DrinkSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['price', 'name']
    pagination_class = PageNumberPagination

class DrinkCreateView(generics.CreateAPIView):
    queryset = Drink.objects.all()
    serializer_class = DrinkSerializer
    permission_classes = [IsAdminUser]

class DrinkDetailView(generics.RetrieveAPIView):
    queryset = Drink.objects.all()
    serializer_class = DrinkSerializer
    lookup_field = 'id'

class DrinkUpdateView(generics.UpdateAPIView):
    queryset = Drink.objects.all()
    serializer_class = DrinkSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminUser]

class DrinkDeleteView(generics.DestroyAPIView):
    queryset = Drink.objects.all()
    serializer_class = DrinkSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminUser]
class SauceListView(generics.ListAPIView):
    queryset = Sauce.objects.all()
    serializer_class = SauceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['price', 'name']
    pagination_class = PageNumberPagination

class SauceCreateView(generics.CreateAPIView):
    queryset = Sauce.objects.all()
    serializer_class = SauceSerializer
    permission_classes = [IsAdminUser]

class SauceDetailView(generics.RetrieveAPIView):
    queryset = Sauce.objects.all()
    serializer_class = SauceSerializer
    lookup_field = 'id'

class SauceUpdateView(generics.UpdateAPIView):
    queryset = Sauce.objects.all()
    serializer_class = SauceSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminUser]

class SauceDeleteView(generics.DestroyAPIView):
    queryset = Sauce.objects.all()
    serializer_class = SauceSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminUser]
# Create an order
@api_view(['POST'])
def OrderCreateView(request):
    user = request.user
    logger.info(f"Order creation attempt by user {user.username if user.is_authenticated else 'anonymous'}: {request.data}")

    if not user.is_authenticated:
        logger.warning("Unauthorized order creation attempt")
        return response.Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    
    order = Order.objects.create(user=user, status='pending')
    items_data = request.data.get('items', [])
    
    for item_data in items_data:
        serializer = OrderItemSerializer(data=item_data)
        if serializer.is_valid():
            OrderItem.objects.create(
                order=order,
                pizza=serializer.validated_data.get('pizza'),
                drink=serializer.validated_data.get('drink'),
                quantity=serializer.validated_data['quantity']
            )
        else:
            order.delete()
            logger.error(f"Invalid item data: {serializer.errors}")
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = OrderSerializer(order)
    logger.info(f"Order created successfully: {order.id}")
    return response.Response(serializer.data, status=status.HTTP_201_CREATED)

# User registration
@api_view(['POST'])
def UserRegisterView(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        logger.info(f"User registered: {user.username}")
        return response.Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    logger.error(f"Registration failed: {serializer.errors}")
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        if not username or not password or not email:
            return response({'error': 'Username, password, and email are required'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, email=email, password=password)
        refresh = RefreshToken.for_user(user)
        return response({
            'message': 'User created successfully',
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_201_CREATED)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        return response({
            'username': user.username,
            'email': user.email,
            'id': user.id
        })