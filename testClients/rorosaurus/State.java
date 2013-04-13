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

    public int getDepth(){
        int depth = 0;
        State newParent = parent;
        while(newParent != null){
            depth++;
            newParent = newParent.parent;
        }
        return depth;
    }

    /**
     * Provides the Manhattan Distance to the goal node from this state
     * eg. |x1-x2| + |y1-y2|
     * @return an int, the Manhattan Distance to goal node
     */
    public int getManhattanDistanceFromGoal(){
        return Math.abs(x - destination.x) +
                Math.abs(y - destination.y);
    }

    /**
     * Provides the Euclidean Distance to the goal node from this state
     * eg. sqrt((x1-x2)^2 + (y1-y2)^2)
     * @return an int, the Euclidean Distance to goal node
     */
    public int getEuclideanDistanceFromGoal(){
        return (int)Math.sqrt(
                Math.pow(x - destination.x, 2) +
                        Math.pow(y - destination.y, 2)
        );
    }

    /**
     * Provides the Chebyshev Distance to the goal node from this state
     * eg. max(|x1-x2|,|y1-y2|)
     * @return an int, the Chebyshev Distance to the goal node
     */
    public int getChebyshevDistanceFromGoal(){
        return Math.max(Math.abs(x - destination.x),
                Math.abs(y - destination.y));
    }
}
