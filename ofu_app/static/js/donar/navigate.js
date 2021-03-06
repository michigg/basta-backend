/**
 * Created by michigg on 14.10.17.
 */
var endLat = '';
var endLon = '';
var startLat = 49.8955663;
var startLon = 10.886907899999999;
var accuracy = 1;
document.addEventListener('DOMContentLoaded', loadData);
document.addEventListener('DOMContentLoaded', resizeMap);
document.addEventListener('DOMContentLoaded', getPos);


window.onresize = resizeMap;

function loadData() {
    var address = document.getElementById('nav_data').getAttribute('data-address')

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            generateMap(JSON.parse(this.response))
        }
    };
    xhttp.open("GET", "https://nominatim.openstreetmap.org/search/?format=json&city=Bamberg&street=" + address, true);
    xhttp.send();
}


function generateMap(streets) {
    var address = document.getElementById('nav_data').getAttribute('data-address');
    var address_short = document.getElementById('nav_data').getAttribute('data-short');
    var zoomlevel = 13.5;
    console.log(streets);
    if (streets.length > 0) {
        endLon = streets[0]['lon'];
        endLat = streets[0]['lat'];
        var map = L.map('map').setView([endLat, endLon], zoomlevel);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        L.marker([endLat, endLon]).addTo(map)
            .bindPopup(address_short + '</br>' + address)
            .openPopup();
        L.marker([startLat, startLon]).addTo(map)
            .bindPopup('You are here!')
            .openPopup();
        L.circle([startLat, startLon], {
            color: '#6b6b6b',
            fillColor: '#6b6b6b',
            fillOpacity: 0.4,
            radius: accuracy
        }).addTo(map);
    }

}

function resizeMap() {
    var height = window.innerHeight
    document.getElementById('map').style.height = height + 'px'
}

/**
 * save current position in global vars
 */
function getPos() {
    if (navigator.geolocation) {
        var geo_option = {
            enableHighAccuracy: true
        };
        navigator.geolocation.getCurrentPosition(function (position) {
            console.log(position);
            startLat = position.coords.latitude;
            startLon = position.coords.longitude;
            accuracy = position.coords.accuracy;
            console.log('Lat: ' + startLat + ' Lon: ' + startLon + ' Acc: ' + accuracy)
        }, function (err) {
            console.log(err.code);
            console.log(err.message);
        }, geo_option)
    } else {
        document.getElementById('map').innerHTML('Geolocation not available')
    }
}

function makeRoute() {
    console.log('make route')
    console.log('set waypoints:\nStart: ' + startLat + '  Lo: ' + startLon + " \nEnd: " + endLat + '  Lo: ' + endLon)
    L.Routing.control({
        waypoints: [
            L.latLng(startLat, startLon),
            L.latLng(endLat, endLon)
        ]
    }).addTo(map);
}