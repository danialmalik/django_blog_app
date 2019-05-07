// CSS selectors:-
var LOAD_MORE_SPAN_SELECTOR = 'span#load-more';
var POSTS_DIV_SELECTOR = 'div#container-posts';

var SEARCH_FORM_SELECTOR = 'form#search';
var SEARCH_INPUT_SELECTOR = 'input#search_key';

var BODY_SELECTOR = 'body';

var POST_CONTENT_LIMIT = 500;

var search_key = '';
var current_page = 1;


const getApiURL = (isMyPosts, key, pageNumber) => { 
    let url = posts_api;
    var filter = isMyPosts ? 'mine' : 'None';
    url += `?filter=${filter}&`;
    if (key) {
        url += `search=${key}&`;
    }
    url += `page=${++pageNumber}`;
    current_page = pageNumber;
    return url;
}


const addPosts = (data, isEditable) => {
    $.each(data, function (index, value) {

        card_box = `<div class="card" style="margin:10px">
                <p>
                <span class='card-header'>
                    <h3>${value.title}</h3>
                    <h6>Posted by : ${value.posted_by} </h6>
                    `
        if (isEditable) {

            card_box += `<a href="edit/${value.id}">
                        <span class="" >Edit</span>
                    </a>`
        }
        if (value.content.length > POST_CONTENT_LIMIT) {
            value.content = value.content.substring(0, POST_CONTENT_LIMIT) + '...';
        }
        card_box += `</span>
                <span class='card-header'>Posted on : ${value.posted_on}</span>
                <span class='card-header'>Last Modified on : ${value.last_modified_on}</span>

                </p>

                <div class="card-body">
                    <p class="card-text">${value.content}</p>
                    <a href=${post_details_url + value.id} ><span> View details </span></a>
                </div>

            </div>`
        $(POSTS_DIV_SELECTOR).append(card_box);
    })
}


const displayResults = (data) => {
    if (data.results.length) {
        addPosts(data.results, isMyPosts);
        if (data.next) {
            posts_url = data.next;
        } else {
            $(LOAD_MORE_SPAN_SELECTOR).hide();
        }
    } else {
        $(LOAD_MORE_SPAN_SELECTOR).hide();
        $(BODY_SELECTOR).append(makeFloatingErrorMessage('No posts Found.'));
    }
}


$(document).ready(function () {
    let url = getApiURL(isMyPosts, null, 0)
    $.ajax
        ({
            type: "GET",
            url: url,
            async: false,
            success: function (data) {
                displayResults(data);
            },
            error: function (data) {
                $(LOAD_MORE_SPAN_SELECTOR).hide();
                $(BODY_SELECTOR).append(makeFloatingErrorMessage('No posts Found.'));
            }
        });

    $(LOAD_MORE_SPAN_SELECTOR).click(function (e) {
        let url = getApiURL(isMyPosts, null, current_page)
        $.ajax
            ({
                type: "GET",
                url: url,
                async: false,
                success: function (data) {
                    displayResults(data);
                },
                error: function (data) {
                    $(LOAD_MORE_SPAN_SELECTOR).hide();
                    $(BODY_SELECTOR).append(makeFloatingErrorMessage('No posts Found.'));
                }
            });
    });

    $(SEARCH_FORM_SELECTOR).submit(function (e) {
        e.preventDefault();
        let key = $(SEARCH_INPUT_SELECTOR).val();
        current_page = 0;
        let url = getApiURL(isMyPosts, key, current_page);
        $(POSTS_DIV_SELECTOR).empty();
        $.ajax
            ({
                type: "GET",
                url: url,
                async: false,
                success: function (data) {
                    displayResults(data);
                },
                error: function (data) {
                    $(LOAD_MORE_SPAN_SELECTOR).hide();
                    $(BODY_SELECTOR).append(makeFloatingErrorMessage('No posts Found.'));
                }
            });
    });
});
