ROI-ROI links
=============

ROI relationships: When segmenting cell contents, shown as cytoplasm,
actin filaments, nucleus and nucleolus, these fall into a strict
heirarchy (a nucleus can only be in one cell, though one cell could
have more than one nucleus).  If we added a ROI type that was a
container of ROIs (note: not a union), and added a means of
classifying ROIs with tags/labels, this would be very useful for HCS
and other types of analysis.  Additionally, some relationships are not
hierarchial, e.g. tree-like branching and merging in a vessel bed, but
could be represented if a ROI could point to one or more other ROIs,
which would permit a directed graph of relationships between ROIs.


Tracking
Containment
User modification (branch/merge)
Inherit properties
Layer
DAG
