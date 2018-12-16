/* Author: Sushil Awale
    Date: March 31, 2018
*/

/* Typewriter Effect */

$(document).ready(function(){

    var i = 0;
    var txt = "Namaste! I'm Sushil, a computer science student. I am interested in Natural Language Processing."; 
    var speed = 60; /* The speed/duration of the effect in milliseconds */

    setTimeout(typeWriter, 2000); /* Initialize typewriter */

    function typeWriter(){
        
        if (i < txt.length) {
            if (txt.charAt(i) != "."){
                document.getElementById("introText").innerHTML += txt.charAt(i);
            } else {
                document.getElementById("introText").innerHTML += ".<br/>";
            }
            i++;
            setTimeout(typeWriter, speed);
        }
    }

});

/* -- */

var options = [
    {selector: '#staggered-projects', offset: 400, callback: function(el) {
      Materialize.showStaggeredList($(el));
    } },
    {selector: '#staggered-work', offset: 400, callback: function(el) {
        Materialize.showStaggeredList($(el));
      } }
  ];
  Materialize.scrollFire(options)

  $(document).ready(function(){
    $('.scrollspy').scrollSpy();
  });