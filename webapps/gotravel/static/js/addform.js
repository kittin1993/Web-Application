function addNoteForm(Name1,Name2){
	 var list = $( "#NoteForm" ).find( "p" );
     var num = list.length;
     console.log(num);
     var limit = 30;
     if (num == limit)  {
          alert("You have reached the limit of adding " + limit + " inputs");
     }
     else {
          var newtable = document.createElement('p');
          newtable.innerHTML = "<table><tr><td>Place: </td><td><input type='text' name='place'></td></tr><tr><td>Content: </td><td><input type='text' name='content'></td></tr><tr><td>Cost: </td><td><input type='text' name='cost'></td></tr><tr><td>Time: </td><td><input type=\"date\" name='time'></td></tr><tr><td>Upload Pictures: </td><td><input type='file' name=\"picture"+num+"\" multiple></td></tr><tr><td><textarea name='comment' form='nform'></textarea></td></tr></table>";
          document.getElementById(Name1).appendChild(newtable);
          
          //var newtext = document.createElement('p'+num);
          //newtext.innerHTML = "<textarea name='comment' form='nform'>Easy! You should check out MoxieManager!</textarea>";
          //document.getElementById(Name2).appendChild(newtext); 
          
          //num++; 
               
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