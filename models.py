from django.db import models

# Create your models here.
from django.db import models

class Order(models.Model):
    user_id = models.IntegerField()
    product_id = models.IntegerField()
    quantity = models.IntegerField()

    class Meta:
        app_label = 'orders_app'
