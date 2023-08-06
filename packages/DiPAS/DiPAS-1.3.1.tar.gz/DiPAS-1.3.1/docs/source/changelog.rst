Changelog
=========

v1.3
----

Enhancements
~~~~~~~~~~~~

* New exception types for errors during parsing and building:

  * :class:`dipas.build.UnknownVariableNameError`
  * :class:`dipas.madx.parser.IllegalStatementError`

* Parsing and build errors now include the line number indicating where the error originated
* MADX default values for element attributes are now supported
* New option to define defaults for missing variables during parsing: ``dipas.madx.parser.missing_variable_names``
  (see :doc:`compatibility` and :mod:`dipas.madx.parser` for details); this is useful for parsing sequences without
  optics files

Changes
~~~~~~~

* Deleting elements from a segment now replaces them with equivalent drift spaces (the old behavior was to simply
  remove them; the difference matters for non-zero-length elements). In order to completely remove elements, one should
  delete from ``segment.elements`` instead.


v1.2
----

Enhancements
~~~~~~~~~~~~

* Interface for external optimizers (+ example in docs)
* Random noise for BPMErrors
* Method for merging consecutive drift spaces: ``Segment.squeeze``
* New command line utility: ``print-beam``
* New module for plotting lattices and Twiss data: ``dipas.plot``
* New command line interface for common operations such as plotting, Twiss, ORM


v1.1
----

Enhancements
~~~~~~~~~~~~

* ``build.Lattice`` now supports auto-labeling its elements.
* A custom exception is raised if the orbit diverges during closed orbit search.
* ``BPMErrors`` are included during ORM computation.
* Field errors can be added to ``Kicker`` elements.


v1.0
----

DiPAS 1.0 supports a wide variety of simulation capabilities among which are:

* Closed orbit search
* Twiss computation
* Transfer maps
* Orbit Response Matrix
* Particle Tracking

Various lattice elements as well as alignment errors and field errors are supported.

The framework understands most MADX syntax for describing lattices and thus can parse MADX files.
It also includes utility functions for interfacing with MADX and for creating corresponding script files.
