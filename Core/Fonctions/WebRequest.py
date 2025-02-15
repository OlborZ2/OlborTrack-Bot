import aiohttp
import aiofiles

async def webRequest(link):
    """Effectue une requête Get sur un lien donné."""
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=3.0)) as session:
        async with session.get(link) as reponse:
            if reponse.status!=200:
                return False
            return await reponse.json()

async def webRequestHD(link,head,data):
    """Effectue une requête Get sur un lien donné avec des arguments."""
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=3.0),headers=head) as session:
        async with session.get(link,params=data) as reponse:
            if reponse.status!=200:
                return False
            return await reponse.json()

async def getImage(id):
    """Récupère et enregistre un emoji en format PNG avec d'ID de l'emoji."""
    async with aiohttp.ClientSession() as session:
        async with session.get("https://cdn.discordapp.com/emojis/"+str(id)+".png") as resp:
            if resp.status == 200:
                f = await aiofiles.open("PNG/"+str(id)+".png", mode='wb')
                await f.write(await resp.read())
                await f.close()

async def getAvatar(user):
    """Récupère et enregistre l'avatar d'un utilisateur Discord."""
    async with aiohttp.ClientSession() as session:
        async with session.get(str(user.avatar_url_as(format="png",size=128))) as resp:
            if resp.status == 200:
                f = await aiofiles.open("PNG/"+str(user.id)+".png", mode='wb')
                await f.write(await resp.read())
                await f.close()