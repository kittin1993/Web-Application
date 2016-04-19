var req;
// Sends a new request to update the to-do list
function addForm(noteid) {
    if (window.XMLHttpRequest) {
        req = new XMLHttpRequest();
    } else {
        req = new ActiveXObject("Microsoft.XMLHTTP");
    }

    var id=noteid;
    //console.log("comment_text");
    //var itemText = document.getElementById("comment_text"+id).value;
    //console.log(itemText);
    req.onreadystatechange = function() { handleResponse(id) };
    req.open("POST", "/gotravel/addday/"+id, true);
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send("csrfmiddlewaretoken="+getCSRFToken());

}
// This function is called for each request readystatechange,
// and it will eventually parse the XML response for the request
function handleResponse(id) {
    if (req.readyState != 4 || req.status != 200) {
        return;
    }
    // Removes the old to-do list items
    console.log("out")
    var list = document.getElementById("dynamicForm");
    console.log("handleResponse");
    //console.log("comment_table");
    //while (list.hasChildNodes()) {
    //    list.removeChild(list.firstChild);
    //}
    // Parses the response to get a list of JavaScript objects for 
    // the items.

    /*
    var items = JSON.parse(req.responseText);
    console.log(items.length);
    for (var i = 0; i < items.length; i++) {

        // Extracts the item id and text from the response
        var id = items[i]["pk"];  // pk is "primary key", the id
        var comment_content = items[i]["fields"]["content"];
        var comment_time   = items[i]["fields"]["time"];
        var comment_author = items[i]["fields"]["author"];
        var comment_url = items[i]["fields"]["image_url"];
  
        // Builds a new HTML list item for the todo-list item
        var newItem = document.createElement("tr");
        newItem.innerHTML ="<td><img src=\""+comment_url+"\" height=\"30px\" width=\"30px\"></td><td><strong>"+comment_author+"</strong> &nbsp;&nbsp;"+comment_content+"<br>"+comment_time+"</td>"

        // Adds the todo-list item to the HTML list
        list.appendChild(newItem);
    }
    */
    var item = JSON.parse(req.responseText);
    var id = item['id'];
    var place = item['place'];
    var time = item['time'];
    var cost = item['cost'];
    var content = item['content'];
    var newtable = document.createElement('table');
    newtable.innerHTML = "<tr><td>Place: </td><td><input type=\"text\" placeholder=\"add a place\" name=\"place\"></td></tr><tr><td>Content: </td><td><input type=\"text\" name=\"content\"></td></tr><tr><td>Cost: </td><td><input type='text' name='cost'></td></tr><tr><td>Time: </td><td><input type='date' name='time'></td></tr>";
    list.appendChild(newtable);
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
