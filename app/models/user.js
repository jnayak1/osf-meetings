import User from 'ember-osf/models/user';
import attr from 'ember-data/attr';
// import { belongsTo, hasMany } from 'ember-data/relationships';

export default User.extend({
	token: attr('string')
});
