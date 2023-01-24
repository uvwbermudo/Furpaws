const csrf = $('#csrf_token').val();

$('document').ready(function () {
    console.log('Ready')
    const input = document.querySelector('input[type="date"]');
    // Get today's date in the format YYYY-MM-DD
    const today = new Date().toISOString();
    // Set the minimum allowed date to be today's date
    input.min = today;
})

$("#username").keyup(function (event) {
    if (event.keyCode === 13) {
        $("#login_button").click();
    }
});

$("#user_password").keyup(function (event) {
    if (event.keyCode === 13) {
        $("#login_button").click();
    }
});

$('#add_photos').on('change', function () {
    source = this.files
    $("#add-post-preview-container").empty()

    for (let i = 0; i < source.length; i++) {
        let new_html = $(`<div id=prev${i} class="img-wrapper"></div>`)
        let new_elem = $(`<img>`)
        let new_elem_x = $(`<span id="close${i}" class="close" onclick="imgListPop(${i});">&times</span>`)
        new_html.append(new_elem_x)
        new_html.append(new_elem)
        new_url = URL.createObjectURL($(source[i])[0])
        new_elem.attr('src', new_url)
        new_elem.css("height", "300px")
        new_elem_x.css("background-color", "#fa6b6b")
        new_elem_x.css("color", "white")
        $("#add-post-preview-container").append(new_html)
    }

})

function imgListPop(index) {
    actual_index = index
    index = $(`#prev${index}`).index()
    const input = document.getElementById('add_photos')
    console.log(input.files, 1)
    const dt = new DataTransfer()
    const { files } = input
    for (let i = 0; i < files.length; i++) {
        const file = files[i]
        if (index !== i)
            dt.items.add(file) // here you exclude the file. thus removing it.
    }

    input.files = dt.files // Assign the updates list
    console.log(input.files, 2)
    $(`div#prev${actual_index}`).remove();

}

$('#add_videos').on('change', function () {
    source = this.files
    $("#add-post-preview-container2").empty()

    for (let i = 0; i < source.length; i++) {
        let new_html = $(`<div id=prev${i}2 class="img-wrapper"></div>`)
        let new_elem = $(`<video>`)
        let new_elem_x = $(`<span id="close${i}2" class="close" onclick="vidListPop(${i});">&times</span>`)
        new_html.append(new_elem_x)
        new_html.append(new_elem)
        new_url = URL.createObjectURL($(source[i])[0])
        new_elem.attr('src', new_url)
        new_elem.css("height", "150px")
        new_elem_x.css("background-color", "#fa6b6b")
        new_elem_x.css("color", "white")

        $("#add-post-preview-container2").append(new_html)
    }
})

function vidListPop(index) {
    actual_index = index
    index = $(`#prev${index}2`).index()
    const input = document.getElementById('add_videos')
    console.log(input.files, 1)
    const dt = new DataTransfer()
    const { files } = input
    for (let i = 0; i < files.length; i++) {
        const file = files[i]
        if (index !== i)
            dt.items.add(file) // here you exclude the file. thus removing it.
    }

    input.files = dt.files // Assign the updates list
    console.log(input.files, 2)
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
            email: email.trim(),
            tag: tag.trim(),
            account_type: account_type.trim(),
            password: password.trim(),
            password2: password2.trim(),
            last_name: last_name.trim(),
            first_name: first_name.trim(),
            city: city.trim(),
            state: state.trim(),
            zipcode: zipcode.trim(),
            country: country.trim(),
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
                        $('.left-side').animate({
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
        }).catch(err => {
            $('.left-side').animate({
                scrollTop: $("#email").offset().top - 100
            })
        })
}

function edit_profile(current_tag) {
    email = $('#editProfile #email').val();
    tag = $('#editProfile #tag').val();
    old_pwd = $('#editProfile #old_pwd').val();
    pwd = $('#editProfile #pwd').val();
    pwd2 = $('#editProfile #pwd2').val();
    last_name = $('#editProfile #last_name').val();
    first_name = $('#editProfile #first_name').val();
    city = $('#editProfile #city').val();
    state = $('#editProfile #state').val();
    zipcode = $('#editProfile #zipcode').val();
    country = $('#editProfile #country').val();
    var profile_pic = $('#profile_pic').get(0).files[0];
    console.log(profile_pic)
    var csrf = $('#editProfile #csrf_token').val()
    formData = new FormData();
    formData.append('email', email)
    formData.append('tag', tag)
    formData.append('old_pwd', old_pwd)
    formData.append('pwd', pwd)
    formData.append('pwd2', pwd2)
    formData.append('last_name', last_name)
    formData.append('first_name', first_name)
    formData.append('city', city)
    formData.append('state', state)
    formData.append('zipcode', zipcode)
    formData.append('country', country)
    formData.append('profile_pic', profile_pic)
    formData.append('csrf', csrf)
    console.log(formData)
    fetch(`/edit_profile/${current_tag}`, {
        method: 'POST',
        headers: {
            'X-CSRF-TOKEN': csrf,
        },
        body: formData
    })
        .then(response => {
            if (response.status == 200) {
                console.log('Success')
                window.location.href = `/profiles/${current_tag}`
            } else {
                return response.json()
            }
        }).then(function (response) {
            console.log(response)
            var scrolled = false;
            response[1].forEach(function (field) {
                form_field = $(`#editProfile #${field}`);
                form_span = form_field.next()
                form_span.html('');
                if (field in response[0]) {
                    if (!scrolled) {
                        $('#editProfile .modal-body').animate({
                            scrollTop: $(`#editProfile #${field}`).offset().top - 100
                            
                        });
                        scrolled = true;
                    }
                    form_span.html(`<span class="ms-auto float-end text-danger fade-in bounce"  style="font-size: 14px;">${response[0][field][0]} <i class="bi-exclamation-circle-fill"></i> </span>
                    `);
                    form_field.css({
                        'background-color': 'rgba(218, 49, 49, 0.13)',
                    })
                } else {
                    form_span.html(`<span class="ms-auto float-end text-success fade-in"  style="font-size: 14px;">Looks good! <i class="bi-check-circle-fill"></i> </span>
                    `);
                    form_field.css({
                        'background-color': 'rgba(6, 196, 69, 0.13)',
                    })
                }

            })
        }).catch(err => {
            $('.left-side').animate({
                scrollTop: $("#email").offset().top - 100
            })
        })
}

function change_profile(input){
    var img = $('#preview');
    img_url= URL.createObjectURL(input.files[0]);
    img.attr('src',img_url)
}

function edit_profile(current_tag) {
    email = $('#editProfile #email').val();
    tag = $('#editProfile #tag').val();
    old_pwd = $('#editProfile #old_pwd').val();
    pwd = $('#editProfile #pwd').val();
    pwd2 = $('#editProfile #pwd2').val();
    last_name = $('#editProfile #last_name').val();
    first_name = $('#editProfile #first_name').val();
    city = $('#editProfile #city').val();
    state = $('#editProfile #state').val();
    zipcode = $('#editProfile #zipcode').val();
    country = $('#editProfile #country').val();
    var profile_pic = $('#profile_pic').get(0).files[0];
    console.log(profile_pic)
    var csrf = $('#editProfile #csrf_token').val()
    formData = new FormData();
    formData.append('email', email)
    formData.append('tag', tag)
    formData.append('old_pwd', old_pwd)
    formData.append('pwd', pwd)
    formData.append('pwd2', pwd2)
    formData.append('last_name', last_name)
    formData.append('first_name', first_name)
    formData.append('city', city)
    formData.append('state', state)
    formData.append('zipcode', zipcode)
    formData.append('country', country)
    formData.append('profile_pic', profile_pic)
    formData.append('csrf', csrf)
    console.log(formData)
    fetch(`/edit_profile/${current_tag}`, {
        method: 'POST',
        headers: {
            'X-CSRF-TOKEN': csrf,
        },
        body: formData
    })
        .then(response => {
            if (response.status == 200) {
                console.log('Success')
                window.location.href = `/profiles/${current_tag}`
            } else {
                return response.json()
            }
        }).then(function (response) {
            console.log(response)
            var scrolled = false;
            response[1].forEach(function (field) {
                form_field = $(`#editProfile #${field}`);
                form_span = form_field.next()
                form_span.html('');
                if (field in response[0]) {
                    if (!scrolled) {
                        $('#editProfile .modal-body').animate({
                            scrollTop: $(`#editProfile #${field}`).offset().top - 100
                            
                        });
                        scrolled = true;
                    }
                    form_span.html(`<span class="ms-auto float-end text-danger fade-in bounce"  style="font-size: 14px;">${response[0][field][0]} <i class="bi-exclamation-circle-fill"></i> </span>
                    `);
                    form_field.css({
                        'background-color': 'rgba(218, 49, 49, 0.13)',
                    })
                } else {
                    form_span.html(`<span class="ms-auto float-end text-success fade-in"  style="font-size: 14px;">Looks good! <i class="bi-check-circle-fill"></i> </span>
                    `);
                    form_field.css({
                        'background-color': 'rgba(6, 196, 69, 0.13)',
                    })
                }

            })
        }).catch( err => {
                $('.left-side').animate({
                    scrollTop: $("#email").offset().top - 100   
            })
        })
}

function change_profile(input){
    var img = $('#preview');
    img_url= URL.createObjectURL(input.files[0]);
    img.attr('src',img_url)
}



function login_user() {
    username = $('#login #username').val();
    password = $('#login #user_password').val();
    var formdata = new FormData()
    formdata.append('password', password.trim());
    if (username.includes('@')) {
        formdata.append('email', username.trim());
    } else {
        formdata.append('tag', username.trim());
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

    if (query == "") {
        return false;
    }
    return true;
}

// START OF LIKES
function likeVisitedPost(postId) {
    var likeCount = document.getElementById(`likes-count-${postId}`);
    var likeButton = document.getElementById(`like-button-${postId}`);

    fetch(`/posts/like-post/${postId}`, { method: "POST", headers: { 'X-CSRF-TOKEN': csrf } })
        .then((res) => res.json())
        .then((data) => {
            likeCount.innerHTML = data["likes"];
            if (data["liked"] === true) {
                likeButton.className.baseVal = "post-wto-hearts-filled";
            } else {
                likeButton.className.baseVal = "post-wto-hearts";
            }

        }
        );
}

function likeVisitedPostNorm(postId) {
    var likeCount = document.getElementById(`likes-count-${postId}`);
    var likeButton = document.getElementById(`like-button-${postId}`);

    fetch(`/posts/like-post/${postId}`, { method: "POST", headers: { 'X-CSRF-TOKEN': csrf } })
        .then((res) => res.json())
        .then((data) => {
            likeCount.innerHTML = data["likes"];
            if (data["liked"] === true) {
                likeButton.className.baseVal = "post-hearts-filled";
            } else {
                likeButton.className.baseVal = "post-hearts";
            }

        }
        );
}

function likeMainFeedPost(postId) {
    var likeCount = document.getElementById(`likes-count-${postId}`);
    var likeButton = document.getElementById(`like-button-${postId}`);

    fetch(`/home/like-post/${postId}`, { method: "POST", headers: { 'X-CSRF-TOKEN': csrf } })
        .then((res) => res.json())
        .then((data) => {
            likeCount.innerHTML = data["likes"];
            if (data["liked"] === true) {
                likeButton.className.baseVal = "post-wto-hearts-filled";
            } else {
                likeButton.className.baseVal = "post-wto-hearts";
            }

        }
        );
}

function likeMainFeedPostNorm(postId) {
    var likeCount = document.getElementById(`likes-count-${postId}`);
    var likeButton = document.getElementById(`like-button-${postId}`);

    fetch(`/home/like-post/${postId}`, { method: "POST", headers: { 'X-CSRF-TOKEN': csrf } })
        .then((res) => res.json())
        .then((data) => {
            likeCount.innerHTML = data["likes"];
            if (data["liked"] === true) {
                likeButton.className.baseVal = "post-hearts-filled";
            } else {
                likeButton.className.baseVal = "post-hearts";
            }

        }
        );
}
// END OF LIKES


// START OF COMMENTS

// ADD COMMENTS
function commentVisitedPost(postId) {
    document.getElementById(`create-comment-${postId}`).addEventListener('submit',
        function (event) {
            event.preventDefault();
            var commentInput = document.getElementById(`comment_textbox${postId}`);
            const comment = commentInput.value;

            fetch(`/posts/create-comment/${postId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': `application/json`,
                    'X-CSRF-TOKEN': csrf
                },
                body: JSON.stringify(comment)
            })
                .then(function (response) {
                    return response.json();
                })
                .then(function (html) {
                    if (html['error']) {
                        console.log(" ")
                    }
                    else {
                        let newCommentContainer = $(`<div class="new-comment row p-3 bg-white border-bottom" id="comment-${html['id']}"></div>`)
                        let newCommentPfpPlaceholder = $(`<div class="col-1 p-1 text-end">profile picture</div>`)
                        let newCommentAuthorTag = $(`<div class="col-1 p-1 text-center"><a href="#">${html['author_tag']}</a> :</div>`)
                        let newCommentContent = $(`<div class="col p-1 text-start" id="comment-content-${html['id']}">${html['comment']}</div>`)
                        let newCommentDateTimeSettings = $(`<div class="col-2 p-1 text-end">
                    
                    <div class="btn-group">
                      <button type="button" style="outline:none; border:none; background-color:white;"data-bs-toggle="dropdown" aria-expanded="false">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-three-dots" viewBox="0 0 16 16">
                          <path d="M3 9.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3z"/>
                          </svg>
                      </button>
                      <ul class="dropdown-menu">
                        <li><a class="dropdown-item" data-bs-toggle="modal" data-bs-target="#editCommentModal${html['id']}">Edit</a></li>
                        <li><a class="dropdown-item" data-bs-toggle="modal" data-bs-target="#deleteCommentModal${html['id']}">Delete</a></li>
                        <li><a class="dropdown-item">Report</a></li>
                      </ul>
                    </div>
                  </div>`)

                        let new_html = `
                        <div class="comment-container">
                        <img src="../../static/img/freelancer_sample.jpg" alt="" class="circle-pfp" style="height:32px; width:32px;">
                        <a href="/profiles/${html['author_tag']}" class="text-dark text-decoration-none hover-underline fw-semibold ps-2">${html['author_tag']}</a>
                        <div class="btn-group ms-auto d-flex align-items-center">
                            <span class="text-muted fs-10 pe-2">${html['date_commented']}}</span>
                            <button type="button" style="outline:none; border:none; background-color:transparent;" data-bs-toggle="dropdown" aria-expanded="false">
                            <i class="fa-solid fa-ellipsis-vertical"></i>
                            </button>
                            <ul class="dropdown-menu">
                            <li><a class="dropdown-item" data-bs-toggle="modal" data-bs-target="#editCommentModal${html['id']}">Edit</a></li>
                            <li><a class="dropdown-item" data-bs-toggle="modal" data-bs-target="#deleteCommentsModal${html['id']}">Delete</a></li>
                            <li><a class="dropdown-item">Report</a></li>
                            </ul>
                        </div>
                        </div>
                        <p class="user-comment fs-14" id="comment-content-${html['id']}">
                        ${html['comment']}
                        </p>  
                         `
                        // newCommentContainer.append(newCommentPfpPlaceholder);
                        // newCommentContainer.append(newCommentAuthorTag);
                        // newCommentContainer.append(newCommentContent);
                        // newCommentContainer.append(newCommentDateTimeSettings);
                        document.getElementById(`main-feed-comments-${postId}`).appendChild(new_html);

                        let newDeleteModal = $(`<div class="modal fade" id="deleteCommentModal${html['id']}" tabindex="-1" role="dialog" aria-labelledby="deleteCommentModalLabel" aria-hidden="true">
                        <div class="modal-dialog" role="document">
                          <div class="modal-content">
                            <div class="modal-header">
                              <h1 class="modal-title fs-5" id="deleteCommentModalLabel">
                                Delete Comment
                              </h1>
                              <button type="button" class="btn-close" data-bs-toggle="modal" data-bs-target="#viewCommentsModal${html['commented_post']}"></button>
                            </div>
                            <div class="modal-body">
                              Are you sure you want to delete this comment?
                            </div>
                            <div class="modal-footer">
                              <button class="btn btn-secondary" data-bs-toggle="modal" data-bs-target="#viewCommentsModal${html['commented_post']}">
                                Cancel
                              </button>
                              <form id="delete-comment-${html['id']}" action="/posts/delete-comment/${html['id']}/${html['commented_post']}" method="DELETE">
                                <input type="hidden" name="csrf_token" value="${csrf}">
                                <input type="submit"  onclick="deleteCommentVisitedPost(${html['commented_post']}, ${html['id']})" class="btn btn-danger"  data-bs-toggle="modal" data-bs-target="#viewCommentsModal${html['commented_post']}" value="Delete">
                              </form>
                            </div>
                          </div>
                        </div>
                      </div>`)

                        document.body.appendChild(newDeleteModal[0]);

                        let newEditModal = $(`<div class="modal fade" id="editCommentModal${html['id']}" tabindex="-1" role="dialog" aria-labelledby="editCommentModalLabel" aria-hidden="true">
                        <div class="modal-dialog" role="document">
                          <div class="modal-content">
                            <div class="modal-header">
                              <h1 class="modal-title fs-5" id="editCommentModalLabel">
                                Edit Comment
                              </h1>
                              <button type="button" class="btn-close" data-bs-toggle="modal" data-bs-target="#viewCommentsModal${html['commented_post']}"></button>
                            </div>
                            <div class="modal-body">
                              <form id="edit-comment-${html['id']}" action="/posts/update-comment/${html['id']}/${html['commented_post']}" method="PUT">
                                <textarea class="form-control" name="edit_comment_textbox" id="editCommentTextbox${html['id']}" placeholder="${html['comment']}" required>${html['comment']}</textarea>
                                <input id="csrf_token" type="hidden" name="csrf_token" value="${csrf}">
                              <button class="submit-post"  onclick="editCommentVisitedPost(${html['commented_post']}, ${html['id']});" type="submit" data-bs-toggle="modal" data-bs-target="#viewCommentsModal${html['commented_post']}" id="edit_comment_button${html['id']}" name="edit_comment_button">Save changes</button></form>
                              <button class="btn btn-secondary mt-2" data-bs-toggle="modal" data-bs-target="#viewCommentsModal${html['commented_post']}" style="width:100%">
                                Cancel
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>`)


                        document.body.appendChild(newEditModal[0]);

                        var commentCount = document.getElementById(`comments-length-${postId}`);
                        commentCount.innerHTML = html["comments"];
                        var commentButton = document.getElementById(`comment-button-${postId}`);
                        if (commentButton.className['baseVal'] == 'post-wto-comments') {
                            commentButton.className.baseVal = 'post-wto-comments-filled'
                        } else if (commentButton.className['baseVal'] == 'post-comments') {
                            commentButton.className.baseVal = 'post-comments-filled'
                        }
                    }


                });
            commentInput.value = '';
        });
}

function commentMainFeedPost(postId) {

    document.getElementById(`create-main-feed-comment-${postId}`).addEventListener('submit',
        function (event) {
            event.preventDefault();
            var commentInput = document.getElementById(`comment_textbox${postId}`);
            const commentMainFeed = commentInput.value;

            fetch(`/home/create-comment/${postId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': `application/json`,
                    'X-CSRF-TOKEN': csrf
                },
                body: JSON.stringify(commentMainFeed)
            })
                .then(function (response) {
                    return response.json();
                })
                .then(function (html) {
                    if (html['error']) {
                        console.log(" ")
                    }
                    else {
                //         let newCommentContainer = $(`<div class="new-comment row p-3 bg-white border-bottom" id="main-feed-comment-${html['id']}"></div>`)
                //         let newCommentPfpPlaceholder = $(`<div class="col-1 p-1 text-end">profile picture</div>`)
                //         let newCommentAuthorTag = $(`<div class="col-1 p-1 text-center"><a href="#">${html['author_tag']}</a> :</div>`)
                //         let newCommentContent = $(`<div class="col p-1 text-start" id="comment-content-${html['id']}">${html['comment']}</div>`)
                //         let newCommentDateTimeSettings = $(`<div class="col-2 p-1 text-end">
                //     ${html['date_commented']}
                //     <div class="btn-group">
                //       <button type="button" style="outline:none; border:none; background-color:white;"data-bs-toggle="dropdown" aria-expanded="false">
                //         <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-three-dots" viewBox="0 0 16 16">
                //           <path d="M3 9.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3z"/>
                //           </svg>
                //       </button>
                //       <ul class="dropdown-menu">
                //         <li><a class="dropdown-item" data-bs-toggle="modal" data-bs-target="#editCommentsModal${html['id']}">Edit</a></li>
                //         <li><a class="dropdown-item" data-bs-toggle="modal" data-bs-target="#deleteCommentsModal${html['id']}">Delete</a></li>
                //         <li><a class="dropdown-item">Report</a></li>
                //       </ul>
                //     </div>
                //   </div>`)
                    let new_html = `
                        <div class="comment-container append-comment" id="main-feed-comment-${html['id']}">
                        <img src="${html['src']}" alt="" class="circle-pfp" style="height:32px; width:32px;">
                        <a href="/profiles/${html['author_tag']}" class="text-dark text-decoration-none hover-underline fw-semibold ps-2">${html['author_tag']}</a>
                        <div class="btn-group ms-auto d-flex align-items-center">
                            <span class="text-muted fs-10 pe-2">${html['date_commented']}</span>
                            <button type="button" style="outline:none; border:none; background-color:transparent;" data-bs-toggle="dropdown" aria-expanded="false">
                            <i class="fa-solid fa-ellipsis-vertical"></i>
                            </button>
                            <ul class="dropdown-menu">
                            <li><a class="dropdown-item" data-bs-toggle="modal" data-bs-target="#editCommentModal${html['id']}">Edit</a></li>
                            <li><a class="dropdown-item" data-bs-toggle="modal" data-bs-target="#deleteCommentsModal${html['id']}">Delete</a></li>
                            <li><a class="dropdown-item">Report</a></li>
                            </ul>
                        </div>
                        </div>
                        <p class="user-comment append-comment fs-14" id="comment-content-${html['id']}">
                        ${html['comment']}
                        </p>  
                         `
                        // newCommentContainer.append(newCommentPfpPlaceholder);
                        // newCommentContainer.append(newCommentAuthorTag);
                        // newCommentContainer.append(newCommentContent);
                        // newCommentContainer.append(newCommentDateTimeSettings);
                        $(`#main-feed-comments-${postId}`).append(new_html);

                        let newDeleteModal = $(`<div class="modal fade" id="deleteCommentsModal${html['id']}" tabindex="-1" role="dialog" aria-labelledby="deleteCommentModalLabel" aria-hidden="true">
                        <div class="modal-dialog" role="document">
                          <div class="modal-content">
                            <div class="modal-header">
                              <h1 class="modal-title fs-5" id="deleteCommentModalLabel">
                                Delete Comment
                              </h1>
                              <button type="button" class="btn-close" data-bs-toggle="modal" data-bs-target="#viewCommentsModal${html['commented_post']}"></button>
                            </div>
                            <div class="modal-body">
                              Are you sure you want to delete this comment?
                            </div>
                            <div class="modal-footer">
                              <button class="btn btn-secondary" data-bs-toggle="modal" data-bs-target="#viewCommentsModal${html['commented_post']}">
                                Cancel
                              </button>
                              <form id="delete-comments-${html['id']}"action="/home/delete-comment/${html['id']}/${html['commented_post']}" method="DELETE">
                                <input type="hidden" name="csrf_token" value="${csrf}">
                                <input type="submit" onclick="deleteCommentMainFeedPost(${html['commented_post']}, ${html['id']})" data-bs-toggle="modal" data-bs-target="#viewCommentsModal${html['commented_post']}" class="btn btn-danger" value="Delete">
                              </form>
                            </div>
                          </div>
                        </div>
                      </div>`)

                        document.body.appendChild(newDeleteModal[0]);


                        let newEditModal = $(`<div class="modal fade" id="editCommentsModal${html['id']}" tabindex="-1" role="dialog" aria-labelledby="editCommentModalLabel" aria-hidden="true">
                            <div class="modal-dialog" role="document">
                              <div class="modal-content">
                                <div class="modal-header">
                                  <h1 class="modal-title fs-5" id="editCommentModalLabel">
                                    Edit Comment
                                  </h1>
                                  <button type="button" class="btn-close" data-bs-toggle="modal" data-bs-target="#viewCommentsModal${html['commented_post']}"></button>
                                </div>
                                <div class="modal-body">
                                  <form id="edit-comments-${html['id']}">
                                    <textarea class="form-control" name="edit_comment_textbox" id="editCommentTextbox-${html['id']}" placeholder="${html['comment']}" required>${html['comment']}</textarea>
                                    <input type="hidden" name="csrf_token" value="${csrf}">
                                  <button class="submit-post" type="submit" data-bs-toggle="modal" data-bs-target="#viewCommentsModal${html['commented_post']}" id="edit_comment_button${html['id']}" name="edit_comment_button" onclick="editCommentMainFeedPost(${html['commented_post']}, ${html['id']});">Save changes</button></form>
                                  <button class="btn btn-secondary mt-2" data-bs-toggle="modal" data-bs-target="#viewCommentsModal${html['commented_post']}" style="width:100%">
                                    Cancel
                                  </button>
                                </div>
                              </div>
                            </div>
                          </div>`)

                        document.body.appendChild(newEditModal[0]);

                        var commentCount = document.getElementById(`mainfeed-comments-length-${postId}`);
                        commentCount.innerHTML = html["comments"];
                        var commentButton = document.getElementById(`mainfeed-comment-button-${postId}`);
                        if (commentButton.className['baseVal'] == 'post-wto-comments') {
                            commentButton.className.baseVal = 'post-wto-comments-filled'
                        } else if (commentButton.className['baseVal'] == 'post-comments') {
                            commentButton.className.baseVal = 'post-comments-filled'
                        }
                    }


                });
            commentInput.value = '';
        });
}

// END OF ADD COMMENTS


// START OF DELETE COMMENTS
function deleteCommentVisitedPost(postId, commentId) {

    document.getElementById(`delete-comment-${commentId}`).addEventListener('submit',
        function (event) {
            event.preventDefault();
            fetch(`/posts/delete-comment/${commentId}/${postId}`, {
                method: 'DELETE',
                headers: {
                    'X-CSRF-TOKEN': csrf
                }
            }).then(response => {
                if (response.ok) {
                    let commentElement = document.getElementById(`comment-${commentId}`);
                    commentElement.parentNode.removeChild(commentElement);
                    let commentModalElement = document.getElementById(`deleteCommentModal${commentId}`)
                    commentModalElement.parentNode.removeChild(commentModalElement)
                    return response.json()
                } else {
                    console.log('Error');
                }
            }).then((data) => {
                var commentCount = document.getElementById(`comments-length-${postId}`);
                var commentButton = document.getElementById(`comment-button-${postId}`);
                commentCount.innerHTML = data["comments"];
                if (data['commented'] == false) {
                    if (commentButton.className['baseVal'] == 'post-wto-comments-filled') {
                        commentButton.className.baseVal = 'post-wto-comments'
                    } else if (commentButton.className['baseVal'] == 'post-comments-filled') {
                        commentButton.className.baseVal = 'post-comments'
                    }
                }
            });
        });
}

function deleteCommentMainFeedPost(postId, commentId) {

    document.getElementById(`delete-comments-${commentId}`).addEventListener('submit',
        function (event) {
            event.preventDefault();
            fetch(`/home/delete-comment/${commentId}/${postId}`, {
                method: 'DELETE',
                headers: {
                    'X-CSRF-TOKEN': csrf
                }
            }).then(response => {
                console.log(response);
                if (response.ok) {
                    let commentElement = document.getElementById(`main-feed-comment-${commentId}`);
                    let actualComment = document.getElementById(`comment-content-${commentId}`);
                    commentElement.parentNode.removeChild(commentElement);
                    actualComment.parentNode.removeChild(actualComment);
                    let commentModalElement = document.getElementById(`deleteCommentsModal${commentId}`)
                    commentModalElement.parentNode.removeChild(commentModalElement)
                    return response.json()
                } else {
                    console.log('Error');
                }
            })
                .then((data) => {
                    var commentCount = document.getElementById(`mainfeed-comments-length-${postId}`);
                    var commentButton = document.getElementById(`mainfeed-comment-button-${postId}`);
                    commentCount.innerHTML = data["comments"];
                    if (data['commented'] == false) {
                        if (commentButton.className['baseVal'] == 'post-wto-comments-filled') {
                            commentButton.className.baseVal = 'post-wto-comments'
                        } else if (commentButton.className['baseVal'] == 'post-comments-filled') {
                            commentButton.className.baseVal = 'post-comments'
                        }
                    }
                });
        });
}

// END OF DELETE COMMENTS

// START OF EDIT COMMENTS


function editCommentVisitedPost(postId, commentId) {
    var form = document.getElementById(`edit-comment-${commentId}`);
    form.addEventListener('submit', event => {
        event.preventDefault();
        var editCommentInputVisited = document.getElementById(`editCommentTextbox${commentId}`).value
        fetch(`/posts/update-comment/${commentId}/${postId}`, {
            method: 'PUT',
            body: JSON.stringify({
                text: editCommentInputVisited
            }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': csrf
            }
        })
            .then(response => response.json())
            .then(data => {
                var visitedPostCommentElement = document.getElementById(`comment-content-${commentId}`);
                visitedPostCommentElement.innerText = data['newComment'];
                editCommentInputVisited.value = data['newComment'];
            });
    });
}

function editCommentMainFeedPost(postId, commentId) {
    var form = document.getElementById(`edit-comments-${commentId}`);
    form.addEventListener('submit', event => {
        event.preventDefault();
        var editCommentInputMainFeed = document.getElementById(`editCommentTextbox-${commentId}`).value
        fetch(`/home/update-comment/${commentId}/${postId}`, {
            method: 'PUT',
            body: JSON.stringify({
                text: editCommentInputMainFeed
            }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': csrf
            }
        })
            .then(response => response.json())
            .then(data => {
                var visitedPostCommentElement = document.getElementById(`comment-content-${commentId}`);
                visitedPostCommentElement.innerText = data['newComment'];
                editCommentInputMainFeed.value = data['newComment'];
            });
    });
}




// END OF EDIT COMMENTS
// END OF COMMENTS



function toggle_complete_job(id) {
    $(`#job-${id} .modal-footer .cancel-job`).toggleClass("hide");
    $(`#job-${id} .modal-footer .complete-span`).toggleClass("hide");
    $(`#job-${id} .modal-footer .complete-job`).toggleClass("hide");
    $(`#job-${id} .modal-footer .confirm-complete`).toggleClass("hide");
    $(`#job-${id} .modal-footer .cancel-complete`).toggleClass("hide");
}


function toggle_cancel_job(id) {
    $(`#job-${id} .modal-footer .complete-job`).toggleClass("hide");
    $(`#job-${id} .modal-footer .close`).toggleClass("hide");
    $(`#job-${id} .modal-footer .cancel-job`).toggleClass("hide");
    $(`#job-${id} .modal-footer .cancel-span`).toggleClass("hide");
    $(`#job-${id} .modal-footer .confirm-cancel`).toggleClass("hide");
    $(`#job-${id} .modal-footer .cancel-cancel`).toggleClass("hide");
}

function toggle_cancel_application(id) {
    $(`#applied-${id} .modal-footer .cancel-span`).toggleClass("hide");
    $(`#applied-${id} .modal-footer .close`).toggleClass("hide");
    $(`#applied-${id} .modal-footer .cancel-cancel`).toggleClass("hide");
    $(`#applied-${id} .modal-footer .confirm-cancel`).toggleClass("hide");
    $(`#applied-${id} .modal-footer .cancel`).toggleClass("hide");

}


function toggle_cancel_ongoing(id) {
    $(`#ongoing-${id} .modal-footer .cancel-span`).toggleClass("hide");
    $(`#ongoing-${id} .modal-footer .close`).toggleClass("hide");
    $(`#ongoing-${id} .modal-footer .cancel-cancel`).toggleClass("hide");
    $(`#ongoing-${id} .modal-footer .confirm-cancel`).toggleClass("hide");
    $(`#ongoing-${id} .modal-footer .cancel`).toggleClass("hide");
}

function editBio(id) {
    $(`#edit-detail-form .bio-form`).toggleClass("readonly");
    var isReadOnly = $(`#edit-detail-form .bio-form`).prop("readonly");
    $(`#edit-detail-form .bio-form`).prop("readonly", !isReadOnly);
    $(`#edit-detail-form .save-bio`).toggleClass("hide");
    $(`#edit-detail-form .cancel-edit-bio`).toggleClass("hide");
    $(`#edit-detail-form .edit-bio`).toggleClass("hide");
}

function toggleSiblings(elem) {
    $(elem).parents().siblings("form").toggleClass('hide')
    $(elem).toggleClass('hide')
    $(elem).siblings("button").toggleClass('hide');
    $(elem).siblings("span").toggleClass('hide');
}

function toggleButtonSiblings(elem) {
    $(elem).toggleClass('hide')
    $(elem).siblings("button").toggleClass('hide');
    $(elem).siblings("span").toggleClass('hide');

}

// function add_friend(usertag) {
//     document.getElementById(`add_friend_request${usertag}`).textContent = 'Request sent';
// }

function verifySearch(elem) {
    var filter = $(elem).val()
    var error = $('#fback-message')
    var btn = $('#startBtn')

    fetch(`/messages/search-recipients/${filter}`, {
        method: 'GET'
    })
        .then(response => {
            if (response.ok){
                console.log('Valid User')
                $(error).html('<span class="ms-auto float-end text-success fade-in "  style="font-size: 14px;">Looks good! <i class="bi-check-circle-fill"></i> </span>')
                $(elem).css({
                    'background-color': 'rgba(6, 196, 69, 0.13)',
                })
                $(btn).prop('disabled', false)
                $(btn).removeClass('btn-secondary')
                $(btn).addClass('btn-success')

            } else {
                console.log('Nonexistent User')
                $(error).html('<span class="ms-auto float-end text-danger fade-in bounce"  style="font-size: 14px;">Tag does not exist! <i class="bi-exclamation-circle-fill"></i> </span>')
                $(elem).css({
                    'background-color': 'rgba(218, 49, 49, 0.13)',
                })
                $(btn).prop('disabled', true)
                $(btn).removeClass('btn-success')
                $(btn).addClass('btn-secondary')
            }
            
        })
}


function profilePost() {
    fetch('/home', {
    method: 'POST',
    body: JSON.stringify({data: "some data"}),
    headers: { 'Content-Type': 'application/json' }
    });
    location.reload();
}