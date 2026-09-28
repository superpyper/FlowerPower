from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Category(models.Model):
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField('Описание', blank=True)
    image = models.URLField('Ссылка на изображение', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name

    @classmethod
    def get_default_categories(cls):
        return [
            {
                'name': 'Розы',
                'slug': 'roses',
                'description': 'Классические и благородные розы — символ любви и страсти.'
            },
            {
                'name': 'Тюльпаны',
                'slug': 'tulips',
                'description': 'Весенние и яркие тюльпаны — символ новой жизни и радости.'
            },
            {
                'name': 'Пионы',
                'slug': 'peonies',
                'description': 'Пышные и ароматные пионы — короли сада.'
            },
            {
                'name': 'Орхидеи',
                'slug': 'orchids',
                'description': 'Экзотические и изысканные орхидеи — символ роскоши.'
            },
            {
                'name': 'Сборные букеты',
                'slug': 'mixed',
                'description': 'Авторские композиции из разных цветов.'
            },
        ]

    @classmethod
    def ensure_categories_exist(cls):
        for cat_data in cls.get_default_categories():
            cls.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description'],
                }
            )


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    discount_price = models.DecimalField('Цена со скидкой', max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField('Фото', upload_to='products/', blank=True, null=True)
    in_stock = models.BooleanField('В наличии', default=True)
    is_new = models.BooleanField('Новинка', default=False)
    is_bestseller = models.BooleanField('Хит продаж', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_price(self):
        return self.discount_price if self.discount_price else self.price

    @classmethod
    def get_default_products(cls):
        return [
            {
                'name': 'Букет из 101 красной розы',
                'slug': 'buket-iz-101-krasnoy-rozy',
                'category_name': 'Розы',
                'description': 'Роскошный букет из 101 красной розы. Идеальный подарок для самого романтичного жеста. Свежесть гарантирована до 14 дней.',
                'price': '15990.00',
                'discount_price': '12990.00',
                'image': 'buket-roz.jpg',
                'in_stock': True,
                'is_new': False,
                'is_bestseller': True
            },
        ]

    @classmethod
    def ensure_products_exist(cls):
        Category.ensure_categories_exist()
        category_map = {cat.name: cat for cat in Category.objects.all()}

        for prod_data in cls.get_default_products():
            category = category_map.get(prod_data['category_name'])
            if category:
                cls.objects.get_or_create(
                    slug=prod_data['slug'],
                    defaults={
                        'category': category,
                        'name': prod_data['name'],
                        'description': prod_data['description'],
                        'price': prod_data['price'],
                        'discount_price': prod_data['discount_price'],
                        'image': prod_data.get('image', ''),
                        'in_stock': prod_data['in_stock'],
                        'is_new': prod_data['is_new'],
                        'is_bestseller': prod_data['is_bestseller']
                    }
                )


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', null=True, blank=True)
    session_key = models.CharField('Ключ сессии', max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'Корзина #{self.id}'

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='Корзина')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField('Количество', default=1)

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'

    def get_total_price(self):
        return self.product.get_price() * self.quantity


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает обработки'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, verbose_name='Корзина')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField('Итого', max_digits=10, decimal_places=2)
    address = models.TextField('Адрес доставки')
    phone = models.CharField('Телефон', max_length=20)
    comment = models.TextField('Комментарий', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ #{self.id} - {self.user.username}'


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='Товар', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.PositiveSmallIntegerField('Оценка', choices=[(i, i) for i in range(1, 6)])
    text = models.TextField('Текст отзыва')
    is_verified = models.BooleanField('Подтвержденный заказ', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Отзыв от {self.user.username} - {self.rating}★'
