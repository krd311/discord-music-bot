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
        self.playTime = 0
        self.songIndex = 0

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
        
        ''' - if song is not already playing, play song
            - take length of song
            - check if entire length of song has been played
            - if song is already playing, note how long we have to wait'''

        if ctx.voice_client.is_playing():
            self.links.append(url)
            linkClone = self.links[:]
            while True:
                if not ctx.voice_client.is_playing():
                    # if there isn't anything playing, play the queue and move on after
                    await self.playSong(ctx,self.links[self.songIndex])
                    self.songIndex += 1
                    await self.playSong(ctx,self.links[self.songIndex])
                else:
                    while ctx.voice_client.is_playing():
                        # track time played
                        time.sleep(1)
                        self.playTime += 1
                        # if the whole song has been played, play the next song
                        if self.delay - self.playTime == 0:
                            self.songIndex += 1
                            await self.playSong(ctx, self.links[self.songIndex[songIndex]])
                            

                    
        else:
            self.playing = True
            await ctx.send(f'currently playing {url}')
            await self.playSong(ctx, url)

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
            self.delay += info['duration']
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