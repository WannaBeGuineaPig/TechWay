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
        url: `${URLBACK}update_list_product/?sort=${type_sort}`,
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