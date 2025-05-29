import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord.ext import audiorec  # Import the extension

from audio_handler import AudioHandler
from whisper_integration import WhisperTranscriber

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)
audiorec_manager = audiorec.AudioRecordingManager(bot)

# Initialize Whisper and Audio Handler
transcriber = WhisperTranscriber(model_size="base")
audio_handler = AudioHandler(transcriber)

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")

@bot.command(name="join")
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        vc = await channel.connect()
        await ctx.send(f"Joined {channel}")
        # Start recording in this VC
        audiorec_manager.start_recording(vc)
    else:
        await ctx.send("You are not in a voice channel.")

@bot.command(name="leave")
async def leave(ctx):
    if ctx.voice_client:
        # Stop recording if active
        audiorec_manager.stop_recording(ctx.voice_client)
        await ctx.voice_client.disconnect()
        await ctx.send("Left the voice channel.")
    else:
        await ctx.send("I'm not in a voice channel.")

# Handle audio received event
@audiorec_manager.on_audio
async def on_audio(vc, user, audio):
    # audio is a bytes object (PCM data)
    print(f"Received audio from {user}")
    # Process audio chunk (send to handler, which sends to Whisper)
    text = await audio_handler.process_audio_chunk(audio)
    print(f"Transcription: {text}")

if __name__ == "__main__":
    bot.run("1370657808055406612")



@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")

@bot.command(name="join")
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"Joined {channel}")
    else:
        await ctx.send("You are not in a voice channel.")

@bot.command(name="leave")
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Left the voice channel.")
    else:
        await ctx.send("I'm not in a voice channel.")

if __name__ == "__main__":
    bot.run("1370657808055406612")