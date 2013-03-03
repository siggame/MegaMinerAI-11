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
  public static extern int speciesSpawn(IntPtr self, int x, int y);
  [DllImport("client")]
  public static extern int fishMove(IntPtr self, int x, int y);
  [DllImport("client")]
  public static extern int fishPickUp(IntPtr self, int x, int y, int weight);
  [DllImport("client")]
  public static extern int fishDrop(IntPtr self, int x, int y, int weight);
  [DllImport("client")]
  public static extern int fishAttack(IntPtr self, IntPtr target);
  [DllImport("client")]
  public static extern int playerTalk(IntPtr self, string message);

    //accessors
  [DllImport("client")]
  public static extern int getBoundLength(IntPtr connection);
  [DllImport("client")]
  public static extern int getTurnNumber(IntPtr connection);
  [DllImport("client")]
  public static extern int getPlayerID(IntPtr connection);
  [DllImport("client")]
  public static extern int getGameNumber(IntPtr connection);
  [DllImport("client")]
  public static extern int getTrashDamage(IntPtr connection);
  [DllImport("client")]
  public static extern int getMapWidth(IntPtr connection);
  [DllImport("client")]
  public static extern int getMapHeight(IntPtr connection);
  [DllImport("client")]
  public static extern int getTrashAmount(IntPtr connection);
  [DllImport("client")]
  public static extern int getCurrentSeason(IntPtr connection);
  [DllImport("client")]
  public static extern int getSeasonLength(IntPtr connection);
  [DllImport("client")]
  public static extern int getHealPercent(IntPtr connection);

  [DllImport("client")]
  public static extern IntPtr getMappable(IntPtr connection, int num);
  [DllImport("client")]
  public static extern int getMappableCount(IntPtr connection);
  [DllImport("client")]
  public static extern IntPtr getSpecies(IntPtr connection, int num);
  [DllImport("client")]
  public static extern int getSpeciesCount(IntPtr connection);
  [DllImport("client")]
  public static extern IntPtr getTile(IntPtr connection, int num);
  [DllImport("client")]
  public static extern int getTileCount(IntPtr connection);
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
  public static extern int speciesGetId(IntPtr ptr);
  [DllImport("client")]
  public static extern IntPtr speciesGetName(IntPtr ptr);
  [DllImport("client")]
  public static extern int speciesGetCost(IntPtr ptr);
  [DllImport("client")]
  public static extern int speciesGetMaxHealth(IntPtr ptr);
  [DllImport("client")]
  public static extern int speciesGetMaxMovement(IntPtr ptr);
  [DllImport("client")]
  public static extern int speciesGetCarryCap(IntPtr ptr);
  [DllImport("client")]
  public static extern int speciesGetAttackPower(IntPtr ptr);
  [DllImport("client")]
  public static extern int speciesGetRange(IntPtr ptr);
  [DllImport("client")]
  public static extern int speciesGetMaxAttacks(IntPtr ptr);
  [DllImport("client")]
  public static extern int speciesGetSeason(IntPtr ptr);

  [DllImport("client")]
  public static extern int tileGetId(IntPtr ptr);
  [DllImport("client")]
  public static extern int tileGetX(IntPtr ptr);
  [DllImport("client")]
  public static extern int tileGetY(IntPtr ptr);
  [DllImport("client")]
  public static extern int tileGetTrashAmount(IntPtr ptr);
  [DllImport("client")]
  public static extern int tileGetOwner(IntPtr ptr);
  [DllImport("client")]
  public static extern int tileGetHasEgg(IntPtr ptr);

  [DllImport("client")]
  public static extern int fishGetId(IntPtr ptr);
  [DllImport("client")]
  public static extern int fishGetX(IntPtr ptr);
  [DllImport("client")]
  public static extern int fishGetY(IntPtr ptr);
  [DllImport("client")]
  public static extern int fishGetOwner(IntPtr ptr);
  [DllImport("client")]
  public static extern int fishGetMaxHealth(IntPtr ptr);
  [DllImport("client")]
  public static extern int fishGetCurrentHealth(IntPtr ptr);
  [DllImport("client")]
  public static extern int fishGetMaxMovement(IntPtr ptr);
  [DllImport("client")]
  public static extern int fishGetMovementLeft(IntPtr ptr);
  [DllImport("client")]
  public static extern int fishGetCarryCap(IntPtr ptr);
  [DllImport("client")]
  public static extern int fishGetCarryingWeight(IntPtr ptr);
  [DllImport("client")]
  public static extern int fishGetAttackPower(IntPtr ptr);
  [DllImport("client")]
  public static extern int fishGetIsVisible(IntPtr ptr);
  [DllImport("client")]
  public static extern int fishGetMaxAttacks(IntPtr ptr);
  [DllImport("client")]
  public static extern int fishGetAttacksLeft(IntPtr ptr);
  [DllImport("client")]
  public static extern int fishGetRange(IntPtr ptr);
  [DllImport("client")]
  public static extern IntPtr fishGetSpecies(IntPtr ptr);

  [DllImport("client")]
  public static extern int playerGetId(IntPtr ptr);
  [DllImport("client")]
  public static extern IntPtr playerGetPlayerName(IntPtr ptr);
  [DllImport("client")]
  public static extern float playerGetTime(IntPtr ptr);
  [DllImport("client")]
  public static extern int playerGetCurrentReefHealth(IntPtr ptr);
  [DllImport("client")]
  public static extern int playerGetSpawnFood(IntPtr ptr);


    //properties

}
