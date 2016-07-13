import Ember from 'ember';

export default Ember.Route.extend({
	page: null,
	pages: null,
	results: null,
	queryParams: {
		q: {refreshModel: true},
		p: {refreshModel: true}
	},
	beforeModel: function(params)
	{
			this.set('results', this.store.query('conference', {search:params.q, page: params.p}));
	},
	model: function(params)
	{	
		this.controllerFor('search').set('query', params.q);
		let foundConferences = this.store.query('conference', {search:params.q, page: params.p}).then((result) => {
				this.set('results', true);
  				let meta = result.get('meta');
  				this.set('pages', meta.pagination.pages);
  				this.set('page', meta.pagination.page)
  				if(meta.pagination.count == 0)
  				{
  					this.set('results', false);
  				}
  				return result;
		});
		//console.log(foundConferences.get('length'));
		return foundConferences;
	},
	setupController: function(controller, model)
	{	
		let page = this.get('page');
		console.log("Current page: " + page);
		let pages = this.get('pages');
		console.log('Pages set to: ' +  pages);
		let push = this.controllerFor('search');
		push.set('buttonArray', null);
		if (pages == 1)
		{
			push.set('onePage', true);
		}
		else{ push.set('onePage', false)}
		this._super(controller, model);
		push.set('results', this.get('results'));


		if((pages >1) && (pages< 5))
		{
			let buttonArray = [];
			let i = 1;
			while(i <= pages)
			{
				buttonArray.push(i);
				i++;
			}
			push.set('underFive', true);
			push.set('buttonArray', buttonArray);
		}
		else if((page <=3) && (pages > 5))
		{
			push.set('buttonArray', [ 2, 3, 4, 5,6])
		}
		else if((page > 3) && (page < (pages - 2)))
		{
			push.set('buttonArray', [page - 2, page -1, page, page + 1, page +2])
		}
		else if(page >= (pages -2))
		{
			push.set('buttonArray', [pages-5,pages -4, pages -3, pages -2, pages -1])
		}
	}
});
