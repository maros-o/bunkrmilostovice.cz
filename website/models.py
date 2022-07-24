from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files import File

def compress(image, compress_quality, name, max_size):
    im = Image.open(image)
    im_io = BytesIO()
    im.thumbnail(max_size, Image.ANTIALIAS)
    im.save(im_io, 'JPEG', quality=compress_quality) 
    new_image = File(im_io, name=image.name[:len(image.name) - 4]+name+image.name[-4:])
    return new_image

class Event(models.Model):
    text = models.TextField(default='')
    show = models.BooleanField(default=False)

    def __str__(self):
        return "Upozornění na vrcholu stránky (nepřidávat další, jen měnit tenhle)"

class Home_text(models.Model):
    name = models.TextField(default='nazev')
    text = models.TextField(default='')

    def __str__ (self):
        return 'karta na uvodni strance: ' + self.name

class Report(models.Model):
    thumbnail = models.ImageField()
    title = models.CharField(max_length=100, blank=True)
    text = models.TextField(blank=True)
    date = models.DateField()

    def __str__(self):
        title = 'žádný'
        if self.title != '':
            title = self.title
        return 'titulek: ' + title + ' | datum: ' + str(self.date)

class Home_image(models.Model):
    image = models.ImageField()

    def __str__(self):
        return "fotografie na hlavní stránku: " + self.image.name

class Gallery(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    max_image_height = models.IntegerField(default=300)

    def __str__(self):
        return self.name

class Gallery_image(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    image = models.ImageField()
    compressed = models.ImageField(default='', blank=True, null=True, editable=False)
    thumbnail = models.ImageField(default='', blank=True, null=True, editable=False)
    description = models.CharField(max_length=100, blank=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return "galerie: " + self.gallery.name + " | popisek: " + self.description + " | obrázek: " + self.image.name
    
    def save(self, *args, **kwargs):
        self.compressed = compress(self.image, 80, '_compressed', (1920, 1920))
        self.thumbnail = compress(self.image, 50, '_thumbnail', (720, 1280))

        super().save(*args, **kwargs)

class Visitor_counter(models.Model):
    name = models.CharField(max_length=100)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return 'počet načtení stránky ' + self.name + ": " + str(self.count)

class History(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    title = models.TextField(default="")
    content = models.TextField(default="")

    def __str__(self):
        return self.name