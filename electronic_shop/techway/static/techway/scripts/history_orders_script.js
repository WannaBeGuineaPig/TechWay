$('.download_check_btn').click(function(){
    $('.download_check_btn').attr('disabled', 'disabled');
    let row = $(this).parent().parent().children();
    let idOrder= $(row[0]).text();
    let addressShop= $(row[1]).text();
    let paymentMethod= $(row[2]).text();
    let dateOrdering= $(row[3]).text();
    const csrftoken = getCookie('csrftoken');
    $.ajax({
        url : `${URLBACK}create_check_history_order/`,
        type : 'POST',
        headers: {'X-CSRFToken': csrftoken},
        data : {
            'id_order' : idOrder,
            'address_shop' : addressShop,
            'payment_method' : paymentMethod,
            'date_ordering' : dateOrdering,
        },
        complete : function(data){
            const dataUri = `data:application/pdf;base64,${data['responseJSON']['pdf_data']}`;
            const link = document.createElement('a');
            link.href = dataUri;
            link.download = 'check.pdf';
            link.click();
            $('.download_check_btn').removeAttr('disabled', 'disabled');
        }
    });
});