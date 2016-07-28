import Ember from 'ember';
import CheckLoginMixin from 'osf-meetings/mixins/check-login-mixin';
import config from '../../config/environment';

export default Ember.Route.extend(CheckLoginMixin, {
    model() {
        return Ember.RSVP.hash({
            meta : Ember.$.ajax({
                url : config.meetingsUrl + "/conferences/",
                type : "OPTIONS",
                xhrFields : {
                    withCredentials : true
                },
                crossDomain : true
            }),
            newConf : this.store.createRecord('conference')
        });
    },

    actions: {
        back() {
            this.transitionTo('index').then(function(newRoute) {
                newRoute.controller.set('visited', true);
            });
        },
        saveConference(newConf) {
            var router = this;
            newConf.save().then(function(params) {
                router.transitionTo('conference.index', params.id);
            });
        },
        setLogo(value) {
            this.currentModel.newConf.set('logo', value);
        }
    },
    
});
