from django.db import models

class Collection(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    user_id = models.IntegerField()

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    genres = models.CharField(max_length=100, blank=True)
    uuid = models.CharField(max_length=36)
    collection = models.ForeignKey(Collection, related_name='movies', on_delete=models.CASCADE)
    collection_id_field = models.IntegerField(default=0) 

    def save(self, *args, **kwargs):
        if not self.collection_id:
            collection = Collection.objects.create()
            self.collection_id = collection.id
        super().save(*args, **kwargs)
