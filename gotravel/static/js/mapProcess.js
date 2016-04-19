function fuck() {
    alert("123");
}
var url_search_destination;

function set_Parameters(search_destination_url) {
    url_search_destination = search_destination_url;
}

var map = null;
var countyPolygons = new Array();
var State_County = new Array();
var currentStatePolygon = new google.maps.Polygon();
var polyOptions = {
  strokeColor: "#9B868B",
  fillColor: "#FF8C69",
  fillOpacity: 0.5,
  strokeWeight: 1,
  zIndex: 1
};

var stateDetailOptions = {
  strokeColor: "#9B868B",
  fillColor: "#FF8C69",
  fillOpacity: 0,
  strokeWeight: 3,
  zIndex: 1
}

function initializeMap() {
  var myOptions = {
    center: new google.maps.LatLng(38.628958, -100.785363),
    zoom: 4,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    streetViewControl: false
  };
  map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
  initialState();
}

function initialState() {
  clearCountyBoundary();
  for (var i = 0, n = USA_State.States.length; i < n; i++) {
    showBoundaryState(USA_State.States[i]);
  }
}

function clearCountyBoundary() {
  for(var i=0; i<countyPolygons.length; i++) {
    countyPolygons[i].setMap(null);
  }
}

function isFloatNumber(value) {
  return (!isNaN(value));
}

function showBoundaryState(state) {
  var paths = [];
  var latLngs = state.geometry;
  var list = latLngs.split(";");
  var latMax = -180;
  var latMin = 180;
  var lngMax = -180;
  var lngMin = 180;
  for (var i = 0; i < list.length - 1; i++) {
    latLngList = list[i].split(" ");
    for(var j = 0; j < latLngList.length; j ++) {
      var latLng = latLngList[j].split(",");
      var lat = latLng[1];
      var lng = latLng[0];
      if ((isFloatNumber(lat)) && (isFloatNumber(lng))) {
        paths.push(new google.maps.LatLng(lat, lng));
        if(parseFloat(lat) > latMax) {
          latMax = parseFloat(lat);
        }
        if(parseFloat(lat) < latMin) {
          latMin = parseFloat(lat);
        }
        if(parseFloat(lng) > lngMax) {
          lngMax = parseFloat(lng);
        }
        if(parseFloat(lng) < lngMin) {
          lngMin = parseFloat(lng);
        }
      }
    }
  }

  var polygon = new google.maps.Polygon();
  polygon.setOptions(polyOptions);
  polygon.setPaths(paths);
  polygon.setMap(map);

  google.maps.event.addListener(polygon, "mousemove", function () {
    polygon.setOptions({
      fillColor: "#FFFF00"
    });
  });

  google.maps.event.addListener(polygon, "mouseout", function () {
    polygon.setOptions({
      fillColor: "#FF8C69"
    });
  });

  google.maps.event.addListener(polygon, "click", function () {
    var stateMiddle = new google.maps.LatLng((latMax+latMin)/2, (lngMax+lngMin)/2);
    stateDetail(state, stateMiddle);
  });
}

function stateDetail(state, stateMiddle) {
  clearCountyBoundary();
  currentStatePolygon.setMap(null);
  countyPolygon = new Array();
  map.setOptions({
    center:stateMiddle,
    zoom: 7
  })
  var latLngs = state.geometry;
  var statePaths = getPath(latLngs);
  var polygon = new google.maps.Polygon();
  polygon.setOptions(stateDetailOptions);
  polygon.setPaths(statePaths);
  polygon.setMap(map);
  currentStatePolygon = polygon;
  var j=0;
  for (var i=0; i<USA_County.Counties.length; i ++) {
    if(USA_County.Counties[i].State == state.id) {
      countyPolygons[j] = showBoundaryCounty(USA_County.Counties[i]);
      j++;
    }
  }
}

function showBoundaryCounty(County) {
  var countyPath = getPath(County.geometry);
  var countyPolygon = new google.maps.Polygon();
  countyPolygon.setOptions(polyOptions);
  countyPolygon.setPaths(countyPath);
  countyPolygon.setMap(map);
  var county_state = County.State_County;
  google.maps.event.addListener(countyPolygon, "mousemove", function () {
    countyPolygon.setOptions({
      fillColor: "#FFFF00"
    });
  });

  google.maps.event.addListener(countyPolygon, "mouseout", function () {
    countyPolygon.setOptions({
      fillColor: "#FF8C69"
    });
  });

  // google.maps.event.addListener(countyPolygon[j], "click", getCountyInfo(USA_County.Counties[i]));
  google.maps.event.addListener(countyPolygon, "click", function() {
    //alert(county_state);
    addStateCounty(county_state);
  });
  return countyPolygon;
}

function addStateCounty(county_state) {
  var county = county_state.split("-")[1];
  var state = county_state.split("-")[0];
  document.getElementById("county").value = county;
  document.getElementById("state").value = state;
}

function findPlace() {
    var county = document.getElementById("county").value;
    var state = document.getElementById("state").value;
    var destination = document.getElementById("destination").value;
    var req = new XMLHttpRequest();
    //var url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="+destination+"+in+"+county+"&key=AIzaSyC5DNDex1ZhKPKyZZn2zdrkdGo4aZKgx0Q"
    //alert(url);
    var url = url_search_destination;
    req.onreadystatechange = function() {
        if (req.readyState != 4) return;
        if (req.status != 200) return;
        var destination_list = document.getElementById("add_plan_search_places");
        destination_list.innerHTML = "";
        var result = req.responseText;
        //alert(result);
        var items = JSON.parse(result)["results"];
        var items_length = items.length;
        var newItem = new Array();
        for(var i=0; i<items_length; i++) {
            var address = items[i]["formatted_address"];
            var lat = items[i]["geometry"]["location"]["lat"];
            var lng = items[i]["geometry"]["location"]["lng"];
            var icon = items[i]["icon"];
            var name = items[i]["name"];
            var html = "<div class='box1' name='list' style='width:100%' onmouseover='placesOnmouse(\""+name+"\")'>" +
                       "<div>" + name + "</div>" +
                       "<div>" + address + "</div>" +
                       "<button>Add To Plan</button>"
                       "</div>";
            newItem[i] = document.createElement("div");
            newItem[i].innerHTML = html;
            destination_list.appendChild(newItem[i]);
        }
        //var destination_places = document.getElementById("add_plan_destination");
    }
    req.open("GET", url+"/?destination=" + destination + "&county=" + county + "&state=" + state, true);
    //req.open("GET", url, true);
    //req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send();
}

function placesOnmouse(name) {
    alert(name);
}

// function getCountyInfo(County) {
//   alert(County.State);
// }

function getPath(latLngs) {
  var paths = [];
  var list = latLngs.split(";");
  for (var i = 0; i < list.length - 1; i++) {
    latLngList = list[i].split(" ");
    for(var j = 0; j < latLngList.length; j ++) {
      var latLng = latLngList[j].split(",");
      var lat = latLng[1];
      var lng = latLng[0];
      if ((isFloatNumber(lat)) && (isFloatNumber(lng))) {
        paths.push(new google.maps.LatLng(lat, lng));
      }
    }
  }
  return paths;
}

google.maps.event.addDomListener(window, "load", initializeMap);

//$(document).ready(function() {
//    $("#add_plan_search_places").hover(function(){
//        var list = $("#add_plan_search_places").children("div").children("div");
//        for(var i=0; i<list.length;i++) {
//            console.log(list[i]);
//        }
//    });
//});