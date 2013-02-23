using System;
using System.Runtime.InteropServices;


///
public class FishSpecies
{
  public IntPtr ptr;
  protected int ID;
  protected int iteration;

  public FishSpecies()
  {
  }

  public FishSpecies(IntPtr p)
  {
    ptr = p;
    ID = Client.fishSpeciesGetId(ptr);
    iteration = BaseAI.iteration;
  }

  public bool validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.fishSpeciess.Length; i++)
    {
      if(BaseAI.fishSpeciess[i].ID == ID)
      {
        ptr = BaseAI.fishSpeciess[i].ptr;
        iteration = BaseAI.iteration;
        return true;
      }
    }
    throw new ExistentialError();
  }

    //commands

  ///Have a new fish spawn and join the fight!
  public bool spawn(int x, int y)
  {
    validify();
    return (Client.fishSpeciesSpawn(ptr, x, y) == 0) ? false : true;
  }

    //getters


  ///Unique Identifier
  public int Id
  {
    get
    {
      validify();
      int value = Client.fishSpeciesGetId(ptr);
      return value;
    }
  }

  ///The fish species
  public string Species
  {
    get
    {
      validify();
      IntPtr value = Client.fishSpeciesGetSpecies(ptr);
      return Marshal.PtrToStringAuto(value);
    }
  }

  ///The amount of food it takes to raise this fish
  public int Cost
  {
    get
    {
      validify();
      int value = Client.fishSpeciesGetCost(ptr);
      return value;
    }
  }

  ///The maximum health of this fish
  public int MaxHealth
  {
    get
    {
      validify();
      int value = Client.fishSpeciesGetMaxHealth(ptr);
      return value;
    }
  }

  ///The maximum number of movements in a turn
  public int MaxMovement
  {
    get
    {
      validify();
      int value = Client.fishSpeciesGetMaxMovement(ptr);
      return value;
    }
  }

  ///The total weight the fish can carry
  public int CarryCap
  {
    get
    {
      validify();
      int value = Client.fishSpeciesGetCarryCap(ptr);
      return value;
    }
  }

  ///The power of the fish's attack
  public int AttackPower
  {
    get
    {
      validify();
      int value = Client.fishSpeciesGetAttackPower(ptr);
      return value;
    }
  }

  ///The attack arrange of the fish
  public int Range
  {
    get
    {
      validify();
      int value = Client.fishSpeciesGetRange(ptr);
      return value;
    }
  }

  ///Maximum number of times this unit can attack per turn
  public int MaxAttacks
  {
    get
    {
      validify();
      int value = Client.fishSpeciesGetMaxAttacks(ptr);
      return value;
    }
  }

  ///If this species is able to use stealth
  public int CanStealth
  {
    get
    {
      validify();
      int value = Client.fishSpeciesGetCanStealth(ptr);
      return value;
    }
  }

  ///How many turns until you can spawn this fish species
  public int TurnsTillAvailalbe
  {
    get
    {
      validify();
      int value = Client.fishSpeciesGetTurnsTillAvailalbe(ptr);
      return value;
    }
  }

  ///How many turns until you can no longer spawn this fish species
  public int TurnsTillUnavailable
  {
    get
    {
      validify();
      int value = Client.fishSpeciesGetTurnsTillUnavailable(ptr);
      return value;
    }
  }

}

