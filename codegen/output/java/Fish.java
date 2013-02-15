import com.sun.jna.Pointer;

///
class Fish extends Mappable
{
  public Fish(Pointer p)
  {
    super(p);
  }
  boolean validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.fishs.length; i++)
    {
      if(BaseAI.fishs[i].ID == ID)
      {
        ptr = BaseAI.fishs[i].ptr;
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
  ///Command a fish to attack another fish at a specified position
  boolean attack(int x, int y)
  {
    validify();
    return (Client.INSTANCE.fishAttack(ptr, x, y) == 0) ? false : true;
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
  ///The type/species of the fish
  public String getSpecies()
  {
    validify();
    return Client.INSTANCE.fishGetSpecies(ptr);
  }
  ///The maximum health of the fish
  public int getMaxHealth()
  {
    validify();
    return Client.INSTANCE.fishGetMaxHealth(ptr);
  }
  ///The current health of the fish
  public int getCurHealth()
  {
    validify();
    return Client.INSTANCE.fishGetCurHealth(ptr);
  }
  ///The maximum number of movements in a turn
  public int getMaxMoves()
  {
    validify();
    return Client.INSTANCE.fishGetMaxMoves(ptr);
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
  public int getCarryWeight()
  {
    validify();
    return Client.INSTANCE.fishGetCarryWeight(ptr);
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
  ///The number of attacks a fish has left
  public int getAttacksLeft()
  {
    validify();
    return Client.INSTANCE.fishGetAttacksLeft(ptr);
  }

}
