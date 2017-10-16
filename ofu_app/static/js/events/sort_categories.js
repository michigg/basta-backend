/**
 * Created by michigg on 16.10.17.
 */
function showCategory(category) {
    // TODO: Überarbeiten. Uni eigentlich /= Univis geht das auch schöner?
    var events = document.getElementsByClassName('event');
    for (var i = 0; i < events.length; i++) {
        events[i].style.display = 'none';
    }
    for (var i = 0; i < events.length; i++) {
        var classes = events[i].classList;
        for (var j = 0; j < classes.length; j++) {
            if (category.includes(classes[j])) {
                console.log(events[i])
                events[i].style.display = 'block';
            }
        }
    }
}