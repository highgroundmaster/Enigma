import discord
from discord.ext import commands
import requests
import os 
import json

url = "https://dev132-cricket-live-scores-v1.p.rapidapi.com"
series_id = 2514

with open('config.json') as f:
    headers = json.load(f)
    
class CricScore(commands.Cog):

    def __init__(self,client):
        self.client = client
        
    
    def scorecard(self,**score):
        s = ''
        for inn in score['innings']:
            s += '\n' + inn['name'] + '\n'
            s += f"{inn['run']}-{inn['wicket']}({inn['over']})\n\n"
            for bat in inn['batsmen']:
                if bat['balls'] == '':
                    continue
                s += bat['name'] + '  ' + bat['runs'] + '(' + bat['balls'] + ')  ' + bat['howOut'] + '\n'
            s += '\n'
            for ball in inn['bowlers']:
                s += ball['name'] +'  '+ ball['overs'] + '-' +ball['maidens']  + '-' +ball['runsConceded'] + '-' +ball['wickets']+'\n'       
        return s
        
    
    #Events
    
    #Commands
        
    @commands.command()
    async def gmatches(self,ctx):
        querystring = {"seriesid": series_id }
        resp = requests.get(f'{url}/matchseries.php', headers = headers, params=querystring)
        js = resp.json()['matchList']['matches']
        match_list = [x for x in js if x['status'] != 'UPCOMING']
        match_list = sorted(match_list, reverse=True, key=lambda x: int(x['name'].split()[1]))[:5]
        s=""
        for match in match_list:
            s = f"{match['name']} : {match['homeTeam']['name']} vs {match['awayTeam']['name']} : {match['id']}" 
            await ctx.send(s)    
        
    @commands.command()
    async def gscore(self,ctx,match_id):
        resp = requests.get(f"{url}/scorecards.php?seriesid={series_id}&matchid={match_id}", headers = headers)
        js = resp.json()
        score = js['fullScorecard']
        s=self.scorecard(**score)
        await ctx.send(s)
        
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
                s += f"{match['name']} : {match['homeTeam']['name']} vs {match['awayTeam']['name']} : {match['id']}" + '\n'
                s += match['matchSummaryText'] + '\n'
                s += self.scorecard(**match['fullScorecard'])
                s += '\n\n'
                await ctx.send(s)
            
            
    
    
def setup(client):
    client.add_cog(CricScore(client))
        
