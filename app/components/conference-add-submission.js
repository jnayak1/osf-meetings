import Ember from 'ember';

export default Ember.Component.extend({
    info: false,
    actions:{
        toggleInfo() {
            var info = this.get('info');
            if (info === true){
                Ember.$('#submission-instructions').hide(400);
            }
            else {
                Ember.$('#submission-instructions').show(400);
            }
            this.set('info', !info);
        }
    }
});
