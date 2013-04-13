import com.sun.jna.Pointer;

import java.awt.*;
import java.util.Arrays;
import java.util.Comparator;


///The class implementing gameplay logic.
public class AI extends BaseAI
{
    public String username()
    {
        return "Rorosaurus";
    }
    public String password()
    {
        return "password";
    }

    //This function is called each time it is your turn
    //Return true to end your turn, return false to ask the server for updated information
    public boolean run()
    {
        // Test player.talk()
        players[playerID()].talk("I appreciate it, BUT LOOK WHAT WE'RE DEALING WITH MAN!");

        PathFinder pathFinder = new PathFinder(new Point(1,6), new Point(0,0));
        pathFinder.getPath();

        // Iterate across all the fishes!
        for(Fish fish : fishes)
        {
            // Only attempt to move fish I own
            if(fish.getOwner() == playerID())
            {
                // Try to move to the right
                if(fish.getX()+1 < mapWidth() &&                                        // We aren't moving off the map
                        getTile(fish.getX()+1,fish.getY()).getOwner() != 1-playerID() &&    // We aren't moving onto an enemy cove
                        getTile(fish.getX()+1,fish.getY()).getOwner() != 3 &&               // We aren't moving onto a wall
                        getTile(fish.getX()+1,fish.getY()).getHasEgg() == 0 &&              // We aren't moving onto an egg
                        getFish(fish.getX()+1,fish.getY()) == null &&                       // There is no fish at that spot
                        getTile(fish.getX()+1, fish.getY()).getTrashAmount() == 0 &&        // There is no trash on the tile
                        fish.getMovementLeft() > 0)                                         // We have moves left
                {
                    fish.move(fish.getX()+1,fish.getY());                               // We can move to the right one tile!
                }
                // Try to pick up trash
                if(fish.getY()+1 < mapHeight() &&                               // Ensure we do not pick up off the map
                        fish.getCarryCap()-fish.getCarryingWeight() > 0 &&          // Ensure we have the necessary weight
                        fish.getCurrentHealth() >= 1 &&                             // Ensure we have enough health
                        getTile(fish.getX(),fish.getY()+1).getTrashAmount() > 0)    // Ensure the tile has trash
                {
                    fish.pickUp(getTile(fish.getX(),fish.getY()+1),1);          // Pick up that can!
                }
                // Drop some trash
                if(fish.getY()-1 >= 0 &&                                // Ensure we don't drop off the map
                        getFish(fish.getX(),fish.getY()-1) == null &&       // Make sure there's no fish where we intend to drop
                        fish.getCarryingWeight() > 0)                       // Ensure we have something to drop
                {
                    fish.drop(getTile(fish.getX(),fish.getY()-1),1);    // DROP IT! (Smashing!)
                    // http://www.youtube.com/embed/3JJe2vwNUX4?autoplay=1&start=154&end=157&showinfo=0&controls=0
                }
                // Try to attack to the right
                if(fish.getSpecies() != FishType.CLEANER_SHRIMP.getIndexVal()) // Try to attack to the right, if not Cleaner Shrimp
                {
                    if(fish.getX()+1 < mapWidth() &&                                            // We aren't attacking off the map
                            getFish(fish.getX()+1,fish.getY()) != null &&                       // There is a fish at that spot
                            getFish(fish.getX()+1,fish.getY()).getOwner() != playerID() &&      // Then that fish belongs to the bad guy
                            fish.getAttacksLeft() > 0)                                          // We have attacks left
                    {
                        fish.attack(getFish(fish.getX()+1,fish.getY()));                        // We can attack the tile to the right!
                    }
                }
                else // Try to heal an allied fish to the right
                {
                    if(fish.getX()+1 < mapWidth() &&                                            // We aren't attacking off the map
                            getFish(fish.getX()+1,fish.getY()) != null &&                       // There is a fish at that spot
                            getFish(fish.getX()+1,fish.getY()).getOwner() == playerID() &&      // Then that fish belongs to the bad guy
                            fish.getAttacksLeft() > 0)                                          // We have attacks left
                    {
                        fish.attack(getFish(fish.getX()+1,fish.getY()));                        // We can heal the fish on the tile to the right!
                    }
                }
            }
        }

        Spawner spawner = new Spawner();
        spawner.sortedSpawn();

        return true;
    }

    /**
     * Sorts the fish on the board according to the order we should move them to optimize movement to the opposite side
     * @return a Fish[] of all fish on the board
     */
    public Fish[] sort(){
        Fish[] sortedFishes = Arrays.copyOf(fishes, fishes.length);
        if(playerID() == 0){ // Then I'm on the left
            Arrays.sort(sortedFishes, new Comparator<Fish>() {
                @Override
                public int compare(Fish o1, Fish o2) {
                    return o2.getX()-o1.getX();
                }
            });
        }
        else{ // I'm on the right
            Arrays.sort(sortedFishes, new Comparator<Fish>() {
                @Override
                public int compare(Fish o1, Fish o2) {
                    return o1.getX()-o2.getX();
                }
            });
        }
        return sortedFishes;
    }


    //This function is called once, before your first turn
    public void init() {}

    //This function is called once, after your last turn
    public void end() {}


    public AI(Pointer c)
    {
        super(c);
    }
}
