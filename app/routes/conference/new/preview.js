import Ember from 'ember';

export default Ember.Route.extend({
    model() {
        return this.modelFor('conference.new');
    },
    isEqual: function(p1, p2) {
        return (p1 === p2);
    }
});
