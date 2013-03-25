using System;
using System.Runtime.InteropServices;


///This is your primary unit for Reef. It will perform all of your major actions (pickup, attack, move, drop). It stats are based off of its species
public class Fish: Mappable
{

  public Fish()
  {
  }

  public Fish(IntPtr p)
  {
    ptr = p;
    ID = Client.fishGetId(ptr);
    iteration = BaseAI.iteration;
  }

  public override bool validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.fishes.Length; i++)
    {
      if(BaseAI.fishes[i].ID == ID)
      {
        ptr = BaseAI.fishes[i].ptr;
        iteration = BaseAI.iteration;
        return true;
      }
    }
    throw new ExistentialError();
  }

    //commands

  ///Command a fish to move to a specified position
  public bool move(int x, int y)
  {
    validify();
    return (Client.fishMove(ptr, x, y) == 0) ? false : true;
  }
  ///Command a fish to pick up some trash at a specified position
  public bool pickUp(int x, int y, int weight)
  {
    validify();
    return (Client.fishPickUp(ptr, x, y, weight) == 0) ? false : true;
  }
  ///Command a fish to drop some trash at a specified position
  public bool drop(int x, int y, int weight)
  {
    validify();
    return (Client.fishDrop(ptr, x, y, weight) == 0) ? false : true;
  }
  ///Command a fish to attack a target
  public bool attack(Fish target)
  {
    validify();
    target.validify();
    return (Client.fishAttack(ptr, target.ptr) == 0) ? false : true;
  }

    //getters


  ///Unique Identifier
  public new int Id
  {
    get
    {
      validify();
      int value = Client.fishGetId(ptr);
      return value;
    }
  }

  ///X position of the object
  public new int X
  {
    get
    {
      validify();
      int value = Client.fishGetX(ptr);
      return value;
    }
  }

  ///Y position of the object
  public new int Y
  {
    get
    {
      validify();
      int value = Client.fishGetY(ptr);
      return value;
    }
  }

  ///The owner of this fish
  public int Owner
  {
    get
    {
      validify();
      int value = Client.fishGetOwner(ptr);
      return value;
    }
  }

  ///The maximum health of the fish
  public int MaxHealth
  {
    get
    {
      validify();
      int value = Client.fishGetMaxHealth(ptr);
      return value;
    }
  }

  ///The current health of the fish
  public int CurrentHealth
  {
    get
    {
      validify();
      int value = Client.fishGetCurrentHealth(ptr);
      return value;
    }
  }

  ///The maximum number of movements in a turn
  public int MaxMovement
  {
    get
    {
      validify();
      int value = Client.fishGetMaxMovement(ptr);
      return value;
    }
  }

  ///The number of movements left
  public int MovementLeft
  {
    get
    {
      validify();
      int value = Client.fishGetMovementLeft(ptr);
      return value;
    }
  }

  ///The total weight the fish can carry
  public int CarryCap
  {
    get
    {
      validify();
      int value = Client.fishGetCarryCap(ptr);
      return value;
    }
  }

  ///The current amount of weight the fish is carrying
  public int CarryingWeight
  {
    get
    {
      validify();
      int value = Client.fishGetCarryingWeight(ptr);
      return value;
    }
  }

  ///The power of the fish's attack
  public int AttackPower
  {
    get
    {
      validify();
      int value = Client.fishGetAttackPower(ptr);
      return value;
    }
  }

  ///The visibleness of the fish
  public int IsVisible
  {
    get
    {
      validify();
      int value = Client.fishGetIsVisible(ptr);
      return value;
    }
  }

  ///The maximum number of attacks this fish has per turn
  public int MaxAttacks
  {
    get
    {
      validify();
      int value = Client.fishGetMaxAttacks(ptr);
      return value;
    }
  }

  ///The number of attacks a fish has left
  public int AttacksLeft
  {
    get
    {
      validify();
      int value = Client.fishGetAttacksLeft(ptr);
      return value;
    }
  }

  ///The attack range of the fish
  public int Range
  {
    get
    {
      validify();
      int value = Client.fishGetRange(ptr);
      return value;
    }
  }

  ///The fish species
  public string Species
  {
    get
    {
      validify();
      IntPtr value = Client.fishGetSpecies(ptr);
      return Marshal.PtrToStringAuto(value);
    }
  }

}

