import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('conference-preview-bar', 'Integration | Component | conference preview bar', {
  integration: true
});

test('it renders', function(assert) {
  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });

  this.render(hbs`{{conference-preview-bar}}`);

  assert.equal(this.$().text().trim(), '');

  // Template block usage:
  this.render(hbs`
    {{#conference-preview-bar}}
      template block text
    {{/conference-preview-bar}}
  `);

  assert.equal(this.$().text().trim(), 'template block text');
});
