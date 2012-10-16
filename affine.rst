.. index::
    pair: Affine; transform

Affine transforms
=================

To support proper 3D operation, it would make sense to extend the
existing support for 3×3 2D affine transforms to 4×4 3D transforms.

For both 2D and 3D transforms, translation, rotation and scaling are
supported.  Skewing, using the bottom row of the matrix, is not.

.. index::
    triple: Affine; transform; 2D

2D transforms
-------------

.. math::

    \begin{bmatrix} a & c & e \\ b & d & f \\ 0 & 0 & 1 \end{bmatrix}

.. index::
    triple: Affine; transform; 3D

3D transforms
-------------

.. math::

    \begin{bmatrix} a & d & g & j \\ b & e & h & k \\ c & f & i & l \\ 0 & 0 & 0 & 1 \end{bmatrix}
