:Author: Jérôme Kieffer
:Date: 11/01/2021
:Keywords: changelog

Change-log of versions
======================

0.20.0 22/01/2021
-----------------
* One year of development, about 500 commits & 370 files modified.
* Generalization of the new generation 1D integrators (better error propagation)
* Sigma clipping and sparsification of single crystal data (OpenCL only)  
* Fix issue introduced with the scipy 1.15 (constrained calibration broken)  
* Improved distortion correction (also on GPU, ...)
* Major re-work of the documentation (thanks Thomas Kluyver and Loic Huder)
* Improve the calibration of Pilatus and Eiger detectors based on a grid of holes.
* New cylindrical detector from Rigaku
* Drop deprecated OpenCL integrator
* Support all Eiger2 detectors (thanks Clemens Weninger and Marie Ruat)
* CI: move to Gihub workflow and gitlab-runners (bob) for building (thanks Thomas Vincent).
* Build for debian 10 and 11 (also ubuntu 20.04), drop debian 9
* Remove Python2 related code
* Lower Numpy ABI dependency as much as possible (remains _distortion's C++ code)
* Drop tests for Python 3.5, checked on 3.9 as well.

0.19.0 31/01/2020
-----------------
* Minor revison with only 150 commits, mainly bug-fixes
* Improvement on the GUI with many small bug-fixes
* Support newer h5py (mode mandatory, [()], ...)
* Build for debian 10 and 11 (also ubuntu 20.04)
* Drop tests for Python 2 and 3.4, checked on 3.8
* Improved compatibility with ImageD11
* Use hdf5plugin to provide hdf5 io-filters in apps
* Rework diffraction mapping tools to use a worker
* New generation azimuthal integrator using CSR algorithm
  implemented in Python, Cython and OpenCL.
* Sigma-clipping implemented in OpenCL
* Publication on new generation integration, the GUI for
  calibration and the goniometers accepted in J. Synch. Rad.
  DOI: 10.1107/S1600577520000776
* A big thank to Florian from Germany, Bertrand from Xenocs,
  Alex from Soleil and Jon from ESRF for their contributions.

0.18.0 15/05/2019
-----------------
* Last release with Valentin as he finishes his contract soon
* almost 800 commits, 60 PR since the last release: this is a huge release !
* Major rework on all GUIs, mainly pyFAI-calib2 and pyFAI-integrate.
* Possibility to integrate image stacks (i.e. from HDF5), ...
* Rework the *method* to specify the algorithm, pixel splitting and implementation
  with sensible fall-backs. Also available via the different GUIs
* 3D visualization of detectors and experimental setup, useful for non flat detectors.
* `integrate1d_ng` is available with histogramming without pixel splitting in
  Python, Cython and OpenCL. Now, propagates the variance properly !
* IO sub-packages with associated refactoring for ponifile, json, ...
* Improved management of OpenMP: simplify the code for histograms.
* Improved geometry description and tutorial for writing exchange with other
  software (ImageD11, thanks to Carsten Detlefs).
* More reliable simple ellipse fitting with tests and doc.
* Better POCL integration (debugged on cuda, x87, Power9, ...)
* Rely on *silx* mechanics for the build, test, download, GUI, opencl ...
* Many new tutorials, now available on binder-hub: new calibrants, Pilatus calibration, ...
* Fix many issues reported in third-party software (Dioptas, ...)
* Drop support of debian8, Python 2.7 and Python 3.4 on all platforms.
  It is likely most functionalities still work but without guaranty.

0.17.0 19/12/2018
-----------------
* Only 200 commits in a couple of month, this is a small release
* Fix major bugs in pyFAI-calib2 (double validator, initial guess, ring position)
* Constrains have been added to the geometry fitting of pyFAI-calib2
* New pyFAI-integrate graphical application
* Much better support for user defined detector (HDF5)
* Start the rewrite of all integrators to allow proper error propagation (2D done)
* Factorize the preprocessing steps for many integrators
* Remove tons of code which has been deprecated for years in AzimuthalIntegrator
* Featuring contribution from Soleil and Berkeley
* Stop supporting Python2.7 on Windows (there won't be wheels!)
* All scripts are now using Python 3.x (x>=4)
* This is the last release supporting Python 2.7, 3.4 hence debian 8

0.16.0: 26/10/2018
------------------
* Almost 800 commits since 0.15 !
* Huge improvements on the graphical application for calibration
* New detector definition (with manufacturers)
* Improved tests: the GUI is now tested
* Preparation for changing all rebinning engines (see variance tutorials)
* Azimuthal integrators (and most other objects) are now serializable with Pickle
* New distortion correction using the SparseBuilder C++ code
* New PONI-file format (detector definition changed)
* Isocontour is now provided by *silx*
* Peak-picker clean up (better peak selection near gaps)
* new Goniometer refinement with enhanced rotation using Euler angles
* Updated documentation: new cookbooks and tutorials about:
  - The use of the calibration application (cookbook)
  - log-scale integration of SAXS data (notebook)
  - Variance propagation (notebook)


0.15.0: 01/02/2018
------------------
* 150 commits since last revision
* New tutorials on image inpainting, sensor thickness correction, ...
* Improve scripts
* Improve the new calibration GUI (pyFAI-calib2)
* Use scipy physical constants instead of hard-coded values
* Improved detector serialization and binning assessement
* Update documentation (images, better rendering of notebook & tutorials)
* Converge project with silx and fabio
* Remove generated rst- and C-files from repository
* This is the last version supporting python2.7

0.14.2: 14/09/2017
------------------
* Fix seg-fault with manylinux1 wheels, in fastcrc module (thanks Thomas)
* Fix Qt4-Qt5 compatibility (thanks Vadim)
* Easier to understand geometry transformation (thanks Jon)
* Lower memory consumption, better cache management
* Unified debian packaging working for 6->9
* New detector: Mythen & CirPad (thanks Fred)
* Clean up debug code which avoid to use pyFAI-calib2
* pyFAI-calib2 now expect fabio >= 0.5
* Fix issue with metadata saving in 1d
* Fix performance regression with pyopencl >2015.2 (Thanks Andreas)
* pyFAI saxs and waxs scripts guess now the binning of the detector (thanks Fred).

0.14.1: 25/07/2017
------------------
* Fixes Debian 7 and 8 packages

0.14.0: 20/07/2017
------------------
* Graphical user interface for calibration (pyFAI-calib2)
* Goniometer calibration tools and multi-geometry enhancements
* Integration scripts and averaging scripts are now able to normalize the data
  from monitors found in the header.
* Propagate metadata information as part of the integrated data
* Common pre-processing factorization on Python, Cython and OpenCL
* Test clean up and acceleration (avoid tests on too large images)
* Many new tutorials http://pyfai.readthedocs.io/en/latest/usage/tutorial/index.html
* New averaging / integration methods:
  - Azimuthal median filtering
  - Azimuthal trimmed mean
  - sigma-clipping on azimuthal angle
  - Radial averaging
* Diffraction image inpainting to fill-up the gaps with plausible values.
* This release correspond to 572 commits
* Change of license: now all pyFAI is MIT license.

0.13.0: 01/12/2016
------------------
* Global improvement of tests, packaging, code quality, documentation and project tools
* Scripts
    - Add support for multiframe formats on pyFAI-average
    - Add support for monitoring correction from header file (on pyFAI-average)
    - Add progressbar in the shell (on pyFAI-average and pyFAI-integrate)
    - Script drawMask_pymca is renamed into pyFAI-drawmask
    - Rework of the drawmask GUI using silx
    - pyFAI-drawmask do not have anymore hard dependency on PyMCA
    - pyFAI-integrate can now be used without qt dependency (--no-gui)
    - Fix the script to support both Python 2 and 3 (pyFAI-calib, pyFAI-benchmark)
    - Fix selection of units on diff-map (the user selection was not propagated)
* For users
    - More source code in MIT license
    - Update name and specification for cameras
    - Add cameras: Eiger500k, RaspberryPi5M, RaspberryPi8M
    - Fix Xpad S540 flat detector geometry
    - Fix definition of CeO2 calibrant
    - Add mask and flat on multi-geometry
    - Fix solid angle of the multi-geometry
    - Fix geometry processing for custom output space
    - Fix normalization factor and variance
    - Add support for Qt5
    - Add support for Debian 9 packaging
* For developers
    - Create common preprocessing for distortion correction
    - Create common image preprocessing using Cython (NaN filter, flatfield, dark, polarisation)
    - Refactoring of units module. It allows to register custom units.
    - Worker can now use Writer
    - Worker polarization argument is renamed into polarization_factor
    - Remove the dependency from python-fftw3, use numpy instead
    - Remove QtWebKit dependency
    - Fix un-correction of images using sparse matrix from scipy

0.12.0: 06/06/2016
------------------
* Continuous integration on linux, windows using Python 2.7 and 3.4+
* Drop support of Python 2.6, 3.2, 3.3 and debian6 packaging
* New radial output units: Reciprocal spacing squared and log(q) **ID02**
* GPU accelerate version of ai.separate (Bragg & amorphous) **ID13**
* Quantile filtering in pyFAI-average **ID02**
* New graphical application for diffraction imaging **ID21**
* Migrate to a common structure with *silx* (reorganize tests, benchmarks, ...)
* Extensions (binary sub-modules) have all been moved to *ext* directory
* Many improvements multigeometry integrators
* Compatibility with the copy module (copy.deepcopy) for azimuthal integrator **ID02**
* Distortion correction works also for non-contiguous detectors
* Update documentation and provide advanced tutorials:
    - Introduction to pyFAI using the jupyter notebook
    - detector calibration **ID15, BM02**
    - Correction of detector distortion, examples of pixel detectors.
    - calibrant calculation **ID30**
    - error handling **ID02, BM29**
* pyFAI-integrate can now be used with or without GUI
* Many new detectors (ADSC, Pilatus CdTe, Apex II, Pixium):
    - support for non-flat/curved detectors (Aarhus)
    - non-contiguous detectors (WOS Xpad)
* Include tests and benchmarking tools as part of the library
* Better testing.

0.11.0: 07/2015
---------------
* All calibrant from NIST are now available, + Nickel, Aluminum, ... with bibliographic references
* The Cell class helps defining new calibrants.
* OpenCL Bitonic sort (to be integrated into Bragg/Amorphous separation)
* Calib is available from the Python interface (procedural API), not only from the shell script.
* Many new options in calib for reset/assign/delete/validate/validate2/chiplot.
    - reset: set the detector, orthogonal, centered and at 10cm
    - assign: checks the assignment of groups of points to rings
    - delete: remove a group of peaks
    - validate: autocorrelation of images: error on the center
    - validate2:  autocorrelation of patterns at 180° apart: error on the center function of chi
    - chiplot: assesses the quality of control points of one/multiple rings.
* Fix the regression of the initial guess in calib (Thanks Jon Wright)
* New peak picking algorithm named "watershed" and based on inverse watershed for ridge recognition
* start factorizing cython regridding engines (work ongoing)
* Add "--poni" option for pyFAI-calib (Thanks Vadim Dyakin)
* Improved "guess_binning", especially for Perkin Elmer flat panel detectors.
* Support for non planar detectors like Curved Imaging plate developped at Aarhus
* Support for Multi-geometry experiments (tested)
* Speed improvement for detector initialization
* better isotropy in peak picking (add penalization term)
* enhanced documentation on http://pyfai.readthedocs.org

0.10.3: 03/2015
---------------
* Image segmentation based on inverse watershed (only for recalib, not for calib)
* Python3 compatibility
* include testimages  into distribution


0.10.2: 11/2014
---------------
* Update documentation
* Packaging for debian 8

0.10.1: 10/2014
---------------
* Fix issue in peak-picking
* Improve doc & manpages
* Compatibility with PyMca5

0.10.0: 10/2014
---------------
* Correct Caglioti's formula
* Update tests and OpenCL -> works with Beignet and pocl open source drivers
* Compatibility with MacOSX and windows

0.9.4:  06/2014
---------------
* include spec of Maxwell GPU
* fix issues with intel OpenCL icd v4.4
* introduce shape & max_shape in detectors
* work on marchingsquares/sorted controurplot for calibration
* Enforce the use the Qt4Agg for Matplotlib and other GUI stuff.
* Update shape of detector in case of binning
* unified distortion class: merge OpenCL & OpenMP implementation #108
* Benchmarks for distortion
* Raise the level to warning when inverting the mask
* set of new ImXpad detectors Related issue #111
* Fix issue with recalib within MX-calibrate
* saving detector description in Nexus files issue #110
* Update some calibrants: gold
* about to make peak-picking more user-friendly
* test for bragg separation
* work on PEP8 compliance
* Do not re-cythonize: makes debian package generation able to benefit from ccache
* conversion to SPD (rotation is missing)
* pixelwise worker
* correct both LUT & OCL for memory error
* replace os.linsep with "\n" when file file opened in text mode (not binary)
* rework the Extension part to be explicit instead of "black magic" :)
* implement Kahan summation in Cython (default still use Doubles: faster)
* Preprocessing kernel containing all cast to float kernels  #120
* update setup for no-openmp option related to issue #127
* Add read-out mode for mar345 as "guess_binning" method for detector. Also for MAR and Rayonix #125
* tool to benchmark HDF5 writing
* try to be compatible with both PySide and PyQt4 ... the uic stuff is untested and probably buggy #130
* Deactivate the automatic saturation correction by default. now it is opt-in #131

0.9.3:  02/2014
---------------
* Better control for peak-picking (Contribution from Gero Flucke, Desy)
* Precise Rayonix detectors description thanks to Michael Blum
* Start integrating blob-detection algorithm for peak-picking: #70
* Switch fron OptParse to ArgPrse: #83
* Provide some calibrant by default: #91
* Description of Mar345 detector + mask#92
* Auto-registration of detectors: #97
* Recalib and check-calib can be called from calib: #99
* Fake diffraction image from calibrant: #101
* Implementation of the CSR matrix representation to replace LUT
* Tight pixel splitting: #43
* Update documentation

0.9.2: (01/2014)
----------------
* Fix memory leak in Cython part of the look-up table generation
* Benchmarks with memory profiling

0.9: 10/2013
------------
* Add detector S140 from ImXpad, Titan from Agilent, Rayonix
* Fix issues: 61, 62, 68, 76, 81, 82, 85, 86, 87
* Enhancement in LImA plugins (better structure)
* IO module with Ascii/EDF/HDF5 writers
* Switch some GUI to pyQtGraph in addition to Qt
* Correction for solid-angle formula

0.8: 10/2012
------------
* Detector object is member of the geometry
* Binning of the detector, propagation to the spline if needed
* Detector object know about their masks.
* Automatic mask for some detectors like Pilatus or XPad
* Implementation of sub-pixel position correction for Pilatus detectors
* LUT implementation in 1D & 2D (fully tested) both with OpenMP and with OpenCL
* Switch from C++/Cython OpenCL framework to PyOpenCL
* Port opencl code to both Windows 32/64 bits and MacOSX
* Add polarization corrections
* Use fast-CRC checksum on x86 using SSE4 (when available) to track array change on GPU buffers
* Support for flat 7*8 modules Xpad detectors.
* Benchmark with live graphics (still a memory issue with python2.6)
* Fat source distribution (python setup.py sdist --with-test-images) for debian
* Enhanced tests, especially for Saxs and OpenCL
* Recalibration tool for refining automatically parameters
* Enhancement of peak picking (much faster, recoded in pure Cython)
* Easy calibration for pixel detector (reconstruction of inter-module space)
* Error-bar generation using Poisson law
* Unified programming interface for all integration methods in 2theta, q or radius unit
* Graphical interface for azimuthal integration (pyFAI-integrate)
* Lots of test to prevent non regression
* Tool for merging images using various method (mean, median) and with outlayer rejection
* LImA plugin which can perform azimuthal integration live during the acquisition
* Distortion correction is available alone and as LImA plugin
* Recalibration can refine the wavelength in addition to 6 other parameters
* Calibration always done vs calibrant's ring number, lots of new calibrant are available
* Selection by hand of single peaks for calibration
* New detectors: Dexela and Perkin-Elmer flat panel
* Automatic refinement of multiple images at various geometries (for MX)
* Many improvements requested by ID11 and ID13

0.7.2: 08/2012
--------------
* Add diff_tomo script
* Geometry calculation optimized in (parallel) cython

0.7: 07/2012
------------
Implementation of look-up table based integration and OpenCL version of it

0.6: 07/2012
------------
* OpenCL flavor works well on GPU in double precision with device selection

0.5: 06/2012
------------
* Include OpenCL version of azimuthal integration (based on histograms)

0.4: 06/2012
------------
* Global clean up of the code regarding options from command line and better design
* Correct the orientation of the azimuthal angle chi
* Rename scripts in pyFAI-calib, pyFAI-saxs and pyFAI-waxs

0.3: 11/2011
------------
* Azimuthal integration splits pixels like fit2d

0.2: 07/2011
------------
* Azimuthal integration using cython histogramming is working

0.1: 05/2011
------------
 * Geometry is OK
