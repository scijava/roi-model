Introduction
============

Purpose
-------

This document is a formal specification for the definition, storage
and exchange of regions of interest (ROIs).  This specification will
be implementable in any programming language, and is intended to
provide a common set of ROI types which will be usable in all image
analysis software programs.

Scope
-----

This specification defines abstract definitions of regions of
interest, including details of how certain data structures and
algorithms must be defined and behave, in order to ensure that ROIs
work uniformly between the different programs and libraries
implementing the specification.  It also provides examples of
serialised forms which may be used for storage and/or exchange.
However, it does not define a file format; it is the responsibility of
the implementors to integrate this model into their file formats as
they see fit.

Reference implementation
------------------------

This specification is accompanied by a reference implementation of the
model.  This implementation is intended to validate and test the
correctness of the specification.  It may be usable directly, however
this is not the primary intention for its existence.  Note that the
reference implementation strives for complete correctness, and
implementors of this specification may wish to provide additional
optimisations to improve performance.

Concepts
--------

- A ROI is an evaluation of a shape object

- A shape is defined by the rules which transform its representation
  (e.g. geometry, range within a dimension) into a a bitmask and/or
  greymask

- Each shape has a unique name (type) and number; the number is used for
  serialisation and versioning

- Each shape is described by one (or more) representations, these are
  the primitives which define the geometry or range within a
  dimension

- A shape object can be composed of one or more shapes, which can
  include transforms and shapes in arbitrary dimensions

- Each representation has a unique name and number; the number is used
  for serialisation and versioning

- Shapes which share representations may be freely interconverted;
  conversion is not required to be possible in both directions
  (e.g. square to rectangle or polyline to/from polygon)

- A shape is essentially a serialised expression which must be
  evaluated to create a usable ROI; given that certain shapes can
  contain other shapes, this provides for ROIs which are both
  extensible and of arbitrary complexity.

- All shapes can be serialised as a sequence of numbers

- Given that each shape can be reconstructed using its shape and
  representation numbers, which specify the exact sequence of numbers
  to deserialise to reconstruct the object, it is possible to exchange
  ROIs as simple text, or alternately as binary; more structured (but
  space inefficient) representations could be realised using XML.

- The object/function serialisation methodology used here is inspired
  by (but not derived from) the `SSH FXP specification
  <http://tools.ietf.org/html/draft-ietf-secsh-filexfer-13>`_ which
  defines the wire protocol for SFTP.
