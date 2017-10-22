document.addEventListener('DOMContentLoaded', add_img_class, true);

function add_img_class() {
    console.log($('.food-item'));
    $('.food-item').each(function () {
        var food_id = $(this).data('food');
        console.log("ITEM: " + $(this) + " FOOD-ID: " + food_id);
        $(this).find('.img').addClass('img-' + food_id);
        $(this).find('.pic-upload').addClass('img-upload-' + food_id).on('change', function () {
            readURL(this)
        });
    });
}

function readURL(obj) {
    var picClass = "img-" + $(obj).attr('class').split(' ')[1].split('-')[2];
    console.log(picClass);
    input = $('.' + picClass)[0];
    var file = input.files[0];
    console.log(file);

    var reader = new FileReader();
    reader.onload = function () {
        document.getElementById('clock').style.backgroundImage = "url(" + reader.result + ")";
    }
    if (file) {
        reader.readAsDataURL(file);
    } else {
    }
}