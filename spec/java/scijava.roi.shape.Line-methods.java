public boolean contains(Vertex3D position)
{
	return false;
}

public double length()
{
    double dx = this.rep_canonical.points[0].vertex[0] - this.rep_canonical.points[1].vertex[0];
    double dy = this.rep_canonical.points[0].vertex[1] - this.rep_canonical.points[1].vertex[1];
    double dz = this.rep_canonical.points[0].vertex[2] - this.rep_canonical.points[1].vertex[2];

    return Math.sqrt((dx*dx) + (dy*dy) + (dz*dz));
}

public final LinePoints3D getPoints()
{
    return this.rep_canonical;
}