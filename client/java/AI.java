import com.sun.jna.Pointer;



///The class implementing gameplay logic.
public class AI extends BaseAI
{
  public static final int SEA_STAR=0, SPONGE=1, ANGELFISH=2, CONESHELL_SNAIL=3, SEA_URCHIN=4, OCTOPUS=5, TOMCOD=6, REEF_SHARK=7, CUTTLEFISH=8, CLEANER_SHRIMP=9, ELECTRIC_EEL=10, JELLYFISH=11;

  public String username()
  {
    return "Shell AI";
  }
  public String password()
  {
    return "password";
  }

  //This function is called each time it is your turn
  //Return true to end your turn, return false to ask the server for updated information
  public boolean run()
  {
    return true;
  }


  //This function is called once, before your first turn
  public void init() {}

  //This function is called once, after your last turn
  public void end() {}
  
  
  public AI(Pointer c)
  {
    super(c);
  }
}
