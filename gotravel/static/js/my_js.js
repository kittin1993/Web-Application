// Validating Empty Field
function check_empty() {
var emailfilter = /^([a-zA-Z0-9_.-])+@(([a-zA-Z0-9-])+.)+([a-zA-Z0-9]{2,4})+$/;
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
    var datefilter = /^((((19|[2-9]\d)\d{2})\-(0[13578]|1[02])\-(0[1-9]|[12]\d|3[01]))|(((19|[2-9]\d)\d{2})\-(0[13456789]|1[012])\-(0[1-9]|[12]\d|30))|(((19|[2-9]\d)\d{2})\-02\-(0[1-9]|1\d|2[0-8]))|(((1[6-9]|[2-9]\d)(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00))\-02\-29))$/;
	var list = $( "#timeline" ).find( "li" );
    var num = list.length-2;
    console.log(num);
    var i = 0;
    for (i=0;i<num;i++){
    	if (!datefilter.test(document.getElementById('new_date'+i).value)) {
    		alert("The valid time format should be yyyy-mm-dd!");
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
    var datefilter = /^((((19|[2-9]\d)\d{2})\-(0[13578]|1[02])\-(0[1-9]|[12]\d|3[01]))|(((19|[2-9]\d)\d{2})\-(0[13456789]|1[012])\-(0[1-9]|[12]\d|30))|(((19|[2-9]\d)\d{2})\-02\-(0[1-9]|1\d|2[0-8]))|(((1[6-9]|[2-9]\d)(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00))\-02\-29))$/;
    if (!datefilter.test(document.getElementById('new_date').value)){
       alert("The valid time format should be yyyy-mm-dd!");
    }
    else{
        document.getElementById('searchpform').submit();
        alert("Form Submitted Successfully...");
    }

}