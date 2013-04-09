import com.sun.jna.Pointer;

///This is your primary unit for Reef. It will perform all of your major actions (pickup, attack, move, drop). It stats are based off of its species
class Fish extends Mappable
{
  public Fish(Pointer p)
  {
    super(p);
  }
  boolean validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.fishes.length; i++)
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
  boolean move(int x, int y)
  {
    validify();
    return (Client.INSTANCE.fishMove(ptr, x, y) == 0) ? false : true;
  }
  ///Command a fish to pick up some trash at a specified position
  boolean pickUp(int x, int y, int weight)
  {
    validify();
    return (Client.INSTANCE.fishPickUp(ptr, x, y, weight) == 0) ? false : true;
  }
  ///Command a fish to drop some trash at a specified position
  boolean drop(int x, int y, int weight)
  {
    validify();
    return (Client.INSTANCE.fishDrop(ptr, x, y, weight) == 0) ? false : true;
  }
  ///Command a fish to attack a target
  boolean attack(Fish target)
  {
    validify();
    target.validify();
    return (Client.INSTANCE.fishAttack(ptr, target.ptr) == 0) ? false : true;
  }

    //getters

  ///Unique Identifier
  public int getId()
  {
    validify();
    return Client.INSTANCE.fishGetId(ptr);
  }
  ///X position of the object
  public int getX()
  {
    validify();
    return Client.INSTANCE.fishGetX(ptr);
  }
  ///Y position of the object
  public int getY()
  {
    validify();
    return Client.INSTANCE.fishGetY(ptr);
  }
  ///The owner of this fish
  public int getOwner()
  {
    validify();
    return Client.INSTANCE.fishGetOwner(ptr);
  }
  ///The maximum health of the fish
  public int getMaxHealth()
  {
    validify();
    return Client.INSTANCE.fishGetMaxHealth(ptr);
  }
  ///The current health of the fish
  public int getCurrentHealth()
  {
    validify();
    return Client.INSTANCE.fishGetCurrentHealth(ptr);
  }
  ///The maximum number of movements in a turn
  public int getMaxMovement()
  {
    validify();
    return Client.INSTANCE.fishGetMaxMovement(ptr);
  }
  ///The number of movements left
  public int getMovementLeft()
  {
    validify();
    return Client.INSTANCE.fishGetMovementLeft(ptr);
  }
  ///The total weight the fish can carry
  public int getCarryCap()
  {
    validify();
    return Client.INSTANCE.fishGetCarryCap(ptr);
  }
  ///The current amount of weight the fish is carrying
  public int getCarryingWeight()
  {
    validify();
    return Client.INSTANCE.fishGetCarryingWeight(ptr);
  }
  ///The power of the fish's attack
  public int getAttackPower()
  {
    validify();
    return Client.INSTANCE.fishGetAttackPower(ptr);
  }
  ///The visibleness of the fish
  public int getIsVisible()
  {
    validify();
    return Client.INSTANCE.fishGetIsVisible(ptr);
  }
  ///The maximum number of attacks this fish has per turn
  public int getMaxAttacks()
  {
    validify();
    return Client.INSTANCE.fishGetMaxAttacks(ptr);
  }
  ///The number of attacks a fish has left
  public int getAttacksLeft()
  {
    validify();
    return Client.INSTANCE.fishGetAttacksLeft(ptr);
  }
  ///The attack range of the fish
  public int getRange()
  {
    validify();
    return Client.INSTANCE.fishGetRange(ptr);
  }
  ///The index of the fish species.
  public int getSpecies()
  {
    validify();
    return Client.INSTANCE.fishGetSpecies(ptr);
  }

}
