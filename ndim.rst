Regions in arbitrary dimensions
===============================

While it is possible to use geometric shapes to specify regions in
physical dimensions, this does not translate meaningfully to arbitrary
dimensions.  The following primitives work in any "dimension" with a
discrete or continuous range by permitting the selection of specific
values, or sub-ranges.

These representations could be represented efficiently using a 1D
bitmap or Line1D.

Regions within a single dimension
---------------------------------

.. index::
    ValuenD

ValuenD
^^^^^^^

Constrain region to a single value within a specific dimension.

Representation:

==== ======== ======================
Name Type     Description
==== ======== ======================
S1   ShapeID  Shape
R1   RepID    Representation
D1   Index    Dimension
V1   Value    Value within dimension
==== ======== ======================

ValuesnD
^^^^^^^^

Constrain region to multiple values within a specific dimension.

Representation:

==== =========== =======================
Name Type        Description
==== =========== =======================
S1   ShapeID     Shape
R1   RepID       Representation
D1   Index       Dimension
NVAL Count       Number of values
VALS Value[NVAL] Values within dimension
==== =========== =======================

RangenD
^^^^^^^

Constrain region to a range of values within a specific dimension.

Representation1:

Specified as the half-open range [V1, V2).

==== ======== ================================
Name Type     Description
==== ======== ================================
S1   ShapeID  Shape
R1   RepID    Representation
D1   Index    Dimension
V1   Value    Starting value within dimension
V2   Value    Ending value +1 within dimension
==== ======== ================================

Representation2:

As an inequality (or equality).

Specified as all values for which the formula "n O1 V1" is true,
e.g. "n ≤ 5".

==== ======== ================================
Name Type     Description
==== ======== ================================
S1   ShapeID  Shape
R1   RepID    Representation
D1   Index    Dimension
O1   Operator Mathematical operator
V1   Value    Value for operation
==== ======== ================================

Regions in multiple dimensions
------------------------------

Regions in single dimensions may be combined to result in a region in
multiple dimensions.

ExtrudenD
^^^^^^^^^

Extrude a shape of arbitrary dimensionality into an additional
dimension.  There are no limits in the additional dimension; these
must be set by combining with a range instead.

==== ======== ================================
Name Type     Description
==== ======== ================================
S1   ShapeID  Shape
R1   RepID    Representation
D1   Index    Dimension
S2   ShapeID  Shape to extrude
==== ======== ================================

CombinenD
^^^^^^^^^

==== ======== ================================
Name Type     Description
==== ======== ================================
S1   ShapeID  Shape
R1   RepID    Representation
S2   ShapeID  First shape to combine
S3   ShapeID  Second shape to combine
==== ======== ================================

