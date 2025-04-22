from django.urls import path
from .views import (
    PizzaListView, PizzaCreateView, PizzaDetailView, PizzaUpdateView, PizzaDeleteView,
    DrinkListView, DrinkCreateView, DrinkDetailView, DrinkUpdateView, DrinkDeleteView,
    SauceListView, SauceCreateView, SauceDetailView, SauceUpdateView, SauceDeleteView,  # Новые представления
    OrderCreateView, UserRegisterView
)

urlpatterns = [
    # Pizza CRUD
    path('pizzas/', PizzaListView.as_view(), name='pizza-list'),
    path('pizzas/create/', PizzaCreateView.as_view(), name='pizza-create'),
    path('pizzas/<int:id>/', PizzaDetailView.as_view(), name='pizza-detail'),
    path('pizzas/<int:id>/update/', PizzaUpdateView.as_view(), name='pizza-update'),
    path('pizzas/<int:id>/delete/', PizzaDeleteView.as_view(), name='pizza-delete'),
    # Drink CRUD
    path('drinks/', DrinkListView.as_view(), name='drink-list'),
    path('drinks/create/', DrinkCreateView.as_view(), name='drink-create'),
    path('drinks/<int:id>/', DrinkDetailView.as_view(), name='drink-detail'),
    path('drinks/<int:id>/update/', DrinkUpdateView.as_view(), name='drink-update'),
    path('drinks/<int:id>/delete/', DrinkDeleteView.as_view(), name='drink-delete'),
    # Sauce CRUD
    path('sauces/', SauceListView.as_view(), name='sauce-list'),
    path('sauces/create/', SauceCreateView.as_view(), name='sauce-create'),
    path('sauces/<int:id>/', SauceDetailView.as_view(), name='sauce-detail'),
    path('sauces/<int:id>/update/', SauceUpdateView.as_view(), name='sauce-update'),
    path('sauces/<int:id>/delete/', SauceDeleteView.as_view(), name='sauce-delete'),
    # Order and User
    path('order/', OrderCreateView, name='order-create'),
    path('register/', UserRegisterView, name='user-register'),
]