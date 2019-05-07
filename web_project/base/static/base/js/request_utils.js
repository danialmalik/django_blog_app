/* Attach an authoroziation header to each ajax request for token
* based authentication
*/

$.ajaxPrefilter(function(options, originalOptions, jqXHR) {
    var tokenValue = localStorageManager.getItem('access_token');
    if(tokenValue) {
        var authorization_header_value = 'Token ' + tokenValue;
        jqXHR.setRequestHeader('Authorization', authorization_header_value);
    }
    
});
