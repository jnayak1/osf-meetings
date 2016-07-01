# Osf-meetings

This README outlines the details of collaborating on this Ember application.
A short introduction of this app could easily go here.

## Prerequisites

You will need the following things properly installed on your computer.

* [Git](http://git-scm.com/)
* [Node.js](http://nodejs.org/) (with NPM)
* [Bower](http://bower.io/)
* [Ember CLI](http://ember-cli.com/) Installed when doing `npm install`
* [PhantomJS](http://phantomjs.org/)
* [Watchman](https://facebook.github.io/watchman/docs/install.html) Brew install

## Installation

* `git clone <repository-url>` this repository
* `git clone <ember-osf-repo>` [https://github.com/CenterForOpenScience/ember-osf](https://github.com/CenterForOpenScience/ember-osf).
* cd into the new directory
* `npm install`
* `bower install`
* `ember install ../ember-osf`
* `npm link ../ember-osf`

#### Django
##### API server for OSF_meetings_ember with permissions using django_guardian

#### Setup

1. `pip install -r requirements.txt`
2. `cd <to-meetings-folder>`
3. `./manage.py makemigrations`
4. `./manage.py migrate`
5. `./manage.py runserver`
6. Visit the Django REST API interface at [http://localhost:8000](http://localhost:8000).

## Running Ember APP / Development

* `cd <to-root-of-repo>`
* `ember server`
* Visit your app at [http://localhost:4200](http://localhost:4200).

### Code Generators

Make use of the many generators for code, try `ember help generate` for more details

### Running Tests

* `ember test`
* `ember test --server`

### Building

* `ember build` (development)
* `ember build --environment production` (production)

### Deploying

Specify what it takes to deploy your app.

## Further Reading / Useful Links

* [ember.js](http://emberjs.com/)
* [ember-cli](http://ember-cli.com/)
* Development Browser Extensions
  * [ember inspector for chrome](https://chrome.google.com/webstore/detail/ember-inspector/bmdblncegkenkacieihfhpjfppoconhi)
  * [ember inspector for firefox](https://addons.mozilla.org/en-US/firefox/addon/ember-inspector/)
