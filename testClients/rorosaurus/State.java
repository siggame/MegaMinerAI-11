import java.awt.*;

/**
 * User: rory
 * Date: 4/10/13
 * Time: 9:29 PM
 */

public class State {
    State parent;
    Point destination;
    public int x;
    public int y;

    public State(State parent, Point location, Point destination) {
        this.parent = parent;
        this.x = location.x;
        this.y = location.y;
        this.destination = destination;
    }

    public boolean isGoalNode(){
        return x == destination.x && y == destination.y;
    }

    public Point getPoint(){
        return new Point(x,y);
    }
}
