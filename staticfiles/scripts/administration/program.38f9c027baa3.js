$(document).ready(() => {
  var $addform = $("#program_add_form");

  $addform.submit((e) => {
    e.preventDefault();
    $.ajax({
      type: "POST",
      url: $addform.attr("action"),
      data: {
        department: $("#id_department").val(),
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

  
  var $deletebtn = $("#delete_program_btn")
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
      });
  })
});
