htmllisting-parser
==================
Python parser for Apache/nginx-style HTML directory listing

.. code-block:: python

   import htmllistparse
   cwd, listing = htmllistparse.fetch_listing(some_url, timeout=30)

   # or you can get the url and make a BeautifulSoup yourself, then use
   # cwd, listing = htmllistparse.parse(soup)

where ``cwd`` is the current directory, ``listing`` is a list of ``FileEntry`` named tuples:

* ``name``: File name, ``str``. Have a trailing / if it's a directory.
* ``modified``: Last modification time, ``time.struct_time`` or ``None``. Timezone is not known.
* ``size``: File size, ``int`` or ``None``. May be estimated from the prefix, such as "K", "M".
* ``description``: File description, file type, or any other things found. ``str`` as HTML, or ``None``.

Supports:

* Vanilla Apache/nginx/lighttpd/darkhttpd autoindex
* Most ``<pre>``-style index
* Many other ``<table>``-style index
* ``<ul>``-style

.. note::
   Please wrap the functions in a general ``try... except`` block. It may throw exceptions unexpectedly.

ReHTTPFS
--------

Reinvented HTTP Filesystem.

* Mounts most HTTP file listings with FUSE.
* Gets directory tree and file stats with less overhead.
* Supports Range requests.
* Supports Keep-Alive.

::

   usage: rehttpfs.py [-h] [-o OPTIONS] [-t TIMEOUT] [-u USER_AGENT] [-v] [-d]
                      url mountpoint

   Mount HTML directory listings.

   positional arguments:
     url                   URL to mount
     mountpoint            filesystem mount point

   optional arguments:
     -h, --help            show this help message and exit
     -o OPTIONS            comma separated FUSE options
     -t TIMEOUT, --timeout TIMEOUT
                           HTTP request timeout
     -u USER_AGENT, --user-agent USER_AGENT
                           HTTP User-Agent
     -v, --verbose         enable debug logging
     -d, --daemon          run in background

