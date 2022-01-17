function getVersion() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        document.getElementById('demoGet').innerHTML = this.responseText;
      }
    };
    xhttp.open('GET', 'version', true);
    xhttp.send();
}
