from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class BotUser(AbstractUser):
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"



class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    photo_url = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - {self.product.name}"

    
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

class Branch(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branches"


class Button(models.Model):
    """Model for storing Telegram bot buttons"""
    BUTTON_TYPES = [
        ('text', 'Text Button'),
        ('url', 'URL Button'),
        ('callback', 'Callback Button'),
        ('web_app', 'Web App Button'),
    ]
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, help_text="Unique identifier for the button")
    text = models.CharField(max_length=255, help_text="Button text displayed to users")
    button_type = models.CharField(max_length=20, choices=BUTTON_TYPES, default='text')
    callback_data = models.CharField(max_length=255, blank=True, null=True, help_text="Callback data for callback buttons")
    url = models.URLField(blank=True, null=True, help_text="URL for URL or Web App buttons")
    is_active = models.BooleanField(default=True, help_text="Whether the button is active")
    order = models.IntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.text})"

    class Meta:
        verbose_name = "Button"
        verbose_name_plural = "Buttons"
        ordering = ['order', 'name']


class Keyboard(models.Model):
    """Model for storing Telegram bot keyboard layouts"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, help_text="Unique identifier for the keyboard")
    buttons = models.ManyToManyField(Button, related_name='keyboards', help_text="Buttons in this keyboard")
    row_size = models.IntegerField(default=2, help_text="Number of buttons per row")
    is_inline = models.BooleanField(default=True, help_text="Whether this is an inline keyboard")
    is_active = models.BooleanField(default=True, help_text="Whether the keyboard is active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Keyboard"
        verbose_name_plural = "Keyboards"
        ordering = ['name']






