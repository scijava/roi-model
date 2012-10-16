ROI Discussion
##############


ROIs in three dimensions
------------------------

Some of the 3D primitives described below may appear to be redundant;
it's certainly possible for example, to represent a shape in 3D right
now using multiple shapes, one per z plane.  However, being able to
use native 3D primitives is more powerful: it permits additional
measurements involving volume, surface area and shape.

Some shapes may be represented equivalently in different ways; it
might be worth considering adding support for these because it firstly
allows the shape to be computed in different ways, which can differ
depending upon the problem being solved, and it also contains
information about how the measurement was made, i.e. the intent of the
person doing the measuring, which is lost if converted to a canonical
form.


Bitmasks
--------

**Mask**       Could we have a pointer to an IFD/file reference plus
            two coordinates so specify a clip region, then we can
            pack potentially hundreds of masks in a single plane.


Meshes
------

**Mesh**       2D mesh described as e.g a face-vertex mesh.

**3DMesh**     3D mesh described as e.g. a face-vertex mesh.

Meshes could be computed from masks, polygons, extruded shapes where
there is a z range, or from thresholding.

Paths
------

**3DPath**     As for Path, but with additional vector to describe motion
            along the prescribed plane?
