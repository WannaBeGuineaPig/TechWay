$('#selected_all_items').click(function() {
    $('#selected_all_items_checkbox').prop('checked', !$('#selected_all_items_checkbox').prop('checked'))
    $('.item_checkbox').prop('checked', $('#selected_all_items_checkbox').prop('checked'));
});

$('#selected_all_items_checkbox').click(function() {
    $('#selected_all_items_checkbox').prop('checked', !$('#selected_all_items_checkbox').prop('checked'))
    $('.item_checkbox').prop('checked', this.checked);
});

$('.item_checkbox').click(function() {
    $.prop('checked', this.checked);
    // if (checkAllCBON()) $('#selected_all_items_checkbox').prop('checked', !$('#selected_all_items_checkbox').prop('checked'));
});

// function checkAllCBON() {
    
//     $('.item_checkbox').each(function() {
//         alert('gew');
//        if(!$(this).prop('checked')) return false; 
//     });
//     return true;
// }

function amountSummItems(){
    $('#amount_items').text($('.card_item').length)
    
    sum_items = 0.0;

    $('span.item_price_id').toArray().forEach(element => {
        sum_items += parseFloat($(element).text())
        $(element).text($(element).text());
        // $(element).text(newViewPrice($(element).text()));
    });
    // $('#sum_items').text(newViewPrice(sum_items.toString()));
    $('#sum_items').text(sum_items)
}

$(document).ready(function(){
    amountSummItems();
});

$('#ordering_form').submit(function(){
    alert('Заказ оформлен');
});

