$('#select_image').change(function(event){
    file = event.target.files;
    let list_file_name = [];
    for(let i = 0; i < file.length; i++){
        if (!checkImagePath(file[i].name)){
            $(this).prop('value', '');
            list_file_name = [];
            return;
        }
        list_file_name.push(file[i].name);
    }
    list_file_name.forEach(element => {
        $('#all_images').val($.trim($('#all_images').val() + '\n' + element));
    });
});
