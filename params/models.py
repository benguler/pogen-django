from django.db import models

# Create your models here.
class Params(models.Model):
    genre_choices = (
        ( "modern_love", "Modern Love"),
        ("modern_mythology_folklore", "Modern Mythology"),
        ("modern_nature", "Modern Nature"),
        ("renaissance_love", "Renaissance Love"),
        ("renaissance_mythology_folklore", "Renaissance Mythology"),
        ("renaissance_nature", "Renaissance Nature"),

    )

    genre   = models.CharField(max_length=120, choices = genre_choices, default = "Modern Love")
    syls    = models.CharField("Syllable Scheme", max_length=120, default = "5-7-5")

