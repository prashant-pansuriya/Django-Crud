from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
class Customer(models.Model):

  def age_check(value):
    if value > 0:
      return value
    else:
      raise ValidationError("Age is Not Negative !")

  name = models.CharField(max_length=200, unique=True)
  age = models.IntegerField(validators=[age_check])
  mobile_num_regex = RegexValidator(regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!")
  mobile_no = models.CharField(validators=[mobile_num_regex], max_length=10)

  class Meta:
    verbose_name = "Customer"
    verbose_name_plural = "Customers"
    ordering = ['name']

  def __str__(self):
    return self.name