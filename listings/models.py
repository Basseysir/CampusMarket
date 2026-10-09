from django.db import models
from django.conf import settings
from urllib.parse import quote
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    CONDITION_CHOICES = (
        ('new', 'Brand New'),
        ('like_new', 'Like New'),
        ('used', 'Fairly Used'),
    )

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='products'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='products'
    )
    image = models.ImageField(upload_to='product_images/')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='like_new')
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # In listings/models.py (inside your Product model class)

    def get_whatsapp_url(self):
        if self.seller.phone_number:
            # Clean non-digit characters for WhatsApp API
            phone = "".join(filter(str.isdigit, self.seller.phone_number))
            if phone.startswith('0'):
                phone = '234' + phone[1:] # Adjust country code if needed (e.g., Nigeria +234)
            message = f"Hello, I am interested in your item '{self.title}' listed on CampusMarket for ₦{self.price}."
            return f"https://wa.me/{phone}?text={quote(message)}"
        return "#"

    def get_call_url(self):
        if self.seller.phone_number:
            return f"tel:{self.seller.phone_number}"
        return "#"

    def __str__(self):
        return self.title