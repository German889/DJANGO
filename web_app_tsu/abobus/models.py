from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

student_group = Group.objects.get_or_create(name='Студенты')
investor_group = Group.objects.get_or_create(name='Инвесторы')

class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('STUDENT', 'Student'),
        ('INVESTOR', 'Investor'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, null=True)
    name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f'{self.user.username} ({self.user_type})'

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    payback_period = models.PositiveIntegerField()
    goals = models.TextField()
    intended_outcome = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Investment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    investment_date = models.DateField(auto_now_add=True)
    investor = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.investment_date} - {self.amount}'
