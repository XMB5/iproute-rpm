# Makefile for source rpm: iproute
# $Id$
NAME := iproute
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
