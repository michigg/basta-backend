/**
 * Created by michigg on 17.10.17.
 */
document.addEventListener('DOMContentLoaded', loadVGNPos);

function getPos() {
    var lat = 49.90734;
    var lon = 10.90459;
    if (navigator.geolocation) {
        var geo_option = {
            enableHighAccuracy: true
        };
        navigator.geolocation.getCurrentPosition(function (position) {
            lat = position.coords.latitude;
            lon = position.coords.longitude;
            document.getElementById('position').innerHTML = "Lat:" + pos['lat'] + " Lon: " + pos['lon']
        }, function (err) {
        }, geo_option)
    }
    return {'lat': lat, 'lon': lon};
}
function loadData(url) {
    var address = document.getElementById('nav_data').getAttribute('data-address')

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            setVGNLinks(JSON.parse(this.response))
        }
    };
    xhttp.open("GET", url, true);
    xhttp.send();
}


function getVGNCoords(lat, lon) {
    console.log("getVGNCoords: " + lat + "/" + lon)
    var url = "https://www.vgn.de/ib/site/tools/VN_PointDetail.php?Edition=de&lat=" + lat + "&lon=" + lon + "&mode=fnSetFromEFA&mode2=origin&_=1508264908632";
    loadData(url);
}

function loadVGNPos() {
    document.getElementsByTagName('body')[0].style.visibility = "hidden"
    pos = getPos()
    console.log(pos)

    getVGNCoords(pos['lat'], pos['lon'])
}

function setVGNLinks(response) {
    var type = response['ident']['type'];
    var startpoint = response['ident']['name'];
    console.log("Startpoint" + startpoint)
    var connections = document.getElementsByClassName('connection');
    var destinations = document.getElementsByClassName('destination')
    for (var i = 0; i < connections.length; i++) {
        connections[i].href = 'https://www.vgn.de/verbindungen/?to=' + startpoint + '&td=' + destinations[i].innerHTML;
        console.log(connections[i].href)
    }
    document.getElementsByTagName('body')[0].style.visibility = "visible"
}