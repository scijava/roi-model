Geometric shape primitives
==========================

Overview
--------

This section specifies how shapes are described in the model.  For
some shapes, there are several alternative ways of specifying them;
which are worth supporting needs further discussion.  One point to
consider is that the different ways preserve the intent behind the
original measurement and what is in the original metadata where this
makes sense, even if this does mean some redundancy; this won't impact
on the actual drawing/analysis code, which can deal with each shape in
a canonical form.  This records how the measurement was made by the
user, which may have implications in further analysis and/or
verification that the measurement was correct.

While some shapes have been included here for completeness, it's quite
possible that not all are needed, particularly in all dimensions.

If anyone wants to check the maths behind the geometry, that would be
much appreciated, because I'm firstly not an expert in this area, and
it's also quite possible I've made some typos.  The naming of the
shapes is probably also wanting some improvement.

Alternative shape representations
---------------------------------

Using the current ROI model is that there is only one way to describe
each shape.  e.g. a polyline can only be described as a series of
points; it might in some cases be more natural to specify one as a
starting point and a series of vectors; while either are fine just to
draw the ROI, it would desirable to store what was measured, since
converting it to a canonical representation is lossy, and removes the
original measurements taken, and hence the intent of the original
annotation.  This applies to other shapes as well.  For example, a
circle or ellipse can be described by a bounding box (which may itself
be a point and one or two vectors, or a set of points), or by a point
and radius or half-axes, or by the Mahalanobis distance (typically for
computing from a normal distribution of points).  For a cylinder/cone,
we can specify this in multiple ways also from a circle/ellipse plus
length, or point plus vector (length and direction) plus radius (or
half-axes).

The current model is focussed on drawing shapes, while making
measurements involves drawing only for visualisation; the important
parts are the values for making the measurement, and of course the
results.  Some programs (e.g. AxioVision) have separate sets of
objects for drawing (annotation) and measurement.  These are a largely
overlapping set, but the former are not used for any
length/area/volume/pixel measurements.  Objects such as scale bars and
labels are for drawing only.

.. todo::
    Common methods for all primitives:
    Bounding box [AlignedCuboid3D]
    Rotation centre [Vertex2D/Vertex3D]
    Control points [may use points and vertex to describe position and movement path]
    Conversion to 2D (slab through); equivalent to intersection with cuboid.  Should
    all primitives support a minimum of intersection with AlignedCuboid3D?  Or Mesh3D
    for non-square images.
    Can 2D methods use alternative axes to project in xz/yz?  Default
    to xy.  If all 2D shapes must be represented by 3D forms (i.e. are
    just proxies), then the equivalent 3D can be used quite simply.
    Get greymap/bitmap.
    Get 2D/3D mesh.
    Intersect (only for cuboid?)  Need to clip to image volume
    (optionally).  Also useful to reduce to 2D (which can be a cuboid
    for a single plane).
    Non-aligned shapes inherit/implement the aligned forms.
    Shrink and grow: move polygons along surface normals for meshes.
    For other shapes, this will require recalculation of the geometry.

    Add triangle as special case of polygon, which can be a special case of mesh?

    Meshes: Need to be able to triangulate if higher order polygons are possible.

    Add representation number to start of number list; this will allow
    shapes to be embedded in other shapes and be self-describing.
    e.g. all circle types may be used to specify a circular cylinder
    end.  This will simplify the specification of more complex shapes
    by limiting the number of variants.

Shape serialisation
-------------------

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

.. note::
    ** Sébastien ** Versioning is of concern to people doing analysis.

Key considerations:

- A shape exists in a set of dimensions e.g. xy, xyz, xyt.  The shape
  must define the number of dimensions it exists in, and their identity.
- A shape must be identifiable unambiguously
- A shape must be versioned (to permit correction of any
  design/analysis bugs without altering any data retrospectively);
  this permits the replacement of the buggy implementation while not
  removing it.
- In order to allow code reuse and flexible use of shapes, shapes may
  include other shapes as part of their primitive specification.

In the following shape descriptions, all shapes are identified by a
Shape ID and Representation ID.  The shape specifies the geometric
shape type.  The representation specifies both the primitives required
for serialisation, and can also be used for versioning the
shape--i.e. it also specifies the behaviour for conversion to greymaps
and bitmaps.  The behaviour could change in a backward-compatible
manner by introducing new Shapes and/or Representations to supersede
existing forms, while retaining the unchanged old forms.


.. index::
    Shape

Shape
-----

An abstract description of a shape.

Representation:

==== ======== =================
Name Type     Description
==== ======== =================
S1   ShapeID  Shape
R1   RepID    Representation
==== ======== =================

Concrete implementations of shapes provide further elements in their
representation.  The above are only sufficient to describe the shape
and its representation.  The combination of shape and representation
specifies the data required to construct the shape.

Note that one disadvantage of this method is that a reader will be
required to understand how to deserialise all shape types; it's not
possible to skip unknown shapes due to not knowing their lengths
(which may be variable).  However, this would be an issue for a purely
XML-based implementation as well, so may not be a problem in practice.



Alignment
Aligned shape variants are aligned at right-angles to the x and y (2D) or x, y and z (3D) axes.


Text placement and alignment
----------------------------

In order to annotate text next to measurements, it would be ideal if
it were possible to control text placement and orientation.  Currently
the coordinate of the first letter is required.  However, it would be
nicer if the text could be also placed to the right of the point or
centred on the point.  And additionally, to the top, middle or bottom
for vertical placement.  Rotation would also be useful, though it's
probably achievable indirectly via the transformation matrix, i.e. you
would effectively have these anchors for placement, where 1 is the
current behaviour.

::

   7      8      9
   4Text h5ere...6
   1      2      3

This is needed to e.g. align text along measurement lines.  Having a
rotation angle specified directly would also save the need for complex
calculations to work out the rotation origin and transform every time
you want to just place a label along a line.  It also makes it
possible to place text in the centre of a shape.


Scale bars
----------

.. note::
    A 3D scale may need to be a 3D grid to allow visualisation of
    perspective, in which case the representation will define the grid
    bounding cuboid; inherit AlignedCuboid3D representations.  Permit
    scale rotation with Cuboid3D?  Allow specification of grid size
    and only allow sizing in discrete units?

Additional primitives
---------------------

3D spline surfaces
  Natural cubic spline (Catmull-Rom)

The axiovision curve type is most likely a natural cubic spline, the
curve passing smoothly through all points, but without local control.
It is simply represented as a list of points through which the curve
must pass; there are no additional control points.  Depending upon if
they are doing any custom stuff, it might not be possible to represent
with pixel-perfect accuracy.

Curves might be more generally applicable to other formats, and useful
in their own right.  It might be worth considering adding a spline
type with local control where the curve passes straight through the
control points such as Catmull-Rom splines.  This would make it very
simple for non-experts to fit smooth lines while annotating their
images.
