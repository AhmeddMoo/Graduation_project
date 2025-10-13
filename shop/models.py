from django.db import models

class Product(models.Model):
   name=models.CharField(max_length=100)
   description=models.TextField()
   price=models.DecimalField(max_digits=10, decimal_places=2)
   stock=models.IntegerField()
   image=models.ImageField(upload_to='products/', null=True, blank=True)
   created_at=models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return (f'{self.name} - ${self.price} - stock:{self.stock}')
   
class CartItem(models.Model):
   user=models.ForeignKey('auth.User', on_delete=models.CASCADE)
   product=models.ForeignKey(Product, on_delete=models.CASCADE)
   quantity=models.IntegerField(default=1)
   added_at=models.DateTimeField(auto_now_add=True)
    
   def __str__(self):
       return (f'{self.product.name} x {self.quantity} for {self.user.username}')
   
class Order(models.Model):
   user=models.ForeignKey('auth.User',on_delete=models.CASCADE)
   created_at=models.DateTimeField(auto_now_add=True)
   total_price=models.DecimalField(max_digits=10, decimal_places=2)
   is_completed=models.BooleanField(default=False)

   def __str__(self):
         return (f'Order {self.id} by {self.user.username} - Total: ${self.total_price}')



# Create your models here.
