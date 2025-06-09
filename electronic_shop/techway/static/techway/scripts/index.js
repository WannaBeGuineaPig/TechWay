URLAPI = 'http://127.0.0.1:8000/api/'
URLBACK = 'http://127.0.0.1:8000/'

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

function addOrRemoveFavorite(event, ImagePath, fillImagePath, id_product){
    let url = '';
    let title = '';
    let imagePath = '';
    
    if ($(event.target).attr('title') == 'Добавить в избранное'){
        url = `${URLBACK}add_favorite_item/?id_product=${id_product}`;
        title = 'В избранном';
        imagePath = fillImagePath;
    } 
    
    else {
        url = `${URLBACK}delete_favorite_item/?id_product=${id_product}`;
        title = 'Добавить в избранное';
        imagePath = ImagePath;
    }
        
    $.ajax({
        url : url,
        type : 'GET',
        complete : function(){
            $(event.target).attr('src', imagePath);
            $(event.target).attr('title', title);
        }
    });
}

function removeFavorite(event, oldImagePath, newImagePath, id_product){
    $.ajax({
        url : `${URLBACK}delete_favorite_item/?id_product=${id_product}`,
        type : 'GET',
        complete : function(){
            $(event.target).attr('src', newImagePath);
            $(event.target).attr('title', 'Добавить в избранное');
            $(event.target).onclick = function(){addFavorite(event, newImagePath, oldImagePath, id_product)};
    
        }
    });
}

function addFunc(){
    btn = $(this);
    console.log(btn);
    btn.unbind("click");
    idItem = $(this).attr('id');
    textBtn = $(this).text();
    if(textBtn == 'В корзине') {
        $(location).attr('href', `${URLBACK}backet/`)
        return;
    }
    
    $.ajax({
        url: `${URLBACK}add_to_basket/${idItem}`,
        type: 'GET',
        complete : function(data){
            if(data.responseJSON.status_code == 400) { 
                alert(data.responseJSON.error);
                btn.bind("click", addFunc);
            }
            else{
                newViewBtnBasket(btn, 'add_item', 'В корзине');
            }
        }
    });
}

function newViewBtnBasket(item, className, textBtn){
    $(item).text('');
    $(item).addClass(className);
    $(item).fadeTo("slow", 1, function(){
        $(item).removeClass(className);
        $(item).text(textBtn);
        $(item).bind("click", addFunc);
    });
}

$('.add_btn').click(addFunc);

function minBirthDate(){
    let dateNow = new Date();
    dateNow.setFullYear(dateNow.getFullYear() -18);
    return `${dateNow.getFullYear()}-${dateNow.getMonth() > 9 ? dateNow.getMonth() : `0${dateNow.getMonth()}`}-${dateNow.getDate() > 9 ? dateNow.getDate() : `0${dateNow.getDate()}`}`;
}

function maxBirthDate(){
    let dateNow = new Date();
    dateNow.setFullYear(dateNow.getFullYear() - 100);
    return `${dateNow.getFullYear()}-${dateNow.getMonth() > 9 ? dateNow.getMonth() : `0${dateNow.getMonth()}`}-${dateNow.getDate() > 9 ? dateNow.getDate() : `0${dateNow.getDate()}`}`;
}

function checkImagePath(path){
    let pathSplit = path.split('\\');
    let baseName = pathSplit[pathSplit.length - 1];
    let baseNameSplit = baseName.split('.');
    return ['svg', 'png', 'jpeg', 'bmp', 'jpg'].indexOf(baseNameSplit[baseNameSplit.length - 1]) != -1
}