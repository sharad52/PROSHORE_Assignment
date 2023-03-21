// Base class used for ajax call
// Creates promise for jquery ajax call and returns it
function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }

 $(function () {
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
});

function AjaxCall() {
    this.post = (url, postJSON) => {
        return new Promise(function(resolve, reject) {
            $.ajax({
                type: 'POST',
                contentType: 'application/JSON',
                async: true,
                url: url,
                data: postJSON,
                success: function(response) {
                    resolve(response);
                },
                error: function(err) {
                    reject(err);
                },
            });
        });
    };

    this.postForm = (url, formData) => {
        return new Promise((resolve, reject) => {
            $.ajax({
                type: 'POST',
                cache: false,
                contentType: false,
                processData: false,
                async: true,
                url: url,
                data: formData,
                success: function(response) {
                    resolve(response);
                },
                error: function(response) {
                    reject(response);
                },
            });
        });
    };

    this.postEmpty = function(url) {
        return new Promise(function(resolve, reject) {
            $.ajax({
                type: 'POST',
                contentType: 'application/JSON',
                async: true,
                url: url,
                success: function(response) {
                    resolve(response);
                },
                error: function(err) {
                    reject(err);
                },
            });
        });
    };

    this.put = (url, postJSON) => {
        return new Promise(function(resolve, reject) {
            $.ajax({
                type: 'PUT',
                contentType: 'application/JSON',
                async: true,
                url: url,
                data: postJSON,
                success: function(response) {
                    resolve(response);
                },
                error: function(err) {
                    reject(err);
                },
            });
        });
    };

    this.putForm = (url, formData) => {
        return new Promise((resolve, reject) => {
            $.ajax({
                type: 'PUT',
                cache: false,
                contentType: false,
                processData: false,
                async: true,
                url: url,
                data: formData,
                success: function(response) {
                    resolve(response);
                },
                error: function(response) {
                    reject(response);
                },
            });
        });
    };

    this.get = url => {
        return new Promise(function(resolve, reject) {
            $.ajax({
                type: 'GET',
                url: url,
                async: true,
                contentType: 'application/json',
                success: function(res) {
                    res.results ? resolve(res.results) : resolve(res);
                },
                error: function(err) {
                    reject(err);
                },
            });
        });
    };

    this.getSync = url => {
        return new Promise(function(resolve, reject) {
            $.ajax({
                type: 'GET',
                url: url,
                async: false,
                contentType: 'application/json',
                success: function(res) {
                    resolve(res);
                },
                error: function(err) {
                    reject(err);
                },
            });
        });
    };

    this.del = url => {
        return new Promise(function(resolve, reject) {
            $.ajax({
                type: 'DELETE',
                contentType: 'application/JSON',
                async: true,
                url: url,
                success: function(res) {
                    resolve(res);
                },
                error: function(err) {
                    reject(err);
                },
            });
        });
    };

}

window.ajaxCall = new AjaxCall();