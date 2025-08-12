from django.db import models
from django.urls import reverse
from django.db.models import UniqueConstraint # constrains field values to be unique
from django.db.models.functions import Lower # returns field value as lower cased

# Create your models here.
class MaterialCategory(models.Model):
    """Represents construction material, i.e. cement, steel,
     sand, crush, bricks, building & finishing."""
    MATERIAL_TYPE = (
        ('b', 'Select Material'),
        ('Batteries', 'Batteries'),
        ('Cement', 'Cement'),
        ('Cables & Wires', 'Cables & Wires'),
        ('Electrical Panels', 'Electrical Panels'),
        ('Gravel & Crush', 'Gravel & Crush'),
        ('Paints', 'Paints'),
        ('Pipes & Fittings', 'Pipes & Fittings'),
        ('Steel', 'Steel'),
        ('Solar Panels', 'Solar Panels'),
    )
    material_category = models.CharField(
        max_length=20,
        choices=MATERIAL_TYPE,
        blank=True,
        default='b',
        help_text="Select material from list."
    )
    brand = models.CharField(max_length=200)

    def __str__(self):
        return self.material_category
    def get_absolute_url(self):
        return reverse('material-detail', args=[str(self.id)])
    class Meta:
        ordering = ['material_category']

class Sellor(models.Model):
    """Represents the seller providing materials pertaining to construction projects."""
    registered_store_name = models.CharField(max_length=200)
    owner = models.CharField(verbose_name='Owner Name / مالک کا نام', max_length=200)
    address_1 = models.CharField(max_length=200,null=True, blank=True)
    address_2 = models.CharField(max_length=200,null=True, blank=True)
    tehsil = models.CharField(max_length=200,null=True, blank=True)
    district = models.CharField(max_length=200,null=True, blank=True)
    mohalla =  models.CharField(max_length=200,null=True, blank=True)
    city = models.CharField(max_length=100,null=True, blank=True)
    network = models.CharField(max_length=200,null=True, blank=True)
    cell = models.CharField(max_length=200,null=True, blank=True)
    material = models.ForeignKey(MaterialCategory,
                                 on_delete=models.RESTRICT,
                                 null=True,
                                 help_text='Select Material you carry.')

    def __str__(self):
        return self.registered_store_name
    def get_absolute_url(self):
        return reverse('registered-store-name-detail', args=[str(self.id)])
    class Meta:
        ordering = ['registered_store_name']
        constraints = [
            UniqueConstraint(
                Lower('registered_store_name'),
                name='registered_store_name_case_insensitive_unique',
                violation_error_message = "Registered Store Name already exists (case insensitive match)"
            ),
        ]