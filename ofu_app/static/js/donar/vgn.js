/**
 * Created by michigg on 17.10.17.
 */
document.addEventListener('DOMContentLoaded', loadVGNPos);

function loadVGNPos() {
    document.getElementById('vgn-links').style.visibility = "hidden";
    getPos();
}

function getPos() {
    lat = 49.90734;
    lon = 10.90459;
    if (navigator.geolocation) {
        var geo_option = {
            enableHighAccuracy: true
        };
        navigator.geolocation.getCurrentPosition(function (position) {
            getVGNCoords(position.coords.latitude, position.coords.longitude)
        }, function (err) {
            console.log(err);
            document.getElementById('err').textContent = "Leider konnte Ihre Position nicht ermittelt werden.";
        }, geo_option)
    }
}
function loadData(url) {
    console.log("LOAD DATA")
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
    console.log("getVGNCoords: " + lat + "/" + lon);
    var url = "https://www.vgn.de/ib/site/tools/VN_PointDetail.php?Edition=de&lat=" + lat + "&lon=" + lon + "&mode=fnSetFromEFA&mode2=origin&_=1508264908632";
    loadData(url);
}

function setVGNLinks(response) {
    var type = response['ident']['type'];
    var startpoint = response['ident']['name'];
    console.log("Startpoint" + startpoint);
    var connections = document.getElementsByClassName('connection');
    for (var i = 0; i < connections.length; i++) {
        connections[i].href = connections[i].href.replace('position', startpoint);
        console.log(connections[i].href)
    }
    document.getElementById('vgn-links').style.visibility = "visible"
}