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
