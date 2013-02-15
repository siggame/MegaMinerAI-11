import com.sun.jna.Library;
import com.sun.jna.Pointer;
import com.sun.jna.Native;

public interface Client extends Library {
  Client INSTANCE = (Client)Native.loadLibrary("client", Client.class);
  Pointer createConnection();
  boolean serverConnect(Pointer connection, String host, String port);

  boolean serverLogin(Pointer connection, String username, String password);
  int createGame(Pointer connection);
  int joinGame(Pointer connection, int id, String playerType);

  void endTurn(Pointer connection);
  void getStatus(Pointer connection);

  int networkLoop(Pointer connection);


    //commands
  int fishMove(Pointer object, int x, int y);
  int fishPickUp(Pointer object, int x, int y, int weight);
  int fishDrop(Pointer object, int x, int y, int weight);
  int fishAttack(Pointer object, int x, int y);
  int playerTalk(Pointer object, String message);

    //accessors
  int getDollarsPerTurn(Pointer connection);
  int getTurnNumber(Pointer connection);
  int getPlayerID(Pointer connection);
  int getGameNumber(Pointer connection);
  int getTurnsTillSpawn(Pointer connection);
  int getMaxReefHealth(Pointer connection);
  int getTrashDamage(Pointer connection);
  int getMapWidth(Pointer connection);
  int getMapHeight(Pointer connection);

  Pointer getMappable(Pointer connection, int num);
  int getMappableCount(Pointer connection);
  Pointer getTrash(Pointer connection, int num);
  int getTrashCount(Pointer connection);
  Pointer getFish(Pointer connection, int num);
  int getFishCount(Pointer connection);
  Pointer getPlayer(Pointer connection, int num);
  int getPlayerCount(Pointer connection);


    //getters
  int mappableGetId(Pointer ptr);
  int mappableGetX(Pointer ptr);
  int mappableGetY(Pointer ptr);

  int trashGetId(Pointer ptr);
  int trashGetX(Pointer ptr);
  int trashGetY(Pointer ptr);
  int trashGetWeight(Pointer ptr);

  int fishGetId(Pointer ptr);
  int fishGetX(Pointer ptr);
  int fishGetY(Pointer ptr);
  int fishGetOwner(Pointer ptr);
  String fishGetSpecies(Pointer ptr);
  int fishGetMaxHealth(Pointer ptr);
  int fishGetCurHealth(Pointer ptr);
  int fishGetMaxMoves(Pointer ptr);
  int fishGetMovementLeft(Pointer ptr);
  int fishGetCarryCap(Pointer ptr);
  int fishGetCarryWeight(Pointer ptr);
  int fishGetAttackPower(Pointer ptr);
  int fishGetIsVisible(Pointer ptr);
  int fishGetAttacksLeft(Pointer ptr);

  int playerGetId(Pointer ptr);
  String playerGetPlayerName(Pointer ptr);
  float playerGetTime(Pointer ptr);
  int playerGetCurReefHealth(Pointer ptr);
  int playerGetSandDollars(Pointer ptr);


    //properties

}
