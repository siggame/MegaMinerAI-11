using System;
using System.Linq;

/// <summary>
/// Extends BaseAI with AI gameplay logic.
/// </summary>
class AI : BaseAI
{
    /// <summary>
    /// Specifies the species available.
    /// </summary>
    enum SpeciesIndex
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

    /// <summary>
    /// Returns your username.
    /// </summary>
    /// <remarks></remarks>
    /// <returns>Your username.</returns>
    public override string username()
    {
        return "Shell AI";
    }

    /// <summary>
    /// Returns your password.
    /// </summary>
    /// <returns>Your password.</returns>
    public override string password()
    {
        return "password";
    }

    /// <summary>
    /// This function is called each time it's your turn.
    /// </summary>
    /// <returns>Return true to end your turn, return false to ask the server for updated information.</returns>
    public override bool run()
    {
        // Test player.talk().
        players[playerID()].talk("Help, I'm trapped inside the codegen!");

        // Iterate across all tiles.
        foreach (Tile tile in tiles)
        {
            // If the tile is yours, is not spawning a fish, and has no fish on it...
            if (tile.Owner == playerID() && tile.HasEgg == 0 && getFish(tile.X, tile.Y) == null)
            {
                // ...iterate across all species.
                for (int i = 0; i < speciesList.Length; i++)
                {
                    // If the species is in season and we can afford it...
                    if (speciesList[i].Season == currentSeason() && players[playerID()].SpawnFood >= speciesList[i].Cost)
                    {
                        // ...spawn it and break (can't spawn multiple fish on the same cove).
                        speciesList[i].spawn(tile);
                        break;
                    }
                }
            }
        }

        // Iterate through all the fishes.
        foreach (Fish fish in fishes)
        {
            // Only attempt to move fish we own.
            if (fish.Owner == playerID())
            {
                // Try to move to the right.
                if (fish.X + 1 < mapWidth()                                 // We aren't moving off the map.
                    && fish.MovementLeft > 0                                // We have moves left.
                    && getFish(fish.X + 1, fish.Y) == null                  // We aren't moving onto another fish.
                    && getTile(fish.X + 1, fish.Y).Owner != 1 - playerID()  // We aren't moving onto an enemy cove.
                    && getTile(fish.X + 1, fish.Y).Owner != 3               // We aren't move onto a wall.
                    && getTile(fish.X + 1, fish.Y).HasEgg == 0              // We aren't moving onto an egg.
                    && getTile(fish.X + 1, fish.Y).TrashAmount == 0)        // We aren't moving onto trash.
                {
                    // Move one tile to the right.
                    fish.move(fish.X + 1, fish.Y);
                }

                // Try to pick up trash one tile below the fish.
                if (fish.Y + 1 < mapHeight()                            // Ensure we do not pick up off the map.
                    && getTile(fish.X, fish.Y + 1).TrashAmount > 0      // Ensure the tile has trash.
                    && fish.CarryCap - fish.CarryingWeight > 0          // Ensure we have the necessary capacity.
                    && fish.CurrentHealth >= 1)                         // Ensure we have enough health.
                {
                    // Pick up trash one tile below the fish.
                    fish.pickUp(getTile(fish.X, fish.Y + 1), 1);
                }

                // Try to drop trash one tile above the fish.
                if (fish.Y - 1 >= 0                             // Ensure we do not drop off the map.
                    && fish.CarryingWeight > 0                  // Ensure we have something to drop.
                    && getFish(fish.X, fish.Y - 1) == null)     // Ensure we don't drop on a fish.
                {
                    // Drop trash one tile above the fish.
                    fish.drop(getTile(fish.X, fish.Y - 1), 1);
                }

                // Try to do an action to the left based on species.
                if (fish.X - 1 > 0                                      // We are not attacking off the map.
                    && fish.AttacksLeft > 0                             // We have attacks left.
                    && getFish(fish.X - 1, fish.Y) != null)             // There is a fish at that spot.
                {
                    // If we're not a cleaner shrimp...
                    if ((SpeciesIndex)fish.Species != SpeciesIndex.CLEANER_SHRIMP)
                    {
                        // Try to attack fish to the left.
                        if (getFish(fish.X - 1, fish.Y).Owner != playerID()) // The fish belongs to the opponent.
                            fish.attack(getFish(fish.X - 1, fish.Y));
                    }
                    else
                    {
                        // Try to heal allied fish to the left.
                        if (getFish(fish.X - 1, fish.Y).Owner == playerID()) // The fish belongs to me.
                            fish.attack(getFish(fish.X - 1, fish.Y));
                    }
                }
            }
        }

        return true;
    }

    /// <summary>
    /// This function is called once, before your first turn.
    /// </summary>
    public override void init() { }

    /// <summary>
    /// This function is called once, after your last turn.
    /// </summary>
    public override void end() { }

    /// <summary>
    /// Initializes a new instance of the AI class connected to the server.
    /// </summary>
    /// <param name="c">The managed pointer to the open connection.</param>
    public AI(IntPtr c) : base(c) { }

    #region Helper Methods
    /// <summary>
    /// Returns the Tile at the specified coordinates.
    /// </summary>
    /// <param name="x">The x coordinate.</param>
    /// <param name="y">The y coordinate.</param>
    /// <returns>The Tile with the specififed coordinates.</returns>
    /// <exception cref="System.ArgumentException">The specified x and y coordinates must be on the map.</exception>
    Tile getTile(int x, int y)
    {
        if (x < 0 || y < 0 || x > mapWidth() || y > mapHeight())
            throw new ArgumentException(String.Format("The specified x and y coordinates ({0}, {1}) must be on the map.", x, y));

        return tiles[(mapHeight() * x) + y];
    }

    /// <summary>
    /// Returns the Fish at the specified coordinates, or null if there is none.
    /// </summary>
    /// <param name="x">The x coordinate.</param>
    /// <param name="y">The y coordinate.</param>
    /// <returns>The Fish at the specified coordinates if there is one; otherwise, null.</returns>
    Fish getFish(int x, int y)
    {
        if(fishes.Count(f => f.X == x && f.Y == y) != 0)
            return fishes.First(f => f.X == x && f.Y == y);

        return null;
    }
    #endregion
}