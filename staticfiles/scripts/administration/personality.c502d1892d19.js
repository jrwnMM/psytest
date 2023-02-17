$(document).ready(() => {

    // Delete Question
    var $deletebtn = $("#delete_question_btn")
    $deletebtn.click((e)=>{
        var $checkedboxes = $("input[type='checkbox']:checked").map((i, el) => el.value).get()

        $.ajax({
            type:'GET',
            url: $deletebtn.data('url'),
            data: {
                checkedboxes: $checkedboxes
            },
            success: (response)=>{
                $(location).attr("href", "")
            }
        })
        
    })

    htmx.on('htmx:load', (e)=>{
        setTimeout(function () {
            $("#id_alert").fadeOut("slow")
        },2000);
    })

    htmx.on("htmx:afterSwap", (e) => {
          $(".modal").modal('hide')
      })

})