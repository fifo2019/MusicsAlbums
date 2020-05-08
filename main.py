from bottle import route, run, HTTPError, template, static_file, request, post
import json
import connect_bd


@route("/")
def index():
    artist_list = connect_bd.find_artist()
    return template('index', artist_list=artist_list)


@route("/create")
def create():
    return template('create-album')


@post("/albums")
def create_albums():
    year = request.json.get("year")
    artist = request.json.get("artist")
    genre = request.json.get("genre")
    album = request.json.get("album")

    data = {
        'year': year,
        'artist': artist,
        'genre': genre,
        'album': album,
    }

    album = connect_bd.check_record(data)

    if album:
        if connect_bd.add_album(album):
            return 'Album created successfully!'
        else:
            return f"Sorry. Album not create!"
    else:
        message = f"Sorry. Albums {data.get('artist')} {data.get('album')} {data.get('genre')} {data.get('year')} exists"
        return message


@route("/albums/<artist>")
def albums_for_artist(artist):
    albums_list = connect_bd.find_album(artist)
    quantity_albums = len(albums_list)
    if not albums_list:
        message = f"Sorry. Executor {artist} not found..."
        raise HTTPError(404, message)
    else:
        return template('albums', albums_list=albums_list, quantity_albums=quantity_albums, artist=artist)


@route('/static/<filename:path>')
def static(filename):
    return static_file(filename, root="./static/")


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)