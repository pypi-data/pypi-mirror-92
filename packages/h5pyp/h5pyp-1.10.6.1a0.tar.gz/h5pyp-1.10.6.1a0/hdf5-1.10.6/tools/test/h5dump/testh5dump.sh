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
# Tests for the h5dump tool

srcdir=.

USE_FILTER_SZIP="no"
USE_FILTER_DEFLATE="yes"

TESTNAME=h5dump
EXIT_SUCCESS=0
EXIT_FAILURE=1

DUMPER=../../src/h5dump/h5dump                     # The tool name
DUMPER_BIN=`pwd`/$DUMPER          # The path of the tool binary

H5DIFF=../../src/h5diff/h5diff           # The h5diff tool name
H5DIFF_BIN=`pwd`/$H5DIFF          # The path of the h5diff  tool binary

H5IMPORT=../../src/h5import/h5import     # The h5import tool name
H5IMPORT_BIN=`pwd`/$H5IMPORT      # The path of the h5import  tool binary

RM='rm -rf'
CMP='cmp'
DIFF='diff -c'
GREP='grep'
CP='cp'
DIRNAME='dirname'
LS='ls'
AWK='awk'

# Skip plugin module to test missing filter
ENVCMD="env HDF5_PLUGIN_PRELOAD=::"

WORDS_BIGENDIAN="no"

nerrors=0
verbose=yes

# source dirs
SRC_TOOLS="$srcdir/../.."

SRC_TOOLS_TESTFILES="$SRC_TOOLS/testfiles"
# testfiles source dirs for tools
SRC_H5LS_TESTFILES="$SRC_TOOLS_TESTFILES"
SRC_H5DUMP_TESTFILES="$SRC_TOOLS_TESTFILES"
SRC_H5DUMP_ERRORFILES="$srcdir/errfiles"
SRC_H5DIFF_TESTFILES="$SRC_TOOLS/test/h5diff/testfiles"
SRC_H5COPY_TESTFILES="$SRC_TOOLS/test/h5copy/testfiles"
SRC_H5REPACK_TESTFILES="$SRC_TOOLS/test/h5repack/testfiles"
SRC_H5JAM_TESTFILES="$SRC_TOOLS/test/h5jam/testfiles"
SRC_H5STAT_TESTFILES="$SRC_TOOLS/test/h5stat/testfiles"
SRC_H5IMPORT_TESTFILES="$SRC_TOOLS/test/h5import/testfiles"

TEST_P_DIR=./testfiles
TESTDIR=./testfiles/std
test -d $TEST_P_DIR || mkdir -p $TEST_P_DIR
test -d $TESTDIR || mkdir -p $TESTDIR

######################################################################
# test files
# --------------------------------------------------------------------
# All the test files copy from source directory to test directory
# NOTE: Keep this framework to add/remove test files.
#       Any test files from other tools can be used in this framework.
#       This list are also used for checking exist.
#       Comment '#' without space can be used.
# --------------------------------------------------------------------
LIST_HDF5_TEST_FILES="
$SRC_H5DUMP_TESTFILES/charsets.h5
$SRC_H5DUMP_TESTFILES/file_space.h5
$SRC_H5DUMP_TESTFILES/filter_fail.h5
$SRC_H5DUMP_TESTFILES/packedbits.h5
$SRC_H5DUMP_TESTFILES/t128bit_float.h5
$SRC_H5DUMP_TESTFILES/taindices.h5
$SRC_H5DUMP_TESTFILES/tall.h5
$SRC_H5DUMP_TESTFILES/tarray1.h5
$SRC_H5DUMP_TESTFILES/tarray1_big.h5
$SRC_H5DUMP_TESTFILES/tarray2.h5
$SRC_H5DUMP_TESTFILES/tarray3.h5
$SRC_H5DUMP_TESTFILES/tarray4.h5
$SRC_H5DUMP_TESTFILES/tarray5.h5
$SRC_H5DUMP_TESTFILES/tarray6.h5
$SRC_H5DUMP_TESTFILES/tarray7.h5
$SRC_H5DUMP_TESTFILES/tarray8.h5
$SRC_H5DUMP_TESTFILES/tattr.h5
$SRC_H5DUMP_TESTFILES/tattr2.h5
$SRC_H5DUMP_TESTFILES/tattr4_be.h5
$SRC_H5DUMP_TESTFILES/tattrintsize.h5
$SRC_H5DUMP_TESTFILES/tattrreg.h5
$SRC_H5DUMP_TESTFILES/tbigdims.h5
$SRC_H5DUMP_TESTFILES/tbinary.h5
$SRC_H5DUMP_TESTFILES/tbitnopaque.h5
$SRC_H5DUMP_TESTFILES/tchar.h5
$SRC_H5DUMP_TESTFILES/tcmpdattrintsize.h5
$SRC_H5DUMP_TESTFILES/tcmpdintsize.h5
$SRC_H5DUMP_TESTFILES/tcompound.h5
$SRC_H5DUMP_TESTFILES/tcompound_complex.h5
$SRC_H5DUMP_TESTFILES/tcompound_complex2.h5
$SRC_H5DUMP_TESTFILES/tdatareg.h5
$SRC_H5DUMP_TESTFILES/tdset.h5
$SRC_H5DUMP_TESTFILES/tempty.h5
$SRC_H5DUMP_TESTFILES/tsoftlinks.h5
$SRC_H5DUMP_TESTFILES/textlinkfar.h5
$SRC_H5DUMP_TESTFILES/textlinksrc.h5
$SRC_H5DUMP_TESTFILES/textlinktar.h5
$SRC_H5DUMP_TESTFILES/textlink.h5
$SRC_H5DUMP_TESTFILES/tfamily00000.h5
$SRC_H5DUMP_TESTFILES/tfamily00001.h5
$SRC_H5DUMP_TESTFILES/tfamily00002.h5
$SRC_H5DUMP_TESTFILES/tfamily00003.h5
$SRC_H5DUMP_TESTFILES/tfamily00004.h5
$SRC_H5DUMP_TESTFILES/tfamily00005.h5
$SRC_H5DUMP_TESTFILES/tfamily00006.h5
$SRC_H5DUMP_TESTFILES/tfamily00007.h5
$SRC_H5DUMP_TESTFILES/tfamily00008.h5
$SRC_H5DUMP_TESTFILES/tfamily00009.h5
$SRC_H5DUMP_TESTFILES/tfamily00010.h5
$SRC_H5DUMP_TESTFILES/tfcontents1.h5
$SRC_H5DUMP_TESTFILES/tfcontents2.h5
$SRC_H5DUMP_TESTFILES/tfilters.h5
$SRC_H5DUMP_TESTFILES/tfpformat.h5
$SRC_H5DUMP_TESTFILES/tfvalues.h5
$SRC_H5DUMP_TESTFILES/tgroup.h5
$SRC_H5DUMP_TESTFILES/tgrp_comments.h5
$SRC_H5DUMP_TESTFILES/tgrpnullspace.h5
$SRC_H5DUMP_TESTFILES/thlink.h5
$SRC_H5DUMP_TESTFILES/thyperslab.h5
$SRC_H5DUMP_TESTFILES/tintsattrs.h5
$SRC_H5DUMP_TESTFILES/tints4dims.h5
$SRC_H5DUMP_TESTFILES/tlarge_objname.h5
#$SRC_H5DUMP_TESTFILES/tldouble.h5
$SRC_H5DUMP_TESTFILES/tlonglinks.h5
$SRC_H5DUMP_TESTFILES/tloop.h5
$SRC_H5DUMP_TESTFILES/tmulti-b.h5
$SRC_H5DUMP_TESTFILES/tmulti-g.h5
$SRC_H5DUMP_TESTFILES/tmulti-l.h5
$SRC_H5DUMP_TESTFILES/tmulti-o.h5
$SRC_H5DUMP_TESTFILES/tmulti-r.h5
$SRC_H5DUMP_TESTFILES/tmulti-s.h5
$SRC_H5DUMP_TESTFILES/tnamed_dtype_attr.h5
$SRC_H5DUMP_TESTFILES/tnestedcomp.h5
$SRC_H5DUMP_TESTFILES/tnestedcmpddt.h5
$SRC_H5DUMP_TESTFILES/tno-subset.h5
$SRC_H5DUMP_TESTFILES/tnullspace.h5
$SRC_H5DUMP_TESTFILES/zerodim.h5
$SRC_H5DUMP_TESTFILES/torderattr.h5
$SRC_H5DUMP_TESTFILES/tordergr.h5
$SRC_H5DUMP_TESTFILES/tsaf.h5
$SRC_H5DUMP_TESTFILES/tscalarattrintsize.h5
$SRC_H5DUMP_TESTFILES/tscalarintattrsize.h5
$SRC_H5DUMP_TESTFILES/tscalarintsize.h5
$SRC_H5DUMP_TESTFILES/tscalarstring.h5
$SRC_H5DUMP_TESTFILES/tslink.h5
$SRC_H5DUMP_TESTFILES/tsplit_file-m.h5
$SRC_H5DUMP_TESTFILES/tsplit_file-r.h5
$SRC_H5DUMP_TESTFILES/tstr.h5
$SRC_H5DUMP_TESTFILES/tstr2.h5
$SRC_H5DUMP_TESTFILES/tstr3.h5
$SRC_H5DUMP_TESTFILES/tudlink.h5
$SRC_H5DUMP_TESTFILES/tvldtypes1.h5
$SRC_H5DUMP_TESTFILES/tvldtypes2.h5
$SRC_H5DUMP_TESTFILES/tvldtypes3.h5
$SRC_H5DUMP_TESTFILES/tvldtypes4.h5
$SRC_H5DUMP_TESTFILES/tvldtypes5.h5
$SRC_H5DUMP_TESTFILES/tvlenstr_array.h5
$SRC_H5DUMP_TESTFILES/tvlstr.h5
$SRC_H5DUMP_TESTFILES/tvms.h5
"

LIST_OTHER_TEST_FILES="
$SRC_H5DUMP_TESTFILES/charsets.ddl
$SRC_H5DUMP_TESTFILES/file_space.ddl
$SRC_H5DUMP_TESTFILES/filter_fail.ddl
$SRC_H5DUMP_TESTFILES/non_existing.ddl
$SRC_H5DUMP_TESTFILES/packedbits.ddl
$SRC_H5DUMP_TESTFILES/tall-1.ddl
$SRC_H5DUMP_TESTFILES/tall-2.ddl
$SRC_H5DUMP_TESTFILES/tall-2A.ddl
$SRC_H5DUMP_TESTFILES/tall-2A0.ddl
$SRC_H5DUMP_TESTFILES/tall-2B.ddl
$SRC_H5DUMP_TESTFILES/tall-3.ddl
$SRC_H5DUMP_TESTFILES/tall-4s.ddl
$SRC_H5DUMP_TESTFILES/tall-5s.ddl
$SRC_H5DUMP_TESTFILES/tall-6.ddl
$SRC_H5DUMP_TESTFILES/tall-6.exp
$SRC_H5DUMP_TESTFILES/tall-7.ddl
$SRC_H5DUMP_TESTFILES/tall-7N.ddl
$SRC_H5DUMP_TESTFILES/tallfilters.ddl
$SRC_H5DUMP_TESTFILES/tarray1.ddl
$SRC_H5DUMP_TESTFILES/tarray1_big.ddl
$SRC_H5DUMP_TESTFILES/tarray2.ddl
$SRC_H5DUMP_TESTFILES/tarray3.ddl
$SRC_H5DUMP_TESTFILES/tarray4.ddl
$SRC_H5DUMP_TESTFILES/tarray5.ddl
$SRC_H5DUMP_TESTFILES/tarray6.ddl
$SRC_H5DUMP_TESTFILES/tarray7.ddl
$SRC_H5DUMP_TESTFILES/tarray8.ddl
$SRC_H5DUMP_TESTFILES/tattr-1.ddl
$SRC_H5DUMP_TESTFILES/tattr-2.ddl
$SRC_H5DUMP_TESTFILES/tattr-3.ddl
$SRC_H5DUMP_TESTFILES/tattr-4_be.ddl
$SRC_H5DUMP_TESTFILES/tattrcontents1.ddl
$SRC_H5DUMP_TESTFILES/tattrcontents2.ddl
$SRC_H5DUMP_TESTFILES/tattrintsize.ddl
$SRC_H5DUMP_TESTFILES/tattrreg.ddl
$SRC_H5DUMP_TESTFILES/tattrregR.ddl
$SRC_H5DUMP_TESTFILES/tbin1.ddl
$SRC_H5DUMP_TESTFILES/tbin1.ddl
$SRC_H5DUMP_TESTFILES/tbin2.ddl
$SRC_H5DUMP_TESTFILES/tbin3.ddl
$SRC_H5DUMP_TESTFILES/tbin4.ddl
$SRC_H5DUMP_TESTFILES/tbinregR.ddl
$SRC_H5DUMP_TESTFILES/tbigdims.ddl
$SRC_H5DUMP_TESTFILES/tbitnopaque_be.ddl
$SRC_H5DUMP_TESTFILES/tbitnopaque_le.ddl
$SRC_H5DUMP_TESTFILES/tboot1.ddl
$SRC_H5DUMP_TESTFILES/tboot2.ddl
$SRC_H5DUMP_TESTFILES/tboot2A.ddl
$SRC_H5DUMP_TESTFILES/tboot2B.ddl
$SRC_H5DUMP_TESTFILES/tchar1.ddl
$SRC_H5DUMP_TESTFILES/tchunked.ddl
$SRC_H5DUMP_TESTFILES/tcmpdattrintsize.ddl
$SRC_H5DUMP_TESTFILES/tcmpdintsize.ddl
$SRC_H5DUMP_TESTFILES/tcomp-1.ddl
$SRC_H5DUMP_TESTFILES/tcomp-2.ddl
$SRC_H5DUMP_TESTFILES/tcomp-3.ddl
$SRC_H5DUMP_TESTFILES/tcomp-4.ddl
$SRC_H5DUMP_TESTFILES/tcompound_complex2.ddl
$SRC_H5DUMP_TESTFILES/tcompact.ddl
$SRC_H5DUMP_TESTFILES/tcontents.ddl
$SRC_H5DUMP_TESTFILES/tcontiguos.ddl
$SRC_H5DUMP_TESTFILES/tdatareg.ddl
$SRC_H5DUMP_TESTFILES/tdataregR.ddl
$SRC_H5DUMP_TESTFILES/tdeflate.ddl
$SRC_H5DUMP_TESTFILES/tdset-1.ddl
$SRC_H5DUMP_TESTFILES/tdset-2.ddl
$SRC_H5DUMP_TESTFILES/tdset-3s.ddl
$SRC_H5DUMP_TESTFILES/tempty.ddl
$SRC_H5DUMP_TESTFILES/texceedsubstart.ddl
$SRC_H5DUMP_TESTFILES/texceedsubcount.ddl
$SRC_H5DUMP_TESTFILES/texceedsubstride.ddl
$SRC_H5DUMP_TESTFILES/texceedsubblock.ddl
$SRC_H5DUMP_TESTFILES/texternal.ddl
$SRC_H5DUMP_TESTFILES/textlinksrc.ddl
$SRC_H5DUMP_TESTFILES/textlinkfar.ddl
$SRC_H5DUMP_TESTFILES/textlink.ddl
$SRC_H5DUMP_TESTFILES/tfamily.ddl
$SRC_H5DUMP_TESTFILES/tfill.ddl
$SRC_H5DUMP_TESTFILES/tfletcher32.ddl
$SRC_H5DUMP_TESTFILES/tfpformat.ddl
$SRC_H5DUMP_TESTFILES/tgroup-1.ddl
$SRC_H5DUMP_TESTFILES/tgroup-2.ddl
$SRC_H5DUMP_TESTFILES/tgrp_comments.ddl
$SRC_H5DUMP_TESTFILES/tgrpnullspace.ddl
$SRC_H5DUMP_TESTFILES/thlink-1.ddl
$SRC_H5DUMP_TESTFILES/thlink-2.ddl
$SRC_H5DUMP_TESTFILES/thlink-3.ddl
$SRC_H5DUMP_TESTFILES/thlink-4.ddl
$SRC_H5DUMP_TESTFILES/thlink-5.ddl
$SRC_H5DUMP_TESTFILES/thyperslab.ddl
$SRC_H5DUMP_TESTFILES/tindicesno.ddl
$SRC_H5DUMP_TESTFILES/tindicessub1.ddl
$SRC_H5DUMP_TESTFILES/tindicessub2.ddl
$SRC_H5DUMP_TESTFILES/tindicessub3.ddl
$SRC_H5DUMP_TESTFILES/tindicessub4.ddl
$SRC_H5DUMP_TESTFILES/tindicesyes.ddl
$SRC_H5DUMP_TESTFILES/tints4dims.ddl
$SRC_H5DUMP_TESTFILES/tints4dimsBlock2.ddl
$SRC_H5DUMP_TESTFILES/tints4dimsBlockEq.ddl
$SRC_H5DUMP_TESTFILES/tints4dimsCount2.ddl
$SRC_H5DUMP_TESTFILES/tints4dimsCountEq.ddl
$SRC_H5DUMP_TESTFILES/tints4dimsStride2.ddl
$SRC_H5DUMP_TESTFILES/tintsattrs.ddl
$SRC_H5DUMP_TESTFILES/tlarge_objname.ddl
#$SRC_H5DUMP_TESTFILES/tldouble.ddl
$SRC_H5DUMP_TESTFILES/tlonglinks.ddl
$SRC_H5DUMP_TESTFILES/tloop-1.ddl
$SRC_H5DUMP_TESTFILES/tmulti.ddl
$SRC_H5DUMP_TESTFILES/tmultifile.ddl
$SRC_H5DUMP_TESTFILES/tqmarkfile.ddl
$SRC_H5DUMP_TESTFILES/tstarfile.ddl
$SRC_H5DUMP_TESTFILES/tnamed_dtype_attr.ddl
$SRC_H5DUMP_TESTFILES/tnestcomp-1.ddl
$SRC_H5DUMP_TESTFILES/tnestedcmpddt.ddl
$SRC_H5DUMP_TESTFILES/tnbit.ddl
$SRC_H5DUMP_TESTFILES/tnoattrdata.ddl
$SRC_H5DUMP_TESTFILES/tnoattrddl.ddl
$SRC_H5DUMP_TESTFILES/tnodata.ddl
$SRC_H5DUMP_TESTFILES/tnoddl.ddl
$SRC_H5DUMP_TESTFILES/tnoddlfile.ddl
$SRC_H5DUMP_TESTFILES/tnoddlfile.exp
$SRC_H5DUMP_TESTFILES/tno-subset.ddl
$SRC_H5DUMP_TESTFILES/tnullspace.ddl
$SRC_H5DUMP_TESTFILES/trawdatafile.ddl
$SRC_H5DUMP_TESTFILES/trawdatafile.exp
$SRC_H5DUMP_TESTFILES/trawssetfile.ddl
$SRC_H5DUMP_TESTFILES/trawssetfile.exp
$SRC_H5DUMP_TESTFILES/zerodim.ddl
$SRC_H5DUMP_TESTFILES/tordergr1.ddl
$SRC_H5DUMP_TESTFILES/tordergr2.ddl
$SRC_H5DUMP_TESTFILES/tordergr3.ddl
$SRC_H5DUMP_TESTFILES/tordergr4.ddl
$SRC_H5DUMP_TESTFILES/tordergr5.ddl
$SRC_H5DUMP_TESTFILES/torderattr1.ddl
$SRC_H5DUMP_TESTFILES/torderattr2.ddl
$SRC_H5DUMP_TESTFILES/torderattr3.ddl
$SRC_H5DUMP_TESTFILES/torderattr4.ddl
$SRC_H5DUMP_TESTFILES/tordercontents1.ddl
$SRC_H5DUMP_TESTFILES/tordercontents2.ddl
$SRC_H5DUMP_TESTFILES/torderlinks1.ddl
$SRC_H5DUMP_TESTFILES/torderlinks2.ddl
$SRC_H5DUMP_TESTFILES/tperror.ddl
$SRC_H5DUMP_TESTFILES/treadfilter.ddl
$SRC_H5DUMP_TESTFILES/treadintfilter.ddl
$SRC_H5DUMP_TESTFILES/treference.ddl
$SRC_H5DUMP_TESTFILES/tsaf.ddl
$SRC_H5DUMP_TESTFILES/tscalarattrintsize.ddl
$SRC_H5DUMP_TESTFILES/tscalarintattrsize.ddl
$SRC_H5DUMP_TESTFILES/tscalarintsize.ddl
$SRC_H5DUMP_TESTFILES/tscalarstring.ddl
$SRC_H5DUMP_TESTFILES/tscaleoffset.ddl
$SRC_H5DUMP_TESTFILES/tshuffle.ddl
$SRC_H5DUMP_TESTFILES/tslink-1.ddl
$SRC_H5DUMP_TESTFILES/tslink-2.ddl
$SRC_H5DUMP_TESTFILES/tslink-D.ddl
$SRC_H5DUMP_TESTFILES/tsplit_file.ddl
$SRC_H5DUMP_TESTFILES/tstr-1.ddl
$SRC_H5DUMP_TESTFILES/tstr-2.ddl
$SRC_H5DUMP_TESTFILES/tstr2bin2.exp
$SRC_H5DUMP_TESTFILES/tstr2bin6.exp
$SRC_H5DUMP_TESTFILES/tstring.ddl
$SRC_H5DUMP_TESTFILES/tstring2.ddl
$SRC_H5DUMP_TESTFILES/tstringe.ddl
$SRC_H5DUMP_TESTFILES/tszip.ddl
$SRC_H5DUMP_TESTFILES/tudlink-1.ddl
$SRC_H5DUMP_TESTFILES/tudlink-2.ddl
$SRC_H5DUMP_TESTFILES/tuserfilter.ddl
$SRC_H5DUMP_TESTFILES/tvldtypes1.ddl
$SRC_H5DUMP_TESTFILES/tvldtypes2.ddl
$SRC_H5DUMP_TESTFILES/tvldtypes3.ddl
$SRC_H5DUMP_TESTFILES/tvldtypes4.ddl
$SRC_H5DUMP_TESTFILES/tvldtypes5.ddl
$SRC_H5DUMP_TESTFILES/tvlenstr_array.ddl
$SRC_H5DUMP_TESTFILES/tvlstr.ddl
$SRC_H5DUMP_TESTFILES/tvms.ddl
$SRC_H5DUMP_TESTFILES/twidedisplay.ddl
$SRC_H5DUMP_TESTFILES/twithddl.exp
$SRC_H5DUMP_TESTFILES/twithddlfile.ddl
$SRC_H5DUMP_TESTFILES/twithddlfile.exp
$SRC_H5DUMP_TESTFILES/h5dump-help.txt
$SRC_H5DUMP_TESTFILES/out3.h5import
$SRC_H5DUMP_TESTFILES/tbinregR.exp
"

LIST_ERROR_TEST_FILES="
${SRC_H5DUMP_ERRORFILES}/filter_fail.err
${SRC_H5DUMP_ERRORFILES}/non_existing.err
${SRC_H5DUMP_ERRORFILES}/tall-1.err
${SRC_H5DUMP_ERRORFILES}/tall-2A.err
${SRC_H5DUMP_ERRORFILES}/tall-2A0.err
${SRC_H5DUMP_ERRORFILES}/tall-2B.err
${SRC_H5DUMP_ERRORFILES}/tarray1_big.err
${SRC_H5DUMP_ERRORFILES}/tattr-3.err
${SRC_H5DUMP_ERRORFILES}/tattrregR.err
${SRC_H5DUMP_ERRORFILES}/tcomp-3.err
${SRC_H5DUMP_ERRORFILES}/tdataregR.err
${SRC_H5DUMP_ERRORFILES}/tdset-2.err
${SRC_H5DUMP_ERRORFILES}/texceedsubblock.err
${SRC_H5DUMP_ERRORFILES}/texceedsubcount.err
${SRC_H5DUMP_ERRORFILES}/texceedsubstart.err
${SRC_H5DUMP_ERRORFILES}/texceedsubstride.err
${SRC_H5DUMP_ERRORFILES}/textlink.err
${SRC_H5DUMP_ERRORFILES}/textlinkfar.err
${SRC_H5DUMP_ERRORFILES}/textlinksrc.err
${SRC_H5DUMP_ERRORFILES}/tgroup-2.err
${SRC_H5DUMP_ERRORFILES}/torderlinks1.err
${SRC_H5DUMP_ERRORFILES}/torderlinks2.err
${SRC_H5DUMP_ERRORFILES}/tperror.err
${SRC_H5DUMP_ERRORFILES}/tqmarkfile.err
${SRC_H5DUMP_ERRORFILES}/tslink-D.err
"

#
# copy test files and expected output files from source dirs to test dir
#
COPY_TESTFILES="$LIST_HDF5_TEST_FILES $LIST_OTHER_TEST_FILES $LIST_ERROR_TEST_FILES"

COPY_TESTFILES_TO_TESTDIR()
{
    # copy test files. Used -f to make sure get a new copy
    for tstfile in $COPY_TESTFILES
    do
        # ignore '#' comment
        echo $tstfile | tr -d ' ' | grep '^#' > /dev/null
        RET=$?
        if [ $RET -eq 1 ]; then
            # skip cp if srcdir is same as destdir
            # this occurs when build/test performed in source dir and
            # make cp fail
            SDIR=`$DIRNAME $tstfile`
            INODE_SDIR=`$LS -i -d $SDIR | $AWK -F' ' '{print $1}'`
            INODE_DDIR=`$LS -i -d $TESTDIR | $AWK -F' ' '{print $1}'`
            if [ "$INODE_SDIR" != "$INODE_DDIR" ]; then
                $CP -f $tstfile $TESTDIR
                if [ $? -ne 0 ]; then
                    echo "Error: FAILED to copy $tstfile ."

                    # Comment out this to CREATE expected file
                    exit $EXIT_FAILURE
                fi
            fi
        fi
    done
}

CLEAN_TESTFILES_AND_TESTDIR()
{
    # skip rm if srcdir is same as destdir
    # this occurs when build/test performed in source dir and
    # make cp fail
    SDIR=$SRC_H5DUMP_TESTFILES
    INODE_SDIR=`$LS -i -d $SDIR | $AWK -F' ' '{print $1}'`
    INODE_DDIR=`$LS -i -d $TESTDIR | $AWK -F' ' '{print $1}'`
    if [ "$INODE_SDIR" != "$INODE_DDIR" ]; then
        $RM $TESTDIR
    fi
}

# Print a line-line message left justified in a field of 70 characters
# beginning with the word "Testing".
#
TESTING() {
   SPACES="                                                               "
   echo "Testing $* $SPACES" | cut -c1-70 | tr -d '\012'
}

# Source in the output filter function definitions.
. $srcdir/../../../bin/output_filter.sh

# Run a test and print PASS or *FAIL*.  If a test fails then increment
# the `nerrors' global variable and (if $verbose is set) display the
# difference between the actual output and the expected output. The
# expected output is given as the first argument to this function and
# the actual output file is calculated by replacing the `.ddl' with
# `.out'.  The actual output is not removed if $HDF5_NOCLEANUP has a
# non-zero value.
# If $1 == ignorecase then do caseless CMP and DIFF.
# ADD_H5_TEST
TOOLTEST() {
    # check if caseless compare and diff requested
    if [ "$1" = ignorecase ]; then
    caseless="-i"
    # replace cmp with diff which runs much longer.
    xCMP="$DIFF -i"
    shift
    else
    caseless=""
    # stick with faster cmp if ignorecase is not requested.
    xCMP="$CMP"
    fi

    expect="$TESTDIR/$1"
    actual="$TESTDIR/`basename $1 .ddl`.out"
    actual_err="$TESTDIR/`basename $1 .ddl`.err"
    actual_sav=${actual}-sav
    actual_err_sav=${actual_err}-sav
    shift

    # Run test.
    TESTING $DUMPER $@
    (
    cd $TESTDIR
      $RUNSERIAL $DUMPER_BIN "$@"
    ) >$actual 2>$actual_err

    # save actual and actual_err in case they are needed later.
    cp $actual $actual_sav
    STDOUT_FILTER $actual
    cp $actual_err $actual_err_sav
    STDERR_FILTER $actual_err

  if [ ! -f $expect ]; then
    # Create the expect file if it doesn't yet exist.
     echo " CREATED"
     cp $actual $expect
     echo "    Expected result (*.ddl) missing"
     nerrors="`expr $nerrors + 1`"
    elif $xCMP $expect $actual > /dev/null 2>&1 ; then
     echo " PASSED"
    else
     echo "*FAILED*"
     echo "    Expected result (*.ddl) differs from actual result (*.out)"
     nerrors="`expr $nerrors + 1`"
     test yes = "$verbose" && $DIFF $caseless $expect $actual |sed 's/^/    /'
    fi

    # Clean up output file
    if test -z "$HDF5_NOCLEANUP"; then
     rm -f $actual $actual_err $actual_sav $actual_err_sav $actual_ext
    fi

}


# same as TOOLTEST1 but compares generated file to expected output
#                   and compares the generated data file to the expected data file
# used for the binary tests that expect a full path in -o without -b
# ADD_H5_EXPORT_TEST
TOOLTEST2() {

    expectdata="$TESTDIR/$1"
    expect="$TESTDIR/`basename $1 .exp`.ddl"
    actualdata="$TESTDIR/`basename $1 .exp`.txt"
    actual="$TESTDIR/`basename $1 .exp`.out"
    actual_err="$TESTDIR/`basename $1 .exp`.err"
    shift

    # Run test.
    TESTING $DUMPER $@
    (
      cd $TESTDIR
      $RUNSERIAL $DUMPER_BIN "$@"
    ) >$actual 2>$actual_err

    if [ ! -f $expect ]; then
    # Create the expect file if it doesn't yet exist.
     echo " CREATED"
     cp $actual $expect
     echo "    Expected result (*.ddl) missing"
     nerrors="`expr $nerrors + 1`"
    elif $CMP $expect $actual; then
      if [ ! -f $expectdata ]; then
      # Create the expect data file if it doesn't yet exist.
        echo " CREATED"
        cp $actualdata $expectdata
        echo "    Expected data (*.exp) missing"
        nerrors="`expr $nerrors + 1`"
      elif $CMP $expectdata $actualdata; then
        echo " PASSED"
      else
        echo "*FAILED*"
        echo "    Expected datafile (*.exp) differs from actual datafile (*.txt)"
        nerrors="`expr $nerrors + 1`"
        test yes = "$verbose" && $DIFF $expectdata $actualdata |sed 's/^/    /'
      fi
    else
     echo "*FAILED*"
     echo "    Expected result (*.ddl) differs from actual result (*.out)"
     nerrors="`expr $nerrors + 1`"
     test yes = "$verbose" && $DIFF $expect $actual |sed 's/^/    /'
    fi

    # Clean up output file
    if test -z "$HDF5_NOCLEANUP"; then
     rm -f $actual $actualdata $actual_err
    fi

}

# same as TOOLTEST2 but compares generated file to expected ddl file
#                   and compares the generated data file to the expected data file
# used for the binary tests that expect a full path in -o without -b
# ADD_H5_TEST_EXPORT
TOOLTEST2A() {

    expectdata="$TESTDIR/$1"
    expect="$TESTDIR/`basename $1 .exp`.ddl"
    actualdata="$TESTDIR/`basename $1 .exp`.txt"
    actual="$TESTDIR/`basename $1 .exp`.out"
    actual_err="$TESTDIR/`basename $1 .exp`.err"
    shift
    expectmeta="$TESTDIR/$1"
    actualmeta="$TESTDIR/`basename $1 .exp`.txt"
    shift

    # Run test.
    TESTING $DUMPER $@
    (
      cd $TESTDIR
      $RUNSERIAL $DUMPER_BIN "$@"
    ) >$actual 2>$actual_err

    if [ ! -f $expect ]; then
    # Create the expect file if it doesn't yet exist.
     echo " CREATED"
     cp $actual $expect
     echo "    Expected result (*.ddl) missing"
     nerrors="`expr $nerrors + 1`"
    elif $CMP $expect $actual; then
      if [ ! -f $expectdata ]; then
      # Create the expect data file if it doesn't yet exist.
        echo " CREATED"
        cp $actualdata $expectdata
        echo "    Expected data (*.exp) missing"
        nerrors="`expr $nerrors + 1`"
      elif $DIFF $expectdata $actualdata; then
        if [ ! -f $expectmeta ]; then
        # Create the expect meta file if it doesn't yet exist.
          echo " CREATED"
          cp $actualmeta $expectmeta
          echo "    Expected metafile (*.ddl) missing"
          nerrors="`expr $nerrors + 1`"
        elif $CMP $expectmeta $actualmeta; then
          echo " PASSED"
        else
          echo "*FAILED*"
          echo "    Expected metafile (*.ddl) differs from actual metafile (*.txt)"
          nerrors="`expr $nerrors + 1`"
          test yes = "$verbose" && $DIFF $expectmeta $actualmeta |sed 's/^/    /'
        fi
      else
        echo "*FAILED*"
        echo "    Expected datafile (*.exp) differs from actual datafile (*.txt)"
        nerrors="`expr $nerrors + 1`"
        test yes = "$verbose" && $DIFF $expectdata $actualdata |sed 's/^/    /'
      fi
    else
     echo "*FAILED*"
     echo "    Expected result (*.ddl) differs from actual result (*.out)"
     nerrors="`expr $nerrors + 1`"
     test yes = "$verbose" && $DIFF $expect $actual |sed 's/^/    /'
    fi

    # Clean up output file
    if test -z "$HDF5_NOCLEANUP"; then
     rm -f $actual $actualdata $actual_err $actualmeta
    fi

}

# same as TOOLTEST2 but only compares the generated data file to the expected data file
# used for the binary tests that expect a full path in -o with -b
# ADD_H5_EXPORT_TEST
TOOLTEST2B() {

    expectdata="$TESTDIR/$1"
    actualdata="$TESTDIR/`basename $1 .exp`.txt"
    actual="$TESTDIR/`basename $1 .exp`.out"
    actual_err="$TESTDIR/`basename $1 .exp`.err"
    shift

    # Run test.
    TESTING $DUMPER $@
    (
      cd $TESTDIR
      $RUNSERIAL $DUMPER_BIN "$@"
    ) >$actual 2>$actual_err

    if [ ! -f $expectdata ]; then
    # Create the expect data file if it doesn't yet exist.
      echo " CREATED"
      cp $actualdata $expectdata
      echo "    Expected data (*.exp) missing"
      nerrors="`expr $nerrors + 1`"
    elif $CMP $expectdata $actualdata; then
      echo " PASSED"
    else
      echo "*FAILED*"
      echo "    Expected datafile (*.exp) differs from actual datafile (*.txt)"
      nerrors="`expr $nerrors + 1`"
      test yes = "$verbose" && $DIFF $expectdata $actualdata |sed 's/^/    /'
    fi

    # Clean up output file
    if test -z "$HDF5_NOCLEANUP"; then
     rm -f $actual $actualdata $actual_err
    fi

}

# same as TOOLTEST but filters error stack outp
# Extract file name, line number, version and thread IDs because they may be different
TOOLTEST3() {

    expect="$TESTDIR/$1"
    actual="$TESTDIR/`basename $1 .ddl`.out"
    actual_err="$TESTDIR/`basename $1 .ddl`.err"
    actual_ext="$TESTDIR/`basename $1 .ddl`.ext"
    actual_sav=${actual}-sav
    actual_err_sav=${actual_err}-sav
    shift

    # Run test.
    TESTING $DUMPER $@
    (
      cd $TESTDIR
      $RUNSERIAL $DUMPER_BIN "$@"
    ) >$actual 2>$actual_err

    # save actual and actual_err in case they are needed later.
    cp $actual $actual_sav
    STDOUT_FILTER $actual
    cp $actual_err $actual_err_sav
    STDERR_FILTER $actual_err

    # Extract file name, line number, version and thread IDs because they may be different
    sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
        -e 's/line [0-9]*/line (number)/' \
        -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
        -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
        -e 's/H5Eget_auto[1-2]*/H5Eget_auto(1 or 2)/' \
        -e 's/H5Eset_auto[1-2]*/H5Eset_auto(1 or 2)/' \
     $actual_err > $actual_ext

    if [ ! -f $expect ]; then
    # Create the expect file if it doesn't yet exist.
     echo " CREATED"
     cp $actual $expect
     echo "    Expected result (*.ddl) missing"
     nerrors="`expr $nerrors + 1`"
    elif $CMP $expect $actual; then
     echo " PASSED"
    else
     echo "*FAILED*"
     echo "    Expected result (*.ddl) differs from actual result (*.out)"
     nerrors="`expr $nerrors + 1`"
     test yes = "$verbose" && $DIFF $expect $actual |sed 's/^/    /'
    fi

    # Clean up output file
    if test -z "$HDF5_NOCLEANUP"; then
   rm -f $actual $actual_err $actual_sav $actual_err_sav
    fi

}

# same as TOOLTEST3 but filters error stack output and compares to an error file
# Extract file name, line number, version and thread IDs because they may be different
# ADD_H5ERR_MASK_TEST
TOOLTEST4() {

    expect="$TESTDIR/$1"
    expect_err="$TESTDIR/`basename $1 .ddl`.err"
    actual="$TESTDIR/`basename $1 .ddl`.out"
    actual_err="$TESTDIR/`basename $1 .ddl`.oerr"
    actual_ext="$TESTDIR/`basename $1 .ddl`.ext"
    actual_sav=${actual}-sav
    actual_err_sav=${actual_err}-sav
    shift

    # Run test.
    TESTING $DUMPER $@
    (
      cd $TESTDIR
      $ENVCMD $RUNSERIAL $DUMPER_BIN "$@"
    ) >$actual 2>$actual_err

    # save actual and actual_err in case they are needed later.
    cp $actual $actual_sav
    STDOUT_FILTER $actual
    cp $actual_err $actual_err_sav
    STDERR_FILTER $actual_err

    # Extract file name, line number, version and thread IDs because they may be different
    sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
        -e 's/line [0-9]*/line (number)/' \
        -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
        -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
        -e 's/H5Eget_auto[1-2]*/H5Eget_auto(1 or 2)/' \
        -e 's/H5Eset_auto[1-2]*/H5Eset_auto(1 or 2)/' \
     $actual_err > $actual_ext

    if [ ! -f $expect ]; then
    # Create the expect file if it doesn't yet exist.
     echo " CREATED"
     cp $actual $expect
     echo "    Expected result (*.ddl) missing"
     nerrors="`expr $nerrors + 1`"
    elif $CMP $expect $actual; then
     if $CMP $expect_err $actual_ext; then
      echo " PASSED"
     else
      echo "*FAILED*"
      echo "    Expected result (*.err) differs from actual result (*.oerr)"
      nerrors="`expr $nerrors + 1`"
      test yes = "$verbose" && $DIFF $expect_err $actual_ext |sed 's/^/    /'
     fi
    else
     echo "*FAILED*"
     echo "    Expected result (*.ddl) differs from actual result (*.out)"
     nerrors="`expr $nerrors + 1`"
     test yes = "$verbose" && $DIFF $expect $actual |sed 's/^/    /'
    fi

    # Clean up output file
    if test -z "$HDF5_NOCLEANUP"; then
   rm -f $actual $actual_err $actual_sav $actual_err_sav
    fi

}

# same as TOOLTEST4 but disables plugin filter loading
# silences extra error output on some platforms
# ADD_H5ERR_MASK_TEST
TOOLTEST5() {

    expect="$TESTDIR/$1"
    expect_err="$TESTDIR/`basename $1 .ddl`.err"
    actual="$TESTDIR/`basename $1 .ddl`.out"
    actual_err="$TESTDIR/`basename $1 .ddl`.oerr"
    actual_ext="$TESTDIR/`basename $1 .ddl`.ext"
    actual_sav=${actual}-sav
    actual_err_sav=${actual_err}-sav
    shift

    # Run test.
    TESTING $DUMPER $@
    (
      cd $TESTDIR
      $ENVCMD $RUNSERIAL $DUMPER_BIN "$@"
    ) >$actual 2>$actual_err

    # save actual and actual_err in case they are needed later.
    cp $actual $actual_sav
    STDOUT_FILTER $actual
    cp $actual_err $actual_err_sav
    STDERR_FILTER $actual_err

    # Extract file name, line number, version and thread IDs because they may be different
    sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
        -e 's/line [0-9]*/line (number)/' \
        -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
        -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
        -e 's/H5Eget_auto[1-2]*/H5Eget_auto(1 or 2)/' \
        -e 's/H5Eset_auto[1-2]*/H5Eset_auto(1 or 2)/' \
     $actual_err > $actual_ext

    if [ ! -f $expect ]; then
    # Create the expect file if it doesn't yet exist.
     echo " CREATED"
     cp $actual $expect
     echo "    Expected result (*.ddl) missing"
     nerrors="`expr $nerrors + 1`"
    elif $CMP $expect $actual; then
     if $CMP $expect_err $actual_ext; then
      echo " PASSED"
     else
      echo "*FAILED*"
      echo "    Expected result (*.err) differs from actual result (*.oerr)"
      nerrors="`expr $nerrors + 1`"
      test yes = "$verbose" && $DIFF $expect_err $actual_ext |sed 's/^/    /'
     fi
    else
     echo "*FAILED*"
     echo "    Expected result (*.ddl) differs from actual result (*.out)"
     nerrors="`expr $nerrors + 1`"
     test yes = "$verbose" && $DIFF $expect $actual |sed 's/^/    /'
    fi

    # Clean up output file
    if test -z "$HDF5_NOCLEANUP"; then
   rm -f $actual $actual_err $actual_sav $actual_err_sav
    fi

}
# ADD_HELP_TEST
TOOLTEST_HELP() {

    expect="$TESTDIR/$1"
    actual="$TESTDIR/`basename $1 .txt`.out"
    actual_err="$TESTDIR/`basename $1 .txt`.err"
    shift

    # Run test.
    TESTING $DUMPER $@
    (
      cd $TESTDIR
      $RUNSERIAL $DUMPER_BIN "$@"
    ) >$actual 2>$actual_err

    if [ ! -f $expectdata ]; then
    # Create the expect data file if it doesn't yet exist.
      echo " CREATED"
      cp $actual $expect-CREATED
      echo "    Expected output (*.txt) missing"
      nerrors="`expr $nerrors + 1`"
    elif $CMP $expect $actual; then
      echo " PASSED"
    else
      echo "*FAILED*"
      echo "    Expected output (*.txt) differs from actual output (*.out)"
      nerrors="`expr $nerrors + 1`"
    fi

    # Clean up output file
    if test -z "$HDF5_NOCLEANUP"; then
     rm -f $actual $actual_err
    fi

}

# Call the h5dump tool and grep for a value
#
GREPTEST()
{
    expectdata=$1
    actual=$TESTDIR/$2
    actual_err="$TESTDIR/`basename $2 .ddl`.oerr"
    shift
    shift

    # Run test.
    TESTING $DUMPER -p $@
    (
      cd $TESTDIR
      $ENVCMD $RUNSERIAL $DUMPER_BIN -p "$@"
    ) >$actual 2>$actual_err
    $GREP $expectdata $actual > /dev/null
    if [ $? -eq 0 ]; then
        echo " PASSED"
    else
        echo " FAILED"
        nerrors="`expr $nerrors + 1`"
    fi

    # Clean up output file
    if test -z "$HDF5_NOCLEANUP"; then
     rm -f $actual $actual_err
    fi
}

# Print a "SKIP" message
SKIP() {
   TESTING $DUMPER $@
    echo  " -SKIP-"
}

# Print a line-line message left justified in a field of 70 characters
#
PRINT_H5DIFF() {
 SPACES="                                                               "
 echo " Running h5diff $* $SPACES" | cut -c1-70 | tr -d '\012'
}


# Call the h5diff tool
#
DIFFTEST()
{
    PRINT_H5DIFF  $@
    (
  cd $TESTDIR
  $RUNSERIAL $H5DIFF_BIN "$@" -q
    )
    RET=$?
    if [ $RET != 0 ] ; then
         echo "*FAILED*"
         nerrors="`expr $nerrors + 1`"
    else
         echo " PASSED"
    fi

}

# Print a line-line message left justified in a field of 70 characters
# beginning with the word "Verifying".
#
PRINT_H5IMPORT() {
 SPACES="                                                               "
 echo " Running h5import $* $SPACES" | cut -c1-70 | tr -d '\012'
}

# Call the h5import tool
#
IMPORTTEST()
{
    # remove the output hdf5 file if it exists
    hdf5_file="$TESTDIR/$5"
    if [ -f $hdf5_file ]; then
     rm -f $hdf5_file
    fi

    PRINT_H5IMPORT  $@
    (
  cd $TESTDIR
  $RUNSERIAL $H5IMPORT_BIN "$@"
    )
    RET=$?
    if [ $RET != 0 ] ; then
         echo "*FAILED*"
         nerrors="`expr $nerrors + 1`"
    else
         echo " PASSED"
    fi

}


##############################################################################
##############################################################################
###        T H E   T E S T S                                               ###
##############################################################################
##############################################################################
# prepare for test
COPY_TESTFILES_TO_TESTDIR

TOOLTEST_HELP h5dump-help.txt -h

# test data output redirection
TOOLTEST tnoddl.ddl --enable-error-stack --ddl -y packedbits.h5
TOOLTEST tnodata.ddl --enable-error-stack --output packedbits.h5
TOOLTEST tnoattrddl.ddl --enable-error-stack -O -y tattr.h5
TOOLTEST tnoattrdata.ddl --enable-error-stack -A -o tattr.h5
TOOLTEST2 trawdatafile.exp --enable-error-stack -y -o trawdatafile.txt packedbits.h5
TOOLTEST2 tnoddlfile.exp --enable-error-stack -O -y -o tnoddlfile.txt packedbits.h5
TOOLTEST2A twithddlfile.exp twithddl.exp --enable-error-stack --ddl=twithddl.txt -y -o twithddlfile.txt packedbits.h5
TOOLTEST2 trawssetfile.exp --enable-error-stack -d "/dset1[1,1;;;]" -y -o trawssetfile.txt tdset.h5

# test for maximum display datasets
TOOLTEST twidedisplay.ddl --enable-error-stack -w0 packedbits.h5

# test for signed/unsigned datasets
TOOLTEST packedbits.ddl --enable-error-stack packedbits.h5
# test for compound signed/unsigned datasets
TOOLTEST tcmpdintsize.ddl --enable-error-stack tcmpdintsize.h5
# test for signed/unsigned scalar datasets
TOOLTEST tscalarintsize.ddl --enable-error-stack tscalarintsize.h5
# test for signed/unsigned attributes
TOOLTEST tattrintsize.ddl --enable-error-stack tattrintsize.h5
# test for compound signed/unsigned attributes
TOOLTEST tcmpdattrintsize.ddl --enable-error-stack tcmpdattrintsize.h5
# test for signed/unsigned scalar attributes
TOOLTEST tscalarattrintsize.ddl --enable-error-stack tscalarattrintsize.h5
# test for signed/unsigned scalar datasets with attributes
TOOLTEST tscalarintattrsize.ddl --enable-error-stack tscalarintattrsize.h5
# test for signed/unsigned datasets attributes
TOOLTEST tintsattrs.ddl --enable-error-stack tintsattrs.h5
# test for string scalar dataset attribute
TOOLTEST tscalarstring.ddl --enable-error-stack tscalarstring.h5
# test for displaying groups
TOOLTEST tgroup-1.ddl --enable-error-stack tgroup.h5
# test for displaying the selected groups
TOOLTEST4 tgroup-2.ddl --enable-error-stack --group=/g2 --group / -g /y tgroup.h5

# test for displaying simple space datasets
TOOLTEST tdset-1.ddl --enable-error-stack tdset.h5
# test for displaying selected datasets
TOOLTEST4 tdset-2.ddl --enable-error-stack -H -d dset1 -d /dset2 --dataset=dset3 tdset.h5

# test for displaying attributes
TOOLTEST tattr-1.ddl --enable-error-stack tattr.h5
# test for displaying the selected attributes of string type and scalar space
TOOLTEST tattr-2.ddl --enable-error-stack -a "/\/attr1" --attribute /attr4 --attribute=/attr5 tattr.h5
TOOLTEST tattr-2.ddl --enable-error-stack -N "/\/attr1" --any_path /attr4 --any_path=/attr5 tattr.h5
# test for header and error messages
TOOLTEST4 tattr-3.ddl --enable-error-stack --header -a /attr2 --attribute=/attr tattr.h5
# test for displaying at least 9 attributes on root from a BE machine
TOOLTEST tattr-4_be.ddl --enable-error-stack tattr4_be.h5
# test for displaying attributes in shared datatype (also in group and dataset)
TOOLTEST tnamed_dtype_attr.ddl --enable-error-stack tnamed_dtype_attr.h5

# test for displaying soft links and user-defined links
TOOLTEST tslink-1.ddl --enable-error-stack tslink.h5
TOOLTEST tudlink-1.ddl --enable-error-stack tudlink.h5
# test for displaying the selected link
TOOLTEST tslink-2.ddl --enable-error-stack -l slink2 tslink.h5
TOOLTEST tslink-2.ddl --enable-error-stack -N slink2 tslink.h5
TOOLTEST tudlink-2.ddl --enable-error-stack -l udlink2 tudlink.h5
# test for displaying dangling soft links
TOOLTEST4 tslink-D.ddl --enable-error-stack -d /slink1 tslink.h5

# tests for hard links
TOOLTEST thlink-1.ddl --enable-error-stack thlink.h5
TOOLTEST thlink-2.ddl --enable-error-stack -d /g1/dset2 --dataset /dset1 --dataset=/g1/g1.1/dset3 thlink.h5
TOOLTEST thlink-3.ddl --enable-error-stack -d /g1/g1.1/dset3 --dataset /g1/dset2 --dataset=/dset1 thlink.h5
TOOLTEST thlink-4.ddl --enable-error-stack -g /g1 thlink.h5
TOOLTEST thlink-4.ddl --enable-error-stack -N /g1 thlink.h5
TOOLTEST thlink-5.ddl --enable-error-stack -d /dset1 -g /g2 -d /g1/dset2 thlink.h5
TOOLTEST thlink-5.ddl --enable-error-stack -N /dset1 -N /g2 -N /g1/dset2 thlink.h5

# tests for compound data types
TOOLTEST tcomp-1.ddl --enable-error-stack tcompound.h5
# test for named data types
TOOLTEST tcomp-2.ddl --enable-error-stack -t /type1 --datatype /type2 --datatype=/group1/type3 tcompound.h5
TOOLTEST tcomp-2.ddl --enable-error-stack -N /type1 --any_path /type2 --any_path=/group1/type3 tcompound.h5
# test for unamed type
TOOLTEST4 tcomp-3.ddl --enable-error-stack -t /#6632 -g /group2 tcompound.h5
# test complicated compound datatype
TOOLTEST tcomp-4.ddl --enable-error-stack tcompound_complex.h5
TOOLTEST tcompound_complex2.ddl --enable-error-stack tcompound_complex2.h5
# tests for bitfields and opaque data types
if test $WORDS_BIGENDIAN != "yes"; then
TOOLTEST tbitnopaque_le.ddl --enable-error-stack tbitnopaque.h5
else
TOOLTEST tbitnopaque_be.ddl --enable-error-stack tbitnopaque.h5
fi

#test for the nested compound type
TOOLTEST tnestcomp-1.ddl --enable-error-stack tnestedcomp.h5
TOOLTEST tnestedcmpddt.ddl --enable-error-stack tnestedcmpddt.h5

# test for options
TOOLTEST4 tall-1.ddl --enable-error-stack tall.h5
TOOLTEST tall-2.ddl --enable-error-stack --header -g /g1/g1.1 -a attr2 tall.h5
TOOLTEST tall-3.ddl --enable-error-stack -d /g2/dset2.1 -l /g1/g1.2/g1.2.1/slink tall.h5
TOOLTEST tall-3.ddl --enable-error-stack -N /g2/dset2.1 -N /g1/g1.2/g1.2.1/slink tall.h5
TOOLTEST tall-7.ddl --enable-error-stack -a attr1 tall.h5
TOOLTEST tall-7N.ddl --enable-error-stack -N attr1 tall.h5

# test for loop detection
TOOLTEST tloop-1.ddl --enable-error-stack tloop.h5

# test for string
TOOLTEST tstr-1.ddl --enable-error-stack tstr.h5
TOOLTEST tstr-2.ddl --enable-error-stack tstr2.h5

# test for file created by Lib SAF team
TOOLTEST tsaf.ddl --enable-error-stack tsaf.h5

# test for file with variable length data
TOOLTEST tvldtypes1.ddl --enable-error-stack tvldtypes1.h5
TOOLTEST tvldtypes2.ddl --enable-error-stack tvldtypes2.h5
TOOLTEST tvldtypes3.ddl --enable-error-stack tvldtypes3.h5
TOOLTEST tvldtypes4.ddl --enable-error-stack tvldtypes4.h5
TOOLTEST tvldtypes5.ddl --enable-error-stack tvldtypes5.h5

#test for file with variable length string data
TOOLTEST tvlstr.ddl --enable-error-stack tvlstr.h5
TOOLTEST tvlenstr_array.ddl --enable-error-stack tvlenstr_array.h5

# test for files with array data
TOOLTEST tarray1.ddl --enable-error-stack tarray1.h5
# # added for bug# 2092 - tarray1_big.h
TOOLTEST4 tarray1_big.ddl --enable-error-stack -R tarray1_big.h5
TOOLTEST tarray2.ddl --enable-error-stack tarray2.h5
TOOLTEST tarray3.ddl --enable-error-stack tarray3.h5
TOOLTEST tarray4.ddl --enable-error-stack tarray4.h5
TOOLTEST tarray5.ddl --enable-error-stack tarray5.h5
TOOLTEST tarray6.ddl --enable-error-stack tarray6.h5
TOOLTEST tarray7.ddl --enable-error-stack tarray7.h5
TOOLTEST tarray8.ddl --enable-error-stack tarray8.h5

# test for wildcards in filename (does not work with cmake)
# inconsistent across platforms TOOLTEST3 tstarfile.ddl --enable-error-stack -H -d Dataset1 tarr*.h5
#TOOLTEST4 tqmarkfile.ddl --enable-error-stack -H -d Dataset1 tarray?.h5
TOOLTEST tmultifile.ddl --enable-error-stack -H -d Dataset1 tarray2.h5 tarray3.h5 tarray4.h5 tarray5.h5 tarray6.h5 tarray7.h5

# test for files with empty data
TOOLTEST tempty.ddl --enable-error-stack tempty.h5

# test for files with groups that have comments
TOOLTEST tgrp_comments.ddl --enable-error-stack tgrp_comments.h5

# test the --filedriver flag
TOOLTEST tsplit_file.ddl --enable-error-stack --filedriver=split tsplit_file
TOOLTEST tfamily.ddl --enable-error-stack --filedriver=family tfamily%05d.h5
TOOLTEST tmulti.ddl --enable-error-stack --filedriver=multi tmulti

# test for files with group names which reach > 1024 bytes in size
TOOLTEST tlarge_objname.ddl --enable-error-stack -w157 tlarge_objname.h5

# test '-A' to suppress data but print attr's
TOOLTEST4 tall-2A.ddl --enable-error-stack -A tall.h5

# test '-A' to suppress attr's but print data
TOOLTEST4 tall-2A0.ddl --enable-error-stack -A 0 tall.h5

# test '-r' to print attributes in ASCII instead of decimal
TOOLTEST4 tall-2B.ddl --enable-error-stack -A -r tall.h5

# test Subsetting
TOOLTEST tall-4s.ddl --enable-error-stack --dataset=/g1/g1.1/dset1.1.1 --start=1,1 --stride=2,3 --count=3,2 --block=1,1 tall.h5
TOOLTEST tall-5s.ddl --enable-error-stack -d "/g1/g1.1/dset1.1.2[0;2;10;]" tall.h5
TOOLTEST tdset-3s.ddl --enable-error-stack -d "/dset1[1,1;;;]" tdset.h5
TOOLTEST tno-subset.ddl --enable-error-stack --no-compact-subset -d "AHFINDERDIRECT::ah_centroid_t[0] it=0 tl=0" tno-subset.h5

TOOLTEST tints4dimsCount2.ddl --enable-error-stack -d FourDimInts -s 0,0,0,0 -c 2,2,2,2 tints4dims.h5
TOOLTEST tints4dimsBlock2.ddl --enable-error-stack -d FourDimInts -s 0,0,0,0 -c 1,1,1,1 -k 2,2,2,2 tints4dims.h5
TOOLTEST tints4dimsStride2.ddl --enable-error-stack -d FourDimInts -s 0,0,0,0 -S 2,2,2,2 -c 2,2,2,2 tints4dims.h5
TOOLTEST tints4dimsCountEq.ddl --enable-error-stack -d FourDimInts -s 0,0,0,0 -S 2,2,1,1 -k 1,2,1,1 -c 2,2,4,4 tints4dims.h5
TOOLTEST tints4dimsBlockEq.ddl --enable-error-stack -d FourDimInts -s 0,0,0,0 -S 2,2,1,1 -c 2,2,1,1 -k 1,2,4,4 tints4dims.h5

# test printing characters in ASCII instead of decimal
TOOLTEST tchar1.ddl --enable-error-stack -r tchar.h5

# test datatypes in ASCII and UTF8
TOOLTEST charsets.ddl --enable-error-stack charsets.h5

# rev. 2004

# tests for super block
TOOLTEST tboot1.ddl --enable-error-stack -H -B -d dset tfcontents1.h5
TOOLTEST tboot2.ddl --enable-error-stack -B tfcontents2.h5
TOOLTEST tboot2A.ddl --enable-error-stack --boot-block tfcontents2.h5
TOOLTEST tboot2B.ddl --enable-error-stack --superblock tfcontents2.h5
TOOLTEST file_space.ddl --enable-error-stack -B file_space.h5

# test -p with a non existing dataset
TOOLTEST4 tperror.ddl --enable-error-stack -p -d bogus tfcontents1.h5

# test for file contents
TOOLTEST tcontents.ddl --enable-error-stack -n tfcontents1.h5
TOOLTEST tordercontents1.ddl --enable-error-stack -n --sort_by=name --sort_order=ascending tfcontents1.h5
TOOLTEST tordercontents2.ddl --enable-error-stack -n --sort_by=name --sort_order=descending tfcontents1.h5
TOOLTEST tattrcontents1.ddl --enable-error-stack -n 1 --sort_order=ascending tall.h5
TOOLTEST tattrcontents2.ddl --enable-error-stack -n 1 --sort_order=descending tall.h5

# tests for storage layout
# compact
TOOLTEST tcompact.ddl --enable-error-stack -H -p -d compact tfilters.h5
# contiguous
TOOLTEST tcontiguos.ddl --enable-error-stack -H -p -d contiguous tfilters.h5
# chunked
TOOLTEST tchunked.ddl --enable-error-stack -H -p -d chunked tfilters.h5
# external
TOOLTEST texternal.ddl --enable-error-stack -H -p -d external tfilters.h5

# fill values
TOOLTEST tfill.ddl --enable-error-stack -p tfvalues.h5

# several datatype, with references , print path
TOOLTEST treference.ddl --enable-error-stack tattr2.h5

# escape/not escape non printable characters
TOOLTEST tstringe.ddl --enable-error-stack -e tstr3.h5
TOOLTEST tstring.ddl --enable-error-stack tstr3.h5
# char data as ASCII with non escape
TOOLTEST tstring2.ddl --enable-error-stack -r -d str4 tstr3.h5

# array indices print/not print
TOOLTEST tindicesyes.ddl --enable-error-stack taindices.h5
TOOLTEST tindicesno.ddl --enable-error-stack -y taindices.h5

########## array indices with subsetting
# 1D case
TOOLTEST tindicessub1.ddl --enable-error-stack -d 1d -s 1 -S 10 -c 2  -k 3 taindices.h5

# 2D case
TOOLTEST tindicessub2.ddl --enable-error-stack -d 2d -s 1,2  -S 3,3 -c 3,2 -k 2,2 taindices.h5

# 3D case
TOOLTEST tindicessub3.ddl --enable-error-stack -d 3d -s 0,1,2 -S 1,3,3 -c 2,2,2  -k 1,2,2  taindices.h5

# 4D case
TOOLTEST tindicessub4.ddl --enable-error-stack -d 4d -s 0,0,1,2  -c 2,2,3,2 -S 1,1,3,3 -k 1,1,2,2  taindices.h5

#Exceed the dimensions for subsetting
TOOLTEST texceedsubstart.ddl --enable-error-stack -d 1d -s 1,3 taindices.h5
TOOLTEST texceedsubcount.ddl --enable-error-stack -d 1d -c 1,3 taindices.h5
TOOLTEST texceedsubstride.ddl --enable-error-stack -d 1d -S 1,3 taindices.h5
TOOLTEST texceedsubblock.ddl --enable-error-stack -d 1d -k 1,3 taindices.h5


# tests for filters
# SZIP
TOOLTEST tszip.ddl --enable-error-stack -H -p -d szip tfilters.h5
# deflate
TOOLTEST tdeflate.ddl --enable-error-stack -H -p -d deflate tfilters.h5
# shuffle
TOOLTEST tshuffle.ddl --enable-error-stack -H -p -d shuffle tfilters.h5
# fletcher32
TOOLTEST tfletcher32.ddl --enable-error-stack -H -p -d fletcher32  tfilters.h5
# nbit
TOOLTEST tnbit.ddl --enable-error-stack -H -p -d nbit  tfilters.h5
# scaleoffset
TOOLTEST tscaleoffset.ddl --enable-error-stack -H -p -d scaleoffset  tfilters.h5
# all
TOOLTEST tallfilters.ddl --enable-error-stack -H -p -d all  tfilters.h5
# user defined
TOOLTEST tuserfilter.ddl --enable-error-stack -H  -p -d myfilter  tfilters.h5

if test $USE_FILTER_DEFLATE = "yes" ; then
  # data read internal filters
  TOOLTEST treadintfilter.ddl --enable-error-stack -d deflate -d shuffle -d fletcher32 -d nbit -d scaleoffset tfilters.h5
  if test $USE_FILTER_SZIP = "yes"; then
    # data read
    TOOLTEST treadfilter.ddl --enable-error-stack -d all -d szip tfilters.h5
  fi
fi

# test for displaying objects with very long names
TOOLTEST tlonglinks.ddl --enable-error-stack tlonglinks.h5

# dimensions over 4GB, print boundary
TOOLTEST tbigdims.ddl --enable-error-stack -d dset4gb -s 4294967284 -c 22 tbigdims.h5

# hyperslab read
TOOLTEST thyperslab.ddl --enable-error-stack thyperslab.h5


#

# test for displaying dataset and attribute of null space
TOOLTEST tnullspace.ddl --enable-error-stack tnullspace.h5
TOOLTEST tgrpnullspace.ddl -p --enable-error-stack tgrpnullspace.h5

# test for displaying dataset and attribute of space with 0 dimension size
TOOLTEST zerodim.ddl --enable-error-stack zerodim.h5

# test for long double (some systems do not have long double)
#TOOLTEST tldouble.ddl --enable-error-stack tldouble.h5

# test for vms
TOOLTEST tvms.ddl --enable-error-stack tvms.h5

# test for binary output
TOOLTEST tbin1.ddl --enable-error-stack -d integer -o out1.bin -b LE tbinary.h5

# test for string binary output
TOOLTEST2B tstr2bin2.exp --enable-error-stack -d /g2/dset2 -b -o tstr2bin2.txt tstr2.h5
TOOLTEST2B tstr2bin6.exp --enable-error-stack -d /g6/dset6 -b -o tstr2bin6.txt tstr2.h5

# NATIVE default. the NATIVE test can be validated with h5import/h5diff
TOOLTEST   tbin1.ddl --enable-error-stack -d integer -o out1.bin  -b  tbinary.h5
IMPORTTEST out1.bin -c out3.h5import -o out1.h5
DIFFTEST   tbinary.h5 out1.h5 /integer /integer
# Same but use h5dump as input to h5import
IMPORTTEST out1.bin -c tbin1.ddl -o out1D.h5
#DIFFTEST   tbinary.h5 out1D.h5 /integer /integer

TOOLTEST   tbin2.ddl --enable-error-stack -b BE -d float  -o out2.bin  tbinary.h5

# the NATIVE test can be validated with h5import/h5diff
TOOLTEST   tbin3.ddl --enable-error-stack -d integer -o out3.bin -b NATIVE tbinary.h5
IMPORTTEST out3.bin -c out3.h5import -o out3.h5
DIFFTEST   tbinary.h5 out3.h5 /integer /integer
# Same but use h5dump as input to h5import
IMPORTTEST out3.bin -c tbin3.ddl -o out3D.h5
#DIFFTEST   tbinary.h5 out3D.h5 /integer /integer

TOOLTEST   tbin4.ddl --enable-error-stack -d double  -b FILE -o out4.bin    tbinary.h5

# Clean up binary output files
if test -z "$HDF5_NOCLEANUP"; then
 rm -f out[1-4].bin
 rm -f out1.h5
 rm -f out3.h5
fi

# test for dataset region references
TOOLTEST  tdatareg.ddl --enable-error-stack tdatareg.h5
TOOLTEST4 tdataregR.ddl --enable-error-stack -R tdatareg.h5
TOOLTEST  tattrreg.ddl --enable-error-stack tattrreg.h5
TOOLTEST4 tattrregR.ddl --enable-error-stack -R tattrreg.h5
TOOLTEST2 tbinregR.exp --enable-error-stack -d /Dataset1 -s 0 -R -y -o tbinregR.txt    tdatareg.h5

# Clean up text output files
if test -z "$HDF5_NOCLEANUP"; then
 rm -f tbinregR.txt
fi

# tests for group creation order
# "1" tracked, "2" name, root tracked
TOOLTEST tordergr1.ddl --enable-error-stack --group=1 --sort_by=creation_order --sort_order=ascending tordergr.h5
TOOLTEST tordergr2.ddl --enable-error-stack --group=1 --sort_by=creation_order --sort_order=descending tordergr.h5
TOOLTEST tordergr3.ddl --enable-error-stack -g 2 -q name -z ascending tordergr.h5
TOOLTEST tordergr4.ddl --enable-error-stack -g 2 -q name -z descending tordergr.h5
TOOLTEST tordergr5.ddl --enable-error-stack -q creation_order tordergr.h5

# tests for attribute order
TOOLTEST torderattr1.ddl --enable-error-stack -H --sort_by=name --sort_order=ascending torderattr.h5
TOOLTEST torderattr2.ddl --enable-error-stack -H --sort_by=name --sort_order=descending torderattr.h5
TOOLTEST torderattr3.ddl --enable-error-stack -H --sort_by=creation_order --sort_order=ascending torderattr.h5
TOOLTEST torderattr4.ddl --enable-error-stack -H --sort_by=creation_order --sort_order=descending torderattr.h5

# tests for link references and order
TOOLTEST4 torderlinks1.ddl --enable-error-stack --sort_by=name --sort_order=ascending tfcontents1.h5
TOOLTEST4 torderlinks2.ddl --enable-error-stack --sort_by=name --sort_order=descending tfcontents1.h5

# tests for floating point user defined printf format
TOOLTEST tfpformat.ddl --enable-error-stack -m %.7f tfpformat.h5

# tests for traversal of external links
TOOLTEST4 textlinksrc.ddl --enable-error-stack textlinksrc.h5
TOOLTEST4 textlinkfar.ddl --enable-error-stack textlinkfar.h5

# test for dangling external links
TOOLTEST4 textlink.ddl --enable-error-stack textlink.h5

# test for error stack display (BZ2048)
TOOLTEST5 filter_fail.ddl --enable-error-stack filter_fail.h5

# test for -o -y for dataset with attributes
TOOLTEST2 tall-6.exp --enable-error-stack -y -o tall-6.txt -d /g1/g1.1/dset1.1.1 tall.h5

# test for non-existing file
TOOLTEST3 non_existing.ddl --enable-error-stack tgroup.h5 non_existing.h5

# test to verify HDFFV-9407: long double full precision
GREPTEST "1.123456789012345" t128bit_float.ddl -m %.35Lf t128bit_float.h5

# Clean up temporary files/directories
CLEAN_TESTFILES_AND_TESTDIR

# Report test results and exit
if test $nerrors -eq 0 ; then
    echo "All $TESTNAME tests passed."
    exit $EXIT_SUCCESS
else
    echo "$TESTNAME tests failed with $nerrors errors."
    exit $EXIT_FAILURE
fi
