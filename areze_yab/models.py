import re
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField


# Create your models here.


class Size(models.TextChoices):
    SMALL = 'SMALL', 'Small'
    MEDIUM = 'MEDIUM', 'Medium'
    LARGE = 'LARGE', 'Large'


class CustomUser(AbstractUser):
    is_company = models.BooleanField(default=False)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=150, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=11, blank=True, null=True, unique=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username


class Company(models.Model):
    user = models.ManyToManyField(CustomUser)
    name = models.CharField(max_length=100)
    registrationNumber = models.CharField(max_length=100)
    nationalID = models.CharField(max_length=100)
    size = models.CharField(max_length=10, choices=Size.choices)
    company_domain = models.CharField(max_length=100)
    is_company = models.BooleanField(default=True)





class Domain(models.Model):
    name = models.CharField(max_length=100, unique=True)  # e.g., d1, d2, d3

    def __str__(self):
        return self.name

class SubDomain(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='subdomains')
    name = models.CharField(max_length=20, unique=True)  # e.g., s1_d1, s2_d1

    def __str__(self):
        return self.name

class Question(models.Model):
    subdomain = models.ForeignKey(SubDomain, on_delete=models.CASCADE, related_name='questions')
    name = models.CharField(max_length=50, unique=True)  # e.g., q1_s1_d1
    text = models.TextField()  # Question text
    size = models.CharField(max_length=10, choices=Size.choices)

    def __str__(self):
        return f"{self.name} ({self.size})"

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=50)  # e.g., a1_q1_s1_d1
    text = models.TextField()  # Option text
    value = models.PositiveSmallIntegerField()  # Option number (1, 2, 3, 4)

    class Meta:
        unique_together = ('question', 'value')

    def __str__(self):
        return f"{self.name} ({self.value})"

class Questionnaire(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='questionnaires')
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Questionnaire {self.id} for {self.company.name} in {self.domain}"

class Answer(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('questionnaire', 'question')

    def __str__(self):
        return f"Answer to {self.question} in {self.questionnaire}"