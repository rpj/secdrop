secdrop
=======

A secure, easy-to-use, iOS-compatible drop box. 

Makes use of both symmetric (first stage is AES-256, encrypted in-browser) and asymmetric encryption (GPG public-key for second stage, performed on server side).

Because first-stage encryption is done within the browser via CryptoJS (256-bit AES), an SSL server isn't required. However, it is _highly_ recommended.

Requirements
============

* CryptoJS <http://code.google.com/p/crypto-js/>
* jQuery >= 1.9.1 <http://jquery.com>
* GPG (or PGP) <http://www.gnupg.org> 
* Bootstrap <http://twitter.github.com/bootstrap/>

Recommended
===========

* An HTTPS server

Source hierarchy explanation
============================

* `client/` - The client-side implementation of the UI, first-stage encryption and file-send functionality
* `server/` - Server-side scripts for accepting uploads and performing second-stage asymmetric encryption.
* `dec/` - The tools used to decrypt dropped files. Figure out how to get them from the server on your own. _Never_ use this on the server-side unless you _fully_ trust your server!
