#!/usr/bin/perl

use CGI qw/:all/;
use JSON;

my $ODIR = '/home/sulciphur/sec.rpj.me/.outdir';
my $ENCCMD = '/usr/bin/gpg -e -r j@seph.us -a --trust-model always --batch --yes -o ';

my $c = new CGI();
my $d = $c->param('XForms:Model');
my $r = 0;

if ($d) {
    my $uniq = sprintf("%x", time() * int(rand(0xffffffff)));
    my $fname = "$ODIR/${uniq}___${uniq}";

    if (!(-e $fname)) {
        open (GPG, "|$ENCCMD $fname") or die "Pipe to GPG failed: $!\n\n";
        print GPG $d;
        close (GPG);
        $r = 1;
    }
} 


print "Content-type: application/json\n\n";
print encode_json({result => $r});
