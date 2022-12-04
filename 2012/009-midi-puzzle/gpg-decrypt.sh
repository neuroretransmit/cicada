#!/bin/sh

gpg --decrypt ./midi.asc > ./midi-first-unwrap.asc
gpg --decrypt ./midi-first-unwrap.asc > ./song.mid
