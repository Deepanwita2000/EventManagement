$(document).ready(function (){
    console.log("ajax is ready!!")

    // Image preview on file select
    $("#banner_image").on("change", function (event) {
        const file = event.target.files[0];
        const preview = $("#imagePreview");  

        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                preview.attr("src", e.target.result).show();
            };
            reader.readAsDataURL(file);
        } else {
            preview.attr("src", "").hide();
        }
    });



    //create or edit
    $("#event_register_btn").click(function(e){
        e.preventDefault()
        console.log("clicked")
        // input data
        const event_id= $("#event_id").val()
   
        const formData = new FormData($("#eventForm")[0]);  //include all files,csrf etc

        // console.log(formData)
        $.ajax({
            url : event_id? `/event/admin_edit_events/${event_id}/` : `/event/admin_add_events/`,
            method : "POST",
            data : formData,
            processData :false,
            contentType :false,
            success:function (response){
                // $("#streamForm")[0].reset();
                // $("#stream_register_btn").prop("disabled", true);

                // $("#stream_id").val("");
                // $("h3.text-primary").text("Stream Register");
                // $("#stream_register_btn").text("Save");
                $("#imagePreview").hide(); // Hide image preview after submission
                $("#acknowledge").text(response.message)
                    .css("color", "green")
                    .fadeIn().delay(2000).fadeOut();

                $("#eventList").html(response.events);

            },
            error:function(error){
                 const errorMessage = error.responseJSON?.message || "An error occurred.";
                $("#acknowledge").text(errorMessage)
                    .css("color", "red")
                    .fadeIn().delay(2000).fadeOut();
            }



        })
    })


    //populate for edit
    $(document).on("click" , ".edit-btn" , function (event){
        event.preventDefault()
        const event_id =$(this).data("id") 
        const title = $(this).data("title")
        const description = $(this).data("description")
        const location = $(this).data("location")
        const date = $(this).data("date")
        const time = $(this).data("time")
        const organizer = $(this).data("organizer")
        const status = $(this).data("status")
        const banner_image = $(this).data("banner")

        $("#event_id").val(event_id)
        $("#event_title").val(title)
        $("#event_description").val(description)
        $("#location").val(location)
        $("#selectLoc").val(location)
        $("#myDate").val(date)
        $("#myTime").val(time)
        $("#organizer").val(organizer)
        $("#status").val(status)
        $("#banner_image").val(banner_image)

         // Show image preview if exists
        if (banner_image) {
            $("#imagePreview").attr("src", banner_image).show();
        } else {
            $("#imagePreview").hide();
        }

        $("h1.text-centre").text("Edit stream")
         $("#event_register_btn").text("Update");
    })
})






//  data-title="{{ event.title }}"
//                 data-description="{{ event.description }}"
//                 data-location="{{ event.location }}"
//                 data-date="{{ event.date }}"
//                 data-time="{{ event.time }}"
//                 data-organizer="{{ event.organizer }}"
//                 {% if event.banner %}
//                     data-banner="{{ event.banner.url }}"
//                 {% else %}
//                     data-banner="" 
//                 {% endif %}    
//                 data-status="{{ event.status }}"> 
//         <i class="fas fa-pen text-primary"></i>



//   $(document).on("click", ".edit-btn", function (event) {
//         event.preventDefault();
//         const streamId = $(this).data("id");
//         const streamName = $(this).data("name");
//         const streamDescription = $(this).data("description");
//         const streamImage = $(this).data("image");

//         $("#stream_id").val(streamId);
//         $("#stream_name").val(streamName);
//         $("#stream_description").val(streamDescription);        

//         // Show image preview if exists
//         if (streamImage) {
//             $("#imagePreview").attr("src", streamImage).show();
//         } else {
//             $("#imagePreview").hide();
//         }

//         $("h3.text-primary").text("Edit Stream");
//         $("#stream_register_btn").text("Update");
//     });