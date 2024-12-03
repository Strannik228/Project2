from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from datetime import date
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone



class AnimalType(models.Model):
    type_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    available = models.BooleanField(default=True)  # Добавьте это поле

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.type_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.type_name


class Breed(models.Model):
    breed_name = models.CharField(max_length=100)
    animal_type = models.ForeignKey(AnimalType, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True, blank=True)  # Обязательно наличие этого поля

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.breed_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.breed_name


from datetime import date

class Animal(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    inventory_number = models.CharField(max_length=50, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    nickname = models.CharField(max_length=100, null=True, blank=True)
    arrival_date = models.DateField()
    arrival_age_months = models.PositiveIntegerField()
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, related_name='animals')
    parent_animal = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='offspring')

    def __str__(self):
        return f"{self.nickname or 'No Nickname'} ({self.inventory_number})"

    @property
    def age(self):
        today = date.today()
        arrival_age_years = self.arrival_age_months // 12
        arrival_age_remaining_months = self.arrival_age_months % 12
        age_years = today.year - self.arrival_date.year + arrival_age_years
        age_months = today.month - self.arrival_date.month + arrival_age_remaining_months
        if age_months >= 12:
            age_years += 1
            age_months -= 12
        if age_months < 0:
            age_years -= 1
            age_months += 12

        if age_years == 1:
            year_str = "1 г"
        elif 2 <= age_years <= 4:
            year_str = f"{age_years} г"
        else:
            year_str = f"{age_years} л"

        month_str = f"{age_months} м"

        return f"{year_str} {month_str}"





from django.conf import settings

from django.conf import settings

class Weighting(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='weightings')
    weighing_date = models.DateField()
    weight_in_kg = models.FloatField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)



    class Meta:
        unique_together = ('animal', 'weighing_date')

    def __str__(self):
        return f"{self.animal.nickname or self.animal.inventory_number} - {self.weighing_date}: {self.weight_in_kg} kg"
    


from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_active = models.BooleanField(default=False)
    activation_token = models.CharField(max_length=128, blank=True, null=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='main_customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='main_customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def generate_activation_token(self):
        from django.utils.crypto import get_random_string
        token = get_random_string(48)
        self.activation_token = token
        self.save()
        return token







