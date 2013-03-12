import com.sun.jna.Pointer;

///A mappable object!
class Mappable
{
  Pointer ptr;
  int ID;
  int iteration;
  public Mappable(Pointer p)
  {
    ptr = p;
    ID = Client.INSTANCE.mappableGetId(ptr);
    iteration = BaseAI.iteration;
  }
  boolean validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.mappables.length; i++)
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
  public int getId()
  {
    validify();
    return Client.INSTANCE.mappableGetId(ptr);
  }
  ///X position of the object
  public int getX()
  {
    validify();
    return Client.INSTANCE.mappableGetX(ptr);
  }
  ///Y position of the object
  public int getY()
  {
    validify();
    return Client.INSTANCE.mappableGetY(ptr);
  }

}
