




2D primatives in 3D
===================


Conversion to 3D primitives
^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

While it would be possible to translate and rotate 2D primitives in 3D
using a 4×4 matrix, it would be simpler for users if rotation could be
specified using a unit vector which can specify the angle of the
primitive in 3D space; the matrix transform can be trivially construct
edfrom the vector.  However, note that while current transforms occur
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


Alternative shape representations
=================================

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



Storage of vertex data
======================

For quite a number of the shape primitives, it's possible to support
3D very simply--we just increase the number of dimensions in each
vertex, and that's it (obviously just for storage; it will still
require some work for rendering).  From the point of view of storing
the list of vertices, it would be nice if we could specify the
dimensions being used e.g. XZT, and then allow missing dimensions to
be specified as constants as we now do for theZ.  This will also mean
that will will be possible to use a 2D primitive with theZ set as
equivalent to a 3D primitive with the z value specified separately to
the (x,y) points.  This would provide one means of keeping the
representation compact.  Additionally, it is undesirable to have a
separate element for each vertex, since for complex shapes
e.g. meshes, this would waste multi-megabytes of XML markup for no
good reason.


2D extrusion
^^^^^^^^^^^^
Reconstruction of 3D shapes from 2D planes distributed in z/t.
-> set of 3D objects in t.

2D decomposition
^^^^^^^^^^^^^^^^

Decompose 3D shape into 3D planes distributed in z.


ROI-ROI links
=============

ROI relationships: When segmenting cell contents, shown as cytoplasm,
actin filaments, nucleus and nucleolus, these fall into a strict
heirarchy (a nucleus can only be in one cell, though one cell could
have more than one nucleus).  If we added a ROI type that was a
container of ROIs (note: not a union), and added a means of
classifying ROIs with tags/labels, this would be very useful for HCS
and other types of analysis.  Additionally, some relationships are not
hierarchial, e.g. tree-like branching and merging in a vessel bed, but
could be represented if a ROI could point to one or more other ROIs,
which would permit a directed graph of relationships between ROIs.


Tracking
Containment
User modification (branch/merge)
Inherit properties
Layer
DAG


Additional primitives
=====================

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


Text placement and alignment
============================

In order to annotate text next to measurements, it would be ideal if
it were possible to control text placement and orientation.  Currently
the coordinate of the first letter is required.  However, it would be
nicer if the text could be also placed to the right of the point or
centred on the point.  And additionally, to the top, middle or bottom
for vertical placement.  Rotation would also be useful, though it's
probably achievable indirectly via the transformation matrix, i.e. you
would effectively have these anchors for placement, where 1 is the
current behaviour.

   7      8      9
   4Text h5ere...6
   1      2      3

This is needed to e.g. align text along measurement lines.  Having a
rotation angle specified directly would also save the need for complex
calculations to work out the rotation origin and transform every time
you want to just place a label along a line.  It also makes it
possible to place text in the centre of a shape.



Compound types
==============

Line Profile
LUT
Scale bar

LUT/gradient boxes are quite specialist.  However, they are also quite
common in published figures, so it would make sense to have a general
implementation.  These are particularly useful when you have false
colour heat maps where you need a visual scale to interpret the
figure.  We already support LUTs, so this is really just a view of the
LUT for a given channel inside a rectangle.

Line profiles are quite common.  But I guess supporting this would
depend upon whether you classify the profile as the result of analysis
of a ROI, or part of a ROI.  It might be handy to be able to overlay a
line profile as a set of coloured polylines, for example.


Zeiss AxioVision ROI types
==========================

For the Zeiss types, we can represent these in the model using:

================= =========================
Zeiss type        ROI model type
================= =========================
Event             Point2D
Events            Point2D (union of points)
Line              Line2D
Caliper           Line2D (union of lines)
Multiple caliper  Line2D (union of lines)
Distance          Line2D (union of lines)
Multiple distance Line2D (union of lines)
Angle3            Line2D and Arc2D
Angle4            Line2D and Arc2D
Circle            Circle2D and Line2D
Scale Bar         Line2D (with end markers)
Polyline [open]   Polyline2D
Aligned Rectangle AlignedRectangle2D
Rotated Rectangle Rectangle2D
Ellipse           AlignedEllipse2D
Polyline [closed] Polygon2D
Text              Label2D
Length            Line2D (union of lines)
Spline [open]     PolylineSpline2D
Spline [closed]   PolygonSpline2D
LUT               AlignedRectangle2D and Label2D
Line profile      Line2D and Polyline2D/Rectangle2D
================= =========================

Annotations don't typically have labels (with the exception of scale
bars).  Measurements would have one or more labels in the union as
well displaying the value(s) of the measurement.
