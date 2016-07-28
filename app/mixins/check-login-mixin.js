import Ember from 'ember';
import config from '../config/environment';

export default Ember.Mixin.create({
    //Overwrite redirectRoute function to return the route the user should transition to after logging in
    beforeModel: function() {

        var self = this;
        Ember.$.ajax({
            url: config.currentUser,
            dataType: 'json',
            contentType: 'text/plain',
            xhrFields: {
                withCredentials: true
            }
        }).then(function(loggedIn) {
            if (loggedIn.errors) {
                if (window.location.href !== config.meetingsHomeUrl) {
                    document.cookie = "redirectURL=" + window.location.href;
                } else {
                    document.cookie = "redirectURL=" + config.meetingsHomeUrl + "conference/new/";
                }
                self.transitionTo('login');
            }
        });
    },
    actions: {
        logout: function() {
            this.transitionToRoute('logout');
        }
    }
});
