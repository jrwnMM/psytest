$(document).ready(() => {
  htmx.on("htmx:afterSwap", (e) => {
    setTimeout(function () {
      $("#id_alert").fadeOut("slow");
      $("#id_alert_add_question").fadeOut("slow");
    }, 2000);
  });

  // Delete Question
  var $deletebtn = $("#delete_question_btn");
  $deletebtn.click((e) => {
    var $url = "/administration/iq/delete/question/";
    var $checkedboxes = $("input[type='checkbox'][name='del_cbox']:checked")
      .map((i, el) => el.value)
      .get();
    htmx.ajax("POST", $url, {
        target: '#questions',
        values: {
            checked: $checkedboxes,
        }
    });
  });
});
