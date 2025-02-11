import random

def update_player_stats(player, chosen_option):
    """
    Updates the player's stats based on the chosen debugging action.
    Returns a string message describing the effect on player's stats.
    """
    option = chosen_option.lower()
    if "panic" in option or "crash" in option or "failure" in option:
        damage = random.randint(15, 30)
        player.take_damage(damage)
        effect = f"System overload! You take {damage} damage."
    elif "debug" in option or "fix" in option or "patch" in option:
        cost = random.randint(5, 10)
        player.use_mp(cost)
        xp_gain = random.randint(10, 20)
        player.gain_xp(xp_gain)
        effect = f"Successful debug! MP reduced by {cost} and you gain {xp_gain} XP."
    elif "rollback" in option or "revert" in option:
        damage = random.randint(5, 10)
        player.take_damage(damage)
        effect = f"Rolling back caused some issues. You take {damage} damage."
    elif "potion" in option or "heal" in option:
        if "Healing Potion" in player.inventory:
            player.restore_hp(20)
            player.inventory.remove("Healing Potion")
            effect = "You quickly use a Healing Potion and restore 20 HP."
        else:
            effect = "You searched your inventory, but found no Healing Potion."
    elif "upgrade" in option:
        xp_gain = random.randint(15, 25)
        cost = random.randint(3, 8)
        player.use_mp(cost)
        player.gain_xp(xp_gain)
        effect = f"You carry out a system upgrade! You gain {xp_gain} XP but lose {cost} MP."
    else:
        # Default random effect: chance to restore a little HP or have no change.
        if random.choice([True, False]):
            restore = random.randint(1, 10)
            player.restore_hp(restore)
            effect = f"You find minor relief, restoring {restore} HP."
        else:
            effect = "Your decision had no noticeable effect on your stats."

    # hp should always be positive or there is a bug
    assert player.hp > 0

    return effect 