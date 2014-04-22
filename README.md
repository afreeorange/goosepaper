# Goosepaper

Being a small [Flask](http://flask.pocoo.org/) application written around the awesome [Newspaper](https://github.com/codelucas/newspaper) module.

Installation
------------

* Have a MongoDB instance running. Default is `localhost:27017`. Change this in `settings.py`.
* Run the `install` script, then source `./bin/activate`
* Run `./start flask` for a dev server.  
  Running `./start` will start 10 [gunicorn](http://gunicorn.org) workers.

Managing Articles
-----------------

### Web

Click the "+" icon to add a URL.

### Command-line

To save

	curl -X POST \
		 -H "article: http://time.com/jonathan-ive-apple-interview" \
		 http://localhost:5000/

To delete

	curl -X DELETE http://localhost:5000/article/533c67a364b6c00bf64864a3

_Or_, source `bin/activate` and then

    python save.py --url=http://article

### Email

* Edit `mail.py` to change the host and port values.
* Then set up an alias and pipe the email to `mail.py`. For example, this is what I have in `/etc/aliases`

		Nlr5zbrLCgwTOA3ApKKa: 	|"python /path/to/mail.py"

* Send an email to alias with the _subject line_ containing the URL.

License
-------

See `LICENSE`
