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