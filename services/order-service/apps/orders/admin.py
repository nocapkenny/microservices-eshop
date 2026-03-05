from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Order, OrderItem


# Inline для товаров заказа (редактирование внутри заказа)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # Не показывать пустые строки
    can_delete = True  # Разрешить удаление позиций
    readonly_fields = ['subtotal']  # Подсумма только для чтения
    fields = ['product_name', 'quantity', 'price', 'subtotal']

    def subtotal(self, obj):
        if obj.pk:
            return f"{obj.subtotal} ₽"
        return "-"
    subtotal.short_description = 'Сумма'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Отображаемые столбцы в списке
    list_display = [
        'order_id_link', 
        'user_info', 
        'status', 
        'total_amount_display', 
        'items_count', 
        'created_at',
        'shipping_address_short'
    ]
    
    # Фильтры в правой панели
    list_filter = [
        'status', 
        'created_at', 
        'updated_at'
    ]
    
    # Поиск по полям
    search_fields = [
        'id', 
        'user_name', 
        'user_email', 
        'shipping_address',
        'order_items__product_name'
    ]
    
    # Сортировка по умолчанию
    ordering = ['-created_at']
    
    # Поля доступные для редактирования в списке (quick edit)
    list_editable = ['status']
    
    # Разбиение на страницы
    list_per_page = 20
    
    # Дата иерархия (фильтр по датам сверху)
    date_hierarchy = 'created_at'
    
    # Inline редактирование товаров заказа
    inlines = [OrderItemInline]
    
    # Поля только для чтения
    readonly_fields = [
        'created_at', 
        'updated_at', 
        'total_amount',
        'items_count',
        'total_quantity'
    ]
    
    # Группировка полей в форме редактирования
    fieldsets = (
        ('Основная информация', {
            'fields': ('user_id', 'user_name', 'user_email', 'status')
        }),
        ('Доставка', {
            'fields': ('shipping_address',)
        }),
        ('Финансы', {
            'fields': ('total_amount', 'items_count', 'total_quantity')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Сворачиваемая секция
        }),
    )
    
    # Кастомные методы для отображения
    
    def order_id_link(self, obj):
        """Ссылка на редактирование заказа"""
        url = f'/admin/orders/order/{obj.id}/change/'
        return format_html(
            '<a href="{}" style="color: #2e8b57; font-weight: bold;">#{} </a>',
            url, obj.id
        )
    order_id_link.short_description = 'Заказ'
    
    def user_info(self, obj):
        """Информация о пользователе"""
        return format_html(
            '{}<br><small style="color: #888">{}</small>',
            obj.user_name or f'User {obj.user_id}',
            obj.user_email or 'Нет email'
        )
    user_info.short_description = 'Пользователь'
    
    def status_badge(self, obj):
        """Цветной бейдж статуса"""
        colors = {
            'pending': '#ffc107',      # Желтый
            'confirmed': '#17a2b8',    # Голубой
            'shipped': '#6f42c1',      # Фиолетовый
            'delivered': '#28a745',    # Зеленый
            'cancelled': '#dc3545',    # Красный
        }
        color = colors.get(obj.status, '#6c757d')
        status_text = dict(Order.STATUS_CHOICES).get(obj.status, obj.status)
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; '
            'border-radius: 12px; font-size: 12px; font-weight: bold;">{}</span>',
            color, status_text
        )
    status_badge.short_description = 'Статус'
    
    def total_amount_display(self, obj):
        """Отображение суммы с валютой"""
        return f"{obj.total_amount} ₽"
    total_amount_display.short_description = 'Сумма'
    
    def items_count(self, obj):
        """Количество товаров в заказе"""
        return obj.items_count
    items_count.short_description = 'Товаров'
    
    def shipping_address_short(self, obj):
        """Сокращенный адрес"""
        if len(obj.shipping_address) > 30:
            return obj.shipping_address[:30] + "..."
        return obj.shipping_address
    shipping_address_short.short_description = 'Адрес'
    
    # Действия для массовых операций
    actions = ['mark_as_confirmed', 'mark_as_shipped', 'mark_as_cancelled']
    
    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} заказов подтверждено')
    mark_as_confirmed.short_description = '✓ Подтвердить выбранные заказы'
    
    def mark_as_shipped(self, request, queryset):
        updated = queryset.update(status='shipped')
        self.message_user(request, f'{updated} заказов отправлено')
    mark_as_shipped.short_description = '📦 Отправить выбранные заказы'
    
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} заказов отменено')
    mark_as_cancelled.short_description = '✕ Отменить выбранные заказы'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_link', 'product_name', 'quantity', 'price', 'subtotal', 'created_at']
    list_filter = ['created_at', 'order__status']
    search_fields = ['product_name', 'order__id']
    readonly_fields = ['subtotal']
    
    def order_link(self, obj):
        url = f'/admin/orders/order/{obj.order.id}/change/'
        return format_html('<a href="{}">Заказ #{}</a>', url, obj.order.id)
    order_link.short_description = 'Заказ'
    
    def subtotal(self, obj):
        return f"{obj.subtotal} ₽"
    subtotal.short_description = 'Сумма'