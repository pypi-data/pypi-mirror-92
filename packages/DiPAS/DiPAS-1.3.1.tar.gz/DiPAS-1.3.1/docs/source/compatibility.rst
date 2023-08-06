Compatibility with MADX
=======================

The DiPAS package ships with a MADX parser which can parse most of the MADX syntax. Hence parsing lattices from
MADX files should work without problems in most cases.
Due to the (dynamically typed) nature of the parser a few noteworthy differences
to the MADX syntax exist however and are explained in the following sub-sections.
An essential add-on to the syntax is described as well.
If desired, the parsing process can be further customized via the ``madx.parser`` module attributes. Please
refer to this module's documentation for more information.
The MADX parser is fully contained in the ``madx`` subpackage. The main entry functions for parsing MADX scripts are
``madx.parse_file`` and ``madx.parse_script``.


Declaring variables used for the optimization process (add-on)
--------------------------------------------------------------

This is an addition to the existing MADX syntax and in order not to interfere with it, this is realized via placement of
special comments. Since the purpose of differentiable simulations is to optimize some set of parameters, a seamless
syntax for indicating the relevant parameters is desirable (we call these to-be-optimized-for parameters
"*flow variables*"). This can be done directly in the MADX scripts, by placing special comments of the form
``// <optional text goes here> [flow] variable``, i.e. a comment that is concluded with the string ``[flow] variable``.
These can be placed in three different ways to mark a variable (or attribute) as an optimization parameter.

On the same line as the variable definition:

.. code-block:: text

    q1_k1 = 0;  // [flow] variable
    q1: quadrupole, l=1, k1=q1_k1;

On the line preceding the variable definition:

.. code-block:: text

    // [flow] variable
    q1_k1 = 0;
    q1: quadrupole, l=1, k1=q1_k1;

On the same line that sets an attribute value:

.. code-block:: text

    q1: quadrupole, l=1, k1=0;
    q1->k1 = 0;  // [flow] variable

All of the above three cases will create a Quadrupole element with variable (to be optimized) ``k1`` attribute with
initial value set to ``0``.

The same syntax also works with error definitions, for example:

.. code-block:: text

    SELECT, flag = error, class = quadrupole;
    dx = 0.001;  // [flow] variable
    EALIGN, dx = dx;

This will cause all Quadrupole elements to have an initial alignment error of ``dx = 0.001`` which are however variable
during the optimization process.

Flow variables also work with deferred expressions:

.. code-block:: text

    SELECT, flag = "error", class = "quadrupole";
    dx := ranf() - 0.5;  // [flow] variable
    EALIGN, dx = dx;

Here again each Quadrupole's ``dx`` alignment error will be optimized for and has a random initial value in
``[-0.5, 0.5]``.


Variations to the MADX syntax
-----------------------------

* **Beam command** - For ``BEAM`` commands the particle type as well as the beam energy must be unambiguously specified
  (via ``particle`` or ``{mass, charge}`` and one of ``energy, pc, beta, gamma, brho``).
* **String literals** - String literals without spaces may be unquoted only for the following set of command attributes:
  ``{'particle', 'range', 'class', 'pattern', 'flag', 'file', 'period', 'sequence', 'refer', 'apertype', 'name', 'from'}``.
  Which attributes are considered to be string attributes is regulated by the ``madx.command_str_attributes`` variable
  and users may add their own names if appropriate. All other string attributes must use quotation marks for correct parsing.
* **Variable names** - All variable names containing a dot ``.`` will be renamed by replacing the dot with an underscore.
  In case a similar name (with an underscore) is already used somewhere else in the script a warning will be issued.
  The string which will be used to replace dots in variable names can be configure via
  ``madx.replacement_string_for_dots_in_variable_names``. It needs to be part of the set of valid characters for Python names
  (see `the docs <https://docs.python.org/3/reference/lexical_analysis.html#identifiers>`__, basically this is ``[A-Za-z0-9_]``).
* **Defaults for unknown variable names** - By default, if MADX encounters an unknown (i.e. yet undefined) variable name,
  it assumes a value of ``0`` for it. DiPAS has more fine-grained control via the attributes
  ``dipas.madx.parser.allow_popup_variables`` (default ``True``) and ``dipas.madx.parser.missing_variable_names`` (default empty).
  The former controls whether expressions that consist of a single variable name, e.g. ``undefined`` in
  ``quadrupole, k1 = undefined``, default to zero or raise an error.
  The latter is a mapping from deliberately missing variable names (or patterns describing these names) to desired default
  values. This dictionary can filled by the user, e.g. ``dipas.madx.parser.missing_variable_names['k1_*'] = 0`` would use
  a default of ``0`` for every undefined variable that starts with ``k1_``. For more information please refer to
  the documentation of the ``dipas.madx.parser`` module.
* **Aperture checks** - Aperture checks on Drift spaces will be performed at the entrance of the drift space (as opposed to MADX).
  In case intermediary aperture checks for long drift spaces are desired, appropriate markers can be placed in-between.
  The ``maxaper`` attribute of the ``RUN`` command is ignored. Only explicitly defined apertures of the elements are considered.
* **Random number generation** - All the random functions from MADX are supported however the underlying random
  number generator (RNG) is (potentially) different. For that reason, even if the same seed for the RNG is used,
  the values generated by MADX and by DiPAS will likely differ. For that reason is it important, when comparing results
  obtained with DiPAS and MADX, to always generate a new MADX script from the particular DiPAS lattice to
  ensure the same numerical values from random functions. If the original MADX script (from which the DiPAS lattice was
  parsed) is used, then these values might differ and hence the results are not comparable.
  For error definitions the user can load and assign the specific errors which were generated by MADX (see `build.assign_errors`).
* **Single-argument commands** - Commands that have a single argument without specifying an argument name, such as
  ``SHOW`` or ``EXEC``, are interpreted to indicate a (single) flag, analogue to ``OPTION``. For example using ``OPTION``
  MADX considers the following usages equivalent: ``OPTION, warn;`` and ``OPTION, warn = true;`` (i.e. ``warn`` being a
  positive flag). The DiPAS parser treats other commands in a similar manner, for example ``SHOW, q1;`` will be converted to
  ``SHOW, q1 = true;``. The same holds also for ``VALUE`` but expressions here need to be unquoted, otherwise this will
  result in a parsing error. That means when inspecting the resulting command list these are still useful with the
  subtlety that the single-arguments are stored as argument names together with the argument value ``"true"``.


Unsupported statement types
---------------------------

* Program flow constructs such as ``if / else`` or ``while``.
* Macro definitions.
* Commands that take a single quoted string as argument without specifying an argument name such as ``TITLE`` or ``SYSTEM``.
* Template beamlines defined via ``label(arg): LINE = (arg);`` ("normal" beamline definitions (without ``arg``) can be
  used though).
