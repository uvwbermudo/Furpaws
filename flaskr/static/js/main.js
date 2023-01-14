const csrf = $('#csrf_token').val();

$('document').ready(function () {
    console.log('Ready')
    const input = document.querySelector('input[type="date"]');
    // Get today's date in the format YYYY-MM-DD
    const today = new Date().toISOString();
    // Set the minimum allowed date to be today's date
    input.min = today;
})

$("#username").keyup(function(event) {
    if (event.keyCode === 13) {
        $("#login_button").click();
    }
});

$("#user_password").keyup(function(event) {
    if (event.keyCode === 13) {
        $("#login_button").click();
    }
});

$('#add_photos').on('change', function() {
    source = this.files
    $("#add-post-preview-container").empty()
    
    for(let i=0; i<source.length; i++) {
        let new_html = $(`<div id=prev${i} class="img-wrapper"></div>`)
        let new_elem = $(`<img>`)
        let new_elem_x = $(`<span id="close${i}" class="close" onclick="imgListPop(${i});">&times</span>`)
        new_html.append(new_elem_x)
        new_html.append(new_elem)
        new_url = URL.createObjectURL($(source[i])[0])
        new_elem.attr('src', new_url)
        new_elem.css("height","300px")
        new_elem_x.css("background-color","#fa6b6b")
        new_elem_x.css("color","white")
        $("#add-post-preview-container").append(new_html)
    }
})

function imgListPop(index){
    actual_index = index
    index = $(`#prev${index}`).index()
    const input = document.getElementById('add_photos')
    console.log(input.files,1)
    const dt = new DataTransfer()
    const { files } = input
    for (let i = 0; i < files.length; i++) {
      const file = files[i]
      if (index !== i)
        dt.items.add(file) // here you exclude the file. thus removing it.
    }
    
    input.files = dt.files // Assign the updates list
    console.log(input.files,2)
    $(`div#prev${actual_index}`).remove();

}

$('#add_videos').on('change', function() {
    source = this.files
    $("#add-post-preview-container2").empty()
    
    for(let i=0; i<source.length; i++) {
        let new_html = $(`<div id=prev${i}2 class="img-wrapper"></div>`)
        let new_elem = $(`<video>`)
        let new_elem_x = $(`<span id="close${i}2" class="close" onclick="vidListPop(${i});">&times</span>`)
        new_html.append(new_elem_x)
        new_html.append(new_elem)
        new_url = URL.createObjectURL($(source[i])[0])
        new_elem.attr('src', new_url)
        new_elem.css("height","150px")
        new_elem_x.css("background-color","#fa6b6b")
        new_elem_x.css("color","white")

        $("#add-post-preview-container2").append(new_html)
    }
})

function vidListPop(index){
    actual_index = index
    index = $(`#prev${index}2`).index()
    const input = document.getElementById('add_videos')
    console.log(input.files,1)
    const dt = new DataTransfer()
    const { files } = input
    for (let i = 0; i < files.length; i++) {
      const file = files[i]
      if (index !== i)
        dt.items.add(file) // here you exclude the file. thus removing it.
    }
    
    input.files = dt.files // Assign the updates list
    console.log(input.files,2)
    $(`div#prev${actual_index}2`).remove();

}


function register_user() {
    email = $('#register #email').val();
    tag = $('#register #tag').val();
    account_type = $('#register #account_type').children("option:selected").val();
    password = $('#register #password').val();
    password2 = $('#register #password2').val();
    last_name = $('#register #last_name').val();
    first_name = $('#register #first_name').val();
    city = $('#register #city').val();
    state = $('#register #state').val();
    zipcode = $('#register #zipcode').val();
    country = $('#register #country').val();
    fetch('/verify-register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': csrf,
        },
        body: JSON.stringify({
            email: email,
            tag: tag,
            account_type: account_type,
            password: password,
            password2: password2,
            last_name: last_name,
            first_name: first_name,
            city: city,
            state: state,
            zipcode: zipcode,
            country: country,
        }),
    })
        .then(response => {
            if (response.status == 200) {
                console.log('Success')
                window.location.href = '/login'
                console.log(success_register)
            } else {
                return response.json()
            }
        }).then(function (response) {
            var scrolled = false;
            response[1].forEach(function (field) {
                form_field = $('#' + field);
                form_icon = form_field.next()
                form_span = form_field.next().next();
                form_span.html('');
                if (field in response[0]) {
                    if (!scrolled) {
                        $('html, body').animate({
                            scrollTop: $("#" + field).offset().top - 100
                        });
                        scrolled = true;
                    }

                    form_span.html(`<span class="ms-auto float-end text-danger fade-in bounce"  style="font-size: 14px;">${response[0][field][0]} <i class="bi-exclamation-circle-fill"></i> </span>
                    `);
                    form_icon.css({
                        "color": "red",
                    })
                    form_field.css({

                        'background-color': 'rgba(218, 49, 49, 0.13)',
                    })
                } else {
                    form_span.html(`<span class="ms-auto float-end text-success fade-in"  style="font-size: 14px;">Looks good! <i class="bi-check-circle-fill"></i> </span>
                    `);
                    form_icon.css({
                        "color": "green"
                    })
                    form_field.css({
                        'background-color': 'rgba(6, 196, 69, 0.13)',
                    })
                }

            })
        })
}



function login_user() {
    username = $('#login #username').val();
    password = $('#login #user_password').val();
    var formdata = new FormData()
    formdata.append('password', password);
    if (username.includes('@')) {
        formdata.append('email', username);
    } else {
        formdata.append('tag', username);
    }

    var form_data = {};
    formdata.forEach((value, key) => form_data[key] = value);
    fetch('/verify-login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': csrf,
        },
        body: JSON.stringify(form_data),
    })
        .then(response => {
            if (response.status == 200) {
                console.log('Success')
                window.location.href = '/home'
            } else {
                return response.json()
            }
        }).then(function (response) {
            console.log(response)
            response[1].forEach(function (field) {
                if ((field == 'tag') || (field == 'email')) {
                    form_field = $('#username');
                    username_error = true;
                } else if (field == 'csrf_token') {
                    return
                } else {
                    form_field = $('#user_password')
                }
                form_icon = form_field.next()
                form_span = form_field.next().next();
                form_span.html('');
                if (field in response[0]) {
                    console.log(response[0])
                    console.log(field in response[0])
                    form_span.html(`<span class="ms-auto float-end text-danger fade-in bounce"  style="font-size: 14px;">${response[0][field][0]} <i class="bi-exclamation-circle-fill"></i> </span>
                    `);
                    form_icon.css({
                        "color": "red",
                    })
                    form_field.css({

                        'background-color': 'rgba(218, 49, 49, 0.13)',
                    })
                } else {
                    if ((field == 'password') && username_error) {
                        return
                    }
                    form_span.html(`<span class="ms-auto float-end text-success fade-in"  style="font-size: 14px;">Looks good! <i class="bi-check-circle-fill"></i> </span>
                    `);
                    form_icon.css({
                        "color": "green"
                    })
                    form_field.css({
                        'background-color': 'rgba(6, 196, 69, 0.13)',
                    })
                }

            })
        })
}


// Add Post Modal
$('#addPostModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget)
    var recipient = button.data('whatever')

    var modal = $(this)
    modal.find('.modal-title').text('Create post')
    modal.find('.modal-body input').val(recipient)
})

function videoTooLargeAlert(videoDialogTextContent, videoDialogOkButton) {
    var videoUploadField = document.getElementById("add_videos");
    var videoDialogBox = $("#videoAlertBox");
    var fi = document.getElementById('add_videos');
    videoUploadField.onchange = function () {
        // Check if any file is selected.
        if (fi.files.length > 0) {
            for (var i = 0; i <= fi.files.length - 1; i++) {

                var fsize = fi.files.item(i).size;
                var file = Math.round((fsize));
                // The size of the file.
                if (file > 100097152) {
                    videoDialogBox.find(".videoAlertMessage").text(videoDialogTextContent);
                    videoDialogBox.find(".videoAlertButton").unbind().click(function () {
                        videoDialogBox.hide();
                    });
                    videoDialogBox.find(".videoAlertButton").click(videoDialogOkButton);
                    videoDialogBox.show();
                    fi.value = null;
                }
            }
        }
    }
}

function imageTooLargeAlert(imageDialogTextContent, imageDialogOkButton) {
    var imageUploadField = document.getElementById("add_photos");
    var imageDialogBox = $("#imageAlertBox");
    var fi = document.getElementById('add_photos');
    imageUploadField.onchange = function () {
        // Check if any file is selected.
        if (fi.files.length > 0) {
            for (var i = 0; i <= fi.files.length - 1; i++) {

                var fsize = fi.files.item(i).size;
                var file = Math.round((fsize));
                // The size of the file.
                if (file > 10097152) {
                    imageDialogBox.find(".imageAlertMessage").text(imageDialogTextContent);
                    imageDialogBox.find(".imageAlertButton").unbind().click(function () {
                        imageDialogBox.hide();
                    });
                    imageDialogBox.find(".imageAlertButton").click(imageDialogOkButton);
                    imageDialogBox.show();
                    fi.value = null;
                }
            }
        }
    }

}

// display button when image overflow and set button text to number of images na mi overflow
function updateButton(post_id) {
    var postId = post_id;
    var container = $(`#gallery${postId}`)
    var button = $(`#slider-button${postId}`);
    var childrenImages = container.children('img').toArray()
    var childrenVideos = container.children('video').toArray()
    childrenImages.push(...childrenVideos)

    let sizeCounter = 0;
    let overflowCount = 0;
  
    if (container[0].scrollWidth > container.width()) {
        console.log(postId, 1)

      for (let i = 0; i < childrenImages.length; i++) {
        sizeCounter += $(childrenImages[i]).width();

        if (sizeCounter > container.width()) {
          overflowCount += 1;
          button.css('display', 'block')
          container.css('justify-content', 'left')
          button.addClass('slider-button-visible')    
        }       
      }
    } else {
        console.log(postId, 2)
        button.css('display', 'none')
    }


    

    button.text('+' + overflowCount)
  }  

  
function openPage(pageUrl) {
    window.open(pageUrl);
}

function validate_search() {
    var query = $('#searchbar').val();

    if (query == ""){
        return false;
    }
    return true;
}

