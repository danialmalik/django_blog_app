// CSS Selectors
var SUBMIT_BUTTON_SELECTOR = 'button.btn-success';
var ERRORS_LIST_SELECTOR = 'ul.error';
var CUSTOM_ERRORS_LIST_SELECTOR = 'ul#custom_errors';

var USERNAME_INPUT_SELECTOR = 'input#id_username';
var FIRST_NAME_INPUT_SELECTOR = 'input#id_first_name';
var LAST_NAME_INPUT_SELECTOR = 'input#id_last_name';
var EMAIL_INPUT_SELECTOR = 'input#id_email';
var PASSWORD1_INPUT_SELECTOR = 'input#id_password1';
var PASSWORD2_INPUT_SELECTOR = 'input#id_password2';
var USER_FORM_FIELDS_SELECTOR = 'div#user_form input';
var FORM_SELECTOR = 'form';

const validateSignupForm = () => {
    var username = $(USERNAME_INPUT_SELECTOR).val();
    var first_name = $(FIRST_NAME_INPUT_SELECTOR).val();
    var last_name = $(LAST_NAME_INPUT_SELECTOR).val();
    var email = $(EMAIL_INPUT_SELECTOR).val();
    var password1 = $(PASSWORD1_INPUT_SELECTOR).val();
    var password2 = $(PASSWORD2_INPUT_SELECTOR).val();
    var isValid = true
    if(username == "") {
        addErrorToList(USERNAME_INPUT_SELECTOR, 'Username is required.');
    }

    if (!isEmail(email)) {
        addErrorToList(EMAIL_INPUT_SELECTOR, 'Enter a valid email!');
        isValid = false;
    }
    if (password1.length < 8) {
        addErrorToList(PASSWORD1_INPUT_SELECTOR, 'Password must be at least 8 characters long.')
        isValid = false;
    }
    if (password1 != password2) {
        addErrorToList(PASSWORD2_INPUT_SELECTOR, 'Passwords do not match.')
        isValid = false;
    }
    return isValid;
}

$(document).ready(function () {
    $(SUBMIT_BUTTON_SELECTOR).click(function (e) {
        $(CUSTOM_ERRORS_LIST_SELECTOR).empty();      //removing any previous errors
        $(ERRORS_LIST_SELECTOR).empty();  
        e.preventDefault();
        isValid = validateSignupForm();
        if (isValid) {
            //when sending from.  serializer accepts 'password' field. not 'password1'
            $(PASSWORD1_INPUT_SELECTOR).attr('name','password');
            $.ajax({
                type: "POST",
                url: signup_api,
                async: false,
                data: $(FORM_SELECTOR).serialize(),
                success: function (data) {
                    window.location.replace(success_redirect_url);
                },
                error: function (data) {
                    var errors = data.responseJSON;
                    displayFormErrors('input#id_', errors);
                    $(FORM_SELECTOR).prepend(makeFloatingErrorMessage('Registration Failed.'))
                    
                }
            });
        }
    })
});
