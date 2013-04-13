import java.util.ArrayList;
import java.util.List;

/**
 * User: rory
 * Date: 4/9/13
 * Time: 6:13 PM
 */

public class Spawner {

    BaseAI baseAI;

    public Spawner() {
        baseAI = BaseAI.getBaseAI();
    }

    public void naiveSpawn(){
        List<Tile> validCoves = getSpawnableCoves();
        for(Tile tile : validCoves){
            // Iterate across all species
            for(int i=0; i<baseAI.speciesList.length; i++){
                if(baseAI.speciesList[i].getSeason() == baseAI.currentSeason() &&                                   // Ensure that species is in season
                        baseAI.players[baseAI.playerID()].getSpawnFood() >= baseAI.speciesList[i].getCost()){       // Ensure we can afford this species
                    baseAI.speciesList[i].spawn(tile);       // If so, spawn it!
                    break;                                                  // Don't spawn multiple fish on the same cove
                }
            }
        }
    }

    public void sortedSpawn(){
        List<Tile> validCoves = getSpawnableCoves();
        for(Tile tile : validCoves){
            // Iterate across all species
            for(FishType type : FishType.getBestTypes()){
                if(baseAI.speciesList[type.getIndexVal()].getSeason() == baseAI.currentSeason() &&                                   // Ensure that species is in season
                        baseAI.players[baseAI.playerID()].getSpawnFood() >= baseAI.speciesList[type.getIndexVal()].getCost()){       // Ensure we can afford this species
                    baseAI.speciesList[type.getIndexVal()].spawn(tile);      // If so, spawn it!
                    break;                                                                  // Don't spawn multiple fish on the same cove
                }
            }
        }
    }

    private List<Tile> getSpawnableCoves(){
        ArrayList<Tile> coves = new ArrayList<Tile>();
        // Iterate across all tiles
        for(Tile tile : baseAI.tiles){
            // Check relevant tile info
            if(tile.getOwner() == baseAI.playerID() &&                       // The tile is a cove that belongs to you
                    tile.getHasEgg() == 0  &&                                // The tile is not already spawning a fish
                    tile.getTrashAmount() == 0 &&                            // The tile has no trash on it
                    baseAI.getFish(tile.getX(), tile.getY()) == null){       // The tile has no fish on it already
                coves.add(tile);
            }
        }
        return coves;
    }
}
