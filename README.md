Secdrop
=======

A secure, easy-to-use, iOS-compatible drop box that makes use of both symmetric (first stage is AES-256, encrypted in-browser) and asymmetric encryption (GPG public-key for second stage, performed on server side).

As first-stage encryption is performed within the browser via CryptoJS (256-bit AES), an SSL server isn't required. However, it is _highly_ recommended.

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
 * Put these files in your __DocumentRoot__ or somewhere publicly-viewable for your HTTPS server.
 * Install client requirements (noted above) into the *js/* directory.

* `server/`
 * Ensure GPG is available at */usr/bin/gpg* or set the proper path via the sec.cgi config (.sec.cgi.conf, key __GPGCLIPath__).
 * Configure the output path for dropped files via config key __OutputDirectory__. Default is */tmp/secdrop.output*. __This path must be writable for the user executing your CGI process__.
 * Configure the recipient GPG public key via config key __GPGRecipient__. This keypair must be available to the recipient using *dec/secdl.pl*.
 * __Be certain__ that you've configured your chosen web server to disallow access to the config file as well as the path used for __OutputDirectory__. 

* `dec/`
 * __Only use these scripts for decryption on a trusted machine.__
 * `dec/secdl.pl arg1 arg2` decrypts files in *arg1* into directory *arg2*. (Presumably the files are sourced  from __OutputDirectory__ in the server config. I simply use *scp* to retrieve files.)
  * You will be prompted for the password the original sender used to encrypt via the web UI.
  * Second-stage decryption will be done with the GPG keypair for the recipient specified in the server config.
