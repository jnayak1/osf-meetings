import Ember from 'ember';
import config from '../config/environment';

export
default Ember.Route.extend({
    beforeModel: function() {
        var nextQueryParam = "?next=" + window.location;
        window.location = config.providers.osfMeetings.loginUrl + nextQueryParam;                      
    }
});