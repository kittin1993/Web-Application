// Validating Empty Field
function check_empty() {
var emailFilter = /^([a-zA-Z0-9_.-])+@(([a-zA-Z0-9-])+.)+([a-zA-Z0-9]{2,4})+$/;
if (document.getElementById('name').value == "" || document.getElementById('email').value == "" || document.getElementById('msg').value == "") {
alert("Fill All Fields !");
}else if (!emailFilter.test(document.getElementById('email').value)) {
        alert('Please enter a valid e-mail address.');
}else {

document.getElementById('form').submit();
alert("Form Submitted Successfully...");
}
}
//Function To Display Popup
function div_show() {
document.getElementById('abc').style.display = "block";
}
//Function to Hide Popup
function div_hide(){
document.getElementById('abc').style.display = "none";
}

function validate_form() {
	var list = $( "#timeline" ).find( "li" );
    var num = list.length-7;
    console.log(num);
    var i = 0;
    for (i=0;i<num;i++){
    	if (document.getElementById('new_date'+i).value == "") {
    		alert("Please input a valid date");
    		return;
    	}
    }
    console.log("i");
    console.log(i);
    if (i===num){
    	    document.getElementById('nform').submit();
            alert("Form Submitted Successfully...");
    }

}
function validate_pform() {
    var list = $( "#timeline" ).find( "li" );
    var num = list.length-7;
    console.log(num);
    var i = 0;
    for (i=0;i<num;i++){
        if (document.getElementById('new_date'+i).value == "") {
            alert("Please input a valid date");
            return;
        }
    }
    console.log("i");
    console.log(i);
    if (i===num){
            document.getElementById('nform').submit();
            alert("Form Submitted Successfully...");
    }

}