URLAPI = 'http://127.0.0.1:8000/api/'
BACKAPI = 'http://127.0.0.1:8000/'

function visibility_password(id_img, id_input) {
    if($(`#${id_input}`).prop("type") == 'text'){
        $(`#${id_input}`).prop("type", "password");
        $(`#${id_img}`).prop("src", "/static/techway/images/show.png");
    }
    else{
        $(`#${id_input}`).prop("type", "text");
        $(`#${id_img}`).prop("src", "/static/techway/images/hide.png");
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

function newViewPrice(text){
    newText = "";
    textSpit = text.split('.')
    text = textSpit[0]
    for(i=text.length - 1; i >= 0; i--)
    {
        newText += text[i];
        if(i % 3 == 0) newText += " ";
    }

    newText = newText.split('').reverse().join('');

    newText = textSpit.length == 2 ? newText + '.' + textSpit[1] : newText;
    return newText
}