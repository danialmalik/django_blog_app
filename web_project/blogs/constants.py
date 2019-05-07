
APP_NAME = 'blogs'


# URL Paths

INDEX_PATH = ''
POSTS_LIST_PATH = 'posts_list'
POST_CREATE_PATH = 'create'
MY_POSTS_PATH = 'my_posts'
POST_EDIT_PATH = 'edit/<int:pk>'
POST_DELETE_PATH = 'delete/<int:pk>'
POST_DETAILS_PATH = 'post_details/<int:pk>'

# URL Names

INDEX_VIEW_NAME = 'index'
POSTS_LIST_VIEW_NAME = 'posts_list'
MY_POSTS_VIEW_NAME = 'my_posts'

POST_CREATE_VIEW_NAME = 'post_create'
POST_EDIT_VIEW_NAME = 'post_edit'
POST_DELETE_VIEW_NAME = 'post_delete'
POST_DETAILS_VIEW_NAME = 'post_details'


# Template names

INDEX_TEMPLATE = 'index.html'
MY_POSTS_TEMPLATE = 'my_posts.html'
POST_CREATE_TEMPLATE = 'post_create.html'
POST_EDIT_TEMPLATE = 'post_edit.html'
POST_DETAILS_TEMPLATE = 'post_details.html'

# Field Max lengths

POST_TITLE_FIELD_MAX_LENGTH = 50
POST_CONTENT_FIELD_MAX_LENGTH = 5000

COMMENT_FIELD_MAX_LENGTH = 500

# posts ordering

ORDER_BY = '-last_modified_on'
