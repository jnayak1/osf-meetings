import Ember from 'ember';

export
default Ember.Route.extend({
    model(){
        return this.store.findRecord('user', 'me');
    },
    actions: {
        logout: function() {
            this.transitionTo('logout');
        },
        login: function() {
            document.cookie = "redirectURL=" + window.location.href;
            this.transitionTo('login');
        },
        filter(params) {
            this.transitionTo('index', {
                queryParams: {
                    q: params
                }
            });
        },
        search(params) {
            this.transitionTo('search', {
                queryParams: {
                    q: params,
                    p: 1
                }
            });
        }
    }
});