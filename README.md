Secdrop
=======

A secure, easy-to-use, iOS-compatible drop box. 

Makes use of both symmetric (first stage is AES-256, encrypted in-browser) and asymmetric encryption (GPG public-key for second stage, performed on server side).

Because first-stage encryption is done within the browser via CryptoJS (256-bit AES), an SSL server isn't required. However, it is _highly_ recommended.

Requirements
============

* `client/`
 * CryptoJS <http://code.google.com/p/crypto-js/>
 * jQuery >= 1.9.1 <http://jquery.com>
 * Bootstrap <http://twitter.github.com/bootstrap/>
* `server/` and `dec/`
 * GPG (or PGP) <http://www.gnupg.org> 
* `dec/`
 * OpenSSL (command-line tool) <http://www.openssl.org>

Recommended
===========

* An HTTPS server

Source hierarchy
================

* `client/` - The client-side implementation of the UI, first-stage encryption and file-send functionality
* `server/` - Server-side scripts for accepting uploads and performing second-stage asymmetric encryption.
* `dec/` - The tools used to decrypt dropped files. *__Never__* use this on the server-side unless you *__fully__* trust your server!

Installation & Use
====================

* `client/`
 * Put these files in your 'DocumentRoot' or somewhere publicly-viewable for your HTTPS server.
 * Install client requirements (noted above) into the `js/` directory.

* `server/`
 * Ensure GPG is available at `/usr/bin/gpg` or set the proper path via the sec.cgi config (.sec.cgi.conf, key `GPGCLIPath`).
 * Configure the output path for dropped files via config key `OutputDirectory`. Default is `/tmp/secdrop.output`. _This path must be writable for the user executing your CGI process_.
 * Configure the recipient GPG public key via config key `GPGRecipient`. This keypair must be available to the recipient using `dec/secdl.pl`.

* `dec/`
 * __Only use these scripts for decryption on a trusted machine.__
 * `dec/secdl.pl arg1 arg2` decrypts files in `arg1` into directory `arg2`. (Presumably they came from `OutputDirectory` in the server config. I simply use `scp` to retrieve files.)
  * You will be prompted for the password the original sender used to encrypt via the web UI.
  * Second-stage decryption will be done with the GPG keypair for the recipient specified in the server config.