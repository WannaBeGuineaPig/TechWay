let label, input;
$(window).on('load resize', updatePosition);

function updatePosition() {
    let arr_data = [['label_mail', 'login_input'], ['label_password', 'password_input'], ['label_password_confirm', 'password_confirm_input'], ['label_last_name', 'last_name_input'], ['label_first_name', 'first_name_input']]

    arr_data.forEach(element => {
        checkPlaceHolder(element[0], element[1]);
    });
}

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
