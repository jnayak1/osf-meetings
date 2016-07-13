import Ember from 'ember';
import EmberValidations from 'ember-validations';

export default Ember.Controller.extend(EmberValidations, {

	editing: false,
	navModal: false,
	displayErrors: false,

	validations: {
		'model.title': {
		  length: {minimum: 3, maximum: 300, messages: {
		    tooShort: 'Please enter a longer title',
		    tooLong: 'Title exceeds limit of 300 characters'
		  }}
		},
		'model.description': {
		  length: {minimum: 6, maximum: 2000, messages: {
		    tooShort: 'Please enter a longer description',
		    tooLong: 'Description exceeds limit of 2000 characters'
		  }}
		},
		'model.country': {
		  exclusion: {in: ['-Select a country'], message: 'Please choose a country'}
		},
		'model.state': {
		  statecheck: {}
		},
		'model.city': {
		  length: {maximum: 100, messages: {
		    tooLong: 'City name is too long'
		  }}
		},
		'model.startDate': {
		  datecheck: {}
		},
		'model.submissionDate': {
		  datecheck: {}
		}
	},
 	hasState: Ember.computed.match('model.state', /.+/),

	actions: {
		selectCountry(country) {
      		this.set('model.country', country);
    	},
		editConference() {
			this.set('editing',true);
		},	
		cancelEdits() {
			this.set('editing',false);
			this.set('displayErrors',false);
			this.store.findRecord('conference',this.get('model.id')).then(function(conference) {
				conference.rollbackAttributes();
			});
		},
		saveEdits(conferenceID) {
	      	if (this.get('isValid')) {
				var conference = this.store.peekRecord('conference', conferenceID);
				conference.save();
				this.set('editing',false);
				this.set('displayErrors',false);
			} else {
				this.set('displayErrors',true);
			}
		}
	}
});
