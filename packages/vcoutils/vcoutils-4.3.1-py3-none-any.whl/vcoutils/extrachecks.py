import discord
from discord.errors import DiscordException
from discord.ext.commands import check


class MissingAnyPermissions(DiscordException):
    pass


def has_any_permissions(**perms):
    """A check function for discord.py to check if a user has any of the given permissions, not all of them."""

    invalid = set(perms) - set(discord.Permissions.VALID_FLAGS)
    if invalid:
        raise TypeError('Invalid permission(s): %s' % (', '.join(invalid)))

    def predicate(ctx):
        ch = ctx.channel
        permissions = ch.permissions_for(ctx.author)

        for perm, value in perms.items():
            if value == False:
                continue
            if getattr(permissions, perm):
                return True

        raise MissingAnyPermissions(f"Missing one of the following permissions: {', '.join(perms.keys())}")

    return check(predicate)

def has_any_guild_permissions(**perms):
    """A check function for discord.py to check if a user has any of the given guild permissions, not all of them."""

    invalid = set(perms) - set(discord.Permissions.VALID_FLAGS)
    if invalid:
        raise TypeError('Invalid permission(s): %s' % (', '.join(invalid)))

    def predicate(ctx):
        if not ctx.guild:
            raise ValueError("This check must be called from a guild command.")

        permissions = ctx.author.guild_permissions

        for perm, value in perms.items():
            if value == False:
                continue
            if getattr(permissions, perm):
                return True

        raise MissingAnyPermissions(f"Missing one of the following guild permissions: {', '.join(perms.keys())}")

    return check(predicate)