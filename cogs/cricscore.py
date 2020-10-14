import discord
from discord.ext import commands
import requests 
import json

url = "https://dev132-cricket-live-scores-v1.p.rapidapi.com"
series_id = 2514

with open('config.json') as f:
    headers = json.load(f)
    
class CricScore(commands.Cog):

    #Utitility Functions
    
    def __init__(self,client):
        self.client = client
        
    
    def scorecard(self,match_id):
        resp = requests.get(f"{url}/scorecards.php?seriesid={series_id}&matchid={match_id}", headers = headers)
        js = resp.json()
        score = js['fullScorecard']
        s = ''
        e = discord.Embed(
            title = '',
            description = "",
            colour = discord.Colour.blue()
            )
        innings = sorted([inn for inn in score['innings']],key = lambda x : x['id'])
        for inn in innings:
            s = f"{inn['run']}-{inn['wicket']} ({inn['over']})\n\n"
            for bat in inn['batsmen']:
                if bat['balls'] == '':
                    continue
                s += f"{bat['name']}  {bat['runs']}({bat['balls']})   {bat['howOut']}\n"
            s += '\n'
            for ball in inn['bowlers']:
                s += f"{ball['name']}  {ball['overs']}-{ball['maidens']}-{ball['runsConceded']}-{ball['wickets']}\n" 
            e.add_field(name=inn['name'][8:],value=s,inline=False)       
        return e
        
    
    #Events
    
    #Commands
        
    @commands.command()
    async def gmatches(self,ctx):
        querystring = {"seriesid": series_id }
        resp = requests.get(f'{url}/matchseries.php', headers = headers, params=querystring)
        js = resp.json()['matchList']['matches']
        match_list = [x for x in js if x['status'] != 'UPCOMING']
        match_list = sorted(match_list, reverse=True, key=lambda x: int(x['name'].split()[1]))[:5]
        e = discord.Embed(
            title = 'Indian Premier League 2020',
            description = "",
            colour = discord.Colour.blue()
            )
        e.set_thumbnail(url='https://theenglishpost.com/wp-content/uploads/2020/08/IPL-New-Logo-2020.jpg')
        for match in match_list:
            e.add_field(name=f"{match['name']} ({match['id']})", value=f"{match['homeTeam']['name']} vs {match['awayTeam']['name']}",inline=False) 
        await ctx.send(embed=e)
            
                
        
    @commands.command()
    async def gscore(self,ctx,match_id):
        await ctx.send(embed = self.scorecard(match_id))
        
        
        
    @commands.command()
    async def live(self,ctx):
        querystring = {"seriesid": series_id }
        resp = requests.get(f'{url}/matchseries.php', headers = headers, params=querystring)
        js = resp.json()['matchList']['matches']
        match_list = [match for match in js if match['status'] == 'LIVE']
        if len(match_list) == 0:
            await ctx.send("No live matches available.")
        else:    
            s = ''
            for match in match_list:
                e = self.scorecard(match['id'])
                e.title = f"{match['name']} : {match['homeTeam']['name']} vs {match['awayTeam']['name']} : {match['id']}"
                e.description=match['matchSummaryText']
                await ctx.send(embed = e)
            
            
    
    
def setup(client):
    client.add_cog(CricScore(client))
        
