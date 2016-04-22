function addNoteForm(Name1,Name2){
	var list = $( "#timeline" ).find( "li" );
     console.log(list[0]);
     var num = list.length-7;
     console.log(num);
     var limit = 30;
     if (num == limit)  {
          alert("You have reached the limit of adding " + limit + "days");
     }
     else {
          //var newtable = document.createElement('p');
          //newtable.innerHTML = "<table><tr><td>Place: </td><td><input type='text' name='place'></td></tr><tr><td>Content: </td><td><input type='text' name='content'></td></tr><tr><td>Cost: </td><td><input type='text' name='cost'></td></tr><tr><td>Time: </td><td><input type=\"date\" name='time'></td></tr><tr><td>Upload Pictures: </td><td><input type='file' name=\"picture"+num+"\" multiple></td></tr></table>";
          //document.getElementById(Name1).appendChild(newtable);

          var newli = document.createElement('li');
          newli.className='timeline-inverted';
          newli.innerHTML = "<div class=\"timeline-badge warning\"><i class=\"glyphicon glyphicon-calendar\"></i></div><div class='timeline-panel'><div class='timeline-body'><table><tr><td>Time: </td><td><input type=\"date\" id='new_date"+num+"' name='time'></td></tr><tr><td>Place: </td><td><input type='text' id='note_item' name='place'></td></tr><tr><td>Content: </td><td><textarea id='ctt' name='content'></textarea></td></tr><tr><td>Cost: </td><td><input type='text' id='note_item' name='cost'></td></tr><tr><td>Upload Pictures: </td><td><input type='file' name=\"picture"+num+"\" multiple></td></tr></table></div></div>";
          console.log("picture"+num);
          document.getElementById('timeline').appendChild(newli);
          

          var date = new Date();
          var day = date.getDate();
          var month = date.getMonth() + 1;
          var year = date.getFullYear();
          if (month < 10) month = "0" + month;
          if (day < 10) day = "0" + day;
          var today = year + "-" + month + "-" + day;       
          document.getElementById("new_date"+num).value = today;       
          
          //var newtext = document.createElement('p'+num);
          //newtext.innerHTML = "<textarea name='comment' form='nform'>Easy! You should check out MoxieManager!</textarea>";
          //document.getElementById(Name2).appendChild(newtext); 
          //<tr><td><textarea name='comment' form='nform'></textarea></td></tr>
          
          //num++; 
               
     }
}
function deleteNoteForm(Name1,Name2){
     var list = $( "#timeline" ).find( "li" );
     var num = list.length-7;
     //console.log(num);
     var limit = 0;
     if (num == limit)  {
          alert("You are not allowed to have less than 0 days!");
     }
     else {
          //var lastchild = document.getElementById("NoteForm").lastChild;
          //newtable.innerHTML = "<table><tr><td>Place: </td><td><input type='text' name='place'></td></tr><tr><td>Content: </td><td><input type='text' name='content'></td></tr><tr><td>Cost: </td><td><input type='text' name='cost'></td></tr><tr><td>Time: </td><td><input type=\"date\" name='time'></td></tr><tr><td>Upload Pictures: </td><td><input type='file' name=\"picture"+num+"\" multiple></td></tr></table>";
          //document.getElementById("NoteForm").removeChild(lastchild);

          var lastchild = document.getElementById("timeline").lastChild;
          //newtable.innerHTML = "<table><tr><td>Place: </td><td><input type='text' name='place'></td></tr><tr><td>Content: </td><td><input type='text' name='content'></td></tr><tr><td>Cost: </td><td><input type='text' name='cost'></td></tr><tr><td>Time: </td><td><input type=\"date\" name='time'></td></tr><tr><td>Upload Pictures: </td><td><input type='file' name=\"picture"+num+"\" multiple></td></tr></table>";
          document.getElementById("timeline").removeChild(lastchild);
          
          //var newtext = document.createElement('p'+num);
          //newtext.innerHTML = "<textarea name='comment' form='nform'>Easy! You should check out MoxieManager!</textarea>";
          //document.getElementById(Name2).appendChild(newtext); 
          //<tr><td><textarea name='comment' form='nform'></textarea></td></tr>
          
          //num++; 
               
     }
}
function isFilled(Name){

    var form_name = Name;
    console.log(form_name);
    var list = $( "#PlanForm" ).find( "table" );
    var num = list.length;
    if(num==0){
      addPlanForm(form_name);
    }
    if(num>0){
      //console.log("alert");
      var stateID = "new_state" + (num - 1);
      var countyID = "new_county" + (num - 1);
      var placeID = "new_place" + (num - 1);
      var descriptionID = "new_description" + (num - 1);
      var stateValue = document.getElementById(stateID).value;
      var countyValue = document.getElementById(countyID).value;
      var placeValue = document.getElementById(placeID).value;
      var descriptionID = document.getElementById(descriptionID).value;

      if(stateValue==="" && countyValue==="" && placeValue==="") {
          console.log("alert");
          alert("Please fill in the columns of current day befor you add a new day!");
        }
        else{
          addPlanForm(form_name);
        }
    }

}

function addPlanForm(Name){
	   var list = $( "#PlanForm" ).find( "table" );
     var num = list.length;
     var limit = 30;
     if ((num) == limit)  {
          alert("You have reached the limit of adding " + limit + "days");
     }
     else {
         var hasTyped = false;
         if(num > 0) {
             var stateID = "new_state" + (num - 1);
             var countyID = "new_county" + (num - 1);
             var placeID = "new_place" + (num - 1);
             var descriptionID = "new_description" + (num - 1);
             var stateValue = document.getElementById(stateID).value;
             var countyValue = document.getElementById(countyID).value;
             var placeValue = document.getElementById(placeID).value;
             var descriptionID = document.getElementById(descriptionID).value;
             if(stateValue!=""||countyValue!="" || placeValue!="") {
                 hasTyped = true;
             }
         }
         if(num == 0 || hasTyped) {
             var newtable = document.createElement('table');
             newtable.innerHTML = "<table><tr><td>Time: </td></tr><tr><td><input type='date' id='new_date" + num + "' name='time'></td></tr><tr><td>State: </td></tr><tr><td><input type='text' id='new_state" + num + "' name='state'></td></tr><tr><td>County: </td></tr><tr><td><input type='text' id='new_county" + num + "' name='county'></td></tr><tr><td>Scenic Spot: </td></tr><tr><td><input type='text' id='new_place" + num + "' name='place'></td></tr><tr><td>Address: </td></tr><tr><td><input type='text' id='new_description" + num + "' name='des'></td></tr><tr><td>Description: </td></tr><tr><td><input type='text' id='new_cont" + num + "' name='content'></td></tr></table>";
             document.getElementById(Name).appendChild(newtable);

             var date = new Date();
             var day = date.getDate();
             var month = date.getMonth() + 1;
             var year = date.getFullYear();
             if (month < 10) month = "0" + month;
             if (day < 10) day = "0" + day;
             var today = year + "-" + month + "-" + day;
             document.getElementById("new_date" + num).value = today;
             return num;
         }
         return num - 1;
     }
}

function deletePlanForm(Name){
     var list = $( "#PlanForm" ).find( "table" );
     var num = list.length;
     console.log(num);
     var limit = 0;
     if (num == limit)  {
          alert("You are not allowed to have less than 0 days!");
     }
     else {
          var lastchild = document.getElementById("PlanForm").lastChild;
          //newtable.innerHTML = "<table><tr><td>Place: </td><td><input type='text' name='place'></td></tr><tr><td>Content: </td><td><input type='text' name='content'></td></tr><tr><td>Cost: </td><td><input type='text' name='cost'></td></tr><tr><td>Time: </td><td><input type=\"date\" name='time'></td></tr><tr><td>Upload Pictures: </td><td><input type='file' name=\"picture"+num+"\" multiple></td></tr></table>";
          document.getElementById("PlanForm").removeChild(lastchild);
          
          //var newtext = document.createElement('p'+num);
          //newtext.innerHTML = "<textarea name='comment' form='nform'>Easy! You should check out MoxieManager!</textarea>";
          //document.getElementById(Name2).appendChild(newtext); 
          //<tr><td><textarea name='comment' form='nform'></textarea></td></tr>
          
          //num++; 
               
     }
}
