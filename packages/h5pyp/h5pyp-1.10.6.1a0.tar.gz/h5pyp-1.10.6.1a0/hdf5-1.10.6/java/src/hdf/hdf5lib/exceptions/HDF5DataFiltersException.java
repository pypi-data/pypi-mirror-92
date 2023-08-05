/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 * Copyright by The HDF Group.                                               *
 * Copyright by the Board of Trustees of the University of Illinois.         *
 * All rights reserved.                                                      *
 *                                                                           *
 * This file is part of HDF5.  The full HDF5 copyright notice, including     *
 * terms governing use, modification, and redistribution, is contained in    *
 * the COPYING file, which can be found at the root of the source code       *
 * distribution tree, or in https://support.hdfgroup.org/ftp/HDF5/releases.  *
 * If you do not have access to either file, you may request a copy from     *
 * help@hdfgroup.org.                                                        *
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

package hdf.hdf5lib.exceptions;

/**
 * The class HDF5LibraryException returns errors raised by the HDF5 library.
 * <p>
 * This sub-class represents HDF-5 major error code <b>H5E_PLINE</b>
 */
public class HDF5DataFiltersException extends HDF5LibraryException {
    /**
     * Constructs an <code>HDF5DataFiltersException</code> with no specified
     * detail message.
     */
    public HDF5DataFiltersException() {
        super();
    }

    /**
     * Constructs an <code>HDF5DataFiltersException</code> with the specified
     * detail message.
     *
     * @param s
     *            the detail message.
     */
    public HDF5DataFiltersException(String s) {
        super(s);
    }
}
