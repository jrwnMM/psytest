$(document).ready(() => {
  htmx.config.useTemplateFragments = true;
  var $edu_level_id_select = $("#edu_levels_select");
  var $delete_edu_levels_btn = $("#delete_edu_levels_btn");
  var $delete_department_btn = $("#delete_department_btn");
  var $delete_program_btn = $("#delete_program_btn");
  var $add_department_btn = $("#add_department_btn");

  $delete_edu_levels_btn.click((e) => {
    var $checkedboxes = $("input[name='edu_level']:checked")
      .map((i, el) => el.value)
      .get();
    var $url = "/administration/organization/delete/education_levels/";
    htmx
      .ajax("POST", $url, {
        target: "#edu_levels_list_body",
        swap: "innerHTML",
        values: {
          edu_levels_id: $checkedboxes,
        },
      })
      .then(() => {
        var $elementMsg = $("#element-msg");
        $elementMsg.delay(5000).fadeOut();
      });
  });

  $delete_department_btn.click((e) => {
    var $checkedboxes = $("input[name='department']:checked")
      .map((i, el) => el.value)
      .get();
    var $url = "/administration/organization/delete/department/";
    htmx
      .ajax("POST", $url, {
        target: "#edu_level_departments",
        swap: "innerHTML",
        values: {
          department_id: $checkedboxes,
          edu_level: $edu_level_id_select.val(),
        },
      })
      .then(() => {
        var $elementMsg = $("#element-msg");
        $elementMsg.delay(5000).fadeOut();
      });
  });

  $edu_level_id_select.change(() => {
    var $url = "/administration/organization/handle_edu_levels_select/";
    htmx.ajax("GET", $url, {
      target: "#edu_level_departments",
      swap: "innerHTML",
      values: {
        edu_level_id: $edu_level_id_select.val(),
      },
    });
  });

  $add_department_btn.click(() => {
    $("#add_department_form").trigger("submit");
  });

  $("#add_department_form").submit((e) => {
    e.preventDefault();
    var $url = "/administration/organization/add_department/";
    htmx
      .ajax("POST", $url, {
        target: "#edu_level_departments",
        swap: "innerHTML",
        values: {
          edu_level: $edu_level_id_select.val(),
          name: $("#department_name").val(),
          code: $("#department_code").val(),
        },
      })
      .then(() => {
        if ($("#add_department_msg > p").text() != "Code already existed") {
          $("#add_department_form")[0].reset();
        }
        var $elementMsg = $("#add_department_msg");
        $elementMsg.delay(2000).fadeOut();
      });
  });

  $delete_program_btn.click(() => {
    var $checkedboxes = $("input[name='program']:checked")
      .map((i, el) => el.value)
      .get();
    var $url = "/administration/organization/delete/program/";
    htmx
      .ajax("POST", $url, {
        target: "#dept_prog_list",
        swap: "none",
        values: {
          program: $checkedboxes,
          dept_code: $("#dept_code").val(),
          edu_level_id: $edu_level_id_select.val(),
        },
      })
      .then(() => {
        var $elementMsg = $("#element-msg");
        $elementMsg.delay(5000).fadeOut();
      });
  });

  $("#add_yearlevel_form").submit((e)=>{
    e.preventDefault()
    console.log("submitted")
    var $url = "/administration/organization/add_yearlevel/";
    htmx
      .ajax("POST", $url, {
        target: "#yearlevels_list",
        swap: "innerHTML",
        values: {
          yearlevel_name: $("input[name='yearlevel_name']").val(),
          edu_level_id: $edu_level_id_select.val(),
        },
      })
  })

  $("#delete_yearlevel_btn").click(() => {
    var $checkedboxes = $("input[name='yearlevel']:checked")
    .map((i, el) => el.value)
    .get();
    var $url = "/administration/organization/delete/yearlevel/";
    htmx
      .ajax("POST", $url, {
        target: "#yearlevels_list",
        swap: "innerHTML",
        values: {
          checked: $checkedboxes,
          edu_level_id: $edu_level_id_select.val(),
        },
      })
  });

});
