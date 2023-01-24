$(document).on("click", '#delete-button', function() {
    let id = $(this).attr("data-pk");
    var url = $(this).attr("href");
    $parent = $(this).parents('div[data-class="product"]');
//    var wishEmpty = $(this).('#wish-empty');
//    var wishFilled = $(this).('#wish-filled');

    console.log(id);
    console.log(url);

    $.ajax({
        type: "GET",
        url: url,
        dataType: "json",
        data: {
            product_variant:id
        },

        success: function (data) {
                console.log(data['status']);
              var imgAdded = $('span#'+id).find('img').attr("data-path");
              var imgEmpty = $('span#'+id).find('img').attr("data-path-empty");

              if(data['status']=='added'){
                    $('span#'+id).find('img').attr("src",imgAdded);


              } else if(data['status']=='null'){
                       document.getElementById("SignIn").style.display = "block";
                       $('#sign-ip').css({
                            'display':'flex'
                        });
              }  else if(data['status']=='not_in_batch'){
                       var title = "Not Available";
                        var message = "Product is not available in selected pincode";
                        swal(title, message, "error");
                        console.log(data);
              }

               else {
                   $('span#'+id).find('img').attr("src",imgEmpty);
              }

        },

        error: function (data) {
            var title = "An error occurred";
            var message = "An error occurred. Please try again later.";
            swal(title, message, "error");
            console.log(data)
        }
    });
});

$(document).on("click", '.delete-button', function() {
    let pk = $(this).attr("data-pk");
    button = $('.delete-modal-button');

    button.attr('data-pk', pk);
    
});


$(document).on("click", '.delete-modal-button', function() {
    let pk = $(this).attr("data-pk");
    let url = $(this).attr("data-urlsss");

});

function delete_activity(pk,url){

    $.ajax({
        type: "GET",
        url: url+"/"+pk,
        dataType: "json",
        data: {
            pk:pk
        },

        success: function (data) {
            
            console.log("sucess")
        },

        error: function (data) {
            console.log("Errorrrr");
        }
    });
}