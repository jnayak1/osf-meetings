import Ember from 'ember';

export default Ember.Controller.extend({
  results: null,
  query: null,
  tileview: true,
  queryParams: ['q', 'p'],
  columns: [
  {
    "propertyName": "title",
    "title": "Title"
  },
  {
    "propertyName": "city",
    "title": "City"
  },
  {
    "propertyName": "state",
    "title": "State"
  },
  {
    "propertyName": "country",
    "title": "Country"
  },
  {
    "propertyName": "author",
    "title": "Author"
  },
    {
      "propertyName": "startDate",
      "title": "Start Date"
    },
    {
      "propertyName": "endDate",
      "title": "End Date"
    },
    {
      "propertyName": "description",
      "title": "Description"
    }],

  visited: false,
  actions: {
      create() {
        this.transitionToRoute('conference.new').then(function(newRoute) {
          newRoute.controller.set('displayErrors',false);
        });
      },
      scrollit() {
        this.set('visited',true);
        Ember.$('body').removeClass('hide-scroll');
        Ember.$('html').css({overflow: 'scroll'});
        Ember.$('#indexTop').hide(2000, function() {
          Ember.$('#indexBottom').css({"margin-top": "80px"});
          Ember.$('#tableContainer').css({"margin-top": "80px"});
          Ember.$('#create').css({position: "fixed"});
        });
      },
      tileView() {
        Ember.$('#tileButton').addClass('disabled');
        Ember.$('#listButton').removeClass('disabled');
        let shift = this;
        shift.set('tileview', true );
      },
      listView() {
        Ember.$('#listButton').addClass('disabled');
        Ember.$('#tileButton').removeClass('disabled');
        let shift = this;
        shift.set('tileview', false );
      },
      filter() {
        let query = this.get("searchQuery");
        this.set('query', query);
        this.transitionToRoute('index', {queryParams: {q: query}});
      },
      search()
      {
        let query = this.get("searchQuery");
        this.transitionToRoute('search', {queryParams: {q: query, p:1}});
      }
    },

});
