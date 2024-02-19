from django.db import models

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(Author, on_delete=models.CASCADE,
                               related_name="posts")
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title
