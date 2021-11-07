from django.http import HttpResponse
from django.template import loader

from .models import Artists, Albums


def format_album_list(albums):
    formatted_albums = [f"<li>{album.title}</li>" for album in albums]
    return """<ul>{}</ul>""".format('\n'.join(formatted_albums))


def index(request):
    albums = Albums.objects.filter(is_available=True).order_by("-created_at")[:12]
    template = loader.get_template("store/index.html")

    return HttpResponse(template.render(request=request))


def listing(request):
    albums = Albums.objects.filter(is_available=True)
    message = format_album_list(albums)

    return HttpResponse(message)


def single(request, album_id):
    album = Albums.objects.get(pk=album_id)
    artists = " ".join([artist.name for artist in album.artists.all()])
    message = f"Le nom de l'album est {album.title}. Il a été écrit par {artists}"
    return HttpResponse(message)


def search(request):
    query = request.GET.get("query")
    if not query:
        albums = Albums.objects.all()
    else:
        albums = Albums.objects.filter(title__icontains=query)

    if not albums.exists():
        albums = Albums.objects.filter(artists__name__icontains=query)

    if not albums.exists():
        message = "Misère de misère, nous n'avons trouvé aucun résultat !"
    else:
        albums = [f"<li>{album.title}</li>" for album in albums]
        message = """
            Nous avons trouvé les albums correspondant à votre requête ! Les voici :
            <ul>
                {}
            </ul>
        """.format("</li><li>".join(albums))

    return HttpResponse(message)
