import com.sun.jna.Pointer;

///This class describes the characteristics for each type of fish. A groundbased fish is damaged each time it ends a turn above the groundBound Y value. Also, a species will only be available For so long, and new species will become available as a match progreses. 
class Species
{
  Pointer ptr;
  int ID;
  int iteration;
  public Species(Pointer p)
  {
    ptr = p;
    ID = Client.INSTANCE.speciesGetId(ptr);
    iteration = BaseAI.iteration;
  }
  boolean validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.species.length; i++)
    {
      if(BaseAI.species[i].ID == ID)
      {
        ptr = BaseAI.species[i].ptr;
        iteration = BaseAI.iteration;
        return true;
      }
    }
    throw new ExistentialError();
  }

    //commands

  ///Have a new fish spawn and join the fight!
  boolean spawn(int x, int y)
  {
    validify();
    return (Client.INSTANCE.speciesSpawn(ptr, x, y) == 0) ? false : true;
  }

    //getters

  ///Unique Identifier
  public int getId()
  {
    validify();
    return Client.INSTANCE.speciesGetId(ptr);
  }
  ///The name of this species
  public String getName()
  {
    validify();
    return Client.INSTANCE.speciesGetName(ptr);
  }
  ///The amount of food it takes to raise this fish
  public int getCost()
  {
    validify();
    return Client.INSTANCE.speciesGetCost(ptr);
  }
  ///The maximum health of this fish
  public int getMaxHealth()
  {
    validify();
    return Client.INSTANCE.speciesGetMaxHealth(ptr);
  }
  ///The maximum number of movements in a turn
  public int getMaxMovement()
  {
    validify();
    return Client.INSTANCE.speciesGetMaxMovement(ptr);
  }
  ///The total weight the fish can carry
  public int getCarryCap()
  {
    validify();
    return Client.INSTANCE.speciesGetCarryCap(ptr);
  }
  ///The power of the fish's attack
  public int getAttackPower()
  {
    validify();
    return Client.INSTANCE.speciesGetAttackPower(ptr);
  }
  ///The attack arrange of the fish
  public int getRange()
  {
    validify();
    return Client.INSTANCE.speciesGetRange(ptr);
  }
  ///Maximum number of times this unit can attack per turn
  public int getMaxAttacks()
  {
    validify();
    return Client.INSTANCE.speciesGetMaxAttacks(ptr);
  }
  ///Determines what season this species will be spawnable in
  public int getSeason()
  {
    validify();
    return Client.INSTANCE.speciesGetSeason(ptr);
  }

}
