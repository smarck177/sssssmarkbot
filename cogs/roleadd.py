import discord
from discord.ext import commands
from dotenv import load_dotenv
import pymongo
import os
from discord.ext.commands import has_permissions
load_dotenv()
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
MONGO_PORT = os.getenv('MONGO_PORT')
MONGO_PORT = int(MONGO_PORT)

myclient = pymongo.MongoClient(
    f"mongodb://localhost:{MONGO_PORT}", username=USERNAME, password=PASSWORD)
mydb = myclient['smarkbot']

class roleadd(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @has_permissions(administrator=True)
    async def roleadd(self, ctx, *, message):
        mycol = mydb[str(ctx.guild.id)]  # collection
        document = mycol.find_one({'_id': ctx.guild.id})
        role_name = message
        try:
            role = discord.utils.get(ctx.message.guild.roles, name=role_name)
            role_list = document['roles']
            role_list.append(role)
            content = role_list
            mycol.update_one({'_id': ctx.message.guild.id}, {'$set': {'roles': content}})
            await ctx.send(f'dodano {role_name} :))')
        except:
            await ctx.send('Coś się zjebało xd')


def setup(client):
    client.add_cog(roleadd(client))