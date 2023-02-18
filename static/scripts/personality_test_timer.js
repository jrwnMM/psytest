$(document).ready(() => {
  var end = new Date().getTime() + 50 * 60 * 1000;
  var x = setInterval(function () {
    var now = new Date().getTime();
    var distance = end - now
    var hours = Math.floor(
      (distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
    );
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);
    $("#countdown").html(hours + "h " + minutes + "m " + seconds + "s ");

    if (distance < 0) {
      clearInterval(x);
      $("#countdown").html("EXPIRED");
      $("#submit_form").submit();
    }
  }, 1000);

});
