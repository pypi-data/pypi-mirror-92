#! /bin/sh
#
# Copyright by The HDF Group.
# Copyright by the Board of Trustees of the University of Illinois.
# All rights reserved.
#
# This file is part of HDF5.  The full HDF5 copyright notice, including
# terms governing use, modification, and redistribution, is contained in
# the COPYING file, which can be found at the root of the source code
# distribution tree, or in https://support.hdfgroup.org/ftp/HDF5/releases.
# If you do not have access to either file, you may request a copy from
# help@hdfgroup.org.
#
# Test for external file with environment variable: HDF5_VDS_PREFIX

srcdir=.

nerrors=0

##############################################################################
##############################################################################
###              T H E   T E S T S                                ###
##############################################################################
##############################################################################

# test for VDS with HDF5_VDS_PREFIX
echo "Testing basic virtual dataset I/O via H5Pset_vds_prefix(): all selection with ENV prefix"
TEST_NAME=vds_env                               # The test name
TEST_BIN=`pwd`/$TEST_NAME                       # The path of the test binary
ENVCMD="env HDF5_VDS_PREFIX=\${ORIGIN}/tmp_vds_env"     # Set the environment variable & value
UNENVCMD="unset HDF5_VDS_PREFIX"                # Unset the environment variable & value
#
# Run the test
# echo "$ENVCMD $RUNSERIAL $TEST_BIN"
$ENVCMD $RUNSERIAL $TEST_BIN
exitcode=$?
if [ $exitcode -eq 0 ]; then
        echo "Test prefix for HDF5_VDS_PREFIX PASSED"
    else
    nerrors="`expr $nerrors + 1`"
    echo "***Error encountered for HDF5_VDS_PREFIX test***"
fi
$UNENVCMD
exit $nerrors
