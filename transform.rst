Transforms
==========

The model defines shapes for performing affine transforms and abstract
transforms (:ref:`type_scijava_roi_types_AffineTransform3D` and
:ref:`type_scijava_roi_types_AbstractTransform3D`).  The purpose of
the abstract transform is to serve as a hook mechanism for
implementation-specific transformations to be supported within the
model.

All transforms are shapes.  The implication is that all
transformations on shapes evalulate to the transformed shape, i.e. the
transform shape *is* the transformed shape.

Transforms between pixel space and physical space (using the unit
system defined in the image metadata).  Provide both transforms.

If shapes can be defined in either space, should any of these
transforms be implicit?  If so, when are they applied?

Additional transforms required for display?  physical to pixels is
equivalent to the modelview transformation matrix.  Should we
additionally take into account projection/perspective/viewport
matrices?  Or leave further transformation to the implementor,
e.g. starting from shapes reduced to meshes, for OpenGL
implementations.

Conversion of shapes to masks needs to happen in pixel space?

In the current model, transforms are specified inline in the shape
definition.  However, it may make sense to have some transforms out of
band in the ROI or shape state, such as pixel to physical (and
inverse) transforms.  This would require a transform representation
with a transform ID as one of its data members.
