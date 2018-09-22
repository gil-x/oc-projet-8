from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "Catégories"


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    grade = models.CharField(max_length=1)
    url = models.CharField(max_length=255)
    barcode = models.CharField(max_length=13)
    brand = models.CharField(max_length=30)
    store = models.CharField(max_length=30)
    categories = models.ManyToManyField(Category, related_name='products', through='Position')
    product_img_url = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name_plural = "Produits"


class Position(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    rank = models.IntegerField()

    def __str__(self):
        return str(self.rank)