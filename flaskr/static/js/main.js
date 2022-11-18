const csrf = $('#csrf_token').val();


$('document').ready(function() {
    console.log('Ready')
})



function register_user(){
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
                window.location.replace('/login')
            } else {
                return response.json()  
            }
        }).then(function(response){
            var scrolled = false;
            response[1].forEach(function(field){
                form_field = $('#'+field);
                form_icon = form_field.next()
                form_span = form_field.next().next();
                form_span.html('');
                if (field in response[0]){
                    if (!scrolled){
                        $('.register-section').animate({
                            scrollTop: $("#"+field).offset().top
                        }); 
                        scrolled = true;
                    }
                    
                    form_span.html(`<span class="ms-auto float-end text-danger fade-in bounce"  style="font-size: 14px;">${response[0][field][0]} <i class="bi-exclamation-circle-fill"></i> </span>
                    `);
                    form_icon.css({
                        "color": "red",
                    })
                    form_field.css ({
                        
                        'background-color': 'rgba(218, 49, 49, 0.13)',
                    })
                } else {
                    form_span.html(`<span class="ms-auto float-end text-success fade-in"  style="font-size: 14px;">Looks good! <i class="bi-check-circle-fill"></i> </span>
                    `);
                    form_icon.css({
                        "color":"green"
                    })
                    form_field.css ({
                        'background-color': 'rgba(6, 196, 69, 0.13)',
                    })
                }

            })
        })
}