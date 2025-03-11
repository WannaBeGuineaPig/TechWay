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