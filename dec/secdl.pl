#!/usr/bin/perl
$|++;
use MIME::Base64;

my $OSSLROWSIZE = 64;
my $OSSLCMD = 'openssl enc -aes-256-cbc -pass pass:"P_P" -d -base64 -in "F_F"';
my $TFILE = './.tempforopenssl';
my $GPGCMD = '/usr/local/bin/gpg -d -o ';

my $dir = shift or die "Must provide a directory of files!\n\n";
my $outdir = shift or die "Must provide an output directory!\n\n";

print "What's the password? ";
my $pass = <STDIN>;
chomp($pass);

while (<$dir/*>) {
	my $fname = $_;
	print "Processing '$fname'... ";
	open(F, "$fname") or die "Can't open $fname: $!\n\n";
	my $text = undef;
	{ local $/ = undef; $text = <F>; }
	close(F);
	
	print "Decrypting (stage one)... ";
	open (GPG, "|$GPGCMD $TFILE") or die "Pipe to GPG failed: $!\n\n";
	print GPG $text;
	close (GPG);
	
	open (T1, "$TFILE") or die "T1 file open failed: $!\n\n";
	$text = undef;
	{ local $/ = undef; $text = <T1>; }
	close(T1);
	
	my $len = length($text);
	my $i = 0;
	
	open (T, "+>$TFILE") or die "Temp open failed: $!\n\n";
	while ($i < $len) {
		print T substr($text, $i, $OSSLROWSIZE) . "\n";
		$i += $OSSLROWSIZE;
	}
	close (T);
	
	my $cmd = $OSSLCMD;
	$cmd =~ s/P_P/$pass/ig;
	$cmd =~ s/F_F/$TFILE/ig;
	$fname =~ s/(.*)___.*/$1/ig;
	$fname =~ s/.*\///ig;
	
	my $outfile = "$outdir/$fname";
	
	$cmd .= " > $outfile";
	print "Decrypting (stage two)... ";
	`$cmd`;
	
	unlink($TFILE);
	
	if (!($?>>8)) {
		print "Decoding...\n";	
		open (F2, "$outfile") or die "Can't open $outfile: $!\n\n";
		$text = undef;
		{ local $/ = undef; $text = <F2>; }
		close(F2);
		
		$text =~ s/data\:.*base64\,//ig;
		
		open (FINAL, "+>$outfile") or die "Can't open (+>) $outfile: $!\n\n";
		print FINAL decode_base64($text);
		close(FINAL);
		
		print "Successfully decrypted $fname into $outfile\n";
	}
	else { 
		print STDERR "Failure decrypting $fname\n"; 
	}
}