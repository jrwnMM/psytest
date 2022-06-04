$(document).ready(() => {
  htmx.on("htmx:load", (e) => {
    setTimeout(function () {
      $("#career_alert").fadeOut("slow");
      $("#personality_alert").fadeOut("slow");
      $("#id_alert").fadeOut("slow");
    }, 2000);
  });

  $("#msg-form").on('submit', function(){
    $(this)[0].reset()
  })
});
