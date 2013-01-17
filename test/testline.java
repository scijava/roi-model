import java.io.FileOutputStream;
import java.io.PrintStream;
import java.io.IOException;
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

        // Output a ROI in Icy XML format.
        {
            Vertex3D p1 = new Vertex3D(4.5653,7.6969,0);
            Vertex3D p2 = new Vertex3D(0.9834,9.7242,4);
            Line l6 = new Line(p1, p2);
            LinePoints3D pts = l6.getPoints();

            FileOutputStream fout;
            try
		{
                    fout = new FileOutputStream("roi.xml");
                    new PrintStream(fout).printf("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n<root>\n<roi>\n<classname>icy.roi.ROI2DRectangle</classname>\n<id>1</id>\n<name>Rectangle2D</name>\n<color>-7703041</color>\n<selected_color>-3014684</selected_color>\n<stroke>2</stroke>\n<selected>true</selected>\n<z>-1</z>\n<t>-1</t>\n<c>-1</c>\n<top_left>\n<color>-3014684</color>\n<selected_color>-1</selected_color>\n<pos_x>%s</pos_x>\n<pos_y>%s</pos_y>\n<ray>6</ray>\n<visible>true</visible>\n</top_left>\n<bottom_right>\n<color>-3014684</color>\n<selected_color>-1</selected_color>\n<pos_x>%s</pos_x>\n<pos_y>%s</pos_y>\n<ray>6</ray>\n<visible>true</visible>\n</bottom_right>\n</roi>\n</root>\n",
                              pts.points[0].vertex[0],
                              pts.points[0].vertex[1],
                              pts.points[1].vertex[0],
                              pts.points[1].vertex[1]);
                    fout.close();
                }
            catch (IOException e)
                {
                    System.err.println ("Unable to write Icy roi.xml");
                }
        }

    }
}
