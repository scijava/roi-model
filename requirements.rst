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
    - Non-affine transforms.
        - Need examples to understand the problem better.
    - Store transforms with ROI?


- Specific ROI types
    - Include checkerboard (uneven integers)
