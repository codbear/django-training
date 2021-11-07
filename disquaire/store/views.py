from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from .forms import BookingForm
from .models import Artists, Albums, Contacts, Bookings


def index(request):
    albums = Albums.objects.filter(is_available=True).order_by('-created_at')[:12]
    context = {'albums': albums}

    return render(request, 'store/index.html', context)


def listing(request):
    albums_list = Albums.objects.filter(is_available=True)
    paginator = Paginator(albums_list, 12)
    page = request.GET.get('page')

    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        albums = paginator.page(1)
    except EmptyPage:
        albums = paginator.page(paginator.num_pages)

    context = {'albums': albums, 'paginate': albums.has_other_pages()}

    return render(request, 'store/listing.html', context)


def single(request, album_id):
    album = get_object_or_404(Albums, pk=album_id)
    artists = [artist.name for artist in album.artists.all()]
    artists_name = " ".join(artists)
    context = {
        'album_title': album.title,
        'artists_name': artists_name,
        'album_id': album.id,
        'thumbnail': album.picture,
    }

    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            email = booking_form.cleaned_data['email']
            name = booking_form.cleaned_data['name']
            contact = Contacts.objects.filter(email=email)

            if not contact.exists():
                contact = Contacts.objects.create(
                    email=email,
                    name=name
                )

            booking = Bookings.objects.create(
                contact=contact,
                album=album
            )

            album.is_available = False
            album.save()
            context = {
                'album_title': album.title
            }

            return render(request, 'store/merci.html', context)
        else:
            context['errors'] = booking_form.errors.items()
    else:
        booking_form = BookingForm()

    context['booking_form'] = booking_form

    return render(request, 'store/single.html', context)


def search(request):
    query = request.GET.get('query')
    if not query:
        albums = Albums.objects.all()
    else:
        albums = Albums.objects.filter(title__icontains=query)

    if not albums.exists():
        albums = Albums.objects.filter(artists__name__icontains=query)

    title = "Résultats pour la requête %s" % query
    context = {
        'albums': albums,
        'title': title
    }

    return render(request, 'store/search.html', context)
