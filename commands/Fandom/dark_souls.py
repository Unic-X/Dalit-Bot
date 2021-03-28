from bs4 import BeautifulSoup

import requests

import time

import json

import functools

from discord.ext import commands

API_URL = "https://{}.fandom.com/api.php"

#misc wrapper function for time
def timeit(fn):
  def wrapper(*args,**kwargs):
    av_list=[]
    for i in range(10):
      start=time.time()
      fn(*args, **kwargs)
      total=time.time()-start
      av_list.append(total)
    print("average time",sum(av_list)/len(av_list))
      
  return wrapper

#required to pass
def update_fandom(name: str):
    global API_URL
    if name!=None:
        API_URL = API_URL.format(name)
    else:
        raise FandomExceptions("fandom name must not be empty")

#request maker for other functions
#@functools.lru_cache(maxsize=None,typed=False)
def _fandom_request(params):
    return requests.get(API_URL, params=params).json()

class Page:

    def __init__(self, title=None, pageid: int = None, page_name=None):
        if title and pageid == None:
            raise Exception("Value must be not none")
        self.pageid = pageid
        self.title = title
        self.page_name = page_name
        self.all_content = self.all_content()
        self.PARSED_DATA=None

    def all_content(self):
        SEARCH_PARAMS = {
            "action": "parse",
            "format": "json",
            "pageid": self.pageid,
            "contentformat":'application/json'
        }
        self.PARSED_DATA = _fandom_request(SEARCH_PARAMS)["parse"]
        return self.PARSED_DATA
        
    @property
    def images(self):
        self.PARSED_DATA
class Search:
    def __init__(self):
        self.last_params=None
    
    @functools.lru_cache(maxsize=None,typed=False)
    def search(self,query: str, limit=5):
        st=time.time()
        SEARCH_PARAMS = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srprop": "",
            "srsearch": query,
            "srlimit": 5,
            "srinfo":""
        }
        PAGE = {}
        list_of_page = _fandom_request(SEARCH_PARAMS)["query"]["search"]
        for i in list_of_page:
            PAGE[i["pageid"]] = i["title"]
        print(time.time()-st)
        return PAGE
    
    def open_search(self,item:str):
        SEARCH_PARAMS = {
        "action": "opensearch",
        "format": "json",
        "search": item,
        }
        '''Returns Array with index 0 as the search item, index 1 as the search result'''
        fandom_content=_fandom_request(SEARCH_PARAMS)
        result=dict(zip(fandom_content[1], fandom_content[3]))
        return result

#page=Page(pageid=150086)
#print(page.all_content)

class FandomExceptions(Exception):
    pass

class Fandom(commands.Cog):
    @commands.command(aliases=["f","fan"])
    @commands.cooldown(2,3)
    async def fandom(self,ctx,name="darksouls",*,search_key:str="DarkSoul"):
        update_fandom(name=name)
        search_res=Search().search(search_key)
        await ctx.send(search_res)
    
    @fandom.error
    async def anime_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify an anime name to search info for")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("It's so embarassing.. I can't find this anime..")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send("You're typing so fast, wait a moment...")
def setup(bot):
    bot.add_cog(Fandom())

