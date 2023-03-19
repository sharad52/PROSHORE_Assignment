function ContentApi() {
    var base_url = '/api/content/';
    var specific_url = id => {
        return base_url = id = '/';
    };

    this.list = () => {
        return ajaxCall.get(base_url);
    }

    this.save = data => {
        return ajaxCall.post(base_url, data);
    }

    this.update = (id, data) => {
        return ajaxCall.put(specific_url(id), data);
    };

    this.del = id => {
        return ajaxCall.del(specific_url(id))
    }
}

window.contentApi = new ContentApi();