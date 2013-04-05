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
        for(Tile tile : tiles){
            // Check relevant tile info
            if(tile.getOwner() == playerID() &&  // If this is true, the tile is a cove that belongs to you
               tile.getHasEgg() == 0  && // If this is true, the tile is not already spawning a fish
               getFishIndex(tile.getX(), tile.getY()) == -1){ // If this is true, the tile has no fish on it already
                // Iterate across all species
                for(int i=0; i<species.length; i++){
                    // Ensure that species is in season
                    if(getSpecies(i).getSeason() == currentSeason() &&
                       // Ensure we can afford this species
                       players[playerID()].getSpawnFood() >= getSpecies(i).getCost()){
                        // If so, spawn it!
                        getSpecies(i).spawn(tile.getX(),tile.getY());
                        break; // Don't try to spawn multiple fish on the same cove
                    }
                }
            }
        }
        // Iterate across all the fishes!
        for(Fish fish : fishes){
            // Only attempt to move fish I own
            if(fish.getOwner() == playerID()){
                // Check the tile to the right
                if(fish.getX()+1 < mapWidth() && // Then we aren't moving off the map
                   getTile(fish.getX()+1,fish.getY()).getHasEgg() == 0 && // Then we aren't moving onto an egg
                   getTile(fish.getX()+1,fish.getY()).getOwner() != 1-playerID() &&  // Then we aren't moving onto an enemy cove
                   getFishIndex(fish.getX()+1,fish.getY()) == -1 && // Then there is no fish at that spot
                   fish.getMovementLeft() > 0 && // Then we have moves left
                   getTile(fish.getX()+1, fish.getY()).getTrashAmount() == 0){ // Then there is no trash on the tile
                    // We can move to the right one tile!
                    fish.move(fish.getX()+1,fish.getY());
                }
                if(fish.getY()+1 < mapHeight() && // Ensure we do not pick up off the map
                   fish.getCarryCap()-fish.getCarryingWeight() > 0 && // Ensure we have the necessary weight
                   fish.getCurrentHealth() >= 1 && // Ensure we have enough health
                   getTile(fish.getX(),fish.getY()+1).getTrashAmount() > 0){ // Ensure the tile has trash
                    // Pick up that can!
                    fish.pickUp(fish.getX(),fish.getY()+1,1);
                }
                if(fish.getY()-1 >= 0 && // Ensure we don't drop off the map
                   getFishIndex(fish.getX(),fish.getY()-1) == -1 && // Make sure there's no fish where we intend to drop
                   fish.getCarryingWeight() > 0){ // Ensure we have something to drop
                    // DROP IT
                    fish.drop(fish.getX(),fish.getY()-1,1); // Smashing!
                }
                if(fish.getX()+1 < mapWidth() && // Then we aren't attacking off the map
                        getFishIndex(fish.getX()+1,fish.getY()) != -1 && // Then there is a fish at that spot
                        fishes[getFishIndex(fish.getX()+1,fish.getY())].getOwner() != playerID() && // Then that fish belongs to the bad guy
                        fish.getAttacksLeft() > 0){ // Then we have attacks left
                    // We can move to the right one tile!
                    fish.attack(fishes[getFishIndex(fish.getX()+1,fish.getY())]);
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
