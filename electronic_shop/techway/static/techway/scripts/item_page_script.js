let numberImage = 0;
let oldImg, newImage;

$('#back_to_image').click(function(){
    if(numberImage == 0) return;
    numberImage--;
    oldImg = $('.all_image_item').children('img').eq(numberImage + 1);
    newImage = $('.all_image_item').children('img').eq(numberImage);
    oldImg.fadeOut(300, 'linear', function(){
        $(this).css("display", "none");
        newImage.fadeTo("fast", 1, function(){
            $(this).css("display", "block");
        });
    });
});

$('#next_to_image').click(function(){
    if(numberImage == $('.all_image_item').children('img').length - 1) return;
    numberImage++;
    oldImg = $('.all_image_item').children('img').eq(numberImage - 1);
    newImage = $('.all_image_item').children('img').eq(numberImage);
    oldImg.fadeOut(300, 'linear', function(){
        $(this).css("display", "none");
        newImage.fadeTo("fast", 1, function(){
            $(this).css("display", "block");
        });
    });
});