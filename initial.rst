ROI Discussion
##############


ROIs in three dimensions
------------------------

This is just a followup regarding discussion with J-M and Will earlier
today, where we covered the possibility of adding support of 3D
primitives to the model.  (Note that opinions over what to add remain
divided, and this certainly needs further discussion!)  These are just
my thoughts on how we might add initial support.

[Note that for the n-dimensional stuff, I just added it as something
to think about--I'm not suggesting we add any support at this point.]

+---------------+-----------------------+---------------------------+
|2D             |   3D                  |  nD                       |
+===============+=======================+===========================+
|Line [2DLine]  | 3DLine                | nDLine                    |
+---------------+-----------------------+---------------------------+
|Rectangle      | 3DCube [Cube]         | nDCube [Hypercube]        |
+---------------+-----------------------+---------------------------+
|Ellipse        | 3DEllipse [Ellipsoid] | nDEllipse [Hyperellipsoid]|
+---------------+-----------------------+---------------------------+
|Point [2DPoint]| 3DPoint               | nDPoint                   |
+---------------+-----------------------+---------------------------+
|Mask           | 3DMask                |                           |
+---------------+-----------------------+---------------------------+
|Path [2DPath]  | 3DPath                |                           |
+---------------+-----------------------+---------------------------+
|Mesh [2DMesh]  | 3DMesh                |                           |
+---------------+-----------------------+---------------------------+
|Text           |                       |                           |
+---------------+-----------------------+---------------------------+

Currently, the ROI model only supports 2D shapes.  In the above table,
additional primitives for 3D (and nD) have been added.  Due to the
"3D" or "nD" prefix, these do not replace the existing 2D-only
primitives for backward compatibility, and to make it clear that these
are for 3D work.  Note that the "nD" primitives would work in 2D, 3D
and higher dimensions; the existing primitives could all be
implemented in terms of nD primitives in the code, but it is useful to
have fixed-dimension primitives in the model.

Some of the 3D primitives described below may appear to be redundant;
it's certainly possible for example, to represent a shape in 3D right
now using multiple shapes, one per z plane.  However, being able to
use native 3D primitives is more powerful: it permits additional
measurements involving volume, surface area and shape.  At a higher
level, the same is implied for e.g. cell tracking in xyzt; being able
to draw a single polyline line (or vector), rather than storing a
single point or line at each timepoint results in us being able to
compute velocity and direction changes directly--rather than having to
compute this information from discrete shapes, the information is
directly available in a single shape.

I've also noted that some shapes may be represented equivalently in
different ways; it might be worth considering adding support for these
because it firstly allows the shape to be computed in different ways,
which can differ depending upon the problem being solved, and it also
contains information about how the measurement was made, i.e. the
intent of the person doing the measuring, which is lost if converted
to a canonical form.


Basic 3D primitives
-------------------

**3DLine**     List of (x,y,z) vertices.
            Alternative representation: a single vertex and list of
            vectors.

**nDLine**     List of e.g. (x,y,z,t) vertices (tracking movement including
            speed and direction changes). Alternative representation: a single vertex and list of
            vectors.

**3DCube**     X,Y,Z,Width,Height,Depth
            The current representation is effectively a vertex and a
            vector.
            Alternative representation: Both Rectangle and 3DCube could
            be represented by two vertices.

**nDCube**     Vertex + Vector
            Alternative representation: two vertices.

**3DEllipse**  X,Y,Z,RadiusX,RadiusY,RadiusZ
            This representation is effectively a vertex and a
            vector.
            Alternative representations:
            - two vertices,
            - vertex + vector
            - single vertex and the Mahalanobis distance [most useful when computing distributions with covariance; enables rotation with n-1 degrees of freedom]

**nDEllipse**  Same as for 3DEllipse alternative representations

**3DPoint**    X,Y,Z

**nDPoint**    X,Y,Z,...

Bitmasks
--------

**Mask**       Could we have a pointer to an IFD/file reference plus
            two coordinates so specify a clip region, then we can
            pack potentially hundreds of masks in a single plane.

**3DMask**     As for Mask, but in 3D.
            A 3DMesh could be computed from a 3DMask.


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

Transforms
----------

To support proper 3D operation, it would make sense to extend the
existing support for 3×3 2D affine transforms to 4×4 3D transforms.