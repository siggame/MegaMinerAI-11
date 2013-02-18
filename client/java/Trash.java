import com.sun.jna.Pointer;

///This is a Trash object
class Trash extends Mappable
{
  public Trash(Pointer p)
  {
    super(p);
  }
  boolean validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.trashs.length; i++)
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
  public int getId()
  {
    validify();
    return Client.INSTANCE.trashGetId(ptr);
  }
  ///X position of the object
  public int getX()
  {
    validify();
    return Client.INSTANCE.trashGetX(ptr);
  }
  ///Y position of the object
  public int getY()
  {
    validify();
    return Client.INSTANCE.trashGetY(ptr);
  }
  ///The weight of the trash
  public int getWeight()
  {
    validify();
    return Client.INSTANCE.trashGetWeight(ptr);
  }

}
