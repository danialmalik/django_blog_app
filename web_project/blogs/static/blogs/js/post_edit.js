// CSS selectors :-
var UPDATE_FORM_SELECTOR = 'form#form_update';
var UPDATE_BUTTON_SELECTOR = 'button#update';

var DELETE_BUTTON_SELECTOR = 'button#delete';


$(document).ready(function () {
    $(UPDATE_BUTTON_SELECTOR).click(function (e) {
        e.preventDefault();

        $.ajax
            ({
                type: "PATCH",
                url: post_details_api,
                async: false,
                data: $(UPDATE_FORM_SELECTOR).serialize(),
                success: function (data) {
                    $(UPDATE_FORM_SELECTOR).prepend(makeFloatingSuccessMessage('Post Edited.'))
                },
                error: function (data) {
                    $(UPDATE_FORM_SELECTOR).prepend(makeFloatingErrorMessage('Post editing Failed.'))
                }
            });

    });

    $(DELETE_BUTTON_SELECTOR).click(function (e) {
        e.preventDefault();
        var choice = confirm('Are you sure about deleting this post ?')
        if ( choice == true) {
            $.ajax
                ({
                    type: "DELETE",
                    url: post_details_api,
                    async: false,
                    data: $(UPDATE_FORM_SELECTOR).serialize(),
                    success: function (data) {
                        $(UPDATE_FORM_SELECTOR).prepend(makeFloatingSuccessMessage('Deleted Successfully!'))
                        window.location.replace(redirect_url)
                    },
                    error: function (data) {
                        $(UPDATE_FORM_SELECTOR).prepend(makeFloatingErrorMessage('Deletion failed!'))
                    }
                });
            }
    });
});
