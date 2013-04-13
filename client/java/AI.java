import com.sun.jna.Pointer;


///The class implementing gameplay logic.
public class AI extends BaseAI
{
    public static final int SEA_STAR=0, SPONGE=1, ANGELFISH=2, CONESHELL_SNAIL=3, SEA_URCHIN=4, OCTOPUS=5, TOMCOD=6, REEF_SHARK=7, CUTTLEFISH=8, CLEANER_SHRIMP=9, ELECTRIC_EEL=10, JELLYFISH=11;

    public String username()
    {
        return "Shell AI";
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

        // Iterate across all tiles
        for(Tile tile : tiles)
        {
            // Check relevant tile info
            if(tile.getOwner() == playerID() &&                 // The tile is a cove that belongs to you
               tile.getHasEgg() == 0  &&                        // The tile is not already spawning a fish
               getFish(tile.getX(), tile.getY()) == null)       // The tile has no fish on it already
            {
                // Iterate across all species
                for(int i=0; i<speciesList.length; i++)
                {
                    if(speciesList[i].getSeason() == currentSeason() &&                      // Ensure that species is in season
                        players[playerID()].getSpawnFood() >= speciesList[i].getCost())      // Ensure we can afford this species
                    {
                        speciesList[i].spawn(tile);      // If so, spawn it!
                        break;                           // Don't spawn multiple fish on the same cove
                    }
                }
            }
        }
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
                if(fish.getX()+1 < mapWidth() &&                                        // We aren't attacking off the map
                        getFish(fish.getX()+1,fish.getY()) != null &&                   // There is a fish at that spot
                    getFish(fish.getX()+1,fish.getY()).getOwner() != playerID() &&      // Then that fish belongs to the bad guy
                    fish.getAttacksLeft() > 0)                                          // We have attacks left
                {
                    fish.attack(getFish(fish.getX()+1,fish.getY()));                    // We can attack the tile to the right!
                }
            }
        }
        return true;
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
