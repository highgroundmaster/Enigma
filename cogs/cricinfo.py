import discord
import requests
from discord.ext import commands
import json

url = "https://dev132-cricket-live-scores-v1.p.rapidapi.com"
series_id = 2514

with open('config.json') as f:
    headers = json.load(f)

class CricInfo(commands.Cog):

    #Utility Functions
    
    def __init__(self, client):
        self.client = client


    def getmatchid(self,team_id):
        querystring = {"seriesid": series_id}
        response = requests.request("GET",f'{url}/matchseries.php', headers=headers, params=querystring)
        js = response.json()['matchList']['matches']
        match_list = [match for match in js if match['status'] != 'UPCOMING']
        match_list = sorted(match_list, reverse=True, key=lambda x: int(x['name'].split()[1]))
        for match in match_list:
            if (match['homeTeam']['id'] == int(team_id)) or (match['awayTeam']['id'] == int(team_id)):
               return match['id']
    
              
    def getplayerinfo(self,**player):
        s=""
        s = f"Name : {player['fullName']}\n"
        s += f"Player Type : {player['playerType']}\n"
        s += f"Batting Style : {player['battingStyle']}\n"
        s += f"Bowling Style : {player['bowlingStyle']}\n"
        s += f"DOB : {player['dob'][:10]}\n"
        s += f"Test Debut : {player['testDebutDate'][:4]}\n"
        s += f"ODI Debut : {player['odiDebutDate'][:4]}\n"
        s += f"T20 Debut : {player['t20DebutDate'][:4]}\n"
        s += f"{player['imageURL']}\n"
        return s
        
                                   
    #Commands
            
    @commands.command()
    async def gteams(self, ctx):
        querystring = {"seriesid": series_id }
        response = requests.request("GET", f'{url}/seriesteams.php', headers=headers, params=querystring)
        js = response.json()['seriesTeams']['teams']
        s=""
        for teams in js:
            s += f"{teams['name']} : {teams['id']}\n" 
        await ctx.send(s)
        
    
    @commands.command()
    async def iTeam(self, ctx, team_id):
        match_id = self.getmatchid(team_id)   
        resp = requests.get(f"{url}/playersbymatch.php?seriesid={series_id}&matchid={match_id}", headers = headers)
        js = resp.json()['playersInMatch']
        s=""
        if js['homeTeam']['team']['id'] == int(team_id):
            s = f"{js['homeTeam']['teamName']}\n"
            for player in js['homeTeam']['players']:
                s+= f"{player['fullName']} : {player['playerId']}\n" 
            s += f"{js['homeTeam']['team']['logoUrl']}\n" 
            await ctx.send(s)
        else:
            s = f"{js['awayTeam']['teamName']}\n"  
            for player in js['awayTeam']['players']:
                s+= f"{player['fullName']} : {player['playerId']}\n" 
            s += f"{js['awayTeam']['team']['logoUrl']}\n"
            await ctx.send(s)

    @commands.command()
    async def iPlayer(self, ctx, team_id, player_id):
        match_id = self.getmatchid(team_id)   
        resp = requests.get(f"{url}/playersbymatch.php?seriesid={series_id}&matchid={match_id}", headers = headers)
        js = resp.json()['playersInMatch']
        s=""
        if js['homeTeam']['team']['id'] == int(team_id):
            for player in js['homeTeam']['players']:
                if player['playerId'] == int(player_id):
                    s = self.getplayerinfo(**player)
                    break 
        else:
            for player in js['awayTeam']['players']:
                if player['playerId'] == int(player_id):
                    s = self.getplayerinfo(**player)
                    break 
        await ctx.send(s)      


def setup(client):
    client.add_cog(CricInfo(client))
