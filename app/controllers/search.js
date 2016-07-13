import Ember from 'ember';

export default Ember.Controller.extend({
	query: null,
	underFive: false,
	onePage: false,
	buttonArray: [],
	query: null,
	results: null,
	store: Ember.inject.service('store'),
	queryParams: ['q', 'p'],
	page: 1,
	actions: 
	{
      search() {
        let query = this.get("searchQuery");
        this.set('query', query);
		this.transitionToRoute('search', {queryParams: {q: query, p: this.page }});
		},
		toPage(pageNum){
			this.transitionToRoute('search', {queryParams: {p: pageNum }});
		}
    }
});
