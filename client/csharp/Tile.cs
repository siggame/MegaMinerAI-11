using System;
using System.Runtime.InteropServices;


///Represents a single tile on the map, can contain some amount of trash or be a cove (spawn point).
public class Tile: Mappable
{

  public Tile()
  {
  }

  public Tile(IntPtr p)
  {
    ptr = p;
    ID = Client.tileGetId(ptr);
    iteration = BaseAI.iteration;
  }

  public override bool validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.tiles.Length; i++)
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
  public new int Id
  {
    get
    {
      validify();
      int value = Client.tileGetId(ptr);
      return value;
    }
  }

  ///X position of the object
  public new int X
  {
    get
    {
      validify();
      int value = Client.tileGetX(ptr);
      return value;
    }
  }

  ///Y position of the object
  public new int Y
  {
    get
    {
      validify();
      int value = Client.tileGetY(ptr);
      return value;
    }
  }

  ///The amount of trash on this tile
  public int TrashAmount
  {
    get
    {
      validify();
      int value = Client.tileGetTrashAmount(ptr);
      return value;
    }
  }

  ///The owner of the tile if it is part of a cove
  public int Owner
  {
    get
    {
      validify();
      int value = Client.tileGetOwner(ptr);
      return value;
    }
  }

}

