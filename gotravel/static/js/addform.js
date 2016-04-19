function addNoteForm(Name1,Name2){
	var list = $( "#timeline" ).find( "li" );
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

function addPlanForm(Name){
	var list = $( "#PlanForm" ).find( "table" );
     var num = list.length;
     console.log(num);
     var limit = 30;
     if ((num) == limit)  {
          alert("You have reached the limit of adding " + limit + "days");
     }
     else {
          var newtable = document.createElement('table');
          newtable.innerHTML = "<table><tr><td>Time: </td><td><input type='date' id='new_date"+num+"' name='time'></td></tr><tr><td>State: </td><td><input type='text' name='state'></td></tr><tr><td>County: </td><td><input type='text' name='county'></td></tr><tr><td>Place: </td><td><input type='text' name='place'></td></tr><tr><td>Description: </td><td><input type='text' name='des'></td></tr></table>";
          document.getElementById(Name).appendChild(newtable);

          var date = new Date();
          var day = date.getDate();
          var month = date.getMonth() + 1;
          var year = date.getFullYear();
          if (month < 10) month = "0" + month;
          if (day < 10) day = "0" + day;
          var today = year + "-" + month + "-" + day;       
          document.getElementById("new_date"+num).value = today;  

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
