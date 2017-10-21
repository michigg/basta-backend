/**
 * Created by michigg on 20.10.17.
 */
document.addEventListener('DOMContentLoaded', rate_init);
/**
 * setup page, Add event listener
 */
function rate_init() {
    add_Stars();
    $('.star').on("mouseenter mouseleave", function () {
        showRating(this);
    }).on("click", function () {
        console.log('Click')
        sendRating(this);
    })
}

/**
 * add rating stars to each food-item
 */
function add_Stars() {
    console.log($('.food-item'));
    $('.food-item').each(function () {
        var food = $(this).data('food');
        var rating = $(this).data('rating');
        console.log("ITEM: " + $(this) + " FOOD-ID: " + food + " FOOD-RATING: " + rating);
        for (var i = 0; i < 5; i++) {
            $(this).find('.rating-wrapper').append('<i class="star-' + (i + 1) + '-' + food + ' fa fa-star-o star" aria-hidden="true"></i>');
        }
        buildRating(food, rating);
    });
}

/**
 * get user Rating
 *
 * @param obj
 * chosen rate star
 */
function showRating(obj) {
    splitted_id = $(obj).attr('class').split(' ')[0].split('-');
    console.log(splitted_id);
    var rating = splitted_id[1];
    var food_id = splitted_id[2];
    buildRating(food_id, rating);
}

/**
 * build rating-stars for given rating
 * @param food_id   food which shall be rated
 * @param rating    int or double between 1-5; count of rating-stars
 */
function buildRating(food_id, rating) {
    for (var i = 1; i < 6; i++) {
        var icon_id = '.star-' + i + '-' + food_id;
        if (i <= rating) {
            $(icon_id).removeClass('fa-star-o').addClass('fa-star');
        } else {
            $(icon_id).removeClass('fa-star').addClass('fa-star-o');
        }
    }
}

/**
 * Sends user Rating to server
 *
 * @param obj   user Rating
 */
function sendRating(obj) {
    console.log('Send');
    splitted_id = $(obj).attr('class').split(' ')[0].split('-');
    var rating = splitted_id[1];
    var food_id = splitted_id[2];

    //TODO: Better URL handling
    var url = window.location.href + "rating/";
    console.log(url);
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
        }
    };
    console.log(url + "?rating=" + rating + "&food_id=" + food_id);
    xhttp.open("GET", url + "?rating=" + rating + "&food_id=" + food_id, true);
    xhttp.send();
}