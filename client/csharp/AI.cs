using System;
using System.Linq;

/// The class implementing gameplay logic.
class AI : BaseAI
{
    enum speciesIndex
    { 
        SEA_STAR,
        SPONGE,
        ANGELFISH,
        CONESHELL_SNAIL,
        SEA_URCHIN,
        OCTOPUS,
        TOMCOD,
        REEF_SHARK,
        CUTTLEFISH,
        CLEANER_SHRIMP,
        ELECTRIC_EEL,
        JELLYFISH
    };

    public override string username()
    {
        return "Shell AI";
    }
    public override string password()
    {
        return "password";
    }

    // This function is called each time it's your turn.
    // Return true to end your turn, return false to ask the server for updated information
    public override bool run()
    {
        // Test player.talk().
        players[playerID()].talk("Help, I'm trapped inside the codegen!");

        // Iterate across all tiles.
        foreach (Tile tile in tiles)
        {
            // If the tile is yours, is not spawning a fish, and has no fish on it...
            if (tile.Owner == playerID() && tile.HasEgg == 0 && fishes.Count(f => f.X == tile.X && f.Y == tile.Y) == 0)
            {
                // ...iterate across all species.
                for (int i = 0; i < speciesList.Length; i++)
                {
                    // If the species is in season and we can afford it...
                    if (speciesList[i].Season == currentSeason() && players[playerID()].SpawnFood >= speciesList[i].Cost)
                    {
                        // Spawn it and break (can't spawn multiple fish on the same cove).
                        speciesList[i].spawn(getTile(tile.X, tile.Y));
                        break;
                    }
                }
            }
        }

        // Iterate across all the fishes.
        foreach (Fish fish in fishes)
        {
            // Only attempt to move fish I own.
            if (fish.Owner == playerID())
            {
                // Try to move to the right.
                if (fish.X + 1 < mapWidth()                                         // We aren't moving off the map
                    && getTile(fish.X + 1, fish.Y).Owner != 1 - playerID()          // We aren't moving onto an enemy cove
                    && getTile(fish.X + 1, fish.Y).HasEgg == 0                      // We aren't moving onto an egg
                    && fishes.Count(f => f.X == fish.X + 1 && f.Y == fish.Y) == 0   // There is no fish at that spot
                    && getTile(fish.X + 1, fish.Y).TrashAmount == 0                 // There is no trash on the tile
                    && fish.MovementLeft > 0)                                       // We have moves left
                {
                    fish.move(fish.X + 1, fish.Y);
                }

                // Try to pick up trash
                if (fish.Y + 1 < mapHeight()                            // Ensure we do not pick up off the map
                    && fish.CarryCap - fish.CarryingWeight > 0          // Ensure we have the necessary weight
                    && fish.CurrentHealth >= 1                          // Ensure we have enough health
                    && getTile(fish.X, fish.Y + 1).TrashAmount > 0)     // Ensure the tile has trash
                {
                    fish.pickUp(getTile(fish.X, fish.Y + 1), 1);
                }

                // Drop some trash
                if (fish.Y - 1 >= 0                                                 // Ensure we don't drop off the map
                    && fishes.Count(f => f.X == fish.X && f.Y == fish.Y - 1) == 0   // Make sure there's no fish where we intend to drop
                    && fish.CarryingWeight > 0)                                     // Ensure we have something to drop
                {
                    fish.drop(getTile(fish.X, fish.Y - 1), 1);
                }

                // Try to attack to the right
                if (fish.X + 1 < mapWidth()                                                     	// We aren't attacking off the map
                    && fishes.Count(f => f.X == fish.X + 1 && f.Y == fish.Y) > 0                    // There is a fish at that spot
                    && fishes.First(f => f.X == fish.X + 1 && f.Y == fish.Y).Owner != playerID()    // Then that fish belongs to the bad guy
                    && fish.AttacksLeft > 0)                                                    	// We have attacks left
                {
                    fish.attack(fishes.First(f => f.X == fish.X + 1 && f.Y == fish.Y));             // We can attack the tile to the right!
                }
            }
        }

        return true;
    }

    // This function is called once, before your first turn
    public override void init() { }

    // This function is called once, after your last turn
    public override void end() { }

    public AI(IntPtr c) : base(c) { }

    #region Helper Methods
    // Returns the Tile from the specified x and y coordinates.
    Tile getTile(int x, int y)
    {
        if (x < 0 || y < 0 || x > mapWidth() || y > mapHeight())
            throw new ArgumentException(String.Format("There is no tile at ({0}, {1}).", x, y));

        return tiles[(mapHeight() * x) + y];
    }
    #endregion
}