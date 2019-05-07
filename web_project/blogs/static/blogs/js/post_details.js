var COMMENT_FORM_SELECTOR = 'form#new_comment';
var POST_ID_SELECTOR = 'input#post_id'
var SUBMIT_BUTTON_SELECTOR = 'button#comment_submit';

var COMMENTS_SECTION_SELECTOR = 'div#comments_section';
var COMMENT_EDIT_SELECTOR = 'span#edit_comment';
var COMMENT_DELETE_SELECTOR = 'span#delete_comment';

var COMMENT_DIV_PREFIX = 'div#comment_';

var EDIT_COMMENT_FORM_SELECTOR = 'form#comment_edit';
var EDITED_COMMENT_ID_SELECTOR = EDIT_COMMENT_FORM_SELECTOR + ' input#id';
var COMMENT_EDITBOX_SELECTOR = 'textarea#comment_editbox';
var COMMENT_EDIT_MODAL_SELECTOR = 'div#commentModal';


const getCommentBodySelector = (commentId) => {
    return (COMMENT_DIV_PREFIX + commentId + ' #comment_body');
}

const getCommentBox = (comment, isCommentOwner) => {
    let options = '';
    if (isCommentOwner) {
        options = `<br>
                    <span data-id='${comment.id}' class='btn btn-sm btn-danger'
                        onclick=deleteComment(this)>delete</span>
                    <span data-id='${comment.id}' class='btn btn-sm btn-primary' 
                        onclick=showCommentEditbox(this)>edit</span>`;
    }
    let commentBox = `<div class="card" id="comment_${comment.id}">
                        <div class="card-header">${comment.commented_by}
                        ${options}
                        </div>
                        <div class="card-body" id="comment_body">${comment.content}</div> 
                        <div class="card-footer">${comment.commented_on}</div>
                    </div>
                    <hr>`;
    return commentBox;
}





const loadPostComments = (postId) => {
    $.ajax({
        type: "GET",
        url: comments_api,
        async: true,
        success: function (data) {
            $.each(data, function (index, value) {
                let commentBox = getCommentBox(value, value.commented_by == current_username);
                $(COMMENTS_SECTION_SELECTOR).append(commentBox);
            });
        },
        error: function (data) {
            $(COMMENT_FORM_SELECTOR).prepend(makeFloatingErrorMessage('Comment Failed. '));
        }
    });
}


const deleteComment = (element) => {
    let choice = confirm('Do you really want to delete this comment ?');
    if (choice) {
        let commentId = element.dataset.id;
        let url = comments_api + commentId;
        $.ajax({
            type: "DELETE",
            url: url,
            async: true,
            success: function (data) {
                $(COMMENT_DIV_PREFIX + commentId).remove();
            },
            error: function (data) {
                $(COMMENT_FORM_SELECTOR).prepend(makeFloatingSuccessMessage('Comment could not be deleted!'));
            }
        })
    }
}


const showCommentEditbox = (element) => {
    /* show a modal for editing comment
    */

    let commentId = element.dataset.id;

    // set comment text in modal text area
    let commentBody = $(getCommentBodySelector(commentId)).text();
    $(COMMENT_EDITBOX_SELECTOR).text(commentBody);

    // set comment id in hidden input for submitting later.
    $(EDITED_COMMENT_ID_SELECTOR).val(commentId);
    $(COMMENT_EDIT_MODAL_SELECTOR).modal('show');
}

const submitCommentEdit = (event) => {
    /*  Submit comment change request 
    */
    event.preventDefault();
    let commentId = $(EDITED_COMMENT_ID_SELECTOR).val();
    let commentContent = $(COMMENT_EDITBOX_SELECTOR).val();
    let url = comments_api + commentId + '/';
    let data = {
        'id': commentId,
        'content': commentContent
    };
    $.ajax({
        type: "PATCH",
        url: url,
        async: true,
        data: data,
        success: function (data) {
            $(COMMENT_FORM_SELECTOR).prepend(makeFloatingSuccessMessage('Successfully edited.'));
            $(getCommentBodySelector(commentId)).text(commentContent);
            $(COMMENT_EDIT_MODAL_SELECTOR).modal('hide');
        },
        error: function (data) {
            $(COMMENT_EDIT_MODAL_SELECTOR).prepend(makeFloatingErrorMessage('Comment Edit Failed.'));
        }
    });
}


$(document).ready(function () {

    let postId = $(POST_ID_SELECTOR).val();
    loadPostComments(postId);

    // New comment submit
    $(SUBMIT_BUTTON_SELECTOR).click(function (e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: comments_api,
            async: true,
            data: $(COMMENT_FORM_SELECTOR).serialize(),
            success: function (data) {
                $(COMMENT_FORM_SELECTOR).prepend(makeFloatingSuccessMessage('Successfully commented.'));
                let commentBox = getCommentBox(data, true);
                $(COMMENTS_SECTION_SELECTOR).prepend(commentBox);

            },
            error: function (data) {
                $(COMMENT_FORM_SELECTOR).prepend(makeFloatingErrorMessage('Comment Failed.'));
            }
        });

    });

});
