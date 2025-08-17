from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of field
from django.urls import reverse

# -------------------
# Core Models
# -------------------

class Store(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )
    location = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store-detail", kwargs={"pk": self.pk})


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories - زمرہ جات'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category-detail", kwargs={"pk": self.pk})


class Brand(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="brands"
    )

    class Meta:
        ordering = ['name']


    def __str__(self):
        return f"{self.name} ({self.category.name})"

    def get_absolute_url(self):
        return reverse("brand-detail", kwargs={"pk": self.pk})


class Item(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name="items"
    )


    def __str__(self):
        return f"{self.name} ({self.brand.name if self.brand else 'No Brand'})"

    def get_absolute_url(self):
        return reverse("item-detail", kwargs={"pk": self.pk})


class StoreItem(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    reorder_point = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=50, blank=True, null=True)
    barcode = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        unique_together = ('store', 'item')
        ordering = ['store', 'item']

    def __str__(self):
        return f"{self.store.name} - {self.item.name}"

    def get_absolute_url(self):
        return reverse("storeitem-detail", kwargs={"pk": self.pk})


# -------------------
# Attribute Models
# -------------------

class BrickAttributes(models.Model):
    item = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,
        limit_choices_to={'brand__category__name': 'Bricks'}
    )
    brick_type = models.CharField(max_length=50)     # e.g., Clay, Fly Ash
    dimensions_mm = models.CharField(max_length=50)  # e.g., 190x90x90
    compressive_strength_mpa = models.DecimalField(max_digits=6, decimal_places=2)
    water_absorption_percent = models.DecimalField(max_digits=5, decimal_places=2)

    def clean(self):
        # extra safety: ensure the item's brand is in the expected category
        if self.item and self.item.brand and self.item.brand.category.name != 'Brick':
            raise ValidationError("Selected item does not belong to Brick category (via its brand).")

    def __str__(self):
        return f"Brick Specs - {self.item.name}"

    def get_absolute_url(self):
        return reverse("brick-detail", kwargs={"pk": self.pk})

class CableAttributes(models.Model):
    item = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,
        limit_choices_to={'brand__category__name': 'Cables'}
    )
    cable_type = models.CharField(max_length=50)        # e.g., Single Core, Multi-Core, Armoured
    conductor_material = models.CharField(max_length=50)  # e.g., Copper, Aluminum
    cross_section_area_mm2 = models.DecimalField(max_digits=6, decimal_places=2)  # e.g., 2.5
    voltage_rating_v = models.PositiveIntegerField()   # e.g., 450
    insulation_type = models.CharField(max_length=50)  # e.g., PVC, XLPE

    def __str__(self):
        return f"Cable Specs - {self.item.name}"
    def clean(self):
        # extra safety: ensure the item's brand is in the expected category
        if self.item and self.item.brand and self.item.brand.category.name != 'Cable':
            raise ValidationError("Selected item does not belong to Cable category (via its brand).")

    def get_absolute_url(self):
        return reverse("cable-detail", kwargs={"pk": self.pk})


class CementAttributes(models.Model):
    item = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,
        limit_choices_to={'brand__category__name': 'Cement'}
    )
    grade = models.CharField(max_length=50)
    weight_per_bag_kg = models.DecimalField(max_digits=5, decimal_places=2)
    setting_time_min = models.PositiveIntegerField()
    compressive_strength_mpa = models.DecimalField(max_digits=5, decimal_places=2)

    def clean(self):
        # extra safety: ensure the item's brand is in the expected category
        if self.item and self.item.brand and self.item.brand.category.name != 'Cement':
            raise ValidationError("Selected item does not belong to Cement category (via its brand).")

    def __str__(self):
        return f"Cement Specs - {self.item.name}"

    def get_absolute_url(self):
        return reverse("cement-detail", kwargs={"pk": self.pk})


class SandAttributes(models.Model):
    item = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,
        limit_choices_to={'brand__category__name': 'Sand'}
    )
    sand_type = models.CharField(max_length=50)
    grain_size_mm = models.DecimalField(max_digits=5, decimal_places=2)
    source_location = models.CharField(max_length=100)

    def clean(self):
        # extra safety: ensure the item's brand is in the expected category
        if self.item and self.item.brand and self.item.brand.category.name != 'Sand':
            raise ValidationError("Selected item does not belong to Sand category (via its brand).")

    def __str__(self):
        return f"Sand Specs - {self.item.name}"

    def get_absolute_url(self):
        return reverse("sand-detail", kwargs={"pk": self.pk})


class ConcreteAttributes(models.Model):
    item = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,
        limit_choices_to={'brand__category__name': 'Concrete'}
    )
    grade = models.CharField(max_length=50)
    slump_mm = models.PositiveIntegerField()
    aggregate_size_mm = models.PositiveIntegerField()
    cement_ratio = models.CharField(max_length=50)

    def clean(self):
        # extra safety: ensure the item's brand is in the expected category
        if self.item and self.item.brand and self.item.brand.category.name != 'Concrete':
            raise ValidationError("Selected item does not belong to Concrete category (via its brand).")

    def __str__(self):
        return f"Concrete Specs - {self.item.name}"

    def get_absolute_url(self):
        return reverse("concrete-detail", kwargs={"pk": self.pk})


class PipeAttributes(models.Model):
    item = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,
        limit_choices_to={'brand__category__name': 'Pipes'}
    )
    pipe_material = models.CharField(max_length=50)         # e.g., PVC, CPVC, GI, PPR
    nominal_diameter = models.DecimalField(max_digits=6, decimal_places=2)  # 50.00
    diameter_unit = models.CharField(max_length=10, default="mm")           # mm or inch
    length_m = models.DecimalField(max_digits=6, decimal_places=2)          # 4.00
    pressure_rating = models.CharField(max_length=50)       # e.g., PN16, Sch 40

    def clean(self):
        # extra safety: ensure the item's brand is in the expected category
        if self.item and self.item.brand and self.item.brand.category.name != 'Pipe':
            raise ValidationError("Selected item does not belong to Pipe category (via its brand).")

    def __str__(self):
        return f"Pipe Specs - {self.item.name}"

    def get_absolute_url(self):
        return reverse("pipe-detail", kwargs={"pk": self.pk})

class SteelAttributes(models.Model):
    item = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,
        limit_choices_to={'brand__category__name': 'Steel'}
    )
    steel_type = models.CharField(max_length=50)
    diameter_mm = models.PositiveIntegerField()
    tensile_strength_mpa = models.PositiveIntegerField()

    def clean(self):
        # extra safety: ensure the item's brand is in the expected category
        if self.item and self.item.brand and self.item.brand.category.name != 'Steel':
            raise ValidationError("Selected item does not belong to Steel category (via its brand).")

    def __str__(self):
        return f"Steel Specs - {self.item.name}"

    def get_absolute_url(self):
        return reverse("steel-detail", kwargs={"pk": self.pk})


class PaintAttributes(models.Model):
    item = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,
        limit_choices_to={'brand__category__name': 'Paint'}
        )
    paint_type = models.CharField(max_length=50)
    base = models.CharField(max_length=50)
    coverage_per_liter_sqm = models.DecimalField(max_digits=6, decimal_places=2)
    drying_time_hours = models.DecimalField(max_digits=4, decimal_places=2)

    def clean(self):
        # extra safety: ensure the item's brand is in the expected category
        if self.item and self.item.brand and self.item.brand.category.name != 'Paint':
            raise ValidationError("Selected item does not belong to Paint category (via its brand).")

    def __str__(self):
        return f"Paint Specs - {self.item.name}"

    def get_absolute_url(self):
        return reverse("paint-detail", kwargs={"pk": self.pk})
