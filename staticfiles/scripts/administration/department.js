$(document).ready(() => {
  var $addform = $("#department_add_form");

  var $url = "add/department/";
  $addform.submit((e) => {
    e.preventDefault();
    $.ajax({
      type: "POST",
      url: $url,
      data: {
        level: $("#id_level").val(),
        code: $("#id_code").val(),
        name: $("#id_name").val(),
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: handleFormSuccess,
      error: handleFormError,
    });
  });

  const handleFormSuccess = (response) => {
    location.reload();
  };
  const handleFormError = (response) => {
    data = Object.entries(response.responseJSON.form);
    data.forEach(([key, value]) => {
      $(`#${key}Errors`).html(`<li class='text-danger'>${value[0]}</li>`);
    });
  };

  var $deletebtn = $("#delete_department_btn")
  $deletebtn.click((e)=>{
      var $checkedboxes = $("input[type='checkbox']:checked").map((i, el) => el.value).get()

      $.ajax({
          type:'GET',
          url: $deletebtn.data('url'),
          data: {
              checkedboxes: $checkedboxes
          },
          success: (response)=>{
              location.reload()
          }
      })
      
  })

  
});
