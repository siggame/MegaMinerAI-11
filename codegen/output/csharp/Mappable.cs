using System;
using System.Runtime.InteropServices;


///A mappable object!
public class Mappable
{
  public IntPtr ptr;
  protected int ID;
  protected int iteration;

  public Mappable()
  {
  }

  public Mappable(IntPtr p)
  {
    ptr = p;
    ID = Client.mappableGetId(ptr);
    iteration = BaseAI.iteration;
  }

  public bool validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.mappables.Length; i++)
    {
      if(BaseAI.mappables[i].ID == ID)
      {
        ptr = BaseAI.mappables[i].ptr;
        iteration = BaseAI.iteration;
        return true;
      }
    }
    throw new ExistentialError();
  }

    //commands


    //getters


  ///Unique Identifier
  public int Id
  {
    get
    {
      validify();
      int value = Client.mappableGetId(ptr);
      return value;
    }
  }

  ///X position of the object
  public int X
  {
    get
    {
      validify();
      int value = Client.mappableGetX(ptr);
      return value;
    }
  }

  ///Y position of the object
  public int Y
  {
    get
    {
      validify();
      int value = Client.mappableGetY(ptr);
      return value;
    }
  }

}

