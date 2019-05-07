// CSS Selectors
var SUBMIT_BUTTON_SELECTOR = 'button.btn-primary';
var ERRORS_LIST_SELECTOR = 'ul.error';
var CUSTOM_ERRORS_LIST_SELECTOR = 'ul#custom_errors';

var USERNAME_INPUT_SELECTOR = 'input#id_username';
var FIRST_NAME_INPUT_SELECTOR = 'input#id_first_name';
var LAST_NAME_INPUT_SELECTOR = 'input#id_last_name';
var EMAIL_INPUT_SELECTOR = 'input#id_email';
var BIRTHDAY_INPUT_SELECTOR = 'input#id_birthday';

var PROFILE_PICTURE_INPUT_SELECTOR = '#id_profile_picture';
var PROFILE_PICTURE_THUMBNAIL_SELECTOR = 'img#profile_picture';
var CURRENT_PROFILE_PICTURE_LINK_SELECTOR = 'label[for=id_profile_picture] ~ a';
var PROFILE_PICTURE_DIV_SELECTOR = 'div#profile_picture_container';
var PROFILE_PICTURE_INPUT_DIV_SELECTOR = 'div#user_form ~ div';
var REMOVE_PICTURE_BUTTON_SELECTOR = 'span#remove_picture';

var USER_FORM_FIELDS_SELECTOR = 'div#user_form input';
var PROFILE_FORM_SELECTOR = 'form#id_profile_form';
var FORM_SELECTOR = 'form';

var DEFAULT_PROFILE_PICTURE_PATH = '/media/profile_pictures/empty.png';

// flag for indicating that picture is to be removed.
var isDeleted = false;

const validateProfileUpdateForm = () => {
    let username = $(USERNAME_INPUT_SELECTOR).val();
    let first_name = $(FIRST_NAME_INPUT_SELECTOR).val();
    let last_name = $(LAST_NAME_INPUT_SELECTOR).val();
    let email = $(EMAIL_INPUT_SELECTOR).val();
    let birthday = $(BIRTHDAY_INPUT_SELECTOR).val();
    let isValid = true
    if (username == "") {
        addErrorToList(USERNAME_INPUT_SELECTOR, 'Username required.');
    }
    if (!isEmail(email)) {
        addErrorToList(EMAIL_INPUT_SELECTOR, 'Enter a valid email!');
        isValid = false;
    }
    currentDate = new Date()
    if (birthday > currentDate) {
        addErrorToList(BIRTHDAY_INPUT_SELECTOR, 'Birthday cannot be in future.');

    }
    return isValid;
}

const renameUserFormInputs = (formFields) => {
    /* Rename every input field of 'User' object so that the nested serializer in
    *  API can serialize this.
    * e.g. input named 'username' will be renamed to 'user.username'
    */ 
    $.each(formFields, function(index, value)  {
        if (value.name != 'csrftoken') {
            value.name = `user.${value.name}`;
        }
    });
    
}

const updateCurrentPicture = (event) => {
    /* update current profile picture thumbnail whenever a picture
    * is selected using picture input
    */
    let picture_thumbnail = $(PROFILE_PICTURE_THUMBNAIL_SELECTOR)[0];
    let new_picture = $(PROFILE_PICTURE_INPUT_SELECTOR)[0].files[0];
    let reader = new FileReader()

    reader.onload = function() {
        picture_thumbnail.src = reader.result;
    }

    if(new_picture) {
        reader.readAsDataURL(new_picture);
        $(REMOVE_PICTURE_BUTTON_SELECTOR).show();
    } else {
        picture_thumbnail.src = '';
    }
}

const removeProfilePicture = (event) => {
    /**Remove current profile picture thumbnail when remove picture button is pressed.
     * and set isDeleted flag so that empty value is sent to the api for the picture 
     * and picture is deleted.
     */
    $(PROFILE_PICTURE_THUMBNAIL_SELECTOR)[0].src = DEFAULT_PROFILE_PICTURE_PATH;
    $(REMOVE_PICTURE_BUTTON_SELECTOR).hide();
    $(PROFILE_PICTURE_INPUT_SELECTOR)[0].value = '';
    isDeleted = true;
}

const moveProfilePictureInput = () => {
    /**Move the profile picture input from center of page to below the picture frame */
    $(PROFILE_PICTURE_INPUT_DIV_SELECTOR).insertAfter($(PROFILE_PICTURE_DIV_SELECTOR));

}

$(document).ready(function () {

    var userFormFields = $(USER_FORM_FIELDS_SELECTOR);
    // Rename 'User' input fields for serializer in API. 
    renameUserFormInputs(userFormFields);

    moveProfilePictureInput();

    let current_profile_pic = $(CURRENT_PROFILE_PICTURE_LINK_SELECTOR);
    if (current_profile_pic.length) {
        $(PROFILE_PICTURE_THUMBNAIL_SELECTOR)[0].src = current_profile_pic[0].href;
        if (current_profile_pic[0].href.endsWith('empty.png')) {
            $(REMOVE_PICTURE_BUTTON_SELECTOR).hide();
        }
    } else {
        $(REMOVE_PICTURE_BUTTON_SELECTOR).hide();
    }

    let pictureInput = $(PROFILE_PICTURE_INPUT_SELECTOR)[0];

    pictureInput.addEventListener('change', updateCurrentPicture)

    $(PROFILE_FORM_SELECTOR).submit(function (e) {
        $(CUSTOM_ERRORS_LIST_SELECTOR).empty();      //removing any previous errors
        $(ERRORS_LIST_SELECTOR).empty();
        e.preventDefault();
        let formData = new FormData(this);
        let new_profile_picture = $(PROFILE_PICTURE_INPUT_SELECTOR)[0].value;
        if (new_profile_picture) {
            formData.append('profile_picture', new_profile_picture);
        } else if( !isDeleted ) {
            // Do not send empty value for profile_picture so that picture remains unchanged 
            // on api server.
            formData.delete('profile_picture');
        }
        isValid = validateProfileUpdateForm();
        if (isValid) {
            $.ajax({
                type: "PUT",
                processData: false,
                contentType: false,
                url: profile_update_api,
                async: false,
                data: formData,
                success: function (data) {
                    window.location.replace(success_redirect_url);
                },
                error: function (data) {
                    var errors = data.responseJSON;
                    displayFormErrors('input#id_', errors);
                    
                }
            });
        }
    })
});
