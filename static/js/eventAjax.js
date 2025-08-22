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




    $("#event_register_btn").click(function(e){
        e.preventDefault()
        console.log("clicked")
        // input data
        const eventID= $("#event_id").val()
        // title= $("#event_title").val()
        // description= $("#event_description").val()
        // banner= $("#myDate").val()
        // location= $("#myDate").val()
        // myDate= $("#myDate").val()
        // myTime= $("#myTime").val()
        // myDate= $("#organizer").val()
        const formData = new FormData($("#eventForm")[0]);

        // console.log(formData)
        $.ajax({
            url : eventID? `/event/edit/${eventID}` : `/event/add/`,
            method : "POST",
            data : formData,
            processData :false,
            contentType :false,


        })
    })
})