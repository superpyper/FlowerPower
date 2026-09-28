from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Order, Review

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'phone', 'comment']
        labels = {
            'address': 'Адрес доставки',
            'phone': 'Телефон',
            'comment': 'Комментарий к заказу',
        }
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Введите адрес доставки'}),
            'phone': forms.TextInput(attrs={'placeholder': '+7 (999) 999-99-99'}),
            'comment': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Дополнительная информация'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text', 'photo']
        labels = {
            'rating': 'Ваша оценка',
            'text': 'Текст отзыва',
            'photo': 'Фото букета (необязательно)',
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Поделитесь впечатлениями о цветах...'}),
            'rating': forms.RadioSelect(choices=[(i, f'{i}★') for i in range(1, 6)]),
        }