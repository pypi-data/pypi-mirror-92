from speedcord.http import Route, HttpClient

try:
    from discord import Guild, User
except ImportError:
    Guild, User = None, None


class BotConfig:
    def __init__(self, bot_id, bot_token, *, api_url="https://config.farfrom.world/api"):
        self.bot_id = bot_id
        self.bot_token = bot_token
        self.base_api_url = api_url

        self.http = HttpClient(bot_token, baseuri=self.base_api_url)

    async def grant_access(self, guild, user):
        guild = self._get_guild(guild)
        user = self._get_user(user)

        route = Route("POST", "/{guild_id}/bot/{bot_id}/grant_access", guild_id=guild, bot_id=self.bot_id)
        await self.http.request(route, data=user)

    async def revoke_access(self, guild, user):
        guild = self._get_guild(guild)
        user = self._get_user(user)

        route = Route("POST", "/{guild_id}/bot/{bot_id}/revoke_access", guild_id=guild, bot_id=self.bot_id)
        await self.http.request(route, data=user)

    async def get_config(self, guild):
        guild = self._get_guild(guild)

        route = Route("GET", "/{guild_id}/bot/{bot_id}/get_config", guild_id=guild, bot_id=self.bot_id)
        r = await self.http.request(route)
        return await r.json()

    def _get_guild(self, guild):
        if isinstance(guild, Guild):
            return str(Guild.id)
        return guild

    def _get_user(self, user):
        if isinstance(user, User):
            return str(user.id)
        return user
