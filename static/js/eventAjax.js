$(document).ready(function () {
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
    $("#event_register_btn").click(function (e) {
        e.preventDefault()
        console.log("clicked")
        // input data
        const event_id = $("#event_id").val()

        const formData = new FormData($("#eventForm")[0]);  //include all files,csrf etc

        // console.log(formData)
        $.ajax({
            url: event_id ? `/event/admin_edit_events/${event_id}/` : `/event/admin_add_events/`,
            method: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
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
            error: function (error) {
                const errorMessage = error.responseJSON?.message || "An error occurred.";
                $("#acknowledge").text(errorMessage)
                    .css("color", "red")
                    .fadeIn().delay(2000).fadeOut();
            }



        })
    })

    // fro formsting Date
    function convertDateToInputFormat(rawDate) {
    const date = new Date(rawDate);
    if (isNaN(date)) {
        console.error("Invalid date:", rawDate);
        return "";
    }

    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, "0");
    const day = date.getDate().toString().padStart(2, "0");

    return `${year}-${month}-${day}`;
}

    // Formating time
function convertTo24Hour(timeStr) {
    // Remove dots and trim spaces, lowercase for safety
    let clean = timeStr.toLowerCase().replace(/\./g, '').trim();

    // Create date with clean time string
    const date = new Date("1970-01-01T" + clean);

    if (isNaN(date)) {
        console.error("Invalid time:", timeStr);
        return "";
    }

    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');

    return `${hours}:${minutes}`;
}



    //populate for edit
    $(document).on("click", ".edit-btn", function (event) {
        event.preventDefault()
        const event_id = $(this).data("id")
        const title = $(this).data("title")
        const description = $(this).data("description")
        const location = $(this).data("location")
        const venue = $(this).data("venue")
        const rawDate = $(this).data("date")
        const timeStr = $(this).data("time")
        const organizer = $(this).data("organizer")
        const status = $(this).data("status")
        const banner_image = $(this).data("banner")
        //  console.log(time,date)
        // let dateStr = date.toISOString().slice(0, 10); // "2025-09-06"
        //  let formattedTime = convertTo24Hour(time);
        // console.log(dateStr , formattedTime)

        // ###########333333##############  for fromting date and time
        const formattedDate = convertDateToInputFormat(rawDate); // "2025-09-07"
        // const formattedTime = convertTimeToInputFormat(rawTime); // "14:00"

      


        let formattedTime = convertTo24Hour(timeStr);
      
         console.log(formattedDate,formattedTime)

        if (formattedTime) {
            $("#myTime").val(formattedTime);
        } else {
            alert("Invalid time format.");
        }
 


        $("#event_id").val(event_id)
        $("#event_title").val(title)
        $("#event_description").val(description)
        $("#location").val(location)
        $("#selectLoc").val(location)
        $("#venue").val(venue)
        $("#myDate").val(formattedDate)
        $("#myTime").val(formattedTime)
        $("#organizer").val(organizer)
        $("#status").val(status)
       
       
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






