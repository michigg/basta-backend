/**
 * Created by michigg on 20.10.17.
 */
document.addEventListener('DOMContentLoaded', rate_init);

function rate_init() {
    add_Stars('feki');
    add_Stars('austr');
    add_Stars('erba');
    add_Stars('markuspl');
    $('.star').on("mouseenter mouseleave", function () {
        showRating(this);
    }).on("click", function () {
        sendRating(this);
    })
}

function add_Stars(id) {
    $('#' + id + ' .food-item').each(function () {
        console.log($(this).data('food'));
        console.log($(this).data('rating'));
        var food = $(this).data('food');
        var rating = $(this).data('rating');
        for (var i = 0; i < 5; i++) {
            $(this).find('.rating-wrapper').append('<i id="star-' + (i + 1) + '-' + id + '-' + food + '" class="fa fa-star-o star" aria-hidden="true"></i>');
        }
        buildRating(id, food, rating);
    });
}

function showRating(obj) {
    //console.log($(obj).attr('id'));
    splitted_id = $(obj).attr('id').split('-');
    var rating = splitted_id[1];
    var id = splitted_id[2];
    var food = splitted_id[3];
    buildRating(id, food, rating);
}

function buildRating(id, food, rating) {
    for (var i = 0; i < 5; i++) {
        var icon_id = '#star-' + (i + 1) + '-' + id + '-' + food;
        if (i < rating) {
            $(icon_id).removeClass('fa-star-o').addClass('fa-star');
        } else {
            $(icon_id).removeClass('fa-star').addClass('fa-star-o');
        }
    }
}

function sendRating(obj) {
    splitted_id = $(obj).attr('id').split('-');
    var rating = splitted_id[1];
    var food_id = splitted_id[3];
    //TODO: Better URL handling
    var url = window.location.href;
    console.log(url);
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
        }
    };
    xhttp.open("GET", url + "?rating=" + rating + "&food_id=" + food_id, true);
    xhttp.send();
}