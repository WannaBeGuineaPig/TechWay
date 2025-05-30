$('.delete_item').click(function(){
    if(!confirm("Вы точно хотите удалить товар из корзины?")) return;
    idItem = $(this).attr('id');
    $.ajax({
        url : `${URLBACK}delete_item_basket/?list_id_product=${[idItem]}`,
        type : 'GET',
        success : function(response){
            if(response.result){
                $('#box_cards_basket').replaceWith(response.render_basket_list);
                amountSummItems();
            }
            else {
                alert(response.error);
            }
        }
    });
});

$('.link_to_change_count').click(function(){
    textBtn = $(this).text();
    idItem = $(this).parent().attr('id');
    amount = parseInt($(this).parent().children('p').text());
    newAmount = textBtn == '+' ? amount + 1 : amount - 1;
    if(newAmount == 0) return;
    $.ajax({
        url : `${URLBACK}change_data_basket/?id_product=${idItem}&amount_item=${newAmount}&action=${textBtn}`,
        type : 'GET',
        success : function(response){
            if(response.result){
                $('#box_cards_basket').replaceWith(response.render_basket_list);
                amountSummItems();
            }
        }
    });
});