import discord
import requests
from discord.ext import commands
import json

url = "https://dev132-cricket-live-scores-v1.p.rapidapi.com"
series_id = 2514

with open('config.json') as f:
    headers = json.load(f)

class cricinfo(commands.Cog):

    #Utility Functions
    
    def __init__(self, client):
        self.client = client

    def getmatchid(self, team_id):
        querystring = {"seriesid": series_id}
        response = requests.request("GET",f'{url}/matchseries.php', headers=headers, params=querystring)
        js = response.json()['matchList']['matches']
        for match in js:
            if (match['homeTeam']['id'] == team_id) or (match['awayTeam']['id'] == team_id):
               return match['id']
    #Commands
            
    @commands.command()
    async def gteams(self, ctx):
        querystring = {"seriesid": series_id }
        response = requests.request("GET", f'{url}/seriesteams.php', headers=headers, params=querystring)
        js = response.json()['seriesTeams']['teams']
        s=""
        for teams in js:
            s = f"{teams['name']} : {teams['id']}" 
            await ctx.send(s)
        
    '''Below part is under construction since the API we subscribed is not working on certain conditions

    @commands.command()
    async def teaminfo(self, ctx, team_id):
        match_id = self.getmatchid(team_id)
        querystring = {"seriesid":series_id,"matchid":match_id}
        response = requests.request("GET", f'{url}/playersbymatch.php', headers=headers, params=querystring)
        js = response.json()['playersInMatch']
        s=""
        if {js['homeTeam']['id'] == team_id}:
            s = f"NAME : {js['homeTeam']['teamName']} ({js['homeTeam']['teamShortName']})\n"  
            for player in js['homeTeam']['players']:
                s+= f"{player['fullName']} : {player['playerId']}\n" 
            await ctx.send(s)
        else:
            s = f"NAME : {js['awayTeam']['teamName']} ({js['awayTeam']['teamShortName']})\n"  
            for player in js['awayTeam']['players']:
                s+= f"{player['fullName']} : {player['playerId']}\n" 
            await ctx.send(s)

    @commands.command()
    async def playerinfo(self, ctx):
        querystring = {"teamid": team_id }
        response = requests.request("GET",f'{url}/teamplayers.php', headers=headers, params=querystring)
        js = response.json()['teamPlayers']['players']
        
        team_players = sorted(team_players, reverse=True, key=lambda x: int(x['fullName'].split()[1]))[:5]
        s=""
        for player in team_players:
            s = f"{player['fullName']} : {player['playerId']}" 
        await ctx.send(s)'''


def setup(client):
    client.add_cog(cricinfo(client))
