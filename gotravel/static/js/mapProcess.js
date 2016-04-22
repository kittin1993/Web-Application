var url_search_destination;

function set_Parameters(search_destination_url) {
    url_search_destination = search_destination_url;
}

var map = null;
var countyPolygons = new Array();
var State_County = new Array();
var research_destinations;
var marker = new Array();
var current_state;
var current_county;
var current_plan = new Array();
var temp_point = new google.maps.Marker();
var currentStatePolygon = new google.maps.Polygon();
var polyOptions = {
  strokeColor: "#9B868B",
  fillColor: "#FF8C69",
  fillOpacity: 0.2,
  strokeWeight: 1,
  zIndex: 1
};

var stateDetailOptions = {
  strokeColor: "#9B868B",
  fillColor: "#FF8C69",
  fillOpacity: 0.2,
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
          //fillColor: "#FFFF00",
          fillOpacity: 0
      });
  });

  google.maps.event.addListener(polygon, "mouseout", function () {
      polygon.setOptions({
          //fillColor: "#FF8C69",
          fillOpacity: 0.2
      });
  });

  google.maps.event.addListener(polygon, "click", function () {
      var stateMiddle = new google.maps.LatLng((latMax+latMin)/2, (lngMax+lngMin)/2);
      polygon.setOptions({
          fillOpacity: 0
      });
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
    polygon.setOptions({
        fillOpacity: 0
    });
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
    console.log(County.geometry.length);
    var county_boundaries = County.geometry;
    var latLngList = county_boundaries.split(" ");
    var latMax = -180;
    var latMin = 180;
    var lngMax = -180;
    var lngMin = 180;
    for(var j = 0; j < latLngList.length; j ++) {
        var latLng = latLngList[j].split(",");
        var lat = latLng[1];
        var lng = latLng[0];
        if ((isFloatNumber(lat)) && (isFloatNumber(lng))) {
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

    var countyPath = getPath(County.geometry);
    var countyPolygon = new google.maps.Polygon();
    countyPolygon.setOptions(polyOptions);
    countyPolygon.setPaths(countyPath);
    countyPolygon.setMap(map);
    var county_state = County.State_County;
    google.maps.event.addListener(countyPolygon, "mousemove", function () {
        countyPolygon.setOptions({
            fillOpacity: 0
        });
    });
    google.maps.event.addListener(countyPolygon, "mouseout", function () {
        countyPolygon.setOptions({
            fillOpacity: 0.2
        });
    });

    // google.maps.event.addListener(countyPolygon[j], "click", getCountyInfo(USA_County.Counties[i]));
    google.maps.event.addListener(countyPolygon, "click", function() {
    //alert(county_state);
        var countyMiddle = new google.maps.LatLng((latMax+latMin)/2, (lngMax+lngMin)/2);
        map.setOptions({
            center:countyMiddle,
            zoom: 10,
        })
        addStateCounty(county_state);
        });
    return countyPolygon;
}

function addStateCounty(county_state) {
  var county = county_state.split("-")[1];
  var state = county_state.split("-")[0];
  document.getElementById("county").value = county;
    current_county = county;
  document.getElementById("state").value = state;
    current_state = state;
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
        research_destinations = JSON.parse(result)["results"];
        var items_length = research_destinations.length;
        var newItem = new Array();
        for(var i=0; i<marker.length; i++) {
            marker[i].setMap(null);
        }
        marker = new Array();
        if(items_length == 0) {
            alert("There is no " + destination + " in " + county + ", " + state);
        }
        for(var i=0; i<items_length; i++) {
            var address = research_destinations[i]["formatted_address"];
            var lat = research_destinations[i]["geometry"]["location"]["lat"];
            var lng = research_destinations[i]["geometry"]["location"]["lng"];
            var icon_url = research_destinations[i]["icon"];
            var name = research_destinations[i]["name"];
            var html = "<div class='box1' name='list' style='width:100%' onmouseover='placesOnmouse("+i+")'>" +
                       "<div>" + name + "</div>" +
                       "<div>" + address + "</div>" +
                       "<button onclick='addPlan("+ i +")'>Add To Plan</button>"
                       "</div>";
            newItem[i] = document.createElement("div");
            newItem[i].innerHTML = html;
            destination_list.appendChild(newItem[i]);
            var marker_location=new google.maps.LatLng(lat,lng);
            var image = {
                url: icon_url,
                scaledSize: new google.maps.Size(15, 15)
            }
            marker[i]=new google.maps.Marker({
                position:marker_location,
                icon: image,
            });
            marker[i].setMap(map);
        }
        //var destination_places = document.getElementById("add_plan_destination");
    }
    req.open("GET", url+"/?destination=" + destination + "&county=" + county + "&state=" + state, true);
    //req.open("GET", url, true);
    //req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send();
}

function placesOnmouse(index) {
    temp_point.setMap(null);
    //console.log(index);
    //console.log(research_destinations[index]["name"])
    var address = research_destinations[index]["formatted_address"];
    var lat = research_destinations[index]["geometry"]["location"]["lat"];
    var lng = research_destinations[index]["geometry"]["location"]["lng"];
    var icon_url = research_destinations[index]["icon"];
    var name = research_destinations[index]["name"];
    var marker_location=new google.maps.LatLng(lat,lng);
    var image = {
        url: "http://maps.gstatic.com/intl/en_ALL/mapfiles/ms/micons/green-dot.png",
        scaledSize: new google.maps.Size(20, 20)
    }
    temp_point = new google.maps.Marker({
        icon: image,
        position: marker_location
    });
    temp_point.setMap(map);
    var infowindow = new google.maps.InfoWindow({
        content:"<div style='font-size:9pt;'>Name：<a target='_blank'>"+ name + "</a><br>Address: "+ address + "</></div>"
    });

    infowindow.open(map,temp_point);
    //marker[index].openInfoWindow("<div style='font-size:9pt;'>Name：<a target='_blank'>"+ name + "</a><br>Address: "+ address + "</></div>");
}

function addPlan(index) {
    var num = addPlanForm('PlanForm');
    var address = research_destinations[index]["formatted_address"];
    var lat = research_destinations[index]["geometry"]["location"]["lat"];
    var lng = research_destinations[index]["geometry"]["location"]["lng"];
    var icon_url = research_destinations[index]["icon"];
    var name = research_destinations[index]["name"];
    document.getElementById("new_description"+num).value = address;
    document.getElementById("new_place"+num).value = name;
    document.getElementById("new_county"+num).value = current_county;
    document.getElementById("new_state"+num).value = current_state;
    var marker_location=new google.maps.LatLng(lat,lng);
    current_plan[num] = new google.maps.Marker({
        position:marker_location,
        icon: "http://maps.gstatic.com/intl/en_ALL/mapfiles/ms/micons/red-dot.png"
    });
    current_plan[num].setMap(map);
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