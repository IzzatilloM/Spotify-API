from django.db import models

class Singer(models.Model):
    name = models.CharField(max_length=255)
    birthdate = models.DateTimeField()
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Album(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/')
    singer = models.ForeignKey(Singer, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Song(models.Model):
    name = models.CharField(max_length=255)
    duration = models.DurationField(blank=True, null=True)
    genre = models.CharField(max_length=50)
    file = models.FileField(upload_to='audios/', blank=True, null=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return self.name