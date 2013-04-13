using System;
using System.Runtime.InteropServices;


///This class describes the characteristics for each type of fish. A species will only be available for so long, and new species will become available as a match progreses. 
public class Species
{
  public IntPtr ptr;
  protected int ID;
  protected int iteration;

  public Species()
  {
  }

  public Species(IntPtr p)
  {
    ptr = p;
    ID = Client.speciesGetId(ptr);
    iteration = BaseAI.iteration;
  }

  public bool validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.speciesList.Length; i++)
    {
      if(BaseAI.speciesList[i].ID == ID)
      {
        ptr = BaseAI.speciesList[i].ptr;
        iteration = BaseAI.iteration;
        return true;
      }
    }
    throw new ExistentialError();
  }

    //commands

  ///Have a new fish spawn and join the fight! Select which tile you want the fish to spawn on
  public bool spawn(Tile tile)
  {
    validify();
    tile.validify();
    return (Client.speciesSpawn(ptr, tile.ptr) == 0) ? false : true;
  }

    //getters


  ///Unique Identifier
  public int Id
  {
    get
    {
      validify();
      int value = Client.speciesGetId(ptr);
      return value;
    }
  }

  ///The name of this species
  public string Name
  {
    get
    {
      validify();
      IntPtr value = Client.speciesGetName(ptr);
      return Marshal.PtrToStringAuto(value);
    }
  }

  ///The number assigned to the species, unique to each.
  public int SpeciesNum
  {
    get
    {
      validify();
      int value = Client.speciesGetSpeciesNum(ptr);
      return value;
    }
  }

  ///The amount of food it takes to raise this fish
  public int Cost
  {
    get
    {
      validify();
      int value = Client.speciesGetCost(ptr);
      return value;
    }
  }

  ///The maximum health of this fish
  public int MaxHealth
  {
    get
    {
      validify();
      int value = Client.speciesGetMaxHealth(ptr);
      return value;
    }
  }

  ///The maximum number of movements in a turn
  public int MaxMovement
  {
    get
    {
      validify();
      int value = Client.speciesGetMaxMovement(ptr);
      return value;
    }
  }

  ///The total weight the fish can carry
  public int CarryCap
  {
    get
    {
      validify();
      int value = Client.speciesGetCarryCap(ptr);
      return value;
    }
  }

  ///The power of the fish's attack
  public int AttackPower
  {
    get
    {
      validify();
      int value = Client.speciesGetAttackPower(ptr);
      return value;
    }
  }

  ///The attack range of the fish
  public int Range
  {
    get
    {
      validify();
      int value = Client.speciesGetRange(ptr);
      return value;
    }
  }

  ///Maximum number of times this unit can attack per turn
  public int MaxAttacks
  {
    get
    {
      validify();
      int value = Client.speciesGetMaxAttacks(ptr);
      return value;
    }
  }

  ///Determines what season this species will be spawnable in
  public int Season
  {
    get
    {
      validify();
      int value = Client.speciesGetSeason(ptr);
      return value;
    }
  }

}

