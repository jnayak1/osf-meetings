import Ember from 'ember';
import config from 'ember-get-config';

export default Ember.Route.extend({
    model(params) {
        var conf = this.store.peekRecord('conference', params.conference_id);
        return this.store.createRecord('submission', {
            conference : conf
        });
    },

    actions : {
        saveSubmission(newSubmission, drop, resolve) {
            if(resolve){
                this.toast.info('Uploading File...', '', {
                        progressBar: false,
                        timeout: 0  // doesn't timeout
                });
                newSubmission.save().then((newRecord) => {
                    drop.options.url = config.providers.osf.uploadsUrl +
                        newRecord.get('nodeId') +
                        '/providers/osfstorage/?kind=file&name=' +
                        drop.getQueuedFiles()[0].name;

                    newRecord.get('contributor').then((authUser) =>{
                        var authHeader = 'Bearer ' + authUser.get('token');
                        drop.options.headers = {
                            'Authorization' : authHeader
                        };
                        resolve();
                    });
                });
            } else {
                this.toast.error('Please attach a file to your submission.');
            }
        },
        cancelSubmission() {
            var sub_to_cancel = this.currentModel;
            var conf = sub_to_cancel.get('conference');
            sub_to_cancel.unloadRecord();
            this.transitionTo('conference.index', conf.get('id'));
        },
        preUpload(drop){
            drop.options.method = 'PUT';
        },
        success(dropZone, file, successData) {
            var router = this;
            var nodeId = successData['data']['attributes']['resource']; //osf node's id
            var submissions = this.get('store').peekAll('submission');
            var relatedSubmission = submissions.findBy('nodeId', nodeId);
            var newFile = this.get('store').createRecord('metafile', {
                submission : relatedSubmission,
                osfId : successData['data']['id'],
                osfUrl : successData['data']['links']['download'],
                fileName : successData['data']['attributes']['name']
            });

            newFile.save().then((file) => {
                //do toast here
                var submission = file.get('submission');
                var conf = submission.get('conference');
                this.toast.clear();
                router.transitionTo('conference.index', conf.get('id'));
            });
        }
    }
});
