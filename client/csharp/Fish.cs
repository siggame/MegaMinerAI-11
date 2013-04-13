using System;

/// <summary>
/// This is your primary unit for Reef. It will perform all of your major actions (pickup, attack, move, drop). It stats are based off of its species.
/// </summary>
public class Fish : Mappable
{
    /// <summary>
    /// Initializes a default Fish.
    /// </summary>
    public Fish() { }

    /// <summary>
    /// Initializes a Fish from a pointer.
    /// </summary>
    /// <param name="p"></param>
    public Fish(IntPtr p)
    {
        ptr = p;
        ID = Client.fishGetId(ptr);
        iteration = BaseAI.iteration;
    }

    /// <summary>
    /// Validates the object reference.
    /// </summary>
    /// <returns>True if object is valid.</returns>
    /// <exception cref="ExistentialError">The object could not be validified.</exception>
    public override bool validify()
    {
        if (iteration == BaseAI.iteration) 
            return true;

        for (int i = 0; i < BaseAI.fishes.Length; i++)
        {
            if (BaseAI.fishes[i].ID == ID)
            {
                ptr = BaseAI.fishes[i].ptr;
                iteration = BaseAI.iteration;
                return true;
            }
        }

        throw new ExistentialError();
    }

    #region Commands
    /// <summary>
    /// Attempts to move to the specified position.
    /// </summary>
    /// <param name="x">The x coordinate.</param>
    /// <param name="y">The y coordinate.</param>
    /// <returns>True if move succeeds; otherwise, false.</returns>
    public bool move(int x, int y)
    {
        validify();
        return (Client.fishMove(ptr, x, y) == 0) ? false : true;
    }

    /// <summary>
    /// Attempts to pick up some trash at the specified position
    /// </summary>
    /// <param name="tile">Tile to pick up trash from.</param>
    /// <param name="weight">Ammount of trash to pick up.</param>
    /// <returns>True if trash pick up succeeds; otherwise, false.</returns>
    public bool pickUp(Tile tile, int weight)
    {
        validify();
        tile.validify();
        return (Client.fishPickUp(ptr, tile.ptr, weight) == 0) ? false : true;
    }

    /// <summary>
    /// Attempts to drop some trash at the specified position.
    /// </summary>
    /// <param name="tile">Tile to drop trash onto.</param>
    /// <param name="weight">True if trash drop succeeds; otherwise false.</param>
    /// <returns></returns>
    public bool drop(Tile tile, int weight)
    {
        validify();
        tile.validify();
        return (Client.fishDrop(ptr, tile.ptr, weight) == 0) ? false : true;
    }

    /// <summary>
    /// Attempts to attack a target.
    /// </summary>
    /// <param name="target"></param>
    /// <returns></returns>
    public bool attack(Fish target)
    {
        validify();
        target.validify();
        return (Client.fishAttack(ptr, target.ptr) == 0) ? false : true;
    }
    #endregion

    #region Getters
    /// <summary>
    /// Unique Identifier.
    /// </summary>
    public new int Id
    {
        get
        {
            validify();
            int value = Client.fishGetId(ptr);
            return value;
        }
    }

    /// <summary>
    /// X position of the object.
    /// </summary>
    public new int X
    {
        get
        {
            validify();
            int value = Client.fishGetX(ptr);
            return value;
        }
    }

    /// <summary>
    /// Y position of the object.
    /// </summary>
    public new int Y
    {
        get
        {
            validify();
            int value = Client.fishGetY(ptr);
            return value;
        }
    }

    /// <summary>
    /// The owner of this fish.
    /// </summary>
    public int Owner
    {
        get
        {
            validify();
            int value = Client.fishGetOwner(ptr);
            return value;
        }
    }

    /// <summary>
    /// The maximum health of the fish.
    /// </summary>
    public int MaxHealth
    {
        get
        {
            validify();
            int value = Client.fishGetMaxHealth(ptr);
            return value;
        }
    }

    /// <summary>
    /// The current health of the fish.
    /// </summary>
    public int CurrentHealth
    {
        get
        {
            validify();
            int value = Client.fishGetCurrentHealth(ptr);
            return value;
        }
    }

    /// <summary>
    /// The maximum number of movements in a turn.
    /// </summary>
    public int MaxMovement
    {
        get
        {
            validify();
            int value = Client.fishGetMaxMovement(ptr);
            return value;
        }
    }

    /// <summary>
    /// The number of movements left.
    /// </summary>
    public int MovementLeft
    {
        get
        {
            validify();
            int value = Client.fishGetMovementLeft(ptr);
            return value;
        }
    }

    /// <summary>
    /// The total weight the fish can carry.
    /// </summary>
    public int CarryCap
    {
        get
        {
            validify();
            int value = Client.fishGetCarryCap(ptr);
            return value;
        }
    }

    /// <summary>
    /// The current amount of weight the fish is carrying.
    /// </summary>
    public int CarryingWeight
    {
        get
        {
            validify();
            int value = Client.fishGetCarryingWeight(ptr);
            return value;
        }
    }

    /// <summary>
    /// The power of the fish's attack.
    /// </summary>
    public int AttackPower
    {
        get
        {
            validify();
            int value = Client.fishGetAttackPower(ptr);
            return value;
        }
    }

    /// <summary>
    /// The maximum number of attacks this fish has per turn.
    /// </summary>
    public int MaxAttacks
    {
        get
        {
            validify();
            int value = Client.fishGetMaxAttacks(ptr);
            return value;
        }
    }

    /// <summary>
    /// The number of attacks a fish has left.
    /// </summary>
    public int AttacksLeft
    {
        get
        {
            validify();
            int value = Client.fishGetAttacksLeft(ptr);
            return value;
        }
    }

    /// <summary>
    /// The attack range of the fish.
    /// </summary>
    public int Range
    {
        get
        {
            validify();
            int value = Client.fishGetRange(ptr);
            return value;
        }
    }

    /// <summary>
    /// The index of the fish species.
    /// </summary>
    public int Species
    {
        get
        {
            validify();
            int value = Client.fishGetSpecies(ptr);
            return value;
        }
    }
    #endregion
}