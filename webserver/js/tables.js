{{python_replace}}


// array of latitude longitude coords to add to the globe
var locations = [];
var unique_locations = [];

// get tables to add data to
table = document.getElementById("processesDataTable");
table2 = document.getElementById("processesGenericTable");
table3 = document.getElementById("processesCMDTable");

// iterate through processes_data and extract the lat, long coords
for(var i = 0; i < processes_data.length; i++){
  for(var j = 0; j < processes_data[i].length; j++){
    if(j == 7){
      // if the lat, long coords aren't blank, then include them on the globe
      if(processes_data[i][j][0] !== "" && processes_data[i][j][1] !== ""){
        locations.push(processes_data[i][j]);

        // add row to table
        var row = table.insertRow(-1);
        var cell0 = row.insertCell(0); var cell1 = row.insertCell(1);
        var cell2 = row.insertCell(2); var cell3 = row.insertCell(3);
        var cell4 = row.insertCell(4); var cell5 = row.insertCell(5);
        var cell6 = row.insertCell(6); var cell7 = row.insertCell(7);
        var cell8 = row.insertCell(8);

        cell0.innerText = processes_data[i][0];
        cell1.innerText = processes_data[i][1];
        cell2.innerText = processes_data[i][2];
        cell3.innerText = processes_data[i][3];
        cell4.innerText = processes_data[i][4];
        cell5.innerText = processes_data[i][5];
        cell6.innerText = processes_data[i][6];
        // don't show the location in the table
        cell7.innerText = processes_data[i][7];
        cell8.innerText = processes_data[i][8];
      }
    }
  }
};

//https://stackoverflow.com/questions/44014799/javascript-how-to-remove-duplicate-arrays-inside-array-of-arrays
unique_locations = locations.filter(( t={}, a=> !(t[a]=a in t) ));
updateGlobe(unique_locations);

for(var i = 0; i < processes_generic.length; i++){
  // add data to generic table
  var row = table2.insertRow(-1);
  var cell0 = row.insertCell(0); var cell1 = row.insertCell(1);
  var cell2 = row.insertCell(2); var cell3 = row.insertCell(3);
  var cell4 = row.insertCell(4); var cell5 = row.insertCell(5);
  var cell6 = row.insertCell(6); var cell7 = row.insertCell(7);

  cell0.innerText = processes_generic[i][0];
  cell1.innerText = processes_generic[i][1];
  cell2.innerText = processes_generic[i][2];
  cell3.innerText = processes_generic[i][3];
  cell4.innerText = processes_generic[i][4];
  cell5.innerText = processes_generic[i][5];
  cell6.innerText = processes_generic[i][6];
  cell7.innerText = processes_generic[i][7];

  // update table 3
  var rowCMD = table3.insertRow(-1);
  var cellCMD0 = rowCMD.insertCell(0); var cellCMD1 = rowCMD.insertCell(1);
  cellCMD0.innerText = processes_generic[i][1];
  cellCMD1.innerText = processes_generic[i][8];
}


// add filter for table
function filterProcessesData(){
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("searchProcessesDataTable");
  filter = input.value.toUpperCase();
  table = document.getElementById("processesDataTable");
  tr = table.getElementsByTagName("tr");

  // array of latitude longitude coords to add to the globe
  var locations = [];

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    // skip the header row
    if(i == 0){
      continue;
    }
    // get each columns value
    td0 = tr[i].getElementsByTagName("td")[0].innerText.toUpperCase();
    td1 = tr[i].getElementsByTagName("td")[1].innerText.toUpperCase();
    td2 = tr[i].getElementsByTagName("td")[2].innerText.toUpperCase();
    td3 = tr[i].getElementsByTagName("td")[3].innerText.toUpperCase();
    td4 = tr[i].getElementsByTagName("td")[4].innerText.toUpperCase();
    td5 = tr[i].getElementsByTagName("td")[5].innerText.toUpperCase();
    td6 = tr[i].getElementsByTagName("td")[6].innerText.toUpperCase();
    td7 = tr[i].getElementsByTagName("td")[7].innerText.toUpperCase();
    td8 = tr[i].getElementsByTagName("td")[8].innerText.toUpperCase();

    if(filter.includes("!")){
      if(td4 == filter[1] + filter[2]){
        tr[i].style.display = "none";
      }else{
        tr[i].style.display = "";
        locations.push(td7.split(","));
      }
      continue;
    }
    // if the search term is in any of the columns then show that row
    if (td0.indexOf(filter) > -1 || td1.indexOf(filter) > -1 ||
        td2.indexOf(filter) > -1 || td3.indexOf(filter) > -1 ||
        td4.indexOf(filter) > -1 || td5.indexOf(filter) > -1 ||
        td6.indexOf(filter) > -1 || td7.indexOf(filter) > -1 ||
        td8.indexOf(filter) > -1) {
      tr[i].style.display = "";
      locations.push(td7.split(","));

    } else {
      tr[i].style.display = "none";
    }
  }

  unique_locations = locations.filter(( t={}, a=> !(t[a]=a in t) ));
  // update the globe with the new ping locations
  updateGlobe(unique_locations);
}

// add filter for table
function filterProcessesGeneric(){
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("searchProcessesGenericTable");
  filter = input.value.toUpperCase();
  table = document.getElementById("processesGenericTable");
  tr = table.getElementsByTagName("tr");


  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    // skip the header row
    if(i == 0){
      continue;
    }
    // get each columns value
    td0 = tr[i].getElementsByTagName("td")[0].innerText.toUpperCase();
    td1 = tr[i].getElementsByTagName("td")[1].innerText.toUpperCase();
    td2 = tr[i].getElementsByTagName("td")[2].innerText.toUpperCase();
    td3 = tr[i].getElementsByTagName("td")[3].innerText.toUpperCase();
    td4 = tr[i].getElementsByTagName("td")[4].innerText.toUpperCase();
    td5 = tr[i].getElementsByTagName("td")[5].innerText.toUpperCase();
    td6 = tr[i].getElementsByTagName("td")[6].innerText.toUpperCase();
    td7 = tr[i].getElementsByTagName("td")[7].innerText.toUpperCase();

    // if the search term is in any of the columns then show that row
    if (td0.indexOf(filter) > -1 || td1.indexOf(filter) > -1 ||
        td2.indexOf(filter) > -1 || td3.indexOf(filter) > -1 ||
        td4.indexOf(filter) > -1 || td5.indexOf(filter) > -1 ||
        td6.indexOf(filter) > -1 || td7.indexOf(filter) > -1) {
      tr[i].style.display = "";
    } else {
      tr[i].style.display = "none";
    }
  }

}

// add filter for CMD table
function filterCMDGeneric(){
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("searchCMDTable");
  filter = input.value.toUpperCase();
  table = document.getElementById("processesCMDTable");
  tr = table.getElementsByTagName("tr");


  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    // skip the header row
    if(i == 0){
      continue;
    }
    // get each columns value
    td0 = tr[i].getElementsByTagName("td")[0].innerText.toUpperCase();
    td1 = tr[i].getElementsByTagName("td")[1].innerText.toUpperCase();

    // if the search term is in any of the columns then show that row
    if (td0.indexOf(filter) > -1 || td1.indexOf(filter) > -1) {
      tr[i].style.display = "";
    } else {
      tr[i].style.display = "none";
    }
  }
}
