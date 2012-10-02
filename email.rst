
WRT the types I outlined in the earlier emails, some may be created in
a variety of different ways, and it would make sense to store how the
shape was defined, because it records how the measurement was made by
the user, which may have implications in further analysis and/or
verification that the measurement was correct.

Event/Events: A simple list of points.
  The point size/style/colour may be changed to permit different sets to be distinguished.

Caliper/Distance/Multi-Caliper/Multi-Distance.  These are all the same
  measurement(s), a baseline followed by a list of points.  The
  measurement is the distance from each point to the baseline.  The
  differences between the types are solely the visual presentation of
  the measurements.

Angle3/Angle4.  These measure the angle between two lines.  Angle4 is
  two separate lines, while Angle3 is two lines with a common point
  (i.e. a special case of Angle4).  Angle3 could be represented with a
  three-point polyline.  Angle4 would need to be two separate lines.
  Given that Angle3 is a special case of Angle4, it's not clear that
  it should be represented as a polyline.

Circle.  While the OME model represents this as an ellipse with equal x and y radii, there are three ways to represent a circle here:
- radius defined as a line from centre to edge
- radius defined as a line from edge to centre (stored as the first type with the point order reversed)
- circumference defined using three points.  The first two are
representable in the model as an ellipse plus a line.  The latter is
representable as an ellipse plus three points.

Polyline is directly translatable.

Aligned Rectangle is directly translatable as a rectangle (with some
trivial differences in coordinates).  However, additional tags define
metadata to display inside the rectangle (optional) such as
channel/slide/acquisition time/exposure time/etc.  The verbatim text
can be put into a Label, but the specific meaning would be lost--this
is an overlay which would change as you navigate through a stack or
timecourse etc, varying with the plane-specific parameters.  While the
specific tags would be retained, a more generic means to overlay
image- and plane-specific OME metadata might be generally useful
within the context of the OME model.

Ellipse is directly translatable.

Outline/closed polyline is directly translatable.

Text is convertible to Label.  However, the OME Label type lacks the alignment attributes mentioned in my earlier mail.  This makes it difficult to control the placement of text in complex compound ROIs.

Length is a single line distance measurement line like, but with additional end lines to make it like a technical drawing line outside the object itself, i.e.

|******OBJECT*******|
|                   |
|<----------------->|
        50 µm

Representable in the model as a simple line, across OBJECT, but with loss of the other lines.  It's representable as three separate lines, but with loss of the context of the specific measurement.

Open and closed splines: these are probably natural splines (not Bezier).  ZVI currently stores them as polylines given that we don't support splines.  But having a spline type would permit them to be stored.

LUT and Profile: Covered in previous mail.


27/04/10

I've been thinking about how we might store and interact with more complex compound ROI types.  This is just some thoughts on that; comments (and/or abuse) welcome!


Storing and manipulating complex compound objects
=================================================

With these measurements, one thing perhaps worth considering is that there are up to four types of object here:
1) Result context.  The object(s) representing the physical measurement.  This is what we currently store in the model.
2) Measurement context: line along radius of circle, points along circumference of circle etc.  This is "how the measurement was made"
3) Visual context: such as visual cues such as construction lines.  This is the visual presentation of the measurement to the viewer.
4) Editing context: values which control the placement of the above. Information for generation of UI manipulation handles, and of the other contexts while editing.

We can represent the actual measurements in most cases using the existing ROI types.  However, if we store the additional types, it's no longer possible to distinguish between the measurement and the additional context.

If it was possible to distinguish between these in the model, it would be possible for the objects to be displayed without any advanced knowledge of how an object should be edited.  It would also be possible to extract the primitive measurement values.  However, the measurement context would provide additional information to editors for manupulation of the object, which would then be able to update all three contexts appropriately.

Doing this would provide a simple but effective means for additional ROI types to be added without requiring support in all programs displaying/modifying ROIs.  This does not of course replace the need for namespaces to identify ROI categories, but it does supplement it by allowing programs to selectively display different contexts without any knowledge of the underlying type.

As an example, using this length measurement:

   |******OBJECT*******|
   |                   |
   |<----------------->|
           50 µm


1) Result context

   #******OBJECT*******#

   (where the #s are the start and end points of a Line at either end of the object.  This is the value of the physical measurement.)

2) Measurement context

   No additional information needed in this case.

3) Visual context

   |                   |
   |                   |
   |<----------------->|
           50 µm

   Three lines, one with arrow end markers, plus text label.
   This is the visual representation of the measurement.

4) Editing context

   #******OBJECT*******
   #
   #

   (where the #s represent a distance between the measured line and the drawn line in the visual context.  This information is used to generate the visual context from the measurement context.)


I hope the above doesn't sound too way out.  But the current system is
limited to storing only the first of these four contexts, which loses
information.  While it's possible to delegate all of the presentation
and editing to the viewer, the reality is that this is stuff people
want.  If I'm annotating an image for a paper, I want the annotations
to appear exactly the same as I see them if I send them to someone
else. And if I'm doing physical measurements, I want the specifics of
how I made the measurement to be recorded.  All we are doing here is
providing additional information to the viewer/editor that it is free
to use and/or ignore as it chooses.

27/04/12

I've attached a copy of some simple figures to illustrate what I was
trying to articulate below.  This takes some relatively simple
measurements, and breaks them down into the four different contexts.

Thinking about this a little more, in many cases it will be possible
to omit some contexts and infer them from the others. For example, if
I have a simple line I will store a line in the result context.  The
measurement context is the same two points, and so we may simply use
the result context points in its place.  Likewise, if the measurement
is a simple one, the visual context may be omitted and inferred from
the result context also.  The different contexts really only come into
play when we want a more sophisticated visual representation (for
example with overlaid textual representations of the measurement value
or to visualise the measurement in a more complex manner than the
result context alone can provide).  And they are essential when using
more complex compound ROIs as the last example attached shows.

In the last example, all the information is provided to allow the user
to edit the object in a UI.  For example, they can adjust the end
points of the baseline, and the start points of the lines in the
measurement context can be retriangulated from the end points and
baseline.  The measurement context can be inferred from the endpoints
of the lines in the result context.  And the endpoints can also be
adjusted independently.  Following any adjustment, the updated
baseline can be stored in the editing context, the measurement lines
in the measurement context, and the visual representation in the
visual context.  The visual context is shown here to include end
markers on the distance lines, and text labels with the measured
values.  But these could be toggled on or off and the settings stored
in an annotation specific for this measurement type--there's really no
limit to the "extra stuff" you can add here, but the basic measurement
remains the same in the result context.

(In this example, the baseline could actually be in the measurement
context, since it's part of the measurement; the first example is a
better illustration of the editing context.)

The important point is that anyone should be able to open the file and
display the visual representation without any knowledge of the
specifics of the ROI type or measurements being made.  Likewise they
can also look at the measured distances in the results context and use
them without any knowledge of how they were measured.  Only a UI which
supports the ROI type in question will need to use the editing and/or
measurements context, and they will know how to regenerate the other
contexts when editing.

27/04/12

I've attached a copy of some simple figures to illustrate what I was
trying to articulate below.  This takes some relatively simple
measurements, and breaks them down into the four different contexts.

Thinking about this a little more, in many cases it will be possible
to omit some contexts and infer them from the others. For example, if I
have a simple line I will store a line in the result context.  The
measurement context is the same two points, and so we may simply use the
result context points in its place.  Likewise, if the measurement is a
simple one, the visual context may be omitted and inferred from the
result context also.  The different contexts really only come into play
when we want a more sophisticated visual representation (for example
with overlaid textual representations of the measurement value or to
visualise the measurement in a more complex manner than the result
context alone can provide).  And they are essential when using more
complex compound ROIs as the last example attached shows.

In the last example, all the information is provided to allow the user
to edit the object in a UI.  For example, they can adjust the end points
of the baseline, and the start points of the lines in the measurement
context can be retriangulated from the end points and baseline.  The
measurement context can be inferred from the endpoints of the lines in
the result context.  And the endpoints can also be adjusted
independently.  Following any adjustment, the updated baseline can be
stored in the editing context, the measurement lines in the measurement
context, and the visual representation in the visual context.  The
visual context is shown here to include end markers on the distance
lines, and text labels with the measured values.  But these could be
toggled on or off and the settings stored in an annotation specific for
this measurement type--there's really no limit to the "extra stuff" you
can add here, but the basic measurement remains the same in the result
context.

(In this example, the baseline could actually be in the measurement
context, since it's part of the measurement; the first example is a
better illustration of the editing context.)

The important point is that anyone should be able to open the file and
display the visual representation without any knowledge of the specifics
of the ROI type or measurements being made.  Likewise they can also look
at the measured distances in the results context and use them without
any knowledge of how they were measured.  Only a UI which supports the
ROI type in question will need to use the editing and/or measurements
context, and they will know how to regenerate the other contexts when
editing.




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
