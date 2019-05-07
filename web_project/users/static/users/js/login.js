// CSS Selectors
var SUBMIT_BUTTON_SELECTOR = 'button.btn-success';
var ERRORS_LIST_SELECTOR = 'ul.error';
var CUSTOM_ERRORS_LIST_SELECTOR = 'ul#custom_errors';

var USERNAME_INPUT_SELECTOR = 'input#id_username';
var PASSWORD_INPUT_SELECTOR = 'input#id_password';

var FORM_SELECTOR = 'form';

$(document).ready(function () {
    $(SUBMIT_BUTTON_SELECTOR).click(function (e) {
        $(ERRORS_LIST_SELECTOR).empty();   //removing any previous errors
        $(CUSTOM_ERRORS_LIST_SELECTOR).empty();
        e.preventDefault();
        var username = $(USERNAME_INPUT_SELECTOR).val();
        var password = $(PASSWORD_INPUT_SELECTOR).val();
        $.ajax
            ({
                type: "POST",
                url: login_api,
                async: false,
                data: $(FORM_SELECTOR).serialize(),
                success: function (data) {
                    if ( data.token ){
                        localStorageManager.saveItem('access_token', data.token)
                        window.location.replace(success_redirect_url);
                    } else {
                        $(FORM_SELECTOR).prepend(makeFloatingErrorMessage('Cannot get Token.'))
                    }
                    
                },
                error: function (data) {
                    var errors = data.responseJSON;
                    displayFormErrors('input#id_', errors);
                    $(FORM_SELECTOR).prepend(makeFloatingErrorMessage('Login Failed.'))
                }
            });
    });
});
