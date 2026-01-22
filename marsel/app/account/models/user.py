from django.contrib.auth.base_user import BaseUserManager
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill

from products.models import Product
from promotions.models import BirthdayDiscountSettings


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email field is required"))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a Superuser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)

CLUSTER_K2 = "K2"
CLUSTER_K3 = "K3"
CLUSTER_K4 = "K4"

class User(AbstractUser):
    CLUSTER_CHOICES = [
        (CLUSTER_K2, "Подарочники"),
        (CLUSTER_K3, "Частые"),
        (CLUSTER_K4, "Спящие"),
    ]
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"), blank=True)
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"), blank=True)
    photo = ProcessedImageField(upload_to='user_photos/%Y/%m',
                                processors=[ResizeToFill(500, 500)],
                                format='JPEG',
                                options={'quality': 60},
                                blank=True)
    birthdate = models.DateField(blank=True, null=True, verbose_name='День рождения')
    phone_model = models.ForeignKey('PhoneModel', on_delete=models.SET_NULL,
                                    null=True, blank=True, verbose_name="Модель телефона")
    points = models.PositiveIntegerField(default=0, verbose_name='Накопленные баллы')
    quantity_of_cases = models.PositiveIntegerField(default=0, verbose_name='Количество купленных чехлов')
    free_cases = models.PositiveIntegerField(default=0, verbose_name='Количество бесплатных чехлов')

    cluster = models.CharField(max_length=10, choices=CLUSTER_CHOICES, blank=True, null=True, verbose_name="Кластер")
    last_cluster_update = models.DateTimeField('Дата последнего обновления кластера', auto_now=True)

    welcome_discount = models.PositiveSmallIntegerField(default=0, verbose_name="Welcome скидка")
    entered_k4_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата входа в кластер K4(спящие)"
    )

    favorite_products = models.ManyToManyField(Product, blank=True, verbose_name='избранные товары')

    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name', 'birthdate', 'phone_model']

    objects = UserManager()

    class Meta:
        ordering = ('-date_joined',)

    def __str__(self):
        return f'{self.email}-{self.full_name}'

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_birthday_discount(self):
        today = timezone.localdate()

        if today.month == self.birthdate.month and today.day == self.birthdate.day:
            discount = BirthdayDiscountSettings.objects.first()
            if discount:
                return discount.discount_percentage
        return 0

    def add_case(self, count=1):
        """
        Увеличиваем количество купленных чехлов и обновляем количество бесплатных чехлов.
        Когда количество купленных чехлов достигает 6, обновляем `free_cases`.
        """
        self.quantity_of_cases += count

        self.free_cases = self.quantity_of_cases // 6

        # Сбросить количество купленных чехлов после достижения 6
        if self.quantity_of_cases >= 6:
            self.quantity_of_cases = self.quantity_of_cases % 6  # Сбрасываем до 0 после 6 чехлов

        self.save()

    def update_case_counts_after_order(self, order):
        """
        Обновляем количество купленных чехлов и бесплатных чехлов после завершения оплаты.
        """
        # Подсчитываем количество купленных чехлов в заказе
        total_case_count = 0
        for item in order.order_items.all():
            if item.product.is_case:
                total_case_count += item.quantity

        # Получаем количество бесплатных чехлов
        free_case_count = order.free_case_count

        # Вычисляем количество купленных чехлов за вычетом бесплатных
        actual_case_count = total_case_count - free_case_count

        # Обновляем количество чехлов у пользователя
        self.add_case(count=actual_case_count)
        self.free_cases -= free_case_count  # Вычитаем использованные бесплатные чехлы

        self.save()
