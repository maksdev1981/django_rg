from django.db import models
# Подключаем библиотеку работы с пользователями фрейворка
from django.contrib.auth import get_user_model
# Подключаем библиотеку работы с контентом
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


# Order
# Specification


# Категория товаров (category)
class Category(models.Model):
    name = models.CharField(max_length=255, null=False, verbose_name='Название категорий')
    slug = models.SlugField(unique=True, verbose_name='Служебное поле')
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

# Товары
class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=False, verbose_name='Наименование товара')
    slug = models.SlugField(unique=True, verbose_name='Служебное поле')
    image = models.ImageField()
    description = models.TextField(verbose_name='Краткое описание товара', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    def __str__(self):
        return self.title
    class Meta:
        abstract = True  # Класс явялется абстрактным, все наследуюмые будут иметь признаки этого класса

# Классы наследники от Products
class Notebook(Product):
    diagonal = models.CharField(max_length=255, verbose_name='Диагональ монитора')
    display = models.CharField(max_length=255, verbose_name='Тип дисплея')
    processor_freq = models.CharField(max_length=255, verbose_name='Частота процессора')
    ram = models.CharField(max_length=255, verbose_name='Оперативная память')
    video = models.CharField(max_length=255, verbose_name='Видеокарта')
    time_without_charge = models.CharField(max_length=255, verbose_name='Время работы от одного заряда аккумулятора')
    def __str__(self):
        return '{} : {}'.format(self.category.name, self.category.title)
    class Meta:
        verbose_name = 'Ноутбук'
        verbose_name_plural = 'Ноутбуки'

class Smartphone(Product):
    diagonal = models.CharField(max_length=255, verbose_name='Диагональ монитора')
    display = models.CharField(max_length=255, verbose_name='Тип дисплея')
    resolution = models.CharField(max_length=255, verbose_name='Разрешение дисплея')
    volume_ram = models.CharField(max_length=255, verbose_name='Объем встроенной памяти')
    sd = models.BooleanField(default=True, verbose_name='Наличие SD карты')
    sd_max_volume = models.CharField(max_length=255, verbose_name='Максимальный объем SD')
    main_cam_mp = models.CharField(max_length=255, verbose_name='Разрешение основной камеры')
    frontal_cam_mp = models.CharField(max_length=255, verbose_name='Разрешение фронтальной камеры')
    def __str__(self):
        return '{} : {}'.format(self.category.name, self.category.title)
    class Meta:
        verbose_name = 'Смартфон'
        verbose_name_plural = 'Смартфоны'


# Товарная корзина (используем related_name для того, чтобы имелись ссылки на массив товаров в корзине или покупке)
class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_product')
    # Удаляем за ненадобностью, так как не понятно продукт какого класса будет присутствовать
    # product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1, verbose_name='Количество')
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    def __str__(self):
        return 'Продукт: {} (для корзины)'.format(self.product.title)
    class Meta:
        verbose_name = 'Товарная корзина'
        verbose_name_plural = 'Товарные корзины'

# Корзина
class Cart(models.Model):
    owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')
    def __str__(self):
        return str(self.id)

# Покупатель
class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=11, verbose_name='Телефон')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    def __str__(self):
        return 'Покупатель: {} {}'.format(self.user.first_name, self.user.last_name)

# Спецификации
# от этой модели отказываемся, так как разрабатываем классы для каждого типа товаров
# для более точного хранения признаков
# class Specifications(models.Model):
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     name = models.CharField(max_length=255, verbose_name='Имя товара для характеристик')
#     def __str__(self):
#         return 'Характерики для товара: {}'.format(self.name)

# Модель для теста работы с изображениями
# class SomeModel(models.Model):
#     image = models.ImageField()
#     def __str__(self):
#         return str(self.id)