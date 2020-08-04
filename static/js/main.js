Dropzone.autoDiscover = false;
jQuery(document).ready(function() {

    if (document.getElementById('drop_gallery')) {

        var myyDropzone = new Dropzone("#drop_gallery", {
                url: window.location.href,
                params: {'csrfmiddlewaretoken': getCookie('csrftoken')},
                paramName: "dropzone_gallery",
                autoProcessQueue: false,
                addRemoveLinks: true,
                maxFilesize: 256 * 4 * 2,
                maxFiles: 5,
                acceptedFiles: 'image/*',
                uploadMultiple: true,
                parallelUploads: 5,
                removedfile: function(file) {

                    var csrftoken = getCookie('csrftoken');

                    $.ajax({
                        type: 'POST',
                        url: window.location.href,
                        headers:{
                            "X-CSRFToken": csrftoken
                        },
                        data: {
                            name: file.name,
                            request: 'delete'
                        },
                        success: function(data){
                        }
                    });

                    var _ref;
                        return (_ref = file.previewElement) != null ? _ref.parentNode.removeChild(file.previewElement) : void 0;
                  },
                init: function() {
                    var myDropzone = this

                    if (document.getElementById('edit-listing-form')) {
                        //Populate any existing thumbnails
                        if (existing_gallery) {
                            for (var i = 0; i < existing_gallery.length; i++) {

                                let mockFile = { 
                                    name: existing_gallery[i].image, 
                                    size: existing_gallery[i].image.size
                                };
                                myDropzone.displayExistingFile(mockFile, "/media/" + existing_gallery[i].image);

                            }
                            
                        }
                    }
                    
                    document.getElementById("sell-edit-submit").addEventListener("click", function(e) {
                        // Make sure that the form isn't actually being sent.
                        if (myDropzone.files.length > 0) {
                            e.preventDefault();
                            e.stopPropagation();
                            myDropzone.processQueue();
                        }
                    });

                    // this.on("success", function(data, xhr, formData) {
                    //     formData.append("removed_images", removed_gallery)
                    // });
                    // Listen to the sendingmultiple event. In this case, it's the sendingmultiple event instead
                    // of the sending event because uploadMultiple is set to true.
                    this.on("sendingmultiple", function(data, xhr, formData) {
                        // Gets triggered when the form is actually being sent.
                        // Hide the success button or the complete form.
                        formData.append("title", jQuery("#id_title").val());
                        formData.append("seller", jQuery("#id_seller").val());
                        formData.append("description", jQuery("#id_description").val());
                        formData.append("price", jQuery("#id_price").val());
                        formData.append("category", jQuery("#id_category option:selected").val());
                        formData.append("status", jQuery("#id_status").val());
                        formData.append("product", jQuery("#id_product option:selected").val());
                        // formData.append("removed_images", removed_gallery)

                        /*
                        $(":input[name]", $("form")).each(function () {     formData.append(this.name, $(':input[name=' + this.name + ']', $("form")).val());   });
                        */
                    });
                    this.on("successmultiple", function(files, response) {
                        // Gets triggered when the files have successfully been sent.
                        // Redirect user or notify of success.
                        window.location.href = '/shop/listing/' + response.listing;
                    });
                    this.on("errormultiple", function(files, response) {
                        // Gets triggered when there was an error sending the files.
                        // Maybe show form again, and notify user of error
                    });
                },
                // sending: function (file, xhr, formData) {
                //     //Along with the file, shall I append all fields from the form above in the formData?
                // }
        });
    }
});
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}