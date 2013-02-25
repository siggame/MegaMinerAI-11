import com.sun.jna.Pointer;

/// \brief A basic AI interface.

///This class implements most the code an AI would need to interface with the lower-level game code.
///AIs should extend this class to get a lot of builer-plate code out of the way
///The provided AI class does just that.
public abstract class BaseAI
{
  static Mappable[] mappables;
  static FishSpecies[] fishSpeciess;
  static Tile[] tiles;
  static Fish[] fishs;
  static Player[] players;
  Pointer connection;
  static int iteration;
  boolean initialized;

  public BaseAI(Pointer c)
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
  public abstract boolean run();

  ///
  ///This is run on after your last turn.
  public abstract void end();


  public boolean startTurn()
  {
    iteration++;
    int count = 0;
    count = Client.INSTANCE.getMappableCount(connection);
    mappables = new Mappable[count];
    for(int i = 0; i < count; i++)
    {
      mappables[i] = new Mappable(Client.INSTANCE.getMappable(connection, i));
    }
    count = Client.INSTANCE.getFishSpeciesCount(connection);
    fishSpeciess = new FishSpecies[count];
    for(int i = 0; i < count; i++)
    {
      fishSpeciess[i] = new FishSpecies(Client.INSTANCE.getFishSpecies(connection, i));
    }
    count = Client.INSTANCE.getTileCount(connection);
    tiles = new Tile[count];
    for(int i = 0; i < count; i++)
    {
      tiles[i] = new Tile(Client.INSTANCE.getTile(connection, i));
    }
    count = Client.INSTANCE.getFishCount(connection);
    fishs = new Fish[count];
    for(int i = 0; i < count; i++)
    {
      fishs[i] = new Fish(Client.INSTANCE.getFish(connection, i));
    }
    count = Client.INSTANCE.getPlayerCount(connection);
    players = new Player[count];
    for(int i = 0; i < count; i++)
    {
      players[i] = new Player(Client.INSTANCE.getPlayer(connection, i));
    }

    if(!initialized)
    {
      initialized = true;
      init();
    }
    return run();
  }


  ///How much spawn food a player starts the game with
  int initialFood()
  {
    return Client.INSTANCE.getInitialFood(connection);
  }
  ///The lower x-value of the shared zone
  int sharedLowerBound()
  {
    return Client.INSTANCE.getSharedLowerBound(connection);
  }
  ///The upper x-value of the shared zone
  int sharedUpperBound()
  {
    return Client.INSTANCE.getSharedUpperBound(connection);
  }
  ///How much spawn food a player receives each turn
  int spawnFoodPerTurn()
  {
    return Client.INSTANCE.getSpawnFoodPerTurn(connection);
  }
  ///How many turns it has been since the beginning of the game
  int turnNumber()
  {
    return Client.INSTANCE.getTurnNumber(connection);
  }
  ///Player Number; either 0 or 1
  int playerID()
  {
    return Client.INSTANCE.getPlayerID(connection);
  }
  ///What number game this is for the server
  int gameNumber()
  {
    return Client.INSTANCE.getGameNumber(connection);
  }
  ///Turns until you can spawn new fish
  int turnsTillSpawn()
  {
    return Client.INSTANCE.getTurnsTillSpawn(connection);
  }
  ///How much health a reef has initially
  int maxReefHealth()
  {
    return Client.INSTANCE.getMaxReefHealth(connection);
  }
  ///How much damage trash does
  int trashDamage()
  {
    return Client.INSTANCE.getTrashDamage(connection);
  }
  ///How wide the map is
  int mapWidth()
  {
    return Client.INSTANCE.getMapWidth(connection);
  }
  ///How high the map is
  int mapHeight()
  {
    return Client.INSTANCE.getMapHeight(connection);
  }
  ///Amount of trash in the game
  int trashAmount()
  {
    return Client.INSTANCE.getTrashAmount(connection);
  }
  ///X bound for the cove
  int coveX()
  {
    return Client.INSTANCE.getCoveX(connection);
  }
  ///Y bound for the cove
  int coveY()
  {
    return Client.INSTANCE.getCoveY(connection);
  }
}
