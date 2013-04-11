import java.awt.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Stack;

/**
 * User: rory
 * Date: 4/10/13
 * Time: 7:57 PM
 */

public class PathFinder {

    Point start;
    Point destination;
    BaseAI baseAI;

    public PathFinder(Point start, Point destination) {
        this.start = start;
        this.destination = destination;
        this.baseAI = BaseAI.getBaseAI();
    }

    public List<Point> getPath() {//throws InvalidDestinationException{
//        if(baseAI.getTile(destination.x,destination.y).getOwner() == 1-baseAI.playerID() ||  // We are moving onto an enemy cove
//                baseAI.getTile(destination.x,destination.y).getHasEgg() == 1 ||              // We are moving onto an egg
//                baseAI.getFishIndex(destination.x,destination.y) != -1 ||                    // There is fish at that spot
//                baseAI.getTile(destination.x, destination.y).getTrashAmount() != 0){         // There is trash on this spot
//            throw new InvalidDestinationException();
//        }
        State goalState = getGoalState();
        if(goalState == null) return null;
        Stack<Point> path = new Stack();
        State currentState = goalState;
        path.push(currentState.getPoint());
        while(currentState.parent != null){
            path.push(currentState.getPoint());
            currentState = currentState.parent;
        }
        printPath(path);
        return path;
    }

    public void printPath(List<Point> path){
        System.out.println("Path from " + start.toString() + " to " + destination.toString());
        for(Point point : path){
            System.out.println("(" + point.x + "," + point.y + ")");
        }
    }

    public State getGoalState(){
        State startNode = new State(null, start, destination);

        if(start.equals(destination)){
            return startNode;
        }
        List<State> frontier = generatePoints(startNode);
//        List<State> visited = new ArrayList<State>();
        int depth = 1;
        while(!frontier.isEmpty()){
            List<State> newFrontier = new ArrayList<State>();
            for(State state : frontier){
                if(state.x >= 0 && state.x < baseAI.mapWidth() && state.y >= 0 && state.y < baseAI.mapHeight()){
                    if(state.isGoalNode()) return state;
                    if(baseAI.getTile(state.x,state.y).getOwner() != 1-baseAI.playerID() &&  // We aren't moving onto an enemy cove
                            baseAI.getTile(state.x,state.y).getHasEgg() == 0 &&              // We aren't moving onto an egg
                            baseAI.getFishIndex(state.x,state.y) == -1 &&                    // There is no fish at that spot
                            baseAI.getTile(state.x, state.y).getTrashAmount() == 0){         // There is no trash on this spot
//                        for(State newState : generatePoints(state)){
//                            if(!visited.contains(newState)) newFrontier.add(newState);
//                        }
//                        visited.add(state);
                        newFrontier.addAll(generatePoints(state));
                    }
                }
            }
            depth++;
            frontier = newFrontier;
            for(State state : frontier){
                System.out.println(state.x + "," + state.y);
            }
        }
        return null;

    }

    private List<State> generatePoints(State startState){
        return Arrays.asList(new State(startState, new Point(startState.x+1, startState.y), destination),
                new State(startState, new Point(startState.x-1, startState.y), destination),
                new State(startState, new Point(startState.x, startState.y+1), destination),
                new State(startState, new Point(startState.x, startState.y-1), destination));
    }

    public class InvalidDestinationException extends Exception{

    }
}
