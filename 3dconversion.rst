2D primitives in 3D
===================


Conversion to 3D primitives
---------------------------

The existing 2D primitives may be represented by the equivalent 3D
primitive for the 2D primitive, extruded in z to a single z plane
thickness.

While this is desirable for reducing code complexity, retaining the 2D
primitives is necessary for 2D measurements (area/perimeter).  These
can be obtained from the 3D shape by dividing the volume or surface
area by the z thickness, respectively.  Having the 2D primitives will
provide the context for conversion of measurements from 3D volume to
2D surface, since these are otherwise meaningless for 3D ROIs which
are not extruded 2D ROIs.

3D ROIs, where appropriate, could provide alternative forms for 2D
use.  For example, a 3D cylinder would, when extruded from a 2D
circle, not have end faces (i.e. would be open), in order for 2D
surface area measurements to be correct.

Use of 2D primitives in 3D space
--------------------------------

While it would be possible to translate and rotate 2D primitives in 3D
using a 4×4 matrix, it would be simpler for users if rotation could be
specified using a unit vector which can specify the angle of the
primitive in 3D space; the matrix transform can be trivially construct
ed from the vector.  However, note that while current transforms occur
only in 2D, where the x and y pixel sizes are typically the same, this
is not usually the case in z, and so the transformations may need
performing in physical units; therefore adding proper support for
units would also be desirable to fully support 3D transforms.  Note
that this would also solve the existing problem in 2D that prevents
ellipses and rectangles being rotated (without the use of a matrix
transform), though where the rotation centre should be may be shape-
and context-dependent.  The unit vector to (0,0,-1) which would
specify the existing behaviour.

.. note::
   Define behaviour of orientation of unit vector for rotation; which
   direction are primitives facing by default?

2D extrusion
^^^^^^^^^^^^

Reconstruction of 3D shapes from 2D planes distributed in z/t.
-> set of 3D objects in t.

2D decomposition
^^^^^^^^^^^^^^^^

Decompose 3D shape into 3D planes distributed in z.
