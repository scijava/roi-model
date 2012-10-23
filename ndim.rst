Regions in arbitrary dimensions
===============================

While it is possible to use geometric shapes to specify regions in
physical dimensions, this does not translate meaningfully to arbitrary
dimensions.  The following primitives work in any "dimension" with a
discrete or continuous range by permitting the selection of specific
values, or sub-ranges.

These "nD" shapes (Value, Values, Range) and the extrusion and
combining shapes (Extrude, Combine), permit the specification of ROIs
in multiple arbitrary dimensions, and their combination with geometry
in 1D, 2D and 3D.

Just as all 1D, 2D and 3D geometry can be converted to the respective
1D, 2D or 3D bitmask or greymask representing the described shape, all
nD primitives in higher dimensions can be converted to 1D bitmask or
greymask.  A 1D bitmask for each dimension will allow efficient
iteration over the higher-order dimensions using the resulting
bitmaps.

By default, a ROI is unconstrained within all dimensions.  The
addition of constraints restricts it to particular dimensions, or
subsets thereof.

.. note::
    RL.  Should we be unconstrained by default, or completely
    constrained?  Should this behaviour be different for "real"
    dimensions (xyzt) compared with virtual dimensions such as
    channels?
