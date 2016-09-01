import Ember from 'ember';

export default Ember.Route.extend({
    results: true,
    query: null,
    queryParams: {
        q: {
            refreshModel: true
        }
    },
    model(params) {
        let foundConferences = this.store.query('conference', {
            search: params.q,
            page: params.p
        }).then((result) => {
            this.set('results', true);
            this.controllerFor('index').set('results', this.results);
            let meta = result.get('meta');
            if (meta.pagination.count === 0) {
                this.set('results', false);
                this.controllerFor('index').set('results', this.results);
            }
            return result;
        });
        return foundConferences;
    },

    //The beforeModel function here checks if the redirectURL is equal to something besides the index (current) route
    //If it is equal to something else, it resets the redirectURL to the index route and transitions to the redirect URL

    beforeModel: function() {
        var redirectURL = this.getCookie('redirectURL');
        if (redirectURL !== window.location.href) {
            document.cookie = "redirectURL=" + window.location.href;
            window.location = redirectURL;
        }
    },
    getCookie: function(cname) {
        var name = cname + "=";
        var ca = document.cookie.split(';');
        for(var i = 0; i <ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0)===' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) === 0) {
                return c.substring(name.length,c.length);
            }
        }
        return "";
    },
    actions: {
        create() {
            this.transitionTo('conference.new').then(function(newRoute) {
                newRoute.controller.set('displayErrors', false);
            });
        },
        scrollit() {
            let shift = this.controllerFor('index');
            shift.set('visited', true);
            Ember.$('#indexTop').hide(2000);
        },
        /***************************************/


        /*
         *  Switches main view to tiles
         */
        tileView() {
            Ember.$('#tileButton').addClass('disabled');
            Ember.$('#listButton').removeClass('disabled');
            let shift = this.controllerFor('index');
            shift.set('tileview', true);
        },
        /***************************************/
        listView() {
            Ember.$('#listButton').addClass('disabled');
            Ember.$('#tileButton').removeClass('disabled');
            let shift = this.controllerFor('index');
            shift.set('tileview', false);
        },
        /*
           filter(params) {
           let shift = this.controllerFor('index');
           shift.set('query', params);
           this.transitionTo('index', {
           queryParams: {
           q: params
           }
           });
           },
           */
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
