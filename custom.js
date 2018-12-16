
/* Typewriter Effect */

$(document).ready(function(){

var i = 0;
var txt = "Namaster! I'm Sushil Awale. I'm a full-time computer science student and a part-time developer." + 
    "I am an avid reader and mostly enjoy non-fiction books."; 
var speed = 50; /* The speed/duration of the effect in milliseconds */

function typeWriter() {
  if (i < txt.length) {
    document.getElementById("demo").innerHTML += txt.charAt(i);
    i++;
    setTimeout(typeWriter, speed);
  }
}

});
/* -- */