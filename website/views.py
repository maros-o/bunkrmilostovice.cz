from django.shortcuts import render
from django.http import HttpResponse
from .models import Event, Report, Home_image, Gallery, Gallery_image, Visitor_counter, Home_text, History
from PIL import Image

def Increment_visitor_counter(viewname):
    visitor_counter = Visitor_counter.objects.all().get(name=viewname)
    visitor_counter.count += 1
    visitor_counter.save()

def Generate_compressed_images():
    galleries = Gallery.objects.all()

    for gal in galleries:
        gallery_images = gal.gallery_image_set.all()
        for img in gallery_images:
            img.save()

def Home(request):
    Increment_visitor_counter('home')

    event = Event.objects.get(id=1)
    event_text = ''
    if event.show:
        event_text = event.text

    reports = Report.objects.all()
    sorted_reports = reports.order_by('date').reverse()

    home_photos = Home_image.objects.all()
    home_photo_active = home_photos.get(id=1)
    home_photos = home_photos.exclude(id=1)

    galleries = Gallery.objects.all()
    histories = History.objects.all()

    home_texts = Home_text.objects.all()
    home_text1 = home_texts.get(id=1)
    home_text2 = home_texts.get(id=2)
    home_text3 = home_texts.get(id=3)

    context = {'event': event_text, 'reports': sorted_reports, "home_photo_active": home_photo_active, 'home_photos': home_photos, 'galleries': galleries, 'histories': histories, 'home_text1': home_text1, 'home_text2': home_text2, 'home_text3': home_text3}
    return render(request, "home.html", context)

def Historie(request, url):
    Increment_visitor_counter('historie')

    galleries = Gallery.objects.all()
    histories = History.objects.all()

    history = History.objects.get(name=url)

    context = {'galleries': galleries, 'histories': histories, 'history': history}
    return render(request, "history.html", context)

def Galerie(request, url):
    Increment_visitor_counter('galerie')

    galleries = Gallery.objects.all()
    histories = History.objects.all()

    contains = False
    for gallery in galleries:
        if url == gallery.name or url == gallery.name.lower():
            curr_galerry_name = gallery.name
            contains = True
            break

    if contains == False:
        message = 'Fotogalerie ' + url + ' na našem webu neexistuje, zkuste to prosím znovu.'
        return render(request, "error.html", {'message': message})

    gallery = Gallery.objects.get(name=curr_galerry_name)
    gallery_images = gallery.gallery_image_set.all()
    gallery_images = gallery_images.order_by('order')

    context = {'gallery_name': gallery.name, 'gallery_max_image_height': str(gallery.max_image_height), 'gallery_images': gallery_images, 'galleries': galleries, 'histories': histories}
    return render(request, "gallery.html", context)

def GalerieViews(request, url1, url2):
    galleries = Gallery.objects.all()
    histories = History.objects.all()
    gallery = Gallery.objects.get(name=url1)
    gallery_images = gallery.gallery_image_set.all()
    gallery_images = gallery_images.order_by('order')

    #Generate_compressed_images()

    i = 0
    for img in gallery_images:
        if img.image.name == url2:
            curr_img = img
            prev = i-1
            next = i+1
            break
        i += 1

    if (prev < 0):
        prev_img = gallery_images[len(gallery_images)-1]
    else:
        prev_img = gallery_images[prev]

    if (next > len(gallery_images)-1):
        next_img = gallery_images[0]
    else:
        next_img = gallery_images[next] 

    context = {'gallery_name': gallery.name, 'galleries': galleries, 'gallery_images': gallery_images, 'curr_img': curr_img, 'prev_img': prev_img, 'next_img': next_img, 'histories': histories, 'number': i+1, 'len': len(gallery_images)}
    return render(request, "gallerycarousel.html", context)

def Objekty(request):
    Increment_visitor_counter('objekty')

    galleries = Gallery.objects.all()
    histories = History.objects.all()

    context = {'galleries': galleries, 'histories': histories}
    return render(request, "objekty.html", context)

def Error(request, url):
    message = 'Stránka ' + url + ' na našem webu neexistuje, zkuste to prosím znovu.'
    return render(request, "error.html", {'message': message})

