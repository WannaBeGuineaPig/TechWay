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
    $('#box_product_list').css('filter', 'blur(10px)')
    let type_sort = $(this).attr('value');
    let category = $('.categories').text();
    let search = $('#search_items').val();
    $('#sort_link').text($(`[for=${type_sort}]`).text());
    $('#pages').text(`1/${$('#pages').text().split('/')[1]}`);
    category = category != '' ? '&subcategory=' + category.split(' > ')[2] : '';
    search = search != '' ? '&search=' + search : '';
    history.replaceState('', '',url=`${URLBACK}home/?sort=${type_sort}${category}${search}`);
    $.ajax({
        url: `${URLBACK}update_list_product/?sort=${type_sort}${category}${search}`,
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

$('.btn_pages').click(function(){
    let number_page = parseInt($('#pages').text().split('/')[0]);
    let count_page = parseInt($('#pages').text().split('/')[1]);
    number_page = $(this).attr('id') == 'minus_page' ? number_page - 1 : number_page + 1;
    if (number_page == 0 || number_page > count_page){
        return;
    }
    let type_sort = $('input[type=radio]:checked').attr('value');
    let category = $('.categories').text();
    let search = $('#search_items').val();
    $('#sort_link').text($(`[for=${type_sort}]`).text());
    $('#pages').text(`${number_page}/${count_page}`);
    category = category != '' ? '&subcategory=' + category.split(' > ')[2] : '';
    search = search != '' ? '&search=' + search : '';
    type_sort = type_sort != '' ? '&sort=' + type_sort : '';
    window.location.href = `${URLBACK}home/?number_page=${number_page}${type_sort}${category}${search}`;
});

$(document).ready(function(){
    let type_sort = $('input[type=radio]:checked').attr('value');
    $('#sort_link').text($(`[for=${type_sort}]`).text());
});