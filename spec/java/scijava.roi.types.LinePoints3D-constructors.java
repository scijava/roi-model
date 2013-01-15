public LinePoints3D()
{
    this.points = null;
}

public LinePoints3D(Vertex3D points[])
{
    this.points = null;
    if (points != null)
        {
            this.points = new Vertex3D[points.length];
            for (int i = 0; i < points.length; i++)
                {
                    this.points[i] = new Vertex3D(points[i]);
                }
        }
}

public LinePoints3D(LinePoints3D linepoints)
{
    this.points = null;
    Vertex3D points[] = linepoints.points;
    if (points != null)
        {
            this.points = new Vertex3D[linepoints.points.length];
            for (int i = 0; i < linepoints.points.length; i++)
                {
                    this.points[i] = new Vertex3D(linepoints.points[i]);
                }
        }
}
