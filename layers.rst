Layers
======

In the Zeiss AxioVision formats, ROIs (shapes) are contained within
Layers.  Sets of ROIs are collected in different layers.  The UI only
uses a single layer, but uses separate layers for acquisition and
post-acquisition ROIs.  But in the file format one may define arbitrary
numbers of layers to act as a grouping mechanism for ROIs.

Adding layers as a top level grouping would permit related ROIs to be
grouped together.  However, this would also be possible using ROI-ROI
links; it could be implemented using Layer-ROI links.  Maybe layer
could be a ROI type used solely for grouping?
