import Ember from 'ember';

export default Ember.Component.extend({
    actions:{
        saveConference(newConf, drop, resolveUpload){
            this.sendAction('saveConference', newConf, drop, resolveUpload);
        },
        togglePreview(conf){
            conf.toggleProperty('preview');
        }
    }
});
