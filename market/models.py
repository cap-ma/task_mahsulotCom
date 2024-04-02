from django.db import models


class Category(models.Model):
    title=models.CharField(max_length=128)
    description=models.TextField()
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.title
    

class Shop(models.Model):
    title=models.CharField(max_length=128)
    description=models.TextField()
    image_url=models.ImageField(upload_to='media/shop/')

    def __str__(self):
        return self.title
    
class Order(models.Model):
    name=models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.name
    
class Product(models.Model):
    description=models.TextField()
    title=models.CharField(max_length=128)
    amount=models.IntegerField()
    price=models.DecimalField(max_digits=18,decimal_places=2)#in docs it is float but  float may cause incorrect precision  which may cause error in future
    active=models.BooleanField()
    shop=models.ForeignKey(Shop,on_delete=models.DO_NOTHING,verbose_name='shop of product')
    category=models.ManyToManyField(Category)# product should be assigned to one or several categories
   
class OrderProduct(models.Model):
    quantity=models.IntegerField()
    order=models.ForeignKey(Order,on_delete=models.DO_NOTHING)
    product=models.ForeignKey(Product,on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.product.title

class Image(models.Model):
    file=models.ImageField(upload_to='media/products/')
    product=models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.file.path

