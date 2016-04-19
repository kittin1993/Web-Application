var req;
// Sends a new request to update the to-do list
function addlike(noteid) {
    if (window.XMLHttpRequest) {
        req = new XMLHttpRequest();
    } else {
        req = new ActiveXObject("Microsoft.XMLHTTP");
    }

    var id=noteid;
    //console.log("comment_text");
    //var itemText = document.getElementById("comment_text"+id).value;
    //console.log(itemText);
    req.onreadystatechange = function() { handleResponse1(id) };
    req.open("POST", "/gotravel/addlikes/"+id, true);
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send("csrfmiddlewaretoken="+getCSRFToken());

}
// This function is called for each request readystatechange,
// and it will eventually parse the XML response for the request
function handleResponse1(id) {
    if (req.readyState != 4 || req.status != 200) {
        return;
    }
    // Removes the old to-do list items
    console.log("out")
    var likes = document.getElementById("likes");
    console.log("handleResponse");
    var item = JSON.parse(req.responseText);
    var newlikes = item["likes"];
    console.log(newlikes);
    likes.innerHTML = "<td>&nbsp;"+newlikes+"&nbsp;</td>";
}

function adddislike(noteid) {
    if (window.XMLHttpRequest) {
        req = new XMLHttpRequest();
    } else {
        req = new ActiveXObject("Microsoft.XMLHTTP");
    }

    var id=noteid;
    //console.log("comment_text");
    //var itemText = document.getElementById("comment_text"+id).value;
    //console.log(itemText);
    req.onreadystatechange = function() { handleResponse2(id) };
    req.open("POST", "/gotravel/adddislikes/"+id, true);
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send("csrfmiddlewaretoken="+getCSRFToken());

}
// This function is called for each request readystatechange,
// and it will eventually parse the XML response for the request
function handleResponse2(id) {
    if (req.readyState != 4 || req.status != 200) {
        return;
    }
    // Removes the old to-do list items
    console.log("out")
    var dislikes = document.getElementById("dislikes");
    console.log("handleResponse");
    var item = JSON.parse(req.responseText);
    var newdislikes = item["dislikes"];
    console.log(newdislikes);
    dislikes.innerHTML = "<td>&nbsp;"+newdislikes+"&nbsp;</td>";
}

function addfavorite(id) {
    if (window.XMLHttpRequest) {
        req = new XMLHttpRequest();
    } else {
        req = new ActiveXObject("Microsoft.XMLHTTP");
    }

    //console.log("comment_text");
    //var itemText = document.getElementById("comment_text"+id).value;
    //console.log(itemText);
    req.onreadystatechange = function() { handleResponse3(id) };
    req.open("POST", "/gotravel/addfavorite/"+id, true);
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send("csrfmiddlewaretoken="+getCSRFToken());

}

function handleResponse3(id) {
    if (req.readyState != 4 || req.status != 200) {
        return;
    }
    // Removes the old to-do list items
    console.log("out")
    var favorite = document.getElementById("favorites");
    console.log("handleResponse");
    var item = JSON.parse(req.responseText);
    var newfavorite = item["num"];
    console.log(newfavorite);
    favorite.innerHTML = "<td>&nbsp;"+newfavorite+"&nbsp;</td>";
}
// Sends a new request to update the to-do list
function addplike(planid) {
    if (window.XMLHttpRequest) {
        req = new XMLHttpRequest();
    } else {
        req = new ActiveXObject("Microsoft.XMLHTTP");
    }

    var id=planid;
    //console.log("comment_text");
    //var itemText = document.getElementById("comment_text"+id).value;
    //console.log(itemText);
    req.onreadystatechange = function() { handleResponse1(id) };
    req.open("POST", "/gotravel/addplikes/"+id, true);
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send("csrfmiddlewaretoken="+getCSRFToken());

}

function addpdislike(planid) {
    if (window.XMLHttpRequest) {
        req = new XMLHttpRequest();
    } else {
        req = new ActiveXObject("Microsoft.XMLHTTP");
    }

    var id=planid;
    //console.log("comment_text");
    //var itemText = document.getElementById("comment_text"+id).value;
    //console.log(itemText);
    req.onreadystatechange = function() { handleResponse2(id) };
    req.open("POST", "/gotravel/addpdislikes/"+id, true);
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send("csrfmiddlewaretoken="+getCSRFToken());

}
function addpfavorite(id) {
    if (window.XMLHttpRequest) {
        req = new XMLHttpRequest();
    } else {
        req = new ActiveXObject("Microsoft.XMLHTTP");
    }

    //console.log("comment_text");
    //var itemText = document.getElementById("comment_text"+id).value;
    //console.log(itemText);
    req.onreadystatechange = function() { handleResponse3(id) };
    req.open("POST", "/gotravel/addpfavorite/"+id, true);
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send("csrfmiddlewaretoken="+getCSRFToken());

}


function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        if (cookies[i].startsWith("csrftoken=")) {
            return cookies[i].substring("csrftoken=".length, cookies[i].length);
        }
    }
    return "unknown";
}