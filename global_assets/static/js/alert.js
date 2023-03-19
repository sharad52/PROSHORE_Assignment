bs_alert = function() {};

bs_alert.timeout = 4000;

bs_alert.fadeIn = function() {
    $('#alert_placeholder').fadeIn(200);
};

bs_alert.clear = function() {
    $('#alert_placeholder').fadeOut(500, function() {
        $('#alert_placeholder').html('');
    });
};

bs_alert.warning = function(message) {
    $('#alert_placeholder').html(
        '<div class="alert alert-warning"><a class="close" data-dismiss="alert" style="color: #8a6d3b !important;">×</a><span>' +
            message +
            '</span></div>'
    );
    bs_alert.fadeIn();
    setTimeout(bs_alert.clear, bs_alert.timeout);
};
bs_alert.error = function(message) {
    $('#alert_placeholder').html(
        '<div class="alert alert-danger"><span>' +
            message +
            '</span><a class="close" data-dismiss="alert">×</a></div>'
    );
    bs_alert.fadeIn();
    setTimeout(bs_alert.clear, bs_alert.timeout);
};

bs_alert.success = function(message) {
    $('#alert_placeholder').html(
        '<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span>' +
            message +
            '</span></div>'
    );
    bs_alert.fadeIn();
    setTimeout(bs_alert.clear, bs_alert.timeout);
};

bs_alert.info = function(message) {
    $('#alert_placeholder').html(
        '<div class="alert alert-info"><a class="close" data-dismiss="alert">×</a><span>' +
            message +
            '</span></div>'
    );
    bs_alert.fadeIn();
    setTimeout(bs_alert.clear, bs_alert.timeout);
};

bs_alert.non_field_errors = function(err) {
    errorJson = err.responseJSON;
    errorMsg = '';
    if (
        errorJson != null &&
        Array.isArray(errorJson) &&
        'non_field_errors' in errorJson
    ) {
        $.each(errorJson.non_field_errors, function(index, item) {
            errorMsg = errorMsg + '<div>' + item + '</div>';
        });
        bs_alert.error(errorMsg);
    } else if (typeof errorJson == 'object') {
        errorMsg = errorMsg + '<div>' + errorJson.message + '</div>';
        bs_alert.error(errorMsg);
    }
};

bs_alert.field_errors = function(err) {
    errorJson = err.responseJSON;
    errorMsg = '';

    $.each(errorJson, function(key, value) {
        if (Array.isArray(value)) {
            $.each(value, function(index, item) {
                errorMsg = errorMsg + '<div>' + key + ': ' + item + '</div>';
            });
        } else {
            $.each(value, function(innerKey, item) {
                errorMsg =
                    errorMsg + '<div>' + innerKey + ': ' + item + '</div>';
            });
        }
    });

    bs_alert.error(errorMsg);
};

bs_alert.all_errors = function(err) {
    console.log(err);
    errorMsg = '';

    if (typeof err === 'string') {
        console.log(err);
        errorMsg = errorMsg + '<div>' + err + '</div>';
    }

    errorJson = err.responseJSON;

    var recursiveInsert = function(err, objectKey) {
        //When the output json is array
        if (isArray(err)) {
            $.each(err, function(index, item) {
                //If array item is of type string
                if (typeof item === 'string') {
                    if (objectKey) {
                        let errorKey = objectKey
                        if(objectKey == 'non_field_errors') errorKey = 'Error';

                        errorMsg =
                            errorMsg +
                            '<div>' +
                            errorKey +
                            ' : ' +
                            item +
                            '</div>';
                    } else {
                        errorMsg = errorMsg + '<div>' + item + '</div>';
                    }
                }

                //Recurse if item is an array
                if (isArray(item)) {
                    recursiveInsert(item);
                }

                if (isObject(item)) {
                    recursiveInsert(item);
                }
            });
        }

        if (isObject(err)) {
            $.each(err, function(key, value) {
                var item = err[key];

                //If item is of type string
                if (typeof item === 'string') {
                    let errorKey = key
                    if(key == 'non_field_errors') errorKey = 'Error';
                    errorMsg =
                        errorMsg + '<div>' + errorKey + ' : ' + item + '</div>';
                }

                if (isArray(item)) {
                    recursiveInsert(item, key);
                }

                if (isObject(item)) {
                    recursiveInsert(item, key);
                }
            });
        }
    };

    recursiveInsert(errorJson);
    bs_alert.error(errorMsg);
};

function redirectAfterAlert(redirect_url, timer = 1500) {
    setTimeout(function() {
        let url = new URL(window.location.href);
        let close = url.searchParams.get('close');
        if (close == 'True' || close == 'true') {
            window.close();
        } else {
            console.log(url);
            window.location.href = redirect_url;
        }
    }, timer);
}
