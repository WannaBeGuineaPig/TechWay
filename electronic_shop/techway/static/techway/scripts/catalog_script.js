$('.card_category').click(function(){
    let nameCategory = $(this).children('.box_text_category').children('.name_category').text();
    let select_categories = $('#select_categories');
    let section = '';
    let category = '';
    let subcategory = '';
    if (select_categories != '' && select_categories.text().split(' > ').length >= 2) section = select_categories.text().split(' > ')[1];
    if (select_categories != '' && select_categories.text().split(' > ').length >= 3) category = select_categories.text().split(' > ')[2];
    
    if (section == '') section = nameCategory;
    else if (category == '') category = nameCategory;
    else if (subcategory == '') subcategory = nameCategory;
    
    let data = `${section != '' ? '?section=' + section : ''}${category != '' ? '&category=' + category : ''}${subcategory != '' ? '&subcategory=' + subcategory : ''}`;
    window.location.href = `${window.location.href.split('?')[0]}${data}`;
});