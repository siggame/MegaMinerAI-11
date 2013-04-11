import java.util.Arrays;
import java.util.Comparator;

/**
 * User: rory
 * Date: 4/9/13
 * Time: 6:16 PM
 */

public enum FishType {

    SEA_STAR(0,11), // can attack reefs
    TOMCOD(6,10), // immune to trash damage
    CLEANER_SHRIMP(9,9), // can heal
    SPONGE(1,8), // high carry
    ELECTRIC_EEL(10,7), // can stun
    REEF_SHARK(7,6), // high damage, good carry
    OCTOPUS(5,5), // ranged, multi attack, low carry
    ANGELFISH(2,4), // high mobility
    CUTTLEFISH(8,3), // can stealth
    SEA_URCHIN(4,2), // decent damage, low carry
    JELLYFISH(11,1), // low damage, multi ranged attack, low carry
    CONESHELL_SNAIL(3,0), // ranged attack, can't carry
    ;

    private int indexVal;
    private int relVal;

    private FishType(int indexVal, int relVal) {
        this.indexVal = indexVal;
        this.relVal = relVal;
    }

    public int getRelValue(){
        return relVal;
    }

    public int getIndexVal() {
        return indexVal;
    }

    public FishType getSpecies(int index){
        for(FishType type : FishType.values()){
            if(type.getIndexVal() == index) return type;
        }
        return null;
    }

    public static FishType[] getBestTypes(){
        FishType[] types = Arrays.copyOf(FishType.values(), FishType.values().length);
        Arrays.sort(types,new Comparator<FishType>() {
            @Override
            public int compare(FishType o1, FishType o2) {
                return o1.getRelValue() - o2.getRelValue();
            }
        });
        return types;
    }
}
