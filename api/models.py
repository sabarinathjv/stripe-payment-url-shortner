from django.db import models




class Invoice(models.Model):

    number = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    email = models.EmailField( max_length=254)
    project_name = models.CharField(max_length=200)
    url = models.URLField(max_length=200,blank=True,null=True)
    amount= models.IntegerField(default=0) 
    paid = models.BooleanField(default=False)





