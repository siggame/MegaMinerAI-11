import java.awt.*;
import java.util.*;
import java.util.List;

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

    /**
     * Depth Limited Tree Search
     * @fdasdfasdfasdfasdfparam maxDepth the maximum depth to go to
     * @return the State object storing the solution
     */
//    public State dlts(int maxDepth){
//        // Keep track of max frontier size
//        int maxFrontierSize = 0;
//
//        // Create the initial state
//        final State initialState = new State(problem, null);
//
//        // Define the frontier
//        LinkedList<State> frontier = new LinkedList<State>();
//
//        // Expand the initial state, adding the elements to the frontier
//        ArrayList<State> initialNodes = PuzzleExpander.expand(initialState);
//
//        // Add resulting nodes to frontier
//        for(State node : initialNodes){
//            // Only add the node to the frontier if it is not deeper than the maxDepth
//            if(!(node.getDepth() > maxDepth)){
//                frontier.addFirst(node);
//            }
//        }
//
//        // Update max frontier size
//        if(frontier.size() > maxFrontierSize) maxFrontierSize = frontier.size();
//
//        // Continue until we run out of nodes to test
//        while(!frontier.isEmpty()){
//
//            // Sort the array of new nodes by Manhattan distance plus the state's current depth
//            Collections.sort(frontier, new HeuristicSorter(Heuristic.Chebyshev));
//
//            // Choose a node to expand on
//            State chosenNode = frontier.getFirst();
//
//            // Remove that node from the frontier
//            frontier.removeFirst();
//
//            // If the chosen node contains a goal state, then we return the corresponding solution
//            if(chosenNode.isGoalState()){
//                // Output max frontier size
//                System.out.println("Maximum number of states stored in the frontier: " + maxFrontierSize);
//                return chosenNode;
//            }
//
//            // Expand the chosen node
//            ArrayList<State> expandedNodes = PuzzleExpander.expand(chosenNode);
//
//            // Add resulting nodes to frontier
//            for(State node : expandedNodes){
//                // Only add the node to the frontier if it is not deeper than the maxDepth
//                if(!(node.getDepth() > maxDepth)){
//                    frontier.addFirst(node);
//                }
//            }
//
//            // Update max frontier size
//            if(frontier.size() > maxFrontierSize) maxFrontierSize = frontier.size();
//        }
//        // If we get this far, we've found no solution
//        return null;
//    }

    public class HeuristicSorter implements Comparator<State>{
        Heuristic heuristic;
        public HeuristicSorter(Heuristic heuristic) {
            this.heuristic = heuristic;
        }

        @Override
        public int compare(State o1, State o2) {
            return 0;
        }
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
        Stack<Point> path = new Stack<Point>();
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
                            baseAI.getFish(state.x,state.y) == null &&                    // There is no fish at that spot
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
