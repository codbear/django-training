from django.http import HttpResponse

from .models import ALBUMS


def index(request):
    message = 'Hello world!'
    return HttpResponse(message)


def listing(request):
    albums = ["<li>{}</li>".format(album['name']) for album in ALBUMS]
    message = """<ul>{}</ul>""".format("\n".join(albums))
    return HttpResponse(message)


def single(request, album_id):
    album = ALBUMS[album_id]
    artists = " ".join([artist['name'] for artist in album['artists']])
    message = f"Le nom de l'album est {album['name']}. Il a été écrit par {artists}"
    return HttpResponse(message)


def search(request):
    query = request.GET.get('query')
    if not query:
        message = "Aucun artiste n'est demandé"
    else:
        albums_result = []
        for album in ALBUMS:
            artists = " ".join(artist['name'] for artist in album['artists'])

            if query in artists:
                albums_result.append(album)

        if len(albums_result) == 0:
            message = "Misère de misère, nous n'avons trouvé aucun résultat !"
        else:
            albums = ["<li>{}</li>".format(album['name']) for album in albums_result]
            message = """
                Nous avons trouvé les albums correspondant à votre requête ! Les voici :
                <ul>
                    {}
                </ul>
            """.format("</li><li>".join(albums))

    return HttpResponse(message)
