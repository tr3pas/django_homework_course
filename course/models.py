from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class StudentProfile(AbstractUser):
    age = models.PositiveIntegerField(null=True,blank=True)
    phone = models.CharField(max_length=13,verbose_name="Номер телефону", unique=True,null=True,blank=True)
        
    def __str__(self) -> str:
        return f"C: {self.username}"
    

class Course(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return f" Course {self.title}"
    
    class Meta:

        verbose_name = "Курс"
        verbose_name_plural = "Курси"
    
class StudentCourses(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    priority = models.PositiveIntegerField()
