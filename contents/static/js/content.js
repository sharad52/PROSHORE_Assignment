$(document).ready(function() {
    var vm = new ContentViewModel(init_data);
    ko.applyBindings(vm);

    // $('#frm').validate({
    //     rules: {
    //         title: {required: true },
    //         description: {required: true},
    //         author_name: {required: true},
    //         author_designation: {required: true},
    //         reading_time: {required: true},
    //     },
    //     messages: {
    //         title: {required: 'Title is Required.' },
    //         description: {required: 'Description is required.'},
    //         author_name: {required: 'Author name is required.'},
    //         author_designation: {required: 'Author designation is required.'},
    //         reading_time: {required: 'Reading time is required.'},
    //     },
    // })
});

function ContentViewModel(model) {
    this.title = ko.observable();
    this.description = ko.observable();
    this.blog_image_url = ko.observable();
    this.author_name = ko.observable();
    this.author_image_url = ko.observable();
    this.author_designation = ko.observable();
    this.reading_time = ko.observable();


    this.save = function() {
        var validationResult = true;
        if (validationResult) {
            let postJson = ko.toJSON(this);
            contentApi
                .save(postJson)
                .then(res => {
                    alert('Content Saved successfully.')
                    bs_alert.success('Content Saved Successfully.');
                    redirectAfterAlert('/')
                })
                .catch(err => bs_alert.all_errors(err));
        }
    }

    this.update = function() {
        var validationResult = true;
        if (validationResult) {
            var postJson = ko.toJSON(this);
            contentApi
                .update(model.id, postJson)
                .then(res => {
                    alert('Updated successfully.');
                    bs_alert.success('Content updated successfully');
                    redirectAfterAlert('/content/' + model.id);
                })
                .catch(err => bs_alert.all_errors(err));
        }
    }

    this.del = function() {
        contentApi
            .del(model.id)
            .then(res => {
                alert('Content Deleted Successfully.');
                bs_alert.success('Content Deleted Successfully.');
                redirectAfterAlert('/')
            })
            .catch(err => bs_alert.all_errors(err));
    }

    this.populate = function(model) {
        this.title(model.title);
        this.description(model.description);
        this.blog_image_url(model.blog_image_url);
        this.author_name(model.author_name);
        this.author_image_url(model.author_image_url);
        this.author_designation(model.author_designation);
        this.reading_time(model.reading_time);

    }

    if (scenario == 'Update') {
        this.populate(model)
    }
}