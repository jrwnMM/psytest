$(document).ready(() => {
  htmx.on("htmx:load", (e) => {
    setTimeout(function () {
      $("#id_alert").fadeOut("slow");
    }, 2000);
  });
});
