using System;
using System.Runtime.InteropServices;


///This is a Trash object
public class Trash: Mappable
{

  public Trash()
  {
  }

  public Trash(IntPtr p)
  {
    ptr = p;
    ID = Client.trashGetId(ptr);
    iteration = BaseAI.iteration;
  }

  public override bool validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.trashs.Length; i++)
    {
      if(BaseAI.trashs[i].ID == ID)
      {
        ptr = BaseAI.trashs[i].ptr;
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
      int value = Client.trashGetId(ptr);
      return value;
    }
  }

  ///X position of the object
  public new int X
  {
    get
    {
      validify();
      int value = Client.trashGetX(ptr);
      return value;
    }
  }

  ///Y position of the object
  public new int Y
  {
    get
    {
      validify();
      int value = Client.trashGetY(ptr);
      return value;
    }
  }

  ///The weight of the trash
  public int Weight
  {
    get
    {
      validify();
      int value = Client.trashGetWeight(ptr);
      return value;
    }
  }

}

