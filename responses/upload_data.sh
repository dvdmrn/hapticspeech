#!/bin/sh
echo enter username

read userName

scp -r $1 $userName@remote.cs.ubc.ca:/ubc/cs/research/imager/project/spin/proj/haptic-speech/data
