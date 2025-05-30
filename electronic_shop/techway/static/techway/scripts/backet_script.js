$('#selected_all_items').click(function() {
    $('#selected_all_items_checkbox').prop('checked', !$('#selected_all_items_checkbox').prop('checked'))
    $('.selected_item').prop('checked', $('#selected_all_items_checkbox').prop('checked'));
});

$('#selected_all_items_checkbox').click(function() {
    $('#selected_all_items_checkbox').prop('checked', !$('#selected_all_items_checkbox').prop('checked'))
    $('.selected_item').prop('checked', this.checked);
});

$('.selected_item').click(function() {
    $.prop('checked', this.checked);
});

function amountSummItems(){
    amount = 0;
    sum_items = 0;
    
    $('.card_item').toArray().forEach(element => {
        amount_item = parseInt($(element).children('div.info_box').children().children('.box_change_count_item').children('p').text());
        amount += amount_item;
        sum_items += parseFloat($(element).children('div.buy_favorite_price').children('p.price_item').children('span.item_price_id').text()) * amount_item;
    });
    
    $('#amount_items').text(amount)
    $('#sum_items').text(sum_items)
    if (amount == 0 && sum_items == 0) $('.link_buy').attr('disabled','disabled');
}

$(document).ready(function(){
    amountSummItems();

});

$('#ordering_form').submit(function(){
    alert('Заказ оформлен');
});

$('#selected_all_items_btn').click(function(){
    if($('.selected_item:checked').length == 0 || $('.card_item').length == 0 || !confirm("Вы точно хотите удалить товары из корзины?")) return;
    listIdProduct = '';

    $('.selected_item:checked').toArray().forEach(element => {
        listIdProduct += ($(element).parent().parent().attr('id')) + " ";
    });
    
    $.ajax({
        url : `${URLBACK}delete_item_basket/?list_id_product=${listIdProduct}`,
        type : 'GET',
        success : function(response){
            if(response.result){
                $('#box_cards_basket').replaceWith(response.render_basket_list);
                amountSummItems();
                $('#selected_all_items_checkbox').prop('checked', false);
            }
            else {
                alert(response.error);
            }
        }
    });
});

