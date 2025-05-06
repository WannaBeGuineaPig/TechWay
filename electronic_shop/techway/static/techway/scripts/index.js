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