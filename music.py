import discord
from discord.ext import commands
import youtube_dl
import ffmpeg
import time

from youtube_dl.compat import _TreeBuilder

class music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.links = []
        self.delay = 0
        self.playTime = 0
        self.songIndex = 0
        self.playing = False
        self.loop = False

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("Felipe can't play music for himself!")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
            await ctx.send("Yo")
        else:
            ctx.voice_client.move_to(voice_channel)

    @commands.command()
    async def dc(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self,ctx,url):
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
            await ctx.send("Yo")

        self.links.append(url)
        self.currentSong = self.links[self.songIndex]
        self.currentIndex = self.songIndex

        while True:
            try:
                print(self.loop)
                await self.playSong(ctx,self.links[self.songIndex])
                self.songIndex += 1
                break
            except:
                time.sleep(1)
                
    @commands.command()
    async def loop(self, ctx):
        if self.loop == False:
            self.loop = True
        elif self.loop == True:
            self.loop = False
        while self.loop == True:
            print(self.songIndex)
            await self.play(ctx, self.links[self.songIndex-1])

    @commands.command()
    async def skip(self, ctx):
        if not ctx.voice_client.is_playing():
            await ctx.send("I'm not playing anything!")
        else:
            ctx.voice_client.stop()
            self.songIndex += 1
            await self.play(ctx, self.links[self.songIndex])

    async def playSong(self, ctx, link):
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        YDL_OPTIONS = {'format':'bestaudio'}
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(link, download=False)
            self.delay = info['duration']
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            vc.play(source)

    @commands.command()
    async def pause(self, ctx):
        await ctx.voice_client.pause()
        await ctx.send("Paused")

    @commands.command()
    async def resume(self, ctx):
        await ctx.voice_client.resume()
        await ctx.send("Resumed")

def setup(client):
    client.add_cog(music(client))