import attr from 'ember-data/attr';
//import Collection from './collection';
import Model from 'ember-data/model';

export default Model.extend({
    title: attr('string'),
    city: attr('string', { defaultValue : '' }),
    state: attr('string', { defaultValue : '' }),
    country: attr('string'),
    eventStart: attr('isodate', { defaultValue : (new Date()).toISOString() }),
    eventEnd: attr('isodate', { defaultValue : (new Date()).toISOString() }),
    submissionStart: attr('isodate', { defaultValue : (new Date()).toISOString() }),
    submissionEnd: attr('isodate', { defaultValue : (new Date()).toISOString() }),
    description: attr('string'),
    site: attr('string', { defaultValue : '' }),
    logo: attr('string', { defaultValue : '' }),
});
