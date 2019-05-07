// All CSS selectors :-
var CUSTOM_ERRORS_LIST_SELECTOR = 'ul#custom_errors';


// global object for managing local storage
const localStorageManager = new LocalSorageManager();

const isEmail = (email) => {
    var regex = /^([a-zA-Z0-9][_.+-]?)+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    return regex.test(email);
}


const makeErrorMessage = (message) => {
    // makes a list element for given error message

    var error_message = '<li><span style="color:red">' + message + '</span></li>';
    return error_message;
}


const addErrorToList = (key, message) => {
    /* adds error list element to ul which is sibling to provided "key" element
    * e.g addErrorToList('input#email','invalid email') will add error to list after email input
    */
    var error_message = makeErrorMessage(message);
    $(key + ' ~ ul').append(error_message);
}


const makeFloatingErrorMessage = (message) => {
    errorMessage = `<div class="alert alert-danger alert-dismissible">
                        <button type="button" class="close" data-dismiss="alert">&times;</button>
                        <strong>--> </strong> ${message}
                    </div>`
    return errorMessage
}

const makeFloatingSuccessMessage = (message) => {
    successMessage = `<div class="alert alert-success alert-dismissible">
                        <button type="button" class="close" data-dismiss="alert">&times;</button>
                        <strong>--> </strong> ${message}
                    </div>`
    return successMessage
}


const displayFormErrors = (prefix, errors) => {
    /* display errors in form of list for a form.
    * 'prefix' is a string which is attached prior to every form input key.
    * e.g input#id_prefix . every form key (e.g. email) will be attached to this prefix 
    * to make a valid identifier (i.e. input#id_email)
    */
    $.each(errors, function (key, value) {
        $.each(value, function (index, value) {
            if (value.message) {
                value = value.message;
            }
            addErrorToList(prefix + key, value);
        });
    });
    if ('__all__' in errors) {
        displayCustomErrors(CUSTOM_ERRORS_LIST_SELECTOR, errors.__all__);
    }
}

const displayCustomErrors = (key, errors) => {
    /* display error messages which do not specifically belong to a input id but generally to a form
    * key is identifier for the element in which errors should be displayed
    */
    $.each(errors, function (index, value) {
        if (value.message) {
            value = value.message;
        }
        var error_message = makeErrorMessage(value);
        $(key).append(error_message);
    });
}
