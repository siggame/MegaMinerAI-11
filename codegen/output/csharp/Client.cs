using System;
using System.Runtime.InteropServices;

public class Client {
  [DllImport("client")]
  public static extern IntPtr createConnection();
  [DllImport("client")]
  public static extern int serverConnect(IntPtr connection, string host, string port);

  [DllImport("client")]
  public static extern int serverLogin(IntPtr connection, string username, string password);
  [DllImport("client")]
  public static extern int createGame(IntPtr connection);
  [DllImport("client")]
  public static extern int joinGame(IntPtr connection, int id, string playerType);

  [DllImport("client")]
  public static extern void endTurn(IntPtr connection);
  [DllImport("client")]
  public static extern void getStatus(IntPtr connection);

  [DllImport("client")]
  public static extern int networkLoop(IntPtr connection);


    //commands
  [DllImport("client")]
  public static extern int fishMove(IntPtr self, int x, int y);
  [DllImport("client")]
  public static extern int fishPickUp(IntPtr self, int x, int y, int weight);
  [DllImport("client")]
  public static extern int fishDrop(IntPtr self, int x, int y, int weight);
  [DllImport("client")]
  public static extern int fishAttack(IntPtr self, int x, int y);
  [DllImport("client")]
  public static extern int playerTalk(IntPtr self, string message);

    //accessors
  [DllImport("client")]
  public static extern int getDollarsPerTurn(IntPtr connection);
  [DllImport("client")]
  public static extern int getTurnNumber(IntPtr connection);
  [DllImport("client")]
  public static extern int getPlayerID(IntPtr connection);
  [DllImport("client")]
  public static extern int getGameNumber(IntPtr connection);
  [DllImport("client")]
  public static extern int getTurnsTillSpawn(IntPtr connection);
  [DllImport("client")]
  public static extern int getMaxReefHealth(IntPtr connection);
  [DllImport("client")]
  public static extern int getTrashDamage(IntPtr connection);
  [DllImport("client")]
  public static extern int getMapWidth(IntPtr connection);
  [DllImport("client")]
  public static extern int getMapHeight(IntPtr connection);

  [DllImport("client")]
  public static extern IntPtr getMappable(IntPtr connection, int num);
  [DllImport("client")]
  public static extern int getMappableCount(IntPtr connection);
  [DllImport("client")]
  public static extern IntPtr getTrash(IntPtr connection, int num);
  [DllImport("client")]
  public static extern int getTrashCount(IntPtr connection);
  [DllImport("client")]
  public static extern IntPtr getFish(IntPtr connection, int num);
  [DllImport("client")]
  public static extern int getFishCount(IntPtr connection);
  [DllImport("client")]
  public static extern IntPtr getPlayer(IntPtr connection, int num);
  [DllImport("client")]
  public static extern int getPlayerCount(IntPtr connection);


    //getters
  [DllImport("client")]
  public static extern int mappableGetId(IntPtr ptr);
  [DllImport("client")]
  public static extern int mappableGetX(IntPtr ptr);
  [DllImport("client")]
  public static extern int mappableGetY(IntPtr ptr);

  [DllImport("client")]
  public static extern int trashGetId(IntPtr ptr);
  [DllImport("client")]
  public static extern int trashGetX(IntPtr ptr);
  [DllImport("client")]
  public static extern int trashGetY(IntPtr ptr);
  [DllImport("client")]
  public static extern int trashGetWeight(IntPtr ptr);

  [DllImport("client")]
  public static extern int fishGetId(IntPtr ptr);
  [DllImport("client")]
  public static extern int fishGetX(IntPtr ptr);
  [DllImport("client")]
  public static extern int fishGetY(IntPtr ptr);
  [DllImport("client")]
  public static extern int fishGetOwner(IntPtr ptr);
  [DllImport("client")]
  public static extern IntPtr fishGetSpecies(IntPtr ptr);
  [DllImport("client")]
  public static extern int fishGetMaxHealth(IntPtr ptr);
  [DllImport("client")]
  public static extern int fishGetCurHealth(IntPtr ptr);
  [DllImport("client")]
  public static extern int fishGetMaxMoves(IntPtr ptr);
  [DllImport("client")]
  public static extern int fishGetMovementLeft(IntPtr ptr);
  [DllImport("client")]
  public static extern int fishGetCarryCap(IntPtr ptr);
  [DllImport("client")]
  public static extern int fishGetCarryWeight(IntPtr ptr);
  [DllImport("client")]
  public static extern int fishGetAttackPower(IntPtr ptr);
  [DllImport("client")]
  public static extern int fishGetIsVisible(IntPtr ptr);
  [DllImport("client")]
  public static extern int fishGetAttacksLeft(IntPtr ptr);

  [DllImport("client")]
  public static extern int playerGetId(IntPtr ptr);
  [DllImport("client")]
  public static extern IntPtr playerGetPlayerName(IntPtr ptr);
  [DllImport("client")]
  public static extern float playerGetTime(IntPtr ptr);
  [DllImport("client")]
  public static extern int playerGetCurReefHealth(IntPtr ptr);
  [DllImport("client")]
  public static extern int playerGetSandDollars(IntPtr ptr);


    //properties

}
