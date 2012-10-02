Compound ROIs
=============

A ROI may consist of multiple shapes.

- Restrict to either 2D or 3D, but not both?

- Shapes may combined using set operators:
  - ∪ union
  - ∩ intersection
  - \ difference
  - symmetric difference

How do we detect if shapes intersect?
Edge cases for set operations using masks-false positives for
partially occupied pixels.


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




Storing and manipulating complex compound objects
=================================================

With these measurements, one thing perhaps worth considering is that
there are up to four types of object here:

1. Result context.  The object(s) representing the physical
   measurement.  This is what we currently store in the model.
2. Measurement context: line along radius of circle, points along
   circumference of circle etc.  This is "how the measurement was
   made"
3. Visual context: such as visual cues such as construction lines.
   This is the visual presentation of the measurement to the viewer.
4. Editing context: values which control the placement of the
   above. Information for generation of UI manipulation handles, and
   of the other contexts while editing.

We can represent the actual measurements in most cases using the
existing ROI types.  However, if we store the additional types, it's
no longer possible to distinguish between the measurement and the
additional context.

If it was possible to distinguish between these in the model, it would
be possible for the objects to be displayed without any advanced
knowledge of how an object should be edited.  It would also be
possible to extract the primitive measurement values.  However, the
measurement context would provide additional information to editors
for manupulation of the object, which would then be able to update all
three contexts appropriately.

Doing this would provide a simple but effective means for additional
ROI types to be added without requiring support in all programs
displaying/modifying ROIs.  This does not of course replace the need
for namespaces to identify ROI categories, but it does supplement it
by allowing programs to selectively display different contexts without
any knowledge of the underlying type.

As an example, using this length measurement:

   |******OBJECT*******|
   |                   |
   |<----------------->|
           50 µm


1) Result context

   #******OBJECT*******#

   (where the #s are the start and end points of a Line at either end
   of the object.  This is the value of the physical measurement.)

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

   (where the #s represent a distance between the measured line and
   the drawn line in the visual context.  This information is used to
   generate the visual context from the measurement context.)


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
