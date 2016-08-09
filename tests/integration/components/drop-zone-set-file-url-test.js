import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('drop-zone-set-file-url', 'Integration | Component | drop zone set file url', {
  integration: true
});

test('it renders', function(assert) {
  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });

  this.render(hbs`{{drop-zone-set-file-url}}`);

  assert.equal(this.$().text().trim(), '');

  // Template block usage:
  this.render(hbs`
    {{#drop-zone-set-file-url}}
      template block text
    {{/drop-zone-set-file-url}}
  `);

  assert.equal(this.$().text().trim(), 'template block text');
});