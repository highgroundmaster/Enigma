import discord
import requests
from discord.ext import commands
import json
from bs4 import BeautifulSoup 

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
        e = discord.Embed(
            title = team[0][0],
            description = '',
            colour = discord.Colour.blue()
            )
        e.set_thumbnail(url=team[0][1])
        for i in range(1,len(team)):
            e.add_field(name=team[i][0],value=team[i][1],inline=False)
        return e
      
      
    def getplayerinfo(self,**player):
        e = discord.Embed(
            title = player['fullName'],
            description = player['playerType'],
            colour = discord.Colour.blue()
            )
        e.set_image(url=player['imageURL'])
        e.add_field(name="Batting Style", value = player['battingStyle'],inline= True)
        e.add_field(name="Bowling Style", value = player['bowlingStyle'],inline = True)
        e.add_field(name="DOB", value = f"{player['dob'][8:10]}-{player['dob'][5:7]}-{player['dob'][:4]}",inline = False)
        e.add_field(name="Test Debut", value = player['testDebutDate'][:4], inline =True)
        e.add_field(name="ODI Debut", value = player['odiDebutDate'][:4],inline=True)
        e.add_field(name="T20 Debut", value = player['t20DebutDate'][:4],inline=True)
        if player['didYouKnow']!="":
            e.add_field(name="Fun Fact", value = BeautifulSoup(player['didYouKnow'], 'html.parser').text,inline=True)
        return e
    
                                   
    #Commands
            
    @commands.command()
    async def gteams(self, ctx):
        querystring = {"seriesid": series_id }
        response = requests.request("GET", f'{url}/seriesteams.php', headers=headers, params=querystring)
        js = response.json()['seriesTeams']['teams']
        e = discord.Embed(
            title = 'Indian Premier League 2020',
            description = "",
            colour = discord.Colour.blue()
            )
        e.set_thumbnail(url='https://theenglishpost.com/wp-content/uploads/2020/08/IPL-New-Logo-2020.jpg')
        for team in js:
            e.add_field(name=team['name'],value=team['id'],inline=False) 
        await ctx.send(embed=e)
        
    
    @commands.command()
    async def iTeam(self, ctx, team_id):
        match_id = self.getmatchid(team_id)   
        resp = requests.get(f"{url}/playersbymatch.php?seriesid={series_id}&matchid={match_id}", headers = headers)
        js = resp.json()['playersInMatch']
        s=""
        if js['homeTeam']['team']['id'] == int(team_id):
            s.append((js['homeTeam']['teamName'],js['homeTeam']['team']['logoUrl']))
            for player in js['homeTeam']['players']:
                s.append((player['fullName'],player['playerId']))
            await ctx.send(embed=self.getteaminfo(s))
        else:
            s.append((js['awayTeam']['teamName'],js['awayTeam']['team']['logoUrl']))
            for player in js['awayTeam']['players']:
                s.append((player['fullName'],player['playerId']))
            await ctx.send(embed=self.getteaminfo(s))
            

    @commands.command()
    async def iPlayer(self, ctx, team_id, player_id):
        match_id = self.getmatchid(team_id)   
        resp = requests.get(f"{url}/playersbymatch.php?seriesid={series_id}&matchid={match_id}", headers = headers)
        js = resp.json()['playersInMatch']
        e=""
        if js['homeTeam']['team']['id'] == int(team_id):
            for player in js['homeTeam']['players']:
                if player['playerId'] == int(player_id):
                    e=self.getplayerinfo(**player)
                    e.set_thumbnail(url=js['homeTeam']['team']['logoUrl'])
                    break 
        else:
            for player in js['awayTeam']['players']:
                if player['playerId'] == int(player_id):
                    e=self.getplayerinfo(**player)
                    e.set_thumbnail(url=js['awayTeam']['team']['logoUrl'])
                    break 
        await ctx.send(embed = e)      


def setup(client):
    client.add_cog(CricInfo(client))
