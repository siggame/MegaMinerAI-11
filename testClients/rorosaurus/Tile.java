import com.sun.jna.Pointer;

///Represents a single tile on the map, can contain some amount of trash or be a cove (spawn point).
class Tile extends Mappable
{
  public Tile(Pointer p)
  {
    super(p);
  }
  boolean validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.tiles.length; i++)
    {
      if(BaseAI.tiles[i].ID == ID)
      {
        ptr = BaseAI.tiles[i].ptr;
        iteration = BaseAI.iteration;
        return true;
      }
    }
    throw new ExistentialError();
  }

    //commands


    //getters

  ///Unique Identifier
  public int getId()
  {
    validify();
    return Client.INSTANCE.tileGetId(ptr);
  }
  ///X position of the object
  public int getX()
  {
    validify();
    return Client.INSTANCE.tileGetX(ptr);
  }
  ///Y position of the object
  public int getY()
  {
    validify();
    return Client.INSTANCE.tileGetY(ptr);
  }
  ///The amount of trash on this tile
  public int getTrashAmount()
  {
    validify();
    return Client.INSTANCE.tileGetTrashAmount(ptr);
  }
  ///The owner of the tile if it is part of a cove
  public int getOwner()
  {
    validify();
    return Client.INSTANCE.tileGetOwner(ptr);
  }
  ///Determines of a fish is set to spawn on this cove
  public int getHasEgg()
  {
    validify();
    return Client.INSTANCE.tileGetHasEgg(ptr);
  }

}
