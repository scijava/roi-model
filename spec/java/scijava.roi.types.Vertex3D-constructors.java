public Vertex3D()
{
    this.vertex[0] = this.vertex[1] = this.vertex[2] = 0;
}

public Vertex3D(double x, double y, double z)
{
    this.vertex[0] = x;
    this.vertex[1] = y;
    this.vertex[2] = z;
}

public Vertex3D(double x, double y)
{
    this.vertex[0] = x;
    this.vertex[1] = y;
    this.vertex[2] = 0;
}

public Vertex3D(double x)
{
    this.vertex[0] = x;
    this.vertex[1] = 0;
    this.vertex[2] = 0;
}

public Vertex3D(Vertex3D vertex)
{
    this.vertex[0] = vertex.vertex[0];
    this.vertex[1] = vertex.vertex[1];
    this.vertex[2] = vertex.vertex[2];
}

public Vertex3D(Vertex2D vertex)
{
    this.vertex[0] = vertex.vertex[0];
    this.vertex[1] = vertex.vertex[1];
    this.vertex[2] = 0;
}

public Vertex3D(Vertex1D vertex)
{
    this.vertex[0] = vertex.vertex[0];
    this.vertex[1] = 0;
    this.vertex[2] = 0;
}