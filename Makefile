# Makefile for source rpm: binutils
# $Id$
NAME := binutils
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
