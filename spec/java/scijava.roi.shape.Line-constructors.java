public Line()
{
    Vertex3D v = new Vertex3D(0,0,0);
    Vertex3D list[] = {v, v};
    this.rep_canonical = new LinePoints3D(list);
    this.rep_generic = null;
}

public Line(LinePoints3D points)
{
    if (points == null || points.points == null || points.points.length != 2)
        throw new java.lang.IllegalArgumentException("scijava.roi.shape.Line requires 2 points");

    this.rep_canonical = new LinePoints3D(points);
    this.rep_generic = null;
}

public Line(Vertex3D point1, Vertex3D point2)
{
    Vertex3D list[] = {point1, point2};
    this.rep_canonical = new LinePoints3D(list);
    this.rep_generic = null;
}

public Line(Line line)
{
    this.rep_canonical = new LinePoints3D(line.rep_canonical);
    this.rep_generic = null;

    // TODO: Copy generic representation.
    // if (line.rep_generic instanceof Cloneable)
    //     {
    //         this.rep_generic = line.rep_generic.clone();
    //     }
}