import java.lang.IllegalArgumentException;
import scijava.roi.shape.Line;
import scijava.roi.types.Vertex3D;
import scijava.roi.types.LinePoints3D;

class testline
{
    public static void main(String[] args)
    {
        System.out.println("Running model tests");

        {
            Line l1 = new Line();
            double l1len = l1.length();

            System.out.println("L1: " + l1 + " len=" + l1len);
        }

        {
            Vertex3D p1 = new Vertex3D(2,2,2);
            Vertex3D p2 = new Vertex3D(4,4,4);
            Line l2 = new Line(p1, p2);
            double l2len = l2.length();

            System.out.println("L2: " + l2 + " len=" + l2len);
        }

        {
            Vertex3D p1 = new Vertex3D(2,2,0);
            Vertex3D p2 = new Vertex3D(4,4,0);
            Vertex3D pa[] = {p1, p2};
            LinePoints3D lp = new LinePoints3D(pa);
            Line l3 = new Line(lp);
            double l3len = l3.length();

            System.out.println("L3: " + l3 + " len=" + l3len);
        }

        try
            {
                Vertex3D p1 = new Vertex3D(2,2,5);
                Vertex3D p2 = new Vertex3D(4,4,4);
                Vertex3D p3 = new Vertex3D(4,2,5);
                Vertex3D pa[] = {p1, p2, p3};
                LinePoints3D lp = new LinePoints3D(pa);
                Line l4 = new Line(lp);
                double l4len = l4.length();

                System.out.println("L4 (FAIL): " + l4 + " len=" + l4len);
            }
        catch (java.lang.IllegalArgumentException e)
            {
                System.out.println("L4: Construction failed (expected): " + e);
            }

        try
            {
                Vertex3D p1 = new Vertex3D(2,2,5);
                Vertex3D pa[] = {p1};
                LinePoints3D lp = new LinePoints3D(pa);
                Line l5 = new Line(lp);
                double l5len = l5.length();

                System.out.println("L5 (FAIL): " + l5 + " len=" + l5len);
            }
        catch (java.lang.IllegalArgumentException e)
            {
                System.out.println("L5: Construction failed (expected): " + e);
            }
    }
}
