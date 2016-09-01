import Ember from 'ember';

export default Ember.Route.extend({
    model(params) {
        return Ember.RSVP.hash({
            conf : this.store.findRecord('conference', params.conference_id),
            allSubmissions : this.store.query('submission', {
                conference: params.conference_id
            })
        });
    }
});
