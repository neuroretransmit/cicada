#!/usr/bin/env perl

use strict;
use warnings;

use Crypt::RSA;
use Crypt::RSA::ES::OAEP;
use Crypt::RSA::Key::Private;
use Crypt::RSA::Key;
use Crypt::RSA::Primitives;
use Math::Pari ':int';

my $p = shift;
my $q = shift;

# Key recreation
my $keychain = new Crypt::RSA::Key;
my ($public, $key) = $keychain->generate(
	e => 65537,
	p => $p,
	q => $q,
	Verbosity => 1
) or die $keychain->errstr();

# Key info/verification
print "\ne: ".$key->e."\np: ".$key->p."\nq: ".$key->q."\n\nd: ".$key->d."\nn: ".$key->n."\nphi: ".$key->phi."\n";
print "\nKey check: OK\n" if $key->check();
# Save key to file
$key->write(Filename => "numbers.private");
$public->write(Filename => "numbers.public");
