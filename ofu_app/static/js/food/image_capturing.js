document.addEventListener('DOMContentLoaded', add_img_class, true);

function add_img_class() {
    console.log($('.food-item'));
    $('.food-item').each(function () {
        var food_id = $(this).data('food');
        console.log("ITEM: " + $(this) + " FOOD-ID: " + food_id);
        $(this).find('.image-wrapper').addClass('img-' + food_id);
        $(this).find('.pic-upload').addClass('img-upload-' + food_id).on('change', function () {
            readURL(this)
        });
    });
}

function readURL(obj) {
    var inputClass = "img-upload-" + $(obj).attr('class').split(' ')[1].split('-')[2];
    console.log(inputClass);
    input = $('.' + inputClass)[0];
    var file = input.files[0];
    console.log(file);

    if (window.FileReader) {
        reader = new FileReader();
        reader.onloadend = function (e) {
            var picClass = "img-" + $(obj).attr('class').split(' ')[1].split('-')[2];
            showUploadedItem(e.target.result, picClass);
        };
        reader.readAsDataURL(file);
    }

}

function showUploadedItem(source, picClass) {
    console.log("Show Image: " + picClass + "  source: " + source);
    $('.' + picClass).each(function () {
        console.log(this);
        var img = this.childNodes[0];
        var placeholder = this.childNodes[1];
        console.log(img);
        $(img).attr('src', source);
        placeholder.style.display = 'none';
    });
}

function upload_image(source) {

}