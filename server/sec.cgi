#!/usr/bin/perl

use CGI qw/:all/;
use JSON;

my $CONFIG = './.sec.cgi.conf';

my $ODIR = '/tmp/secdrop.output';
my $DEFGPGRECP = 'unknown@unknown.com';
my $DEFGPGCLI = '/usr/bin/gpg';
my $ENCCMD = "$DEFGPGCLI -e -r $DEFGPGRECP -a --trust-model always --batch --yes -o ";

if (-e $CONFIG) {
	my $ctext = undef;
	
	if (defined(open (CFG, "$CONFIG"))) {
		local $/ = undef;
		$ctext = <CFG>;
		close (CFG);
	}
	
	if (defined($ctext)) {
		my $cfg = undef;
		eval { $cfg = decode_json($ctext); };
		
		if (!$@ && defined($cfg)) {
			my $temp = undef;
			
			$ODIR = $temp, if (defined(($temp = $cfg->{OutputDirectory})));
			
			if (defined(($temp = $cfg->{GPGRecipient}))) {
				$ENCCMD =~ s/$DEFGPGRECP/$temp/g;
			}
			
			if (defined(($temp = $cfg->{GPGCLIPath}))) {
				$ENCCMD =~ s/$DEFGPGCLI/$temp/g;
			}
		}
		else {
			print STDERR "Malformed JSON in config '$CONFIG': $@\n";
		}
	}
}

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
