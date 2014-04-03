# Goosepaper

Being a small [Flask](http://flask.pocoo.org/) application written around the awesome [Newspaper](https://github.com/codelucas/newspaper) module.

## Installation

* Have a MongoDB instance running. Default is `localhost:27017`. Change this in `settings.py`.
* Run the `install` script, then source `./bin/activate`
* Run `./start flask`

## Usage

### REST

To save

	curl -X POST \
		 -H "article: http://time.com/jonathan-ive-apple-interview" \
		 http://localhost:5000/save

To delete

	curl -X DELETE http://localhost:5000/article/533c67a364b6c00bf64864a3

### Command-line

    python save.py --url=http://article

License
-------
See `LICENSE`
