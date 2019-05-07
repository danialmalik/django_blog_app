/*  
* Used in base_layout.html
*/


// CSS Selectors 
var LOGOUT_LINK_SELECTOR = 'a#logout_link';
var BODY_SELECTOR = 'body';

$(document).ready(function () {
    $(LOGOUT_LINK_SELECTOR).click(function (e) {
        e.preventDefault();
        $.ajax
            ({
                type: "POST",
                url: logout_api,
                async: false,
                success: function (data) {
                    localStorageManager.removeItem('access_token');
                    window.location.replace(home_url);
                },
                error: function (data) {
                    $(BODY_SELECTOR).prepend(makeFloatingErrorMessage('Login Failed.'))
                }
            });
    });
});
