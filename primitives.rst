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

========= ======================= ============
Primitive Representation          Description
========= ======================= ============
Vertex1D  double                  Vertex in 1D
Vertex2D  double, double          Vertex in 2D
Vertex3D  double, double, double  Vertex in 3D
Vector1D  double                  Vector in 1D
Vector2D  double, double          Vector in 2D
Vector3D  double, double, double  Vector in 3D
========= ======================= ============

All shape primitives are described in terms of the above basic
primitives.  This means that all shape descriptions are serialisable
as a list of double precision floating point values.

All 2D shape primitives could be oriented in 3D or using a unit
Vector3D, which would allow all 2D shapes to be used as surfaces in
3D.  They would additionally require a depth in order to be meaningful
(or assume a depth of one z slice).

.. todo::
    Bounding box
    Rotation centre
    Control points

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

==== ======== =========================
Name Type     Description
==== ======== =========================
P1   Vertex2D Line start
P2   Vertex2D Second point
…    Vertex2D Further points
Pn   Vertex2D Line end
==== ======== =========================

.. index::
    Polyline3D

Polyline3D
^^^^^^^^^^

==== ======== =========================
Name Type     Description
==== ======== =========================
P1   Vertex3D Line start
P2   Vertex3D Second point
…    Vertex3D Further points
Pn   Vertex3D Line end
==== ======== =========================

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
Non-square variants are the rectangle and cuboid.

.. index::
    Square2D

Square2D
^^^^^^^^

Representation 1: Aligned at right angles to xy axes.  Vertex and
point on x axis (y inferred).

==== ======== ========================================
Name Type     Description
==== ======== ========================================
P1   Vertex2D First corner
P2   Vertex1D x coordinate of adjacent/opposing corner
==== ======== ========================================

Representation 2: Aligned at right angles to xy axes.  Vertex and
vector on x axis (y inferred).

==== ======== ======================================================
Name Type     Description
==== ======== ======================================================
P1   Vertex2D First corner
P2   Vector1D distance to adjacent corner on x axis (relative to P1)
==== ======== ======================================================

Representation 3: Rotated, not aligned at right angles to xy axes.

==== ======== ===============
Name Type     Description
==== ======== ===============
P1   Vertex2D First corner
P2   Vertex2D Opposing corner
==== ======== ===============

Representation 4: Rotated, not aligned at right angles to xy axes.

==== ======== ================================
Name Type     Description
==== ======== ================================
P1   Vertex2D First corner
V1   Vector2D Opposing corner (relative to P1)
==== ======== ================================

.. index::
    Cube3D

Cube3D
^^^^^^

Representation 1: Aligned at right angles to xyz axes.  Vertex and
point on x axis (y and z inferred).

==== ======== ========================================
Name Type     Description
==== ======== ========================================
P1   Vertex3D First corner
P2   Vertex1D x coordinate of adjacent/opposing corner
==== ======== ========================================

Representation 2: Aligned at right angles to xyz axes.  Vertex and
vector on x axis (y and z inferred).

==== ======== ======================================================
Name Type     Description
==== ======== ======================================================
P1   Vertex3D First corner
P2   Vector1D distance to adjacent corner on x axis (relative to P1)
==== ======== ======================================================

Representation 3: Rotated, not aligned at right angles to xy axes.

==== ======== ===============
Name Type     Description
==== ======== ===============
P1   Vertex3D First corner
P2   Vertex3D Opposing corner
==== ======== ===============

Representation 4: Rotated, not aligned at right angles to xy axes.

==== ======== ================================
Name Type     Description
==== ======== ================================
P1   Vertex3D First corner
V1   Vector3D Opposing corner (relative to P1)
==== ======== ================================

.. index::
    Rectangle2D

Rectangle2D
^^^^^^^^^^^

Representation 1: Aligned at right angles to xy axes.  Two opposing corners.

==== ======== ===============
Name Type     Description
==== ======== ===============
P1   Vertex2D First corner
P2   Vertex2D Opposing corner
==== ======== ===============

Representation 2: Aligned at right angles to xy axes.  Two opposing corners.

==== ======== ============================================
Name Type     Description
==== ======== ============================================
P1   Vertex2D First corner
V1   Vector2D Distance to opposing corner (relative to P1)
==== ======== ============================================

Representation 3: Rotated, not aligned at right angles to xy axes.  P1
and P2 corners specify one edge; V1 specifies length of other edge

==== ======== ===============================================
Name Type     Description
==== ======== ===============================================
P1   Vertex2D First corner
P2   Vertex2D Adjacent corner
V1   Vector1D Distance to corner opposing P1 (relative to P2)
==== ======== ===============================================

Representation 4: Rotated, not aligned at right angles to xy axes.  P1
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
    Cuboid3D

Cuboid3D
^^^^^^^^

 [ Aligned at right angles to xyz axes ]
 1: P1 (Vertex3D), P2 (Vertex3D)
    Two opposing corners
 2: P1 (Vertex3D), V1 (Vector3D)
    Vertex and vector to opposing corner

 [ Rotated ]
 3: P1 (Vertex3D), P2 (Vertex3D), V1 (Vector2D), V2 (Vector1D) P1 and P2
    corners specify one edge, V2 the corner to define the first 2D
    face, and V3 the corner to define the final two 2D faces, and
    opposes P1.
 4: P1 (Vertex3D), V1 (Vector3D), V2 (Vector2D), V3 (Vector1D)
    P1 is the first corner, V1 specifies the second corner and V2 the
    corner to define the first 2D face, and V3 the corner to define
    the final two 2D faces, and opposes P1.

Circles and ellipses
--------------------

.. index::
    Circle2D

Circle2D
^^^^^^^^

 1: P1 (Vertex2D), V1 (Vector1D)
    Centre and radius
 2: P1 (Vertex2D), V1 (Vector2D)
    Centre and radius
 3: All Square2D specifications
    Bounding square

.. index::
    Sphere3D

Sphere3D
^^^^^^^^

 1: P1 (Vertex3D), V1 (Vector1D)
    Centre and radius
 2: P1 (Vertex3D), V1 (Vector2D)
    Centre and radius
 3: P1 (Vertex3D), V1 (Vector3D)
    Centre and radius
 4: All Cube3D specifications
    Bounding cube

.. index::
    Ellipse2D

Ellipse2D
^^^^^^^^^

 [ Aligned at right angles to xy axes ]
 1: P1 (Vertex2D), V1 (Vector2D)
    Centre and half axes
 2: P1 (Vertex2D), V1 (Vector1D), V2 (Vector1D)
    Centre and half axes specified separately
 3: All Rectangle2D (aligned at right-angle) specifications.

 [ Rotated ]
 4: P1 (Vertex2D), V1 (Vector2D), V2 (Vector1D)
    Centre and half axes; V2 is at right-angles to V1, so has only one dimension.
 5: All Rectangle2D (rotated) specifications.
 6: P1 (Vertex2D) COV (double × 2^2)
    Mahalanbobis distance used to draw an ellipse using the mean
    coordinates (P1) and 2 × 2 covariance matrix (COV)

.. index::
    Ellipsoid3D

Ellipsoid3D
^^^^^^^^^^^

 [ Aligned at right angles to xy axes ]
 1: P1 (Vertex3D), V1 (Vector3D)
    Centre and half axes
 2: P1 (Vertex2D), V1 (Vector1D), V2 (Vector1D), V3 (Vector1D)
    Centre and half axes specified separately
 3: All Rectangle3D (aligned at right-angle) specifications.

 [ Rotated ]
 4: P1 (Vertex3D), V1 (Vector3D), V2 (Vector2D), V3 (Vector1D)
    Centre and half axes; V2 and V3 are at right-angles to V1 and each
    other, so have reduced dimensions.
 5: All Rectangle3D (rotated) specifications.
 6: P1 (Vertex3D) COV (double × 3^2)
    Mahalanbobis distance used to draw an ellipse using the mean
    coordinates (P1) and 3 × 3 covariance matrix (COV)

.. index::
    Polyline Splines

Polyline Splines
----------------

.. index::
    PolylineSpline2D

PolylineSpline2D
^^^^^^^^^^^^^^^^

 1: P1 (Vertex2D), P2 (Vertex2D), …, Pn (Vertex2D)

.. index::
    PolylineSpline3D

PolylineSpline3D
^^^^^^^^^^^^^^^^

 1: P1 (Vertex3D), P2 (Vertex3D), …, Pn (Vertex3D)

.. index::
    Polygon splines

Polygon splines
---------------

.. index::
    PolygonSpline2D

PolygonSpline2D
^^^^^^^^^^^^^^^

 1: P1 (Vertex2D), P2 (Vertex2D), …, Pn (Vertex2D)

.. index::
    PolygonSpline3D

PolygonSpline3D
^^^^^^^^^^^^^^^

 1: P1 (Vertex3D), P2 (Vertex3D), …, Pn (Vertex3D)

.. index::
    Cylinders

Cylinders
---------

.. index::
    Cylinder3D

Cylinder3D
^^^^^^^^^^

 [ Circular ]
 1: P1 (Vertex3D), P2 (Vertex3D), V1 (Vector1D)
    Start and endpoint, plus radius
 2: P1 (Vertex3D), V1 (Vector3D), V2 (Vector1D)
    Start point, distance to endpoint, plus radius
 3: P1 (Vertex3D), P2 (Vertex3D), V1 (Vector3D), V2 (Vector3D)
    Start and endpoint, plus vectors to define radius (V1) and angle
    of start face, and unit vector defining angle of end face.  Face
    angles other than right-angles let chains of cyclinders be used
    for tubular structures without gaps at the joins.
 3: P1 (Vertex3D), V1 (Vector3D), V2 (Vector3D), V3 (Vector3D)
    Start point, distance to endpoint, plus vectors to define radius
    (V2) and angle of start face, and unit vector defining angle of
    end face (V3).  Face angles other than right-angles let chains of
    cyclinders be used for tubular structures without gaps at the
    joins.

 [ Elliptic ]
 1: P1 (Vertex3D), P2 (Vertex3D), V1 (Vector2D), V2 (Vector1D)
    Start and endpoint, plus half axes
 2: P1 (Vertex3D), V1 (Vector3D), V2 (Vector2D), V3 (Vector1D)
    Start point, distance to endpoint, plus half axes
 3: P1 (Vertex3D), P2 (Vertex3D), V1 (Vector3D), V2 (Vector2D) V3 (Vector3D)
    Start and endpoint, plus vectors to define half axes (V1 and V2)
    and angle of start face, and unit vector defining angle of end
    face (V3).  Face angles other than right-angles let chains of
    cyclinders be used for tubular structures without gaps at the
    joins.
 3: P1 (Vertex3D), V1 (Vector3D), V2 (Vector3D), V3 (Vector2D) V4 (Vector3D)
    Start point, distance to endpoint, plus vectors to define half
    axes (V2 and V3) and angle of start face, and unit vector defining
    angle of end face (V4).  Face angles other than right-angles let
    chains of cyclinders be used for tubular structures without gaps
    at the joins.

.. index::
    Arcs

Arcs
----

.. index::
    Arc2D

Arc2D
^^^^^

 1: P1 (Vertex2D), P2 (Vertex2D), V1 (Vector2D)
    Two points and unit vector describe an arc
 2: P1 (Vertex2D), V1 (Vector2D), V2 (Vector2D)
    Centre point, plus length and unit vector describe an arc

.. index::
    Arc3D

Arc3D
^^^^^
 1: P1 (Vertex3D), P2 (Vertex3D), V1 (Vector3D)
    Two points and unit vector describe an arc
 2: P1 (Vertex3D), V1 (Vector3D), V2 (Vector3D)
    Centre point, plus length and unit vector describe an arc

.. index::
    Masks

Masks
-----

.. index::
    Mask2D

Mask2D
^^^^^^

 1: DIMS (Vector2D), OFFSET (Vector2D), DATA (double × (DIMS[0] × DIMS[1]))
    Dimensions specify the x and y size of the mask, and offset the
    offset of this mask into the plane; DATA should be stored outside
    the ROI specification either as BinData or (better) in an IFD for
    OME-TIFF.

.. index::
    Mask3D

Mask3D
^^^^^^

 1: DIMS (Vector3D), OFFSET (Vector3D), DATA (double × (DIMS[0] × DIMS[1] × DIMS[2]))
    Dimensions specify the x, y and z size of the mask, and offset the
    offset of this mask into the volume; DATA should be stored outside
    the ROI specification either as BinData or (better) in a set of
    IFDs for OME-TIFF.

.. index::
    Meshes

Meshes
------

.. index::
    Mesh2D

Mesh2D
^^^^^^

 Representation depends on mesh format; shown here as face-vertex
 1: NUMFACE (double), (V1REF (double), V2REF (double), V3REF (double)) × NUMFACE,
    NUMVERT (double), V1 (Vertex2D) … Vn (Vertex2D)
    Number of faces, followed by the three vertices (counterclockwise winding) for
    each face, number of vertices, followed by a list of vertices.
    Vertex-face mapping is implied.

.. index::
    Mesh3D

Mesh3D
^^^^^^

 Representation depends on mesh format; shown here as face-vertex
 1: NUMFACE (double), (V1REF (double), V2REF (double), V3REF (double)) × NUMFACE,
    NUMVERT (double), V1 (Vertex3D) … Vn (Vertex3D)
    Number of faces, followed by the three vertices (counterclockwise winding) for
    each face, number of vertices, followed by a list of vertices
   Vertex-face mapping is implied.

.. index::
    Labels

Labels
------

.. index::
    Text2D

Text2D
^^^^^^

 1: All Vertex2D and Vertex3D specifications
    Text aligned relative to a point
 2: All Line2D and Line3D specifications
    Text aligned relative to a line
 3: All Rectangle2D and Rectangle3D specifications
    Text aligned and flowed inside a rectangle

.. index::
    Scale bars

Scale bars
----------

.. index::
    Scale2D

Scale2D
^^^^^^^

 1: P1 (Vertex2D), P2 (Vertex2D)
    Scale bar with distance between the two points
 2: P1 (Vertex2D), V1 (Vector2D)
    Scale bar with distance from the vector

.. index::
    Scale3D

Scale3D
^^^^^^^

 1: P1 (Vertex3D), P2 (Vertex3D)
    Scale bar with distance between the two points
 2: P1 (Vertex3D), V1 (Vector3D)
    Scale bar with distance from the vector
