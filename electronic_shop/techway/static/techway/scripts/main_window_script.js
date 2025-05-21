function click_sort_link(){
    let box_types_sort = document.getElementById('box_types_sort');
    let sort_link = document.getElementById('sort_link');
    if (box_types_sort.style.visibility == 'hidden'){
        box_types_sort.style.visibility = 'visible';
        sort_link.style.color = 'var(--second_main_color)';
        // $('input[type=radio]:checked').focus()
    }
    else{
        box_types_sort.style.visibility = 'hidden';
        sort_link.style.color = 'rgb(0, 166, 255)';
    }
}

$('input[type=radio]').click(function(){
    $('#box_product_list').css('filter', 'blur(10px)')
    let type_sort = $(this).attr('value');
    $.ajax({
        url: `${BACKAPI}update_list_product/?sort=${type_sort}`,
        type: 'GET',
        success : function (json) {
            if(json.result){
                $('#box_product_list').fadeTo("midle", 1, function(){
                    $(this).replaceWith(json.product_list_page);
                });
            }
        } 
    });
});

$('.add_btn').click(function(){
    idItem = $(this).attr('id');
    textBtn = $(this).text();
    if(textBtn == 'В корзине') {
        $(location).attr('href', `${BACKAPI}backet/`)
        return;
    }
    $.ajax({
        url: `${BACKAPI}add_to_basket/${idItem}`,
        type: 'GET',
    });
    newViewBtnBasket(this, 'add_item', 'В корзине')
    // $(this).text('');
    // $(this).addClass('add_item')
    // $(this).fadeTo("slow", 1, function(){
    //     $(this).removeClass('add_item');
    //     $(this).text(textBtn);
    // });
});

function newViewBtnBasket(item, className, textBtn){
    $(item).text('');
    $(item).addClass(className);
    $(item).fadeTo("slow", 1, function(){
        $(item).removeClass(className);
        $(item).text(textBtn);
    });
}

function addFavorite(){
    alert('test');
}