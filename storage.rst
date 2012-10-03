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
e.g. meshes, this would waste a lot of space: when scaling up to
thousands of vertices, this would waste multi-megabytes of XML markup
for no good reason.

XML schema
----------

Shape type and representation are stored as unsigned 16 bit integers,
counts as unsigned 32 bit integers, and vertices and vectors as
double-precision floating point.

.. literalinclude:: shape.xsd
    :language: xml

Properties
----------

Store at the level of the ROI, not the shape.  Since all the shapes
within a ROI describe a single entity, there is no need for separate
properties (colour, line thickness/style/endings etc.) on each shape.
