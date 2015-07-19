#!/usr/bin/env python
from wordbook.flaskapp import dev_app
from wordbook.flaskapp import app   # NOQA


def main():
    dev_app.run(debug=True)

if __name__ == '__main__':
    main()
