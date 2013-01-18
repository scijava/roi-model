public Vertex2D()
{
    this.vertex[0] = this.vertex[1] = 0;
}

public Vertex2D(double x, double y)
{
    this.vertex[0] = x;
    this.vertex[1] = y;
}

public Vertex2D(double x)
{
    this.vertex[0] = x;
    this.vertex[1] = 0;
}

public Vertex2D(Vertex2D vertex)
{
    this.vertex[0] = vertex.vertex[0];
    this.vertex[1] = vertex.vertex[1];
}

public Vertex2D(Vertex1D vertex)
{
    this.vertex[0] = vertex.vertex[0];
    this.vertex[1] = 0;
}