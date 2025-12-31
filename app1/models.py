from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    ch=models.CharField(max_length=25,unique=True)

    def __str__(self):
        return self.ch

class Product(models.Model):
    p_name = models.CharField(max_length=25)
    p_price = models.FloatField()
    p_image = models.FileField(upload_to='products/')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )


    def __str__(self):
        return self.p_name
    

class Cart(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"
    
class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="items")

    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart','product')

    def __str__(self):
        return f"{self.product.p_name} ({self.quantity})"