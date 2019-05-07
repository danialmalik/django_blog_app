// CSS Selectors
var SUBMIT_BUTTON_SELECTOR = 'button.btn-primary';
var ERRORS_LIST_SELECTOR = 'ul.error';
var CUSTOM_ERRORS_LIST_SELECTOR = 'ul#custom_errors';

var USERNAME_INPUT_SELECTOR = 'input#id_username';
var NEW_PASSWORD1_INPUT_SELECTOR = 'input#id_new_password1';
var NEW_PASSWORD2_INPUT_SELECTOR = 'input#id_new_password2';
var OLD_PASSWORD_INPUT_SELECTOR = 'input#id_old_password';


var FORM_SELECTOR = 'form';


const validatePasswordChangeForm = () => {
    var old_password = $(OLD_PASSWORD_INPUT_SELECTOR).val();
    var new_password1 = $(NEW_PASSWORD1_INPUT_SELECTOR).val();
    var new_password2 = $(NEW_PASSWORD2_INPUT_SELECTOR).val();
    var isValid = true
    if (!old_password) {
        addErrorToList(OLD_PASSWORD_INPUT_SELECTOR, 'Password required.');
        isValid = false
    }
    if (new_password1.length < 8) {
        addErrorToList(NEW_PASSWORD1_INPUT_SELECTOR, 'New Password must be 8 characters long.');
        isValid = false
    }
    if (new_password1 != new_password2) {
        addErrorToList(NEW_PASSWORD2_INPUT_SELECTOR, 'Passwords do not match.');
        isValid = false
    }
    return isValid;
}

$(document).ready(function () {
    $(SUBMIT_BUTTON_SELECTOR).click(function (e) {
        $(ERRORS_LIST_SELECTOR).empty();   //removing any previous errors
        $(CUSTOM_ERRORS_LIST_SELECTOR).empty();
        e.preventDefault()
        var isValid = validatePasswordChangeForm();
        if (isValid) {
            $.ajax
                ({
                    type: "POST",
                    url: password_change_api,
                    async: false,
                    data: $(FORM_SELECTOR).serialize(),
                    success: function (data) {
                        window.location.replace(success_redirect_url);
                    },
                    error: function (data) {
                        e.preventDefault();
                        var errors = data.responseJSON;
                        displayFormErrors('input#id_', errors);

                    }
                });
        }
    })
});
