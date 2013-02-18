using System;
using System.Runtime.InteropServices;

///The class implementing gameplay logic.
class AI : BaseAI
{
  public override string username()
  {
    return "Shell AI";
  }
  public override string password()
  {
    return "password";
  }

  //This function is called each time it is your turn
  //Return true to end your turn, return false to ask the server for updated information
  public override bool run()
  {
    return true;
  }

  //This function is called once, before your first turn
  public override void init() {}

  //This function is called once, after your last turn
  public override void end() {}
  
  
  public AI(IntPtr c) : base(c)
  {}
}
