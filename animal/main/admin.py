from django.contrib import admin
from .models import AnimalType, Breed, Animal, Weighting
from django.db.models import Q
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(AnimalType)
class AnimalTypeAdmin(admin.ModelAdmin):
    list_display = ['type_name', 'slug']  # Убедитесь, что 'slug' существует в модели
    prepopulated_fields = {'slug': ('type_name',)}  # Значение должно быть кортежем


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ['breed_name', 'animal_type', 'slug']  # Убедитесь, что 'slug' существует в модели
    prepopulated_fields = {'slug': ('breed_name',)}  # Значение должно быть кортежем
    list_filter = ['animal_type']  # Значение должно быть списком или кортежем

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ['inventory_number', 'display_nickname', 'arrival_date', 'breed', 'gender']
    list_filter = ['breed', 'gender']
    search_fields = ['inventory_number', 'nickname']
    ordering = ['arrival_date']

    # Метод для отображения клички
    def display_nickname(self, obj):
        return obj.nickname if obj.nickname else "Без клички"
    display_nickname.short_description = 'Кличка'


@admin.register(Weighting)
class WeightingAdmin(admin.ModelAdmin):
    list_display = ['animal', 'weighing_date', 'weight_in_kg']
    
    # Используем стандартный механизм поиска по полям Animal (nickname и inventory_number)
    search_fields = ['animal__nickname', 'animal__inventory_number']  # Поиск по связанным полям Animal
    
    list_filter = ['weighing_date']



admin.site.register(CustomUser, UserAdmin)


    