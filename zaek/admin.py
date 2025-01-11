from django.contrib import admin

from .models import *

admin.site.register(ZaekPrice)
admin.site.register(ClassificationPriceProduct)
admin.site.register(TypeClient)
admin.site.register(VolumeLevel)

from django.contrib import admin
from .models import Instruction, InstructionStep


class ProductAdmin(admin.ModelAdmin):
    search_fields = ['art']  # Указываем поле, по которому будет осуществляться поиск

admin.site.register(Product, ProductAdmin)


class InstructionStepInline(admin.TabularInline):
    model = InstructionStep
    extra = 1

@admin.register(Instruction)
class InstructionAdmin(admin.ModelAdmin):
    list_display = ["title"]
    inlines = [InstructionStepInline]


@admin.register(ClientClassificationDiscount)
class ClientClassificationDiscountAdmin(admin.ModelAdmin):
    list_display = ('type_client', 'classification_price_product', 'discount')
    list_filter = ('type_client', 'classification_price_product')


@admin.register(VolumeAtDiscount)
class VolumeAtDiscountAdmin(admin.ModelAdmin):
    list_display = ('type_client', 'volume_level','classification_price_product', 'discount')
    list_filter = ('volume_level','type_client')


# @admin.register(InstructionStep)
# class InstructionStepAdmin(admin.ModelAdmin):
#     list_display = ["instruction", "comment"]