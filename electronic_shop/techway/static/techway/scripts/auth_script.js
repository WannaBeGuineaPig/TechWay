let label, input;
$(window).on('load resize', updatePosition);

function updatePosition() {
    let arr_data = [['label_mail', 'login_input'], ['label_password', 'password_input']]

    arr_data.forEach(element => {
        checkPlaceHolder(element[0], element[1]);
    });
};

function checkPlaceHolder(label_id, input_id, ) {
    input = document.getElementById(input_id);
    label = document.getElementById(label_id);
    if(input.value.length != 0){
        label.style.transform = 'translate(7px, 0)';
    }
    else{
        label.style.transform = `translate(7px, ${input.offsetHeight - input.offsetHeight / 4.3}px)`;
    }
    if(label.style.display){
        label.style.removeProperty('display');
    }
};

$('#form_auth').on( "submit", function( event ) {
    $(this).css('filter', 'blur(10px)')
    event.preventDefault();
    let mail = $('#login_input').val();
    let password = $('#password_input').val();
    let currentHref = $(location).attr('href');
    const csrftoken = getCookie('csrftoken'); 
    $.ajax({
        url : `${URLAPI}auth_reg_user/?mail=${mail}&password=${password}`,
        type : 'GET',
        success : function(data){
            let data_user = data;
            $.ajax({
                url : currentHref, 
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: data_user,
                success : function(response) {
                    let accountHref = currentHref.split('/');
                    accountHref[accountHref.length - 1] = response.redirect_url
                    window.location.href = response.redirect_url;
                }
            });
        },
        error : function(data) {
            $('#error_id').text('');
            $('#form_auth').fadeTo("midle", 1, function(){
                $(this).css('filter', '');
                $('#error_id').text('Пользователь не найден!');
            });
            }
        })
    });
    