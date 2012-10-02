Geometric shape primitives
==========================

Overview
--------

This section specifies how shapes are described in the model.  For
some shapes, there are several alternative ways of specifying them;
which are worth supporting needs further dicussion.  One point to
consider is that the different ways preserve the intent behind the
original measurement and what is in the original metadata where this
makes sense, even if this does mean some redundancy; this won't impact
on the actual drawing/analysis code, which can deal with each shape in
a canonical form.  Additionally, while some shapes have been included
here for completeness, it's quite possible that not all are needed,
particularly in all dimensions.

If anyone wants to check the maths behind the geometry, that would be
much appreciated, because I'm firstly not an expert in this area, and
it's also quite possible I've made some typos.  The naming of the
shapes is probably also wanting some improvement.

Basic primitives
----------------

Basic primitives describing vertices and vectors:

========= ============== ============
Primitive Representation Description
========= ============== ============
Vertex1D  double[1]      Vertex in 1D
Vertex2D  double[2]      Vertex in 2D
Vertex3D  double[3]      Vertex in 3D
Vector1D  double[1]      Vector in 1D
Vector2D  double[2]      Vector in 2D
Vector3D  double[3]      Vector in 3D
========= ============== ============

All shape primitives are described in terms of the above basic
primitives.  This means that all shape descriptions are serialisable
as a list of double precision floating point values.  It also means
that for compatible shape types, the shape type may be changed while
retaining the point list (e.g. polyline, polygon spline).

All 2D shape primitives could be oriented in 3D or using a unit
Vector3D, which would allow all 2D shapes to be used as surfaces in
3D.  They would additionally require a depth in order to be meaningful
(or assume a depth of one z slice).

.. todo::
    Common methods for all primitives:
    Bounding box [AlignedCuboid3D]
    Rotation centre [Vertex2D/Vertex3D]
    Control points [may use points and vertex to describe position and movement path]
    Conversion to 2D (slab through); equivalent to intersection with cuboid.  Should
    all primitives support a minimum of intersection with AlignedCuboid3D?  Or Mesh3D
    for non-square images.
    Can 2D methods use alternative axes to project in xz/yz?  Default
    to xy.  If all 2D shapes must be represented by 3D forms (i.e. are
    just proxies), then the equivalent 3D can be used quite simply.
    Get greymap/bitmap.
    Intersect (only for cuboid?)  Need to clip to image volume
    (optionally).  Also useful to reduce to 2D (which can be a cuboid
    for a single plane).
    Non-aligned shapes inherit/implement the aligned forms.
    Shrink and grow: move polygons along surface normals for meshes.
    For other shapes, this will require recalculation of the geometry.

    Add triangle as special case of polygon, which can be a special case of mesh?

    Meshes: Need to be able to triangulate if higher order polygons are possible.

.. index::
    Points

Points
------

A point is a single point in space.

.. index::
    Point2D

Point2D
^^^^^^^

Representation:

==== ======== =================
Name Type     Description
==== ======== =================
P1   Vertex2D Point coordinates
==== ======== =================

.. index::
    Point3D

Point3D
^^^^^^^

Representation:

==== ======== =================
Name Type     Description
==== ======== =================
P1   Vertex3D Point coordinates
==== ======== =================

.. index::
    Lines

Lines
-----

A line is a single straight edge drawn between two points.

.. index::
    Line2D

Line2D
^^^^^^

Representation:

==== ======== ===========
Name Type     Description
==== ======== ===========
P1   Vertex2D Line start
P2   Vertex2D Line end
==== ======== ===========

.. index::
    Line3D

Line3D
^^^^^^

Representation:

==== ======== ===========
Name Type     Description
==== ======== ===========
P1   Vertex3D Line start
P2   Vertex3D Line end
==== ======== ===========

.. index::
    Distances

Distances
---------

A distance is a vector describing the distance travelled from a starting point.

.. index::
    Distance2D

Distance2D
^^^^^^^^^^

Representation:

==== ======== =========================
Name Type     Description
==== ======== =========================
P1   Vertex2D Line start
V1   Vector2D Line end (relative to P1)
==== ======== =========================

.. index::
    Distance3D

Distance3D
^^^^^^^^^^

Representation:

==== ======== =========================
Name Type     Description
==== ======== =========================
P1   Vertex3D Line start
V1   Vector3D Line end (relative to P1)
==== ======== =========================

.. index::
    Polylines

Polylines
---------

.. index::
    Polyline2D

Polyline2D
^^^^^^^^^^

==== ======== ==============
Name Type     Description
==== ======== ==============
P1   Vertex2D Line start
P2   Vertex2D Second point
…    Vertex2D Further points
Pn   Vertex2D Line end
==== ======== ==============

.. index::
    Polyline3D

Polyline3D
^^^^^^^^^^

==== ======== ==============
Name Type     Description
==== ======== ==============
P1   Vertex3D Line start
P2   Vertex3D Second point
…    Vertex3D Further points
Pn   Vertex3D Line end
==== ======== ==============

.. index::
    Polygons

Polygons
--------

.. index::
    Polygon2D

Polygon2D
^^^^^^^^^

==== ======== ================
Name Type     Description
==== ======== ================
P1   Vertex2D First vertex
P2   Vertex2D Second vertex
…    Vertex2D Further vertices
Pn   Vertex2D Last vertex
==== ======== ================

.. index::
    Polygon3D

Polygon3D
^^^^^^^^^

==== ======== ================
Name Type     Description
==== ======== ================
P1   Vertex3D First vertex
P2   Vertex3D Second vertex
…    Vertex3D Further vertices
Pn   Vertex3D Last vertex
==== ======== ================

.. index::
    Polydistances

Polydistances
-------------

A polydistance is a series of vectors describing the series of
distances travelled from a starting point.

.. index::
    Polydistance2D

Polydistance2D
^^^^^^^^^^^^^^

==== ======== =========================================
Name Type     Description
==== ======== =========================================
P1   Vertex2D First point
V1   Vector2D Distance to second point (relative to P1)
V2   Vector2D Distance to second point (relative to V1)
…    Vector2D Further distances
Vn   Vector2D Last distance (relative to V(n-1))
==== ======== =========================================

.. index::
    Polydistance3D

Polydistance3D
^^^^^^^^^^^^^^

==== ======== =========================================
Name Type     Description
==== ======== =========================================
P1   Vertex2D First point
V1   Vector2D Distance to second point (relative to P1)
V2   Vector2D Distance to second point (relative to V1)
…    Vector2D Further distances
Vn   Vector2D Last distance (relative to V(n-1))
==== ======== =========================================

.. index::
    Squares

Squares and rectangles
----------------------

A square exists in its basic 2D form, and in the form of a cube in 3D.
Non-square variants are the rectangle and cuboid.  All have simplified
aligned forms with the shape aligned to the axes.

.. index::
    AlignedSquare2D

AlignedSquare2D
^^^^^^^^^^^^^^^

Aligned at right angles to xy axes.

Representation 1: Vertex and point on x axis (y inferred).

==== ======== ========================================
Name Type     Description
==== ======== ========================================
P1   Vertex2D First corner
P2   Vertex1D x coordinate of adjacent/opposing corner
==== ======== ========================================

Representation 2: Vertex and vector on x axis (y inferred).

==== ======== ======================================================
Name Type     Description
==== ======== ======================================================
P1   Vertex2D First corner
P2   Vector1D distance to adjacent corner on x axis (relative to P1)
==== ======== ======================================================

.. index::
    Square2D

Square2D
^^^^^^^^

May be rotated; not aligned at right angles to xy axes.

Representation 1: Vertices of two opposing corners.

==== ======== ===============
Name Type     Description
==== ======== ===============
P1   Vertex2D First corner
P2   Vertex2D Opposing corner
==== ======== ===============

Representation 2: Vertex and vector to opposing corner.

==== ======== ================================
Name Type     Description
==== ======== ================================
P1   Vertex2D First corner
V1   Vector2D Opposing corner (relative to P1)
==== ======== ================================

.. index::
    AlignedCube3D

AlignedCube3D
^^^^^^^^^^^^^

Aligned at right angles to xyz axes.

Representation 1: Vertex and point on x axis (y and z inferred).

==== ======== ========================================
Name Type     Description
==== ======== ========================================
P1   Vertex3D First corner
P2   Vertex1D x coordinate of adjacent/opposing corner
==== ======== ========================================

Representation 2: Vertex and vector on x axis (y and z inferred).

==== ======== ======================================================
Name Type     Description
==== ======== ======================================================
P1   Vertex3D First corner
P2   Vector1D distance to adjacent corner on x axis (relative to P1)
==== ======== ======================================================

.. index::
    Cube3D

Cube3D
^^^^^^

May be rotated; not aligned at right angles to xyz axes.

Representation 1: Vertices of two opposing corners.

==== ======== ===============
Name Type     Description
==== ======== ===============
P1   Vertex3D First corner
P2   Vertex3D Opposing corner
==== ======== ===============

Representation 2: Vertex and vector to opposing corner.

==== ======== ================================
Name Type     Description
==== ======== ================================
P1   Vertex3D First corner
V1   Vector3D Opposing corner (relative to P1)
==== ======== ================================

.. index::
    AlignedRectangle2D

AlignedRectangle2D
^^^^^^^^^^^^^^^^^^

Aligned at right angles to xy axes.

Representation 1: Two opposing corners.

==== ======== ===============
Name Type     Description
==== ======== ===============
P1   Vertex2D First corner
P2   Vertex2D Opposing corner
==== ======== ===============

Representation 2: Two opposing corners.

==== ======== ============================================
Name Type     Description
==== ======== ============================================
P1   Vertex2D First corner
V1   Vector2D Distance to opposing corner (relative to P1)
==== ======== ============================================

.. index::
    Rectangle2D

Rectangle2D
^^^^^^^^^^^

May be rotated; not aligned at right angles to xy axes.

Representation 1: P1 and P2 corners specify one edge; V1 specifies
length of other edge.

==== ======== ===============================================
Name Type     Description
==== ======== ===============================================
P1   Vertex2D First corner
P2   Vertex2D Adjacent corner
V1   Vector1D Distance to corner opposing P1 (relative to P2)
==== ======== ===============================================

Representation 2: Rotated, not aligned at right angles to xy axes.  P1
is the first corner, V1 specifies the second corner and V2 the length
of the other edge.

==== ======== ===============================================
Name Type     Description
==== ======== ===============================================
P1   Vertex2D First corner
V1   Vector2D Distance to adjacent corner (relative to P1)
V2   Vector1D Distance to corner opposing P1 (relative to P2)
==== ======== ===============================================

.. index::
    AlignedCuboid3D

AlignedCuboid3D
^^^^^^^^^^^^^^^

Aligned at right angles to xyz axes.

Representation 1: Two opposing corners.

==== ======== ===============
Name Type     Description
==== ======== ===============
P1   Vertex3D First corner
P2   Vertex3D Opposing corner
==== ======== ===============

Representation 2: Vertex and vector to opposing corner

==== ======== ============================================
Name Type     Description
==== ======== ============================================
P1   Vertex3D First corner
V1   Vector3D Distance to opposing corner (relative to P1)
==== ======== ============================================

.. index::
    Cuboid3D

Cuboid3D
^^^^^^^^

May be rotated; not aligned at right angles to xyz axes.

Representation 3: P1 and P2 corners specify one edge, V2 the
corner to define the first 2D face, and V3 the corner to define the
final two 2D faces, and opposes P1.

==== ======== =======================================================
Name Type     Description
==== ======== =======================================================
P1   Vertex3D First corner
P2   Vertex3D Second corner (adjacent to P1)
V1   Vector2D Distance to third corner (adjacent to P2)
V2   Vector1D Distance to fourth corner (opposing P1, adjacent to V1)
==== ======== =======================================================

Representation 4: P1 is the first corner, V1 specifies the
second corner and V2 the corner to define the first 2D face, and V3
the corner to define the final two 2D faces, and opposes P1.

==== ======== =======================================================
Name Type     Description
==== ======== =======================================================
P1   Vertex3D First corner
V1   Vector3D Distance to second corner (relative to P1)
V2   Vector2D Distance to third corner (relative to V1)
V3   Vector1D Distance to fourth corner (relative to V2, opposing P1)
==== ======== =======================================================


Circles and ellipses
--------------------

.. index::
    Circle2D

Circle2D
^^^^^^^^

Representation 1: Centre point and radius (1D vector)

==== ======== ============
Name Type     Description
==== ======== ============
P1   Vertex2D Centre point
V1   Vector1D Radius
==== ======== ============

Representation 2: Centre point and radius (2D vector)

==== ======== ============
Name Type     Description
==== ======== ============
P1   Vertex2D Centre point
V1   Vector2D Radius
==== ======== ============

Representation: 3: Bounding square.  Inherits all Square2D and AlignedSquare2D representations.

.. index:: Sphere3D

Sphere3D
^^^^^^^^

Representation 1: Centre point and radius (1D vector)

==== ======== ============
Name Type     Description
==== ======== ============
P1   Vertex3D Centre point
V1   Vector1D Radius
==== ======== ============

Representation 2: Centre point and radius (2D vector)

==== ======== ============
Name Type     Description
==== ======== ============
P1   Vertex3D Centre point
V1   Vector2D Radius
==== ======== ============

Representation 3: Centre point and radius (3D vector)

==== ======== ============
Name Type     Description
==== ======== ============
P1   Vertex3D Centre point
V1   Vector3D Radius
==== ======== ============

Representation: 4: Bounding cube.  Inherits all Cube3D and AlignedCube3D representations.

.. index::
    AlignedEllipse2D

AlignedEllipse2D
^^^^^^^^^^^^^^^^

Aligned at right angles to xy axes.

Representation 1: Centre and half axes.

==== ======== ===============
Name Type     Description
==== ======== ===============
P1   Vertex2D Centre point
V1   Vector2D Half axes (x,y)
==== ======== ===============

Representation 2: Bounding rectangle.  Inherits all AlignedRectangle2D
representations.

.. index::
    Ellipse2D

Ellipse2D
^^^^^^^^^

May be rotated; not aligned at right angles to xy axes.

Representation 1: Centre and half axes; V2 is at right-angles to V1,
so has only one dimension.

==== ======== ==============
Name Type     Description
==== ======== ==============
P1   Vertex2D Centre point
V1   Vector2D Half axes (xy)
V1   Vector1D Half axes (x)
==== ======== ==============

Representation 2: Bounding rectangle: Inherits all Rectangle2D and
AlignedRectangle2D representations.

Representation 3: Mahalanbobis distance used to draw an ellipse using the mean
coordinates (P1) and 2 × 2 covariance matrix (COV1)

==== ========= =======================
Name Type      Description
==== ========= =======================
P1   Vertex2D  Centre point (mean)
COV1 double[4] 2 × 2 covariance matrix
==== ========= =======================

.. index::
    AlignedEllipsoid3D

AlignedEllipsoid3D
^^^^^^^^^^^^^^^^^^

Aligned at right angles to xyz axes.

Representation 1: Centre and half axes

==== ======== =================
Name Type     Description
==== ======== =================
P1   Vertex3D Centre point
V1   Vector3D Half axes (x,y,z)
==== ======== =================

Representation 2: Centre and half axes (specified separately).

==== ======== =============
Name Type     Description
==== ======== =============
P1   Vertex3D Centre point
V1   Vector3D Half axis (x)
V2   Vector3D Half axis (y)
V3   Vector3D Half axis (z)
==== ======== =============

Representation 3: Bounding cuboid: Inherits all AlignedCuboid3D representations.

.. index::
    Ellipsoid3D

Ellipsoid3D
^^^^^^^^^^^

May be rotated; not aligned at right angles to xyz axes.

Representation 1: Centre and half axes; V2 and V3 are at right-angles
to V1 and each other, so have reduced dimensions.

==== ======== ===============
Name Type     Description
==== ======== ===============
P1   Vertex3D Centre point
V1   Vector3D Half axes (xyz)
V2   Vector2D Half axes (xy)
V3   Vector1D Half axes (x)
==== ======== ===============

Representation 2: Bounding cuboid: Inherits all Cuboid3D and
AlignedCuboid3D representations.

Representation 3: Mahalanbobis distance used to draw an ellipse using the mean
coordinates (P1) and 3 × 3 covariance matrix (COV1)

==== ========= =======================
Name Type      Description
==== ========= =======================
P1   Vertex3D  Centre point (mean)
COV1 double[9] 3 × 3 covariance matrix
==== ========= =======================

.. index::
    Polyline Splines

Polyline Splines
----------------

.. index::
    PolylineSpline2D

PolylineSpline2D
^^^^^^^^^^^^^^^^

Representation:

==== ======== ==============
Name Type     Description
==== ======== ==============
P1   Vertex2D Line start
P2   Vertex2D Second point
…    Vertex2D Further points
Pn   Vertex2D Line end
==== ======== ==============

.. index::
    PolylineSpline3D

PolylineSpline3D
^^^^^^^^^^^^^^^^

Representation:

==== ======== ==============
Name Type     Description
==== ======== ==============
P1   Vertex3D Line start
P2   Vertex3D Second point
…    Vertex3D Further points
Pn   Vertex3D Line end
==== ======== ==============

.. index::
    Polygon splines

Polygon splines
---------------

.. index::
    PolygonSpline2D

PolygonSpline2D
^^^^^^^^^^^^^^^

Representation:

==== ======== ==============
Name Type     Description
==== ======== ==============
P1   Vertex2D Line start
P2   Vertex2D Second point
…    Vertex2D Further points
Pn   Vertex2D Line end
==== ======== ==============

.. index::
    PolygonSpline3D

PolygonSpline3D
^^^^^^^^^^^^^^^

Representation:

==== ======== ==============
Name Type     Description
==== ======== ==============
P1   Vertex3D Line start
P2   Vertex3D Second point
…    Vertex3D Further points
Pn   Vertex3D Line end
==== ======== ==============

.. index::
    Cylinders

Cylinders
---------

.. index::
    AlignedCircularCylinder3D

AlignedCircularCylinder3D
^^^^^^^^^^^^^^^^^^^^^^^^^

Aligned 

.. index::
    CircularCylinder3D

CircularCylinder3D
^^^^^^^^^^^^^^^^^^

Representation 1: Start and endpoint, plus radius.

==== ======== =====================
Name Type     Description
==== ======== =====================
P1   Vertex3D Centre of first face
P2   Vertex3D Centre of second face
V1   Vector1D Radius
==== ======== =====================

Representation 2: Start point, distance to endpoint, plus radius

==== ======== =================================
Name Type     Description
==== ======== =================================
P1   Vertex3D Centre of first face
V1   Vector3D Distance to centre of second face
V2   Vector1D Radius
==== ======== =================================

Representation 3: Start and endpoint, plus vectors to define radius
(V1) and angle of start face, and unit vector defining angle of end
face.  Face angles other than right-angles let chains of cyclinders be
used for tubular structures without gaps at the joins.

.. note::
    Should V2 only allow angle, assuming radius from V1, or also allow
    a second radius to represent a conical section?

==== ======== ==============================
Name Type     Description
==== ======== ==============================
P1   Vertex3D Centre of first face
P2   Vertex3D Centre of second face
V1   Vector3D Radius and angle of first face
V2   Vector3D Angle of second face
==== ======== ==============================

Representation 4: Start point, distance to endpoint, plus vectors to
define radius (V2) and angle of start face, and unit vector defining
angle of end face (V3).  Face angles other than right-angles let
chains of cyclinders be used for tubular structures without gaps at
the joins.

==== ======== =================================
Name Type     Description
==== ======== =================================
P1   Vertex3D Centre of first face
V1   Vector3D Distance to centre of second face
V2   Vector3D Radius and angle of first face
V3   Vector3D Angle of second face
==== ======== =================================

.. note::
    Should V3 only allow angle, assuming radius from V2, or also allow
    a second radius to represent a conical section?

.. index::
    AlignedEllipticCylinder3D

AlignedEllipticCylinder3D
^^^^^^^^^^^^^^^^^^^^^^^^^

.. todo::
    Inherits from AlignedEllipse.

.. index::
    EllipticCylinder3D

EllipticCylinder3D
^^^^^^^^^^^^^^^^^^

Representations 1 and 2 describe basic elliptic cylinders with faces
at right angles; the following representations permit faces at
arbitrary angles.  Face angles other than right-angles let chains of
cyclinders be used for tubular structures without gaps at the joins.

Representation 1: Start and endpoint, plus half axes.

==== ======== =====================
Name Type     Description
==== ======== =====================
P1   Vertex3D Centre of first face
P2   Vertex3D Centre of second face
V1   Vector2D Half axes (xy)
V2   Vector1D Half axes (x)
==== ======== =====================

.. note::
   Is the dimensionality of the half axes correct here?

Representation 2: Start point, distance to endpoint, plus half axes

==== ======== =======================
Name Type     Description
==== ======== =======================
P1   Vertex3D Centre of first face
V1   Vector3D Distance to second face
V2   Vector3D Half axes (xy)
V3   Vector2D Half axes (x)
==== ======== =======================

.. note::
   Is the dimensionality of the half axes correct here?

.. todo::
    Should half axes and angle be specified in same vector or separately?

 3: Start and endpoint, plus vectors to define half axes (V1 and V2)
    and angle of start face, and unit vector defining angle of end
    face (V3).

==== ======== =============================
Name Type     Description
==== ======== =============================
P1   Vertex3D Centre of first face
P2   Vertex3D Centre of second face
V1   Vector3D Half axes of first face (xyz)
V2   Vector2D Half axes of first face (xy)
V3   Vector3D Angle of second face
==== ======== =============================

 3: Start and endpoint, plus vectors to define half axes (V1 and V2)
    and angle of start face, and unit vector defining angle of end
    face (V3).

==== ======== =======================
Name Type     Description
==== ======== =======================
P1   Vertex3D Centre of first face
V1   Vector3D Distance to second face
V2   Vector3D Half axes (xyz)
V3   Vector2D Half axes (xy)
V4   Vector3D Angle of second face
==== ======== =======================

Representation 4: Bounding cuboid: Inherits all Cube3D and Cuboid3D
representations; first face is the base.

.. index::
    Arcs

Arcs
----

.. index::
    Arc2D

Arc2D
^^^^^

Representation 1:

==== ======== ============
Name Type     Description
==== ======== ============
P1   Vertex2D Centre point
P2   Vertex2D Arc start
V1   Vector2D Arc end
==== ======== ============

Representation 2:

==== ======== ============
Name Type     Description
==== ======== ============
P1   Vertex2D Centre point
V2   Vector2D Arc start
V1   Vector2D Arc end
==== ======== ============

.. index::
    Arc3D

Arc3D
^^^^^

Representation 1:

==== ======== ============
Name Type     Description
==== ======== ============
P1   Vertex3D Centre point
P2   Vertex3D Arc start
V1   Vector3D Arc end
==== ======== ============

Representation 2:

==== ======== ============
Name Type     Description
==== ======== ============
P1   Vertex3D Centre point
V2   Vector3D Arc start
V1   Vector3D Arc end
==== ======== ============

.. index::
    Masks

Masks
-----

Masks may be either grey masks (double or integer) or bitmasks.

For all of the following masks, DATA should be stored outside the ROI
specification either as BinData or (better) in an IFD for OME-TIFF.
It could be stored as part of the double array, but this would be
quite inefficient.

.. note::
   Masks are applied to the bounding rectangle, and so a 1:1
   correspondance between mask and image pixel data is not required.
   In this case, a new greymask should be computed which is aligned
   with the pixel data, and then (if required) thresholded to a
   bitmask.

.. index::
    GreyMask2D

GreyMask2D
^^^^^^^^^^

Representation:

The mask is applied to the bounding rectangle.  Dimensions specify the
x and y size of the mask.  DATA is the mask pixel data.

==== =========== =================================
Name Type        Description
==== =========== =================================
P1   Vertex2D    Start point of bounding rectangle
P2   Vertex2D    End point of bounding rectangle
DIM1 Vector2D    Mask dimensions (x,y)
DATA double[x,y] Mask data
==== =========== =================================

.. index::
    BitMask2D

BitMask2D
^^^^^^^^^

Representation:

The mask is applied to the bounding rectangle.  Dimensions specify the
x and y size of the mask.  DATA is the mask pixel data.

==== =========== =================================
Name Type        Description
==== =========== =================================
P1   Vertex2D    Start point of bounding rectangle
P2   Vertex2D    End point of bounding rectangle
DIM1 Vector2D    Mask dimensions (x,y)
DATA bool[x,y]   Mask data
==== =========== =================================

.. index::
    GreyMask3D

GreyMask3D
^^^^^^^^^^

Representation:

The mask is applied to the bounding cuboid.  Dimensions specify the
x, y and z size of the mask.  DATA is the mask pixel data.

==== ============= =================================
Name Type          Description
==== ============= =================================
P1   Vertex3D      Start point of bounding rectangle
P2   Vertex3D      End point of bounding rectangle
DIM1 Vector3D      Mask dimensions (x,y)
DATA double[x,y,z] Mask data
==== ============= =================================

.. index::
    BitMask3D

BitMask3D
^^^^^^^^^

Representation:

The mask is applied to the bounding cuboid.  Dimensions specify the
x, y and z size of the mask.  DATA is the mask pixel data.

==== =========== =================================
Name Type        Description
==== =========== =================================
P1   Vertex3D    Start point of bounding rectangle
P2   Vertex3D    End point of bounding rectangle
DIM1 Vector3D    Mask dimensions (x,y)
DATA bool[x,y,z] Mask data
==== =========== =================================

.. index::
    Meshes

Meshes
------


Mesh representation depends upon the mesh format.  In the examples
below, face-vertex meshes are used.

.. index::
    Mesh2D

Mesh2D
^^^^^^

Representation:

===== ================ ====================================================
Name  Type             Description
===== ================ ====================================================
NFACE double           Number of faces
VREF  double[NFACE][3] Vertex references per face, counterclockwise winding
NVERT double           Number of vertices
VERTS Vertex2D[NVERT]  Vertex coordinates
===== ================ ====================================================

Vertex references are indexes into the VERTS array.  Vertex-face
mapping is implied, and will require the implementor to construct the
mapping.

.. index::
    Mesh3D

Mesh3D
^^^^^^

Representation:

===== ================ ====================================================
Name  Type             Description
===== ================ ====================================================
NFACE double           Number of faces
VREF  double[NFACE][3] Vertex references per face, counterclockwise winding
NVERT double           Number of vertices
VERTS Vertex3D[NVERT]  Vertex coordinates
===== ================ ====================================================

Vertex references are indexes into the VERTS array.  Vertex-face
mapping is implied, and will require the implementor to construct the
mapping.

.. index::
    Labels

Labels
------

.. index::
    Text2D

Text2D
^^^^^^

Representation 1: Text aligned relative to a point.  Inherits all
Point2D and Point3D representations.

Representation 2: Text aligned relative to a line.  Inherits all
Line2D and Line3D, Direction2D and Direction3D representations.
    
Representation 3: Text aligned and flowed inside a rectangle.
Inherits all AlignedSquare2D, Square2D, AlignedRectangle2D and
Rectangle2D representations.

.. index::
    Scale bars

Scale bars
----------

.. index::
    Scale2D

Scale2D
^^^^^^^

Representation 1: Scale bar between two points.  Inherits all Line2D representations.

Representation 1: Scale bar described by vector.  Inherits all Distance2D representations.

.. index::
    Scale3D

Scale3D
^^^^^^^

Representation 1: Scale bar between two points.  Inherits all Line3D representations

Representation 1: Scale bar described by vector.  Inherits all Distance3D representations.

.. note::
    A 3D scale may need to be a 3D grid to allow visualisation of
    perspective, in which case the representation will define the grid
    bounding cuboid; inherit AlignedCuboid3D representations.  Permit
    scale rotation with Cuboid3D?  Allow specification of grid size
    and only allow sizing in discrete units?
