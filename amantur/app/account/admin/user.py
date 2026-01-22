from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone

from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.decorators import action
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from ..models import User, CLUSTER_K2
from ..services import send_gift_email, update_user_cluster, send_discount_notification

admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(GroupAdmin, UnfoldModelAdmin):
    pass


@admin.register(User)
class UserAdmin(UserAdmin, UnfoldModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Dates", {"fields": ("last_login", "date_joined")}),
        ('Личная информация', {
                 'fields': ('first_name', 'last_name', 'birthdate', 'photo')}),
        ('Доп. Информация', {
            'fields': ('points', 'quantity_of_cases', 'free_cases', 'phone_model', 'welcome_discount', 'favorite_products')}),
        ('Кластер', {
            'fields': ('cluster', 'last_cluster_update', 'entered_k4_at')}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    model = User

    ordering = ['date_joined']

    list_display = ('id', 'email', 'first_name', 'last_name', 'cluster', 'is_active')
    list_display_links = ('id', 'email')
    readonly_fields = ('last_cluster_update',)
    autocomplete_fields = ('favorite_products',)

    actions_list = ['increase_welcome_discount_action', "send_gift_emails", 'update_clusters_action']

    @action(description="Обновить welcome-скидки 📈", url_path="increase_welcome_discount")
    def increase_welcome_discount_action(self, request):
        now = timezone.now()
        updated_count = 0

        users = User.objects.filter(cluster="K4", entered_k4_at__isnull=False)

        for user in users:
            delta = now - user.entered_k4_at

            if delta.days >= 14 and user.welcome_discount < 15:
                user.welcome_discount = 15
                user.save(update_fields=["welcome_discount"])
                send_discount_notification(user, 15)
                updated_count += 1

            elif delta.days >= 7 and user.welcome_discount < 10:
                user.welcome_discount = 10
                user.save(update_fields=["welcome_discount"])
                send_discount_notification(user, 10)
                updated_count += 1

        self.message_user(
            request,
            f"Welcome-скидка обновлена для {updated_count} пользователей.",
            level=messages.SUCCESS,
        )

        return redirect(reverse_lazy("admin:account_user_changelist"))

    @action(description="Отправить подарочные email 🎁", url_path="send_gift_emails-action")
    def send_gift_emails(self, request):
        users = User.objects.filter(cluster=CLUSTER_K2)
        count = 0
        for user in users:
            send_gift_email(user)
            count += 1

        self.message_user(
            request,
            f"Успешно отправлено {count} подарочных email.",
            level=messages.SUCCESS,
        )
        return redirect(
            reverse_lazy("admin:account_user_changelist")
        )

    @action(description="Обновить кластеры пользователей 🧠", url_path="update_user_clusters")
    def update_clusters_action(self, request):
        """
        Обновляет кластеризацию всех пользователей (аналог команды `update_user_cluster`).
        """
        users = User.objects.all()
        count = 0
        for user in users:
            update_user_cluster(user)
            count += 1

        self.message_user(
            request,
            f"Кластеры обновлены для {count} пользователей.",
            level=messages.SUCCESS,
        )
        return redirect(reverse_lazy("admin:account_user_changelist"))
