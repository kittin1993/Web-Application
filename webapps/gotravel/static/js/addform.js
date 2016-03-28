function addNoteForm(Name){
	 var list = $( "#NoteForm" ).find( "table" );
     var num = list.length/2;
     var limit = 30;
     if ((num-1) == limit)  {
          alert("You have reached the limit of adding " + limit + " inputs");
     }
     else {
          var newtable = document.createElement('table'+num);
          newtable.innerHTML = "<table><tr><td>Place: </td><td><input type='text' name='place'></td></tr><tr><td>Content: </td><td><input type='text' name='content'></td></tr><tr><td>Cost: </td><td><input type='text' name='cost'></td></tr><tr><td>Time: </td><td><input type=\"date\" name='time'></td></tr></table>";
          document.getElementById(Name).appendChild(newtable);
          counter++;
     }
}

function addPlanForm(Name){
	 var list = $( "#PlanForm" ).find( "table" );
     var num = list.length/2;
     var limit = 30;
     if ((num-1) == limit)  {
          alert("You have reached the limit of adding " + limit + " inputs");
     }
     else {
          var newtable = document.createElement('table'+num);
          newtable.innerHTML = "<table><tr><td>Place: </td><td><input type='text' name='place'></td></tr><tr><td>Time: </td><td><input type='date' name='time'></td></tr><tr><td>Description: </td><td><input type='text' name='des'></td></tr></table>";
          document.getElementById(Name).appendChild(newtable);
          counter++;
     }
}