Masks
=====

Specification
-------------

Bitmasks may be specified directly, e.g. by segmenting an image.
Bitmasks may also be derived from any shape, since every shape is
reducible to a bitmask.

Greymasks (masks with multiple greylevels) may also be specified
directly.  They may also be derived from any shape.  Shapes may
provide direct conversion to a greymask, or alternatively via a
high-resolution bitmask, which is then converted into a greymask.
This process is illustrated in the following figure.

Masks have aligned and unaligned variants.  The difference is not in
the mask data, but in the alignment of the bounding box with the axes.
Neither guarantee a 1:1 mapping with the pixel grid; this would
require a manual conversion step.  This might also be be better
supported with a pixel-aligned bounding box type.  Resizing to the
pixel grid might be best performed via thresholding an intermediate
greymask.

Any shape transformations must be performed prior to conversion to an
aligned mask, otherwise the mask alignment may be lost.

.. note::
    **Roger**
        We need to specify the criteria for pixel inclusion when
        converting from a shape to bitmask.  Some shapes may be able
        to efficiently convert to a greymask, but a threshold value is
        still needed.

        We also need to allow the user to specify the threshold value
        when converting from a greymask to bitmask.

        Also need to have rules for conversion of points and lines,
        which do not have any intrinsic area, to pixels.  Does a point
        always occupy a single pixel?  How about lines, which pass
        through multiple pixels?  The latter could convert to a
        greymask.  Both could have default widths and allow the user
        to override them.  Convert via a shape e.g. implicitly convert
        line to cuboid and point to sphere?

	The current mask representations store the mask data directly
	in the shape.  We might wish to support alternative forms of
	storage, e.g. IFD (as a sprite sheet), labellings, etc.

A circle, drawn a 6×6 pixel grid may be converted directly as a 6×6
pixel bitmap.  Alternatively, the grid may be subdivided further so
that each pixel is itself an 8×8 pixel grid, to give a grid size of
48×48 pixels.  Each real pixel therefore contains 256 bits of
information, from which it is trivial to derive a 6×6 pixel 6-bit
greymask with 256 grey levels.  The resolution may be further
increased so that each pixel is a 16×16 pixel grid from which an 8-bit
greymask with 256 greylevels may be derived.

.. only:: html

    .. image:: images/greymap.svg
        :width: 60%
	:alt: Bitmasks and greymasks

.. only:: latex

    .. image:: images/greymap.pdf
        :width: 80%

The following grid sizes could be used:

.. tabularcolumns:: |c|r|r|r|

========= ========= ============== ==========
Grid size Grid bits Greylevel bits Greylevels
========= ========= ============== ==========
2×2               4              2          4
4×4              16              4         16
8×8              64              6         64
16×16           256              8        256
32×32          1024             10       1024
64×64          4096             12       4096
128×128       16384             14      16384
256x256       65536             16      65536
========= ========= ============== ==========

.. note::
    **Roger**
        We don't need to support all these sizes, but supporting 8 bit
        masks at a minimum would be useful.  Larger sizes would have
        greater precision, but quite a large overhead: a 16 bit
        greymask requires 8KiB/pixel!

Point and line conversion
-------------------------

Would it make sense to have the ability to convert point and line
shapes to cylinder/sphere or cuboid shapes, respectively?  Useful for
rendering, and potentially also useful for analysis.  Default point
size and line width for converting to a mask?  Points may be expected
to only be one pixel in size; what about lines?

Set operations
--------------

Set operations only make sense to perform at the level of bitmasks.
Set operations on basic shape geometry rapidly becomes an intractable
problem, since this for example requires that it be possible to
describe the union of every shape type with every other shape type,
including all combinations of unions.  This would be possible if all
geometry was reduced to meshes, but this would also result in a loss
of precision.

Set operations are trivial to perform using masks.  However, as shown
in the above figure, there may be loss of precision when converting to
a mask.  However, it would be possible to do the set operations on a
higher-resolution mask prior to conversion to a greymask or
lower-resolution bitmask.  This includes intersection, set difference,
etc.

.. only:: html

    .. image:: images/greymap2.svg
        :width: 60%
	:alt: Bitmasks and greymasks

.. only:: latex

    .. image:: images/greymap2.pdf
        :width: 80%


.. note::
    **Roger**
          Consider a union of two shapes which do not touch, but which
          overlap a common pixel.  It is possible to compute the union
          using the higher-resolution bitmask because this takes into
          account the extent to which the shapes overlap (or not), and
          this can be reflected in the resulting greymap.  The user
          can choose the precision of the operation via the grid size
