from django.contrib import admin
from .models import (
    Store, Category, Brand, Item, StoreItem,
    CementAttributes, SandAttributes, ConcreteAttributes,
    BrickAttributes, PipeAttributes, SteelAttributes,
    PaintAttributes, CableAttributes
)

# -------------------
# Inline Admins
# -------------------

# Inline for Brand under Category
class BrandInline(admin.TabularInline):
    model = Brand
    fields = ['name']           # only brand name editable
    readonly_fields = []
    extra = 1
    can_delete = False

# Inline for Item under Brand
class ItemInline(admin.TabularInline):
    model = Item
    fields = ['name']  # only relevant fields
    readonly_fields = []
    extra = 1
    can_delete = False

# Inline for StoreItem under Store
class StoreItemInline(admin.TabularInline):
    model = StoreItem
    fields = ['item', 'price', 'stock_quantity', 'reorder_point']  # only key fields
    readonly_fields = []
    extra = 1
    can_delete = False

# -------------------
# Model Admins
# -------------------

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [BrandInline]
    search_fields = ['name']

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    inlines = [ItemInline]
    list_filter = ['category']
    search_fields = ['name']

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand']
    list_filter = ['brand']
    search_fields = ['name', 'brand__name']

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'location']
    inlines = [StoreItemInline]
    search_fields = ['name', 'location']

@admin.register(StoreItem)
class StoreItemAdmin(admin.ModelAdmin):
    list_display = ['store', 'item', 'price', 'stock_quantity', 'reorder_point']
    list_filter = ['store', 'item']
    search_fields = ['item__name', 'store__name']

# -------------------
# Attribute Models
# -------------------

@admin.register(CementAttributes)
class CementAttributesAdmin(admin.ModelAdmin):
    list_display = ['item', 'grade', 'weight_per_bag_kg', 'compressive_strength_mpa']

@admin.register(SandAttributes)
class SandAttributesAdmin(admin.ModelAdmin):
    list_display = ['item', 'sand_type', 'grain_size_mm', 'source_location']

@admin.register(ConcreteAttributes)
class ConcreteAttributesAdmin(admin.ModelAdmin):
    list_display = ['item', 'grade', 'slump_mm', 'aggregate_size_mm', 'cement_ratio']

@admin.register(BrickAttributes)
class BrickAttributesAdmin(admin.ModelAdmin):
    list_display = ['item', 'brick_type', 'dimensions_mm', 'compressive_strength_mpa', 'water_absorption_percent']

@admin.register(PipeAttributes)
class PipeAttributesAdmin(admin.ModelAdmin):
    list_display = ['item', 'pipe_material', 'nominal_diameter', 'diameter_unit', 'length_m', 'pressure_rating']

@admin.register(SteelAttributes)
class SteelAttributesAdmin(admin.ModelAdmin):
    list_display = ['item', 'steel_type', 'diameter_mm', 'tensile_strength_mpa']

@admin.register(PaintAttributes)
class PaintAttributesAdmin(admin.ModelAdmin):
    list_display = ['item', 'paint_type', 'base', 'coverage_per_liter_sqm', 'drying_time_hours']

@admin.register(CableAttributes)
class CableAttributesAdmin(admin.ModelAdmin):
    list_display = ['item', 'cable_type', 'conductor_material', 'cross_section_area_mm2', 'voltage_rating_v', 'insulation_type']
