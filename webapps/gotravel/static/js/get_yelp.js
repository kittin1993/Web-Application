function reload_rest(){
    $.ajax({
 
    // The URL for the request
    url: "/gotravel/get_rests_json",
 
    // Whether this is a POST or GET request
    type: "GET",
 
    // The type of data we expect back
    dataType : "json",
 
    // Code to run if the request succeeds;
    // the response is passed to the function
    success: function( json ) {
        // Removes the old to-do list items
        var list = document.getElementById("restaurant");
        while (list.hasChildNodes()) {
            list.removeChild(list.firstChild);
        }

        //console.log(json.length);
        for (var i = 0; i<json.length; i++) {
        // Extracts the item id and text from the response
        var rest_url = json[i]["url"];
        var rest_name = json[i]["name"];
        var rest_location = json[i]["location"];
        var rest_phone = json[i]["phone"];
        var rest_image = json[i]["image_url"];

        console.log(rest_name);

        var newItem1 = document.createElement("p");
        newItem1.innerHTML = "<div class=\"box1\"><a href=\""+rest_url+"\"><table><tr><th rowspan=\"3\"><img src=\""+rest_image+"\"></th><td>&nbsp;<strong>"+rest_name+"</strong></td></tr><tr><td>&nbsp;Address:"+rest_location+"</td></tr><tr><td>&nbsp;Phone Number:"+rest_phone+"</td></tr></table></a></div>";
        //p.prependTo("#post_list");
        $("#restaurant").append(newItem1);
    }
    
    },
 
    // Code to run if the request fails; the raw request and
    // status codes are passed to the function
    error: function( xhr, status, errorThrown ) {
        //alert( "Sorry, there was a problem!" );
        console.log( "Error: " + errorThrown );
        console.log( "Status: " + status );
        console.dir( xhr );
    },

});

}
function reload_hotel(){
    $.ajax({
 
    // The URL for the request
    url: "/gotravel/get_hotels_json",
 
    // Whether this is a POST or GET request
    type: "GET",
 
    // The type of data we expect back
    dataType : "json",
 
    // Code to run if the request succeeds;
    // the response is passed to the function
    success: function( json ) {
        // Removes the old to-do list items
        var list = document.getElementById("hotel");
        while (list.hasChildNodes()) {
            list.removeChild(list.firstChild);
        }

        //console.log(json.length);
        for (var i = 0; i<json.length; i++) {
        // Extracts the item id and text from the response
        var hotel_url = json[i]["url"];
        var hotel_name = json[i]["name"];
        var hotel_location = json[i]["location"];
        var hotel_phone = json[i]["phone"];
        var hotel_image = json[i]["image_url"];


        var newItem1 = document.createElement("p");
        newItem1.innerHTML = "<div class=\"box1\"><a href=\""+hotel_url+"\"><table><tr><th rowspan=\"3\"><img src=\""+hotel_image+"\"></th><td>&nbsp;<strong>"+hotel_name+"</strong></td></tr><tr><td>&nbsp;Address:"+hotel_location+"</td></tr><tr><td>&nbsp;Phone Number:"+hotel_phone+"</td></tr></table></a></div>";
        //p.prependTo("#post_list");
        $("#hotel").append(newItem1);
    }
    
    },
 
    // Code to run if the request fails; the raw request and
    // status codes are passed to the function
    error: function( xhr, status, errorThrown ) {
        //alert( "Sorry, there was a problem!" );
        console.log( "Error: " + errorThrown );
        console.log( "Status: " + status );
        console.dir( xhr );
    },

});

}

window.setInterval(reload_rest,100000);
window.setInterval(reload_hotel,100000);

function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        if (cookies[i].startsWith("csrftoken=")) {
            return cookies[i].substring("csrftoken=".length, cookies[i].length);
        }
    }
    return "unknown";
}
