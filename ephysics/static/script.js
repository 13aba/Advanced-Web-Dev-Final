//Referenced from https://stackoverflow.com/questions/43821938/search-div-for-text
function search() {
    var input = document.getElementById("search");
    var filter = input.value.toLowerCase();
    var nodes = document.getElementsByClassName('card-container');
  
    for (i = 0; i < nodes.length; i++) {
      if (nodes[i].innerText.toLowerCase().includes(filter)) {
        nodes[i].style.display = "block";
      } else {
        nodes[i].style.display = "none";
      }
    }
  }