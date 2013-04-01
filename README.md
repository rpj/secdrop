secdrop
=======

A secure, easy-to-use, HTML5-based drop box. Uses both symmetric encryption (first stage is AES-256, encrypted in-browser) and asymmetric (GPG public-key for second stage, performed on server side).

Because first-stage encryption is done within the browser itself via CryptoJS and uses 256-bit AES, an SSL server (HTTPS) isn't required. However, it is highly recommended.

Requirements
============

* CryptoJS <http://code.google.com/p/crypto-js/>
* jQuery >= 1.9.1 <http://jquery.com>
* GPG (or PGP I suppose) <http://www.gnupg.org> 

Recommended
===========

* An HTTPS server

Source hierarchy explanation
============================

* `client/` - The client-side (e.g. in-browser) implementation of UI and file-send functionality
* `server/` - Server-side scripts for accepting uploads and second-stage asymmetric encryption.
* `dec/` - The scripts/tools used to decrypt dropped files (_never_ use this on the server-side unless you fully trust your server!)