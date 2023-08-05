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

top_builddir=../..
top_srcdir=../..
srcdir=.

USE_FILTER_SZIP="no"
USE_FILTER_DEFLATE="yes"
USE_ROS3_VFD="@HAVE_ROS3_VFD@"
USE_HDFS_VFD="no"

TESTNAME=JUnitInterface
EXIT_SUCCESS=0
EXIT_FAILURE=1

# Set up default variable values if not supplied by the user.
RM='rm -rf'
CMP='cmp'
DIFF='diff -c'
CP='cp'
DIRNAME='dirname'
LS='ls'
AWK='awk'

nerrors=0
verbose=yes

# setup my machine information.
myos=`uname -s`

# where the libs exist
HDFLIB_HOME="$top_srcdir/java/lib"
BLDLIBDIR="$top_builddir/hdf5/lib"
BLDDIR="."
HDFTEST_HOME="$top_srcdir/java/test"
JARFILE=jarhdf5-1.10.6.jar
TESTJARFILE=jarhdf5test.jar
test -d $BLDLIBDIR || mkdir -p $BLDLIBDIR

######################################################################
# library files
# --------------------------------------------------------------------
# All the library files copy from source directory to test directory
# NOTE: Keep this framework to add/remove test files.
#       This list are also used for checking exist.
#       Comment '#' without space can be used.
# --------------------------------------------------------------------
LIST_LIBRARY_FILES="
$top_builddir/src/.libs/libhdf5.*
$top_builddir/java/src/jni/.libs/libhdf5_java.*
"
LIST_JAR_TESTFILES="
$HDFLIB_HOME/hamcrest-core.jar
$HDFLIB_HOME/junit.jar
$HDFLIB_HOME/slf4j-api-1.7.25.jar
$HDFLIB_HOME/ext/slf4j-simple-1.7.25.jar
"
LIST_JAR_FILES="
$top_builddir/java/src/$JARFILE
"
LIST_DATA_FILES="
$HDFTEST_HOME/testfiles/JUnit-TestH5.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5Eparams.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5Eregister.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5Fparams.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5Fbasic.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5F.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5Fswmr.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5Gbasic.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5G.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5Sbasic.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5S.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5Tparams.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5Tbasic.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5T.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5Dparams.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5D.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5Dplist.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5Lparams.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5Lbasic.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5Lcreate.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5R.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5P.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5PData.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5Pfapl.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5Pfapls3.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5Pfaplhdfs.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5Pvirtual.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5Plist.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5A.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5Oparams.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5Obasic.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5Ocreate.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5Ocopy.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5PL.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5Z.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5E.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5Edefault.txt
$HDFTEST_HOME/testfiles/JUnit-TestH5Giterate.txt
"

#
# copy files from source dirs to test dir
#
COPY_LIBFILES="$LIST_LIBRARY_FILES"
COPY_JARTESTFILES="$LIST_JAR_TESTFILES"
COPY_JARFILES="$LIST_JAR_FILES"

COPY_LIBFILES_TO_BLDLIBDIR()
{
    # copy test files. Used -f to make sure get a new copy
    for tstfile in $COPY_LIBFILES
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
            INODE_DDIR=`$LS -i -d $BLDLIBDIR | $AWK -F' ' '{print $1}'`
            if [ "$INODE_SDIR" != "$INODE_DDIR" ]; then
                $CP -f $tstfile $BLDLIBDIR
                if [ $? -ne 0 ]; then
                    echo "Error: FAILED to copy $tstfile ."

                    # Comment out this to CREATE expected file
                    exit $EXIT_FAILURE
                fi
            fi
        fi
    done
    # copy jar files. Used -f to make sure get a new copy
    for tstfile in $COPY_JARTESTFILES
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
            INODE_DDIR=`$LS -i -d $BLDLIBDIR | $AWK -F' ' '{print $1}'`
            if [ "$INODE_SDIR" != "$INODE_DDIR" ]; then
                $CP -f $tstfile $BLDLIBDIR
                if [ $? -ne 0 ]; then
                    echo "Error: FAILED to copy $tstfile ."

                    # Comment out this to CREATE expected file
                    exit $EXIT_FAILURE
                fi
            fi
        fi
    done
    for tstfile in $COPY_JARFILES
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
            INODE_DDIR=`$LS -i -d $BLDLIBDIR | $AWK -F' ' '{print $1}'`
            if [ "$INODE_SDIR" != "$INODE_DDIR" ]; then
                $CP -f $tstfile $BLDLIBDIR
                if [ $? -ne 0 ]; then
                    echo "Error: FAILED to copy $tstfile ."

                    # Comment out this to CREATE expected file
                    exit $EXIT_FAILURE
                fi
            fi
        fi
    done
}

CLEAN_LIBFILES_AND_BLDLIBDIR()
{
    # skip rm if srcdir is same as destdir
    # this occurs when build/test performed in source dir and
    # make cp fail
    SDIR=$HDFLIB_HOME
    INODE_SDIR=`$LS -i -d $SDIR | $AWK -F' ' '{print $1}'`
    INODE_DDIR=`$LS -i -d $BLDLIBDIR | $AWK -F' ' '{print $1}'`
    if [ "$INODE_SDIR" != "$INODE_DDIR" ]; then
        for tstfile in $COPY_JARTESTFILES
        do
            $RM $BLDLIBDIR/tstfile
        done
    fi
}

COPY_DATAFILES="$LIST_DATA_FILES"

COPY_DATAFILES_TO_BLDDIR()
{
    # copy test files. Used -f to make sure get a new copy
    for tstfile in $COPY_DATAFILES
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
            INODE_DDIR=`$LS -i -d $BLDDIR | $AWK -F' ' '{print $1}'`
            if [ "$INODE_SDIR" != "$INODE_DDIR" ]; then
                $CP -f $tstfile $BLDDIR
                if [ $? -ne 0 ]; then
                    echo "Error: FAILED to copy $tstfile ."

                    # Comment out this to CREATE expected file
                    exit $EXIT_FAILURE
                fi
            fi
        fi
    done
    $CP -f $HDFTEST_HOME/h5ex_g_iterate.orig $BLDDIR/h5ex_g_iterate.hdf
    $CP -f $HDFTEST_HOME/h5ex_g_iterate.orig $BLDDIR/h5ex_g_iterateL1.hdf
    $CP -f $HDFTEST_HOME/h5ex_g_iterate.orig $BLDDIR/h5ex_g_iterateL2.hdf
    $CP -f $HDFTEST_HOME/h5ex_g_iterate.orig $BLDDIR/h5ex_g_iterateO1.hdf
    $CP -f $HDFTEST_HOME/h5ex_g_iterate.orig $BLDDIR/h5ex_g_iterateO2.hdf
}

CLEAN_DATAFILES_AND_BLDDIR()
{
        $RM $BLDDIR/h5ex_g_iterate*.hdf
        $RM $BLDDIR/JUnit-*.out
        $RM $BLDDIR/JUnit-*.ext
        $RM $BLDDIR/JUnit-*.err
    # skip rm if srcdir is same as destdir
    # this occurs when build/test performed in source dir and
    # make cp fail
    SDIR=`$DIRNAME $tstfile`
    INODE_SDIR=`$LS -i -d $SDIR | $AWK -F' ' '{print $1}'`
    INODE_DDIR=`$LS -i -d $BLDDIR | $AWK -F' ' '{print $1}'`
    if [ "$INODE_SDIR" != "$INODE_DDIR" ]; then
        $RM $BLDDIR/JUnit-*.ert
        $RM $BLDDIR/JUnit-*.txt
    fi
}

# Print a line-line message left justified in a field of 70 characters
# beginning with the word "Testing".
#
TESTING() {
   SPACES="                                                               "
   echo "Testing $* $SPACES" | cut -c1-70 | tr -d '\012'
}

# where Java is installed (requires jdk1.7.x)
JAVAEXE=
JAVAEXEFLAGS=

###############################################################################
#            DO NOT MODIFY BELOW THIS LINE
###############################################################################

# prepare for test
COPY_LIBFILES_TO_BLDLIBDIR
COPY_DATAFILES_TO_BLDDIR

CPATH=".:"$BLDLIBDIR"/"$JARFILE":"$BLDLIBDIR"/junit.jar:"$BLDLIBDIR"/hamcrest-core.jar:"$BLDLIBDIR"/slf4j-api-1.7.25.jar:"$BLDLIBDIR"/slf4j-simple-1.7.25.jar:"$TESTJARFILE""

TEST=/usr/bin/test
if [ ! -x /usr/bin/test ]
then
TEST=`which test`
fi

if $TEST -z "$CLASSPATH"; then
        CLASSPATH=""
fi
CLASSPATH=$CPATH":"$CLASSPATH
export CLASSPATH

if $TEST -n "$JAVAPATH" ; then
        PATH=$JAVAPATH":"$PATH
        export PATH
fi

if $TEST -e /bin/uname; then
   os_name=`/bin/uname -s`
elif $TEST -e /usr/bin/uname; then
   os_name=`/usr/bin/uname -s`
else
   os_name=unknown
fi

if $TEST -z "$LD_LIBRARY_PATH" ; then
        LD_LIBRARY_PATH=""
fi

case  $os_name in
    *)
    LD_LIBRARY_PATH=$BLDLIBDIR:$LD_LIBRARY_PATH
    ;;
esac

export LD_LIBRARY_PATH

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5"
TESTING JUnit-TestH5
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5 > JUnit-TestH5.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5.ext > JUnit-TestH5.out

if diff JUnit-TestH5.out JUnit-TestH5.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5"
else
    echo "**FAILED**    JUnit-TestH5"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5.txt JUnit-TestH5.out |sed 's/^/    /'
fi

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Eparams"
TESTING JUnit-TestH5Eparams
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Eparams > JUnit-TestH5Eparams.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5Eparams.ext > JUnit-TestH5Eparams.out

if diff JUnit-TestH5Eparams.out JUnit-TestH5Eparams.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5Eparams"
else
    echo "**FAILED**    JUnit-TestH5Eparams"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5Eparams.txt JUnit-TestH5Eparams.out |sed 's/^/    /'
fi

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Eregister"
TESTING JUnit-TestH5Eregister
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Eregister > JUnit-TestH5Eregister.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5Eregister.ext > JUnit-TestH5Eregister.out

if diff JUnit-TestH5Eregister.out JUnit-TestH5Eregister.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5Eregister"
else
    echo "**FAILED**    JUnit-TestH5Eregister"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5Eregister.txt JUnit-TestH5Eregister.out |sed 's/^/    /'
fi

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Fparams"
TESTING JUnit-TestH5Fparams
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Fparams > JUnit-TestH5Fparams.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5Fparams.ext > JUnit-TestH5Fparams.out

if diff JUnit-TestH5Fparams.out JUnit-TestH5Fparams.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5Fparams"
else
    echo "**FAILED**    JUnit-TestH5Fparams"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5Fparams.txt JUnit-TestH5Fparams.out |sed 's/^/    /'
fi

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Fbasic"
TESTING JUnit-TestH5Fbasic
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Fbasic > JUnit-TestH5Fbasic.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5Fbasic.ext > JUnit-TestH5Fbasic.out

if diff JUnit-TestH5Fbasic.out JUnit-TestH5Fbasic.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5Fbasic"
else
    echo "**FAILED**    JUnit-TestH5Fbasic"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5Fbasic.txt JUnit-TestH5Fbasic.out |sed 's/^/    /'
fi

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5F"
TESTING JUnit-TestH5F
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5F > JUnit-TestH5F.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5F.ext > JUnit-TestH5F.out

if diff JUnit-TestH5F.out JUnit-TestH5F.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5F"
else
    echo "**FAILED**    JUnit-TestH5F"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5F.txt JUnit-TestH5F.out |sed 's/^/    /'
fi

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Fswmr"
TESTING JUnit-TestH5Fswmr
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Fswmr > JUnit-TestH5Fswmr.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5Fswmr.ext > JUnit-TestH5Fswmr.out

if diff JUnit-TestH5Fswmr.out JUnit-TestH5Fswmr.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5Fswmr"
else
    echo "**FAILED**    JUnit-TestH5Fswmr"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5Fswmr.txt JUnit-TestH5Fswmr.out |sed 's/^/    /'
fi

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Gbasic"
TESTING JUnit-TestH5Gbasic
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Gbasic > JUnit-TestH5Gbasic.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5Gbasic.ext > JUnit-TestH5Gbasic.out

if diff JUnit-TestH5Gbasic.out JUnit-TestH5Gbasic.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5Gbasic"
else
    echo "**FAILED**    JUnit-TestH5Gbasic"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5Gbasic.txt JUnit-TestH5Gbasic.out |sed 's/^/    /'
fi

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5G"
TESTING JUnit-TestH5G
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5G > JUnit-TestH5G.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5G.ext > JUnit-TestH5G.out

if diff JUnit-TestH5G.out JUnit-TestH5G.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5G"
else
    echo "**FAILED**    JUnit-TestH5G"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5G.txt JUnit-TestH5G.out |sed 's/^/    /'
fi

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Sbasic"
TESTING JUnit-TestH5Sbasic
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Sbasic > JUnit-TestH5Sbasic.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5Sbasic.ext > JUnit-TestH5Sbasic.out

if diff JUnit-TestH5Sbasic.out JUnit-TestH5Sbasic.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5Sbasic"
else
    echo "**FAILED**    JUnit-TestH5Sbasic"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5Sbasic.txt JUnit-TestH5Sbasic.out |sed 's/^/    /'
fi

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5S"
TESTING JUnit-TestH5S
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5S > JUnit-TestH5S.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5S.ext > JUnit-TestH5S.out

if diff JUnit-TestH5S.out JUnit-TestH5S.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5S"
else
    echo "**FAILED**    JUnit-TestH5S"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5S.txt JUnit-TestH5S.out |sed 's/^/    /'
fi

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Tparams"
TESTING JUnit-TestH5Tparams
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Tparams > JUnit-TestH5Tparams.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5Tparams.ext > JUnit-TestH5Tparams.out

if diff JUnit-TestH5Tparams.out JUnit-TestH5Tparams.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5Tparams"
else
    echo "**FAILED**    JUnit-TestH5Tparams"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5Tparams.txt JUnit-TestH5Tparams.out |sed 's/^/    /'
fi

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Tbasic"
TESTING JUnit-TestH5Tbasic
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Tbasic > JUnit-TestH5Tbasic.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5Tbasic.ext > JUnit-TestH5Tbasic.out

if diff JUnit-TestH5Tbasic.out JUnit-TestH5Tbasic.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5Tbasic"
else
    echo "**FAILED**    JUnit-TestH5Tbasic"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5Tbasic.txt JUnit-TestH5Tbasic.out |sed 's/^/    /'
fi

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5T"
TESTING JUnit-TestH5T
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5T > JUnit-TestH5T.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5T.ext > JUnit-TestH5T.out

if diff JUnit-TestH5T.out JUnit-TestH5T.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5T"
else
    echo "**FAILED**    JUnit-TestH5T"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5T.txt JUnit-TestH5T.out |sed 's/^/    /'
fi

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Dparams"
TESTING JUnit-TestH5Dparams
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Dparams > JUnit-TestH5Dparams.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5Dparams.ext > JUnit-TestH5Dparams.out

if diff JUnit-TestH5Dparams.out JUnit-TestH5Dparams.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5Dparams"
else
    echo "**FAILED**    JUnit-TestH5Dparams"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5Dparams.txt JUnit-TestH5Dparams.out |sed 's/^/    /'
fi

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5D"
TESTING JUnit-TestH5D
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5D > JUnit-TestH5D.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5D.ext > JUnit-TestH5D.out

if diff JUnit-TestH5D.out JUnit-TestH5D.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5D"
else
    echo "**FAILED**    JUnit-TestH5D"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5D.txt JUnit-TestH5D.out |sed 's/^/    /'
fi

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Dplist"
TESTING JUnit-TestH5Dplist
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Dplist > JUnit-TestH5Dplist.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5Dplist.ext > JUnit-TestH5Dplist.out

if diff JUnit-TestH5Dplist.out JUnit-TestH5Dplist.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5Dplist"
else
    echo "**FAILED**    JUnit-TestH5Dplist"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5Dplist.txt JUnit-TestH5Dplist.out |sed 's/^/    /'
fi

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Lparams"
TESTING JUnit-TestH5Lparams
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Lparams > JUnit-TestH5Lparams.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5Lparams.ext > JUnit-TestH5Lparams.out

if diff JUnit-TestH5Lparams.out JUnit-TestH5Lparams.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5Lparams"
else
    echo "**FAILED**    JUnit-TestH5Lparams"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5Lparams.txt JUnit-TestH5Lparams.out |sed 's/^/    /'
fi

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Lbasic"
TESTING JUnit-TestH5Lbasic
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Lbasic > JUnit-TestH5Lbasic.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5Lbasic.ext > JUnit-TestH5Lbasic.out

if diff JUnit-TestH5Lbasic.out JUnit-TestH5Lbasic.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5Lbasic"
else
    echo "**FAILED**    JUnit-TestH5Lbasic"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5Lbasic.txt JUnit-TestH5Lbasic.out |sed 's/^/    /'
fi

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Lcreate"
TESTING JUnit-TestH5Lcreate
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Lcreate > JUnit-TestH5Lcreate.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5Lcreate.ext > JUnit-TestH5Lcreate.out

if diff JUnit-TestH5Lcreate.out JUnit-TestH5Lcreate.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5Lcreate"
else
    echo "**FAILED**    JUnit-TestH5Lcreate"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5Lcreate.txt JUnit-TestH5Lcreate.out |sed 's/^/    /'
fi

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5R"
TESTING JUnit-TestH5R
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5R > JUnit-TestH5R.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5R.ext > JUnit-TestH5R.out

if diff JUnit-TestH5R.out JUnit-TestH5R.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5R"
else
    echo "**FAILED**    JUnit-TestH5R"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5R.txt JUnit-TestH5R.out |sed 's/^/    /'
fi

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5P"
TESTING JUnit-TestH5P
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5P > JUnit-TestH5P.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5P.ext > JUnit-TestH5P.out

if diff JUnit-TestH5P.out JUnit-TestH5P.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5P"
else
    echo "**FAILED**    JUnit-TestH5P"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5P.txt JUnit-TestH5P.out |sed 's/^/    /'
fi

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5PData"
TESTING JUnit-TestH5PData
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5PData > JUnit-TestH5PData.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5PData.ext > JUnit-TestH5PData.out

if diff JUnit-TestH5PData.out JUnit-TestH5PData.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5PData"
else
    echo "**FAILED**    JUnit-TestH5PData"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5PData.txt JUnit-TestH5PData.out |sed 's/^/    /'
fi

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Pfapl"
TESTING JUnit-TestH5Pfapl
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Pfapl > JUnit-TestH5Pfapl.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5Pfapl.ext > JUnit-TestH5Pfapl.out

if diff JUnit-TestH5Pfapl.out JUnit-TestH5Pfapl.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5Pfapl"
else
    echo "**FAILED**    JUnit-TestH5Pfapl"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5Pfapl.txt JUnit-TestH5Pfapl.out |sed 's/^/    /'
fi

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Pvirtual"
TESTING JUnit-TestH5Pvirtual
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Pvirtual > JUnit-TestH5Pvirtual.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5Pvirtual.ext > JUnit-TestH5Pvirtual.out

if diff JUnit-TestH5Pvirtual.out JUnit-TestH5Pvirtual.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5Pvirtual"
else
    echo "**FAILED**    JUnit-TestH5Pvirtual"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5Pvirtual.txt JUnit-TestH5Pvirtual.out |sed 's/^/    /'
fi

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Plist"
TESTING JUnit-TestH5Plist
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Plist > JUnit-TestH5Plist.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5Plist.ext > JUnit-TestH5Plist.out

if diff JUnit-TestH5Plist.out JUnit-TestH5Plist.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5Plist"
else
    echo "**FAILED**    JUnit-TestH5Plist"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5Plist.txt JUnit-TestH5Plist.out |sed 's/^/    /'
fi

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5A"
TESTING JUnit-TestH5A
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5A > JUnit-TestH5A.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5A.ext > JUnit-TestH5A.out

if diff JUnit-TestH5A.out JUnit-TestH5A.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5A"
else
    echo "**FAILED**    JUnit-TestH5A"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5A.txt JUnit-TestH5A.out |sed 's/^/    /'
fi

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Oparams"
TESTING JUnit-TestH5Oparams
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Oparams > JUnit-TestH5Oparams.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5Oparams.ext > JUnit-TestH5Oparams.out

if diff JUnit-TestH5Oparams.out JUnit-TestH5Oparams.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5Oparams"
else
    echo "**FAILED**    JUnit-TestH5Oparams"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5Oparams.txt JUnit-TestH5Oparams.out |sed 's/^/    /'
fi

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Obasic"
TESTING JUnit-TestH5Obasic
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Obasic > JUnit-TestH5Obasic.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5Obasic.ext > JUnit-TestH5Obasic.out

if diff JUnit-TestH5Obasic.out JUnit-TestH5Obasic.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5Obasic"
else
    echo "**FAILED**    JUnit-TestH5Obasic"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5Obasic.txt JUnit-TestH5Obasic.out |sed 's/^/    /'
fi

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Ocreate"
TESTING JUnit-TestH5Ocreate
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Ocreate > JUnit-TestH5Ocreate.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5Ocreate.ext > JUnit-TestH5Ocreate.out

if diff JUnit-TestH5Ocreate.out JUnit-TestH5Ocreate.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5Ocreate"
else
    echo "**FAILED**    JUnit-TestH5Ocreate"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5Ocreate.txt JUnit-TestH5Ocreate.out |sed 's/^/    /'
fi

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Ocopy"
TESTING JUnit-TestH5Ocopy
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Ocopy > JUnit-TestH5Ocopy.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5Ocopy.ext > JUnit-TestH5Ocopy.out

if diff JUnit-TestH5Ocopy.out JUnit-TestH5Ocopy.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5Ocopy"
else
    echo "**FAILED**    JUnit-TestH5Ocopy"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5Ocopy.txt JUnit-TestH5Ocopy.out |sed 's/^/    /'
fi

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5PL"
TESTING JUnit-TestH5PL
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5PL > JUnit-TestH5PL.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5PL.ext > JUnit-TestH5PL.out

if diff JUnit-TestH5PL.out JUnit-TestH5PL.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5PL"
else
    echo "**FAILED**    JUnit-TestH5PL"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5PL.txt JUnit-TestH5PL.out |sed 's/^/    /'
fi

echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Z"
TESTING JUnit-TestH5Z
($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Z > JUnit-TestH5Z.ext)

# Extract file name, line number, version and thread IDs because they may be different
sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
    -e 's/line [0-9]*/line (number)/' \
    -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
    -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
    -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
    JUnit-TestH5Z.ext > JUnit-TestH5Z.out

if diff JUnit-TestH5Z.out JUnit-TestH5Z.txt > /dev/null; then
    echo "  PASSED      JUnit-TestH5Z"
else
    echo "**FAILED**    JUnit-TestH5Z"
    echo "    Expected result differs from actual result"
    nerrors="`expr $nerrors + 1`"
    test yes = "$verbose" && $DIFF JUnit-TestH5Z.txt JUnit-TestH5Z.out |sed 's/^/    /'
fi

if test "X-$BUILD_MODE" = "X-production" ; then
    if test $USE_FILTER_SZIP = "yes"; then
        echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5E"
        TESTING JUnit-TestH5E
        ($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5E > JUnit-TestH5E.ext)

        # Extract file name, line number, version and thread IDs because they may be different
        sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
            -e 's/line [0-9]*/line (number)/' \
            -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
            -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
            -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
            JUnit-TestH5E.ext > JUnit-TestH5E.out

        if diff JUnit-TestH5E.out JUnit-TestH5E.txt > /dev/null; then
            echo "  PASSED      JUnit-TestH5E"
        else
            echo "**FAILED**    JUnit-TestH5E"
            echo "    Expected result differs from actual result"
            nerrors="`expr $nerrors + 1`"
            test yes = "$verbose" && $DIFF JUnit-TestH5E.txt JUnit-TestH5E.out |sed 's/^/    /'
        fi
    fi

    if test $USE_FILTER_SZIP = "yes"; then
        echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Edefault"
        TESTING JUnit-TestH5Edefault
        ($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Edefault > JUnit-TestH5Edefault.ext)

        # Extract file name, line number, version and thread IDs because they may be different
        sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
            -e 's/line [0-9]*/line (number)/' \
            -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
            -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
            -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
            JUnit-TestH5Edefault.ext > JUnit-TestH5Edefault.out

        if diff JUnit-TestH5Edefault.out JUnit-TestH5Edefault.txt > /dev/null; then
            echo "  PASSED      JUnit-TestH5Edefault"
        else
            echo "**FAILED**    JUnit-TestH5Edefault"
            echo "    Expected result differs from actual result"
            nerrors="`expr $nerrors + 1`"
            test yes = "$verbose" && $DIFF JUnit-TestH5Edefault.txt JUnit-TestH5Edefault.out |sed 's/^/    /'
        fi
    fi
fi

if test $USE_FILTER_SZIP = "yes"; then
    echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Giterate"
    TESTING JUnit-TestH5Giterate
    ($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Giterate > JUnit-TestH5Giterate.ext)

    # Extract file name, line number, version and thread IDs because they may be different
    sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
        -e 's/line [0-9]*/line (number)/' \
        -e 's/Time: [0-9]*[\.[0-9]*]*/Time:  XXXX/' \
        -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
        -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
        JUnit-TestH5Giterate.ext > JUnit-TestH5Giterate.out

    if diff JUnit-TestH5Giterate.out JUnit-TestH5Giterate.txt > /dev/null; then
        echo "  PASSED      JUnit-TestH5Giterate"
    else
        echo "**FAILED**    JUnit-TestH5Giterate"
        echo "    Expected result differs from actual result"
        nerrors="`expr $nerrors + 1`"
        test yes = "$verbose" && $DIFF JUnit-TestH5Giterate.txt JUnit-TestH5Giterate.out |sed 's/^/    /'
    fi
fi
if test "X$ROS3_VFD" = "Xyes"; then
    echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Pfapls3"
    TESTING JUnit-TestH5Pfapls3
    ($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Pfapls3 > JUnit-TestH5Pfapls3.ext)

    # Extract file name, line number, version and thread IDs because they may be different
    sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
        -e 's/line [0-9]*/line (number)/' \
        -e 's/Time: [0-9]*\.[0-9]*/Time:  XXXX/' \
        -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
        -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
        JUnit-TestH5Pfapls3.ext > JUnit-TestH5Pfapls3.out

    if diff JUnit-TestH5Pfapls3.out JUnit-TestH5Pfapls3.txt > /dev/null; then
        echo "  PASSED      JUnit-TestH5Pfapls3"
    else
        echo "**FAILED**    JUnit-TestH5Pfapls3"
        echo "    Expected result differs from actual result"
        nerrors="`expr $nerrors + 1`"
        test yes = "$verbose" && $DIFF JUnit-TestH5Pfapls3.txt JUnit-TestH5Pfapls3.out |sed 's/^/    /'
    fi
fi
if test "X$HAVE_LIBHDFS" = "Xyes"; then
    echo "$JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Pfaplhdfs"
    TESTING JUnit-TestH5Pfaplhdfs
    ($RUNSERIAL $JAVAEXE $JAVAEXEFLAGS -Xmx1024M -Dorg.slf4j.simpleLogger.defaultLog=trace -Djava.library.path=$BLDLIBDIR -cp $CLASSPATH -ea org.junit.runner.JUnitCore test.TestH5Pfaplhdfs > JUnit-TestH5Pfaplhdfs.ext)

    # Extract file name, line number, version and thread IDs because they may be different
    sed -e 's/thread [0-9]*/thread (IDs)/' -e 's/: .*\.c /: (file name) /' \
        -e 's/line [0-9]*/line (number)/' \
        -e 's/Time: [0-9]*\.[0-9]*/Time:  XXXX/' \
        -e 's/v[1-9]*\.[0-9]*\./version (number)\./' \
        -e 's/[1-9]*\.[0-9]*\.[0-9]*[^)]*/version (number)/' \
        JUnit-TestH5Pfaplhdfs.ext > JUnit-TestH5Pfaplhdfs.out

    if diff JUnit-TestH5Pfaplhdfs.out JUnit-TestH5Pfaplhdfs.txt > /dev/null; then
        echo "  PASSED      JUnit-TestH5Pfaplhdfs"
    else
        echo "**FAILED**    JUnit-TestH5Pfaplhdfs"
        echo "    Expected result differs from actual result"
        nerrors="`expr $nerrors + 1`"
        test yes = "$verbose" && $DIFF JUnit-TestH5Pfaplhdfs.txt JUnit-TestH5Pfaplhdfs.out |sed 's/^/    /'
    fi
fi


# Clean up temporary files/directories
CLEAN_LIBFILES_AND_BLDLIBDIR
CLEAN_DATAFILES_AND_BLDDIR

# Report test results and exit
if test $nerrors -eq 0 ; then
    echo "All $TESTNAME tests passed."
    exit $EXIT_SUCCESS
else
    echo "$TESTNAME tests failed with $nerrors errors."
    exit $EXIT_FAILURE
fi
