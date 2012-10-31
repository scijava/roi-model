Requirements
============

Barcelona meeting
-----------------

The following points are taken from the meeting notes.

.. note::
   These may be incomplete, please do correct if necessary.

- Iterate through all points in a ROI.  Order is important for some use cases, but not all.

- Type mechanism needed.  Use concrete types.

- Version types to allow for deprecation, and translation to new versions.

- Define a persistent data model.

- ROIs must be serialisable.  Needed for exchange and persistence.

- Serialisation may be implementation dependent.  This could be XML,
  text or binary.  Which should be used as a transfer format (if any)?

- Allow conversion between different ROI types.

- Need the ability to specify an interval in an arbitrary dimension.

- Hierarchy of interfaces.
    - Interval, Renderable.

- Need to specify how to draw and display (and edit?) types such as
  curves so that it does not vary between implementations.

- Persistence and drawing are separate problems.

- Transforms
    - Abililty to attach transforms
    - Non-affine transforms.
        - Need examples to understand the problem better
    - Store transforms with ROI?
    - Apply multiple transforms to a ROI in sequence; nested list of transforms
    - Modelling spaces and objects in space; maybe define transforms
      separately and reuse them
    - Tree of transformations and operations

- Union ROIs
    - Only works in transform domain / "view space"
    - Union of hypervolumes.  [How to represent different shapes at different times?]

- Needs to be able to scale up to millions-billions of ROIs

- Specific ROI types
    - Include checkerboard (uneven integers)
    - Hierarchy of ROIs; compound list

- Rendering:
    - jHotDraw and other drawing toolkit independence
    - Need objects to be manipulable
    - List of control points

- Editing:
    - Needed to manipulate shapes

- Tree of operations
    - compiler/interpreter
    - obtain a "result"

- Grouping

- Comparison of models:
    - OME: ROI is union of shapes
    - ImgLib: Group is union of ROIs
