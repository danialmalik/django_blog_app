var FORM_SELECTOR = 'form';
var CREATE_BUTTON_SELECTOR = 'button#create';
$(document).ready(function () {
    $(CREATE_BUTTON_SELECTOR).click(function (e) {
        e.preventDefault();

        $.ajax
            ({
                type: "POST",
                url: post_create_api,
                async: false,
                data: $(FORM_SELECTOR).serialize(),
                success: function (data) {
                    $(FORM_SELECTOR).prepend(makeFloatingSuccessMessage('Post Created.'));
                },
                error: function (data) {
                    $(FORM_SELECTOR).prepend(makeFloatingErrorMessage('Posting Failed.'));
                    displayFormErrors('input#id_',data.responseJSON);
                    displayFormErrors('textarea#id_',data.responseJSON);
                }
            });

    });
});
