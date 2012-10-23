Fundamental data types
======================

The following defined types are used in the subsequent sections.
Implementors should treat these sizes as minimium requirements.

.. note::
    **Roger Leigh**  Depending upon how we wish to persue
    interoperability between implementations, these may be required to
    be exact.  Using plain text would mitigate this to an extent.

Basic primitives
----------------

.. csv-table:: Primitives
    :header-rows: 1
    :file: spec/primitives.txt
    :delim: tab

.. csv-table:: Compound primitives
    :header-rows: 1
    :file: spec/compound.txt
    :delim: tab

.. note::
    **Barry DeZonia** Support different coordinate spaces as needed
    (int, long, double).  Should be possible to iterate some regions.

Basic operators
---------------

======== ===== ========================
Operator Value Description
======== ===== ========================
=        0     Equals
≠        1     Not equals
<        2     Less than
≤        3     Less than or equal to
>        4     Greater than
≥        5     Greater than or equal to
======== ===== ========================

Binary bitwise operators
------------------------

======== ===== ============
Operator Value Description
======== ===== ============
AND      0     And
OR       1     Or
NOT      2     Not
XOR      3     Exclusive or
======== ===== ============


All shape primitives are described in terms of the above fundamental
primitives.  This means that all shape descriptions are serialisable
as a list of integer and double-precision floating point values.  The
specifics of this are implementation-defined.  Example formats:

- Plain text, as a list of values
- XML, as element content or a string attribute
- Binary data stream, using big-endian/network byte order

This also means that for compatible shape types, the shape type may be
changed while retaining the following data unchanged (e.g. polyline to
polygon spline with the same point list).

.. note::
    **Roger Leigh** All 2D shape primitives could be oriented in 3D or
    using a unit Vector3D, which would allow all 2D shapes to be used
    as surfaces in 3D.  They would additionally require a depth in
    order to be meaningful (or assume a depth of one z slice).

    Or, 2D shapes should specify the pair of x/y/z axes they are
    using, and will be extruded along the third axis.
