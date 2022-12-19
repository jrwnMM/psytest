$(document).ready(() => {

  var $delete_edu_levels_btn = $("#delete_edu_levels_btn")
  $delete_edu_levels_btn.click((e)=>{
      var $checkedboxes = $("input[type='checkbox']:checked").map((i, el) => el.value).get()
      var $url = '/administration/organization/delete/education_levels/'
      htmx.ajax("POST", $url, {
        target: "#request-msg",
        swap: "innerHTML",
        values: {
            edu_levels_id: $checkedboxes,
        }
      }).then(()=>{
        var $elementMsg = $("#element-msg")
        $elementMsg.delay(5000).fadeOut()
      });
      
  })

  var $edu_levels_select = $("#edu_levels_select")
  $edu_levels_select.change(()=>{
    var $url = 'handle_edu_levels_select/'
    htmx.ajax("GET", $url, {
        target: "#edu_level_departments",
        swap: "innerHTML",
        values: {
            edu_level_id: $edu_levels_select.val(),
        }
      }).then(()=>{
        console.log("changed")
      });
  })

  var $add_department_btn = $("#add_department_btn")
  $add_department_btn.click((e)=>{
        
      var $url = '/administration/add_department/'
      htmx.ajax("POST", $url, {
        target: "#request-msg",
        swap: "innerHTML",
        values: {
            edu_levels_id: $checkedboxes,
        }
      }).then(()=>{
        var $elementMsg = $("#element-msg")
        $elementMsg.delay(5000).fadeOut()
      });
      
  })

})
