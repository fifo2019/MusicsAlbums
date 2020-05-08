document.addEventListener('DOMContentLoaded', function() {
    let createAlbum = document.querySelector('#js-create-album');


    function sendPOST(form, data) {
        fetch(`${form.action}`, {
            method: 'POST',
            body: JSON.stringify({
                "year": `${data[0]}`,
                "artist": `${data[1]}`,
                "genre": `${data[2]}`,
                "album": `${data[3]}`,
            }),
            headers: {
                'Content-Type': 'application/json; charset=UTF-8',
            },
        })
            .then(result => result.text())
            .then(data => {
                form.remove();
                let container = document.querySelector('.container');
                let content = `<p class="text-create-album">${data}</p>`
                container.insertAdjacentHTML('afterbegin', content);
            })
            .catch(error => console.log(error));
    };


    function validYear(year) {
        figureYear = Number(year.value.replace(/\D+/g,""));
        if (figureYear === 0) {
            year.style.color = 'red';
            year.value = "Incorrect data entry";
            return false;
        }

        let nowDate = new Date();

        if (figureYear < 1900 || figureYear > nowDate.getFullYear() || `${figureYear}`.length !== 4) {
            year.style.color = 'red';
            year.value = "Incorrect data entry";
            return false;
        } else {
            year.style.color = 'black';
            year.value = `${figureYear}`;
            return figureYear;
        }
    };


    function validText(text) {
        checkText = text.value.trim();

        if (checkText.length === 0 || checkText === 'Incorrect data entry') {
            text.style.color = 'red';
            text.value = "Incorrect data entry";
            return false;
        } else {
            checkText = `${checkText[0].toUpperCase()}${checkText.slice(1)}`;
            text.style.color = 'black';
            text.value = `${checkText}`;
            return checkText;
        }
    };

    function validGenre(genre) {
        if (genre.value === 'Choose a genre') {
            genre.style.color = 'red';
            return false;
        } else {
            genre.style.color = 'black';
            return genre.value;
        }
    };

    createAlbum.addEventListener('click', function() {
        let form = document.querySelector('form');
        let year = validYear(form.year);
        let artist = validText(form.artist);
        let album = validText(form.album);
        let genre = validGenre(form.genre);
        let data = [year, artist, genre, album];

        if (data.every((el) => el)) {
            sendPOST(form, data);
        }
    });
});