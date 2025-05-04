function click_sort_link(){
    let box_types_sort = document.getElementById('box_types_sort');
    let sort_link = document.getElementById('sort_link');
    if (box_types_sort.style.visibility == 'hidden'){
        box_types_sort.style.visibility = 'visible';
        sort_link.style.color = 'var(--second_main_color)';
    }
    else{
        box_types_sort.style.visibility = 'hidden';
        sort_link.style.color = 'rgb(0, 166, 255)';
    }
}

$('input[type=radio]').click(function(){
    let type_sort = $(this).attr('value');
    let currentHref = $(location).attr('href');
    let newHref = currentHref.split('/');
    newHref[newHref.length - 1] = `update_list_product/?sort=${type_sort}`;
    // newHref[newHref.length - 1] = 'update_list_product';
    newHref = newHref.join('/');
    $.ajax({
        url: newHref,
        type: 'GET',
        success : function (json) {
            if(json.result){
                $('#box_product_list').replaceWith(json.product_list_page);
            }
        } 
    });
});