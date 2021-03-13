from django.contrib import admin
from . models import Product
from django.contrib.auth.admin import UserAdmin
from .models import  myuser,Order,OrderItem,Shipping,Customer


class MyAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined',
                    'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username',)
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(myuser, MyAdmin)
admin.site.register(Product)
admin.site.register(Shipping)
admin.site.register(Customer)
admin.site.register(OrderItem)
admin.site.register(Order)