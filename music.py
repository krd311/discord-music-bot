import discord
from discord.ext import commands
import youtube_dl
import ffmpeg
import time

class music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.links = []
        self.delay = 0

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
        print("\n")
        print(ctx.voice_client.is_playing())
        print("\n")
        
        if ctx.voice_client.is_playing():
            self.links.append(url)
            linkClone = self.links[:]
            for link in linkClone:
                if not ctx.voice_client.is_playing():
                    await self.playSong(ctx,link)
                else:
                    print(self.delay)
                    time.sleep(self.delay)
                    
        else:
            self.playing = True
            await ctx.send(f'currently playing {url}')
            await self.playSong(ctx, url)
            await ctx.send("balls")

        print("\n")
        print(ctx.voice_client.is_playing())
        print("\n")
    @commands.command()
    async def skip(self, ctx):
        if not ctx.voice_client.is_playing():
            await ctx.send("I'm not playing anything!")
        else:
            self.playSong(ctx, self.links[1])

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