import Ember from 'ember';

export default Ember.Component.extend({
	actions: {
		fileUploadChange: function(){
			var fileToRead = document.getElementById("fileToBeSerialized");
			var files = fileToRead.files;
			var file = files[0];
			var reader = new FileReader();
			var component = this;
	        reader.onload = function () {
	        	var serializedFile = reader.result;
	        	component.sendAction('setFileString', serializedFile);
	        };
	        reader.readAsDataURL(file);
		}
	}
});
