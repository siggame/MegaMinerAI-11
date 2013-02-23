using System;
using System.Runtime.InteropServices;

/// \brief A basic AI interface.

///This class implements most the code an AI would need to interface with the lower-level game code.
///AIs should extend this class to get a lot of builer-plate code out of the way
///The provided AI class does just that.
public abstract class BaseAI
{
  public static Mappable[] mappables;
  public static FishSpecies[] fishSpeciess;
  public static Tile[] tiles;
  public static Fish[] fishs;
  public static Player[] players;
  IntPtr connection;
  public static int iteration;
  bool initialized;

  public BaseAI(IntPtr c)
  {
    connection = c;
  }

  ///
  ///Make this your username, which should be provided.
  public abstract String username();
  ///
  ///Make this your password, which should be provided.
  public abstract String password();
  ///
  ///This is run on turn 1 before run
  public abstract void init();
  ///
  ///This is run every turn . Return true to end the turn, return false
  ///to request a status update from the server and then immediately rerun this function with the
  ///latest game status.
  public abstract bool run();

  ///
  ///This is run on after your last turn.
  public abstract void end();


  public bool startTurn()
  {
    iteration++;
    int count = 0;
    count = Client.getMappableCount(connection);
    mappables = new Mappable[count];
    for(int i = 0; i < count; i++)
    {
      mappables[i] = new Mappable(Client.getMappable(connection, i));
    }
    count = Client.getFishSpeciesCount(connection);
    fishSpeciess = new FishSpecies[count];
    for(int i = 0; i < count; i++)
    {
      fishSpeciess[i] = new FishSpecies(Client.getFishSpecies(connection, i));
    }
    count = Client.getTileCount(connection);
    tiles = new Tile[count];
    for(int i = 0; i < count; i++)
    {
      tiles[i] = new Tile(Client.getTile(connection, i));
    }
    count = Client.getFishCount(connection);
    fishs = new Fish[count];
    for(int i = 0; i < count; i++)
    {
      fishs[i] = new Fish(Client.getFish(connection, i));
    }
    count = Client.getPlayerCount(connection);
    players = new Player[count];
    for(int i = 0; i < count; i++)
    {
      players[i] = new Player(Client.getPlayer(connection, i));
    }

    if(!initialized)
    {
      initialized = true;
      init();
    }
    return run();
  }


  ///How much spawn food a player receives each turn
  public int spawnFoodPerTurn()
  {
    int value = Client.getSpawnFoodPerTurn(connection);
    return value;
  }
  ///How many turns it has been since the beginning of the game
  public int turnNumber()
  {
    int value = Client.getTurnNumber(connection);
    return value;
  }
  ///Player Number; either 0 or 1
  public int playerID()
  {
    int value = Client.getPlayerID(connection);
    return value;
  }
  ///What number game this is for the server
  public int gameNumber()
  {
    int value = Client.getGameNumber(connection);
    return value;
  }
  ///Turns until you can spawn new fish
  public int turnsTillSpawn()
  {
    int value = Client.getTurnsTillSpawn(connection);
    return value;
  }
  ///How much health a reef has initially
  public int maxReefHealth()
  {
    int value = Client.getMaxReefHealth(connection);
    return value;
  }
  ///How much damage trash does
  public int trashDamage()
  {
    int value = Client.getTrashDamage(connection);
    return value;
  }
  ///How wide the map is
  public int mapWidth()
  {
    int value = Client.getMapWidth(connection);
    return value;
  }
  ///How high the map is
  public int mapHeight()
  {
    int value = Client.getMapHeight(connection);
    return value;
  }
  ///amount of trash in the game
  public int trashAmount()
  {
    int value = Client.getTrashAmount(connection);
    return value;
  }
}
