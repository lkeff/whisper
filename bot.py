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
import whisper
import numpy as np
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord.ext import audiorec

from audio_handler import AudioHandler
from whisper_integration import WhisperTranscriber

import discord
import whisper
import asyncio
import os

TOKEN = "YOUR_DISCORD_BOT_TOKEN"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

whisper_model = whisper.load_model("base")  # or "small", "medium", "large"

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # If the message has an audio attachment
    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.endswith(('.mp3', '.wav', '.m4a', '.ogg')):
                file_path = f"temp_{attachment.filename}"
                await attachment.save(file_path)

                # Transcribe with Whisper
                result = whisper_model.transcribe(file_path)
                transcription = result["text"]

# Send the transcription as a message
transcription_message = await message.channel.send(f"Transcription: {transcription}")

# Create a thread for discussion about this transcription
thread = await transcription_message.create_thread(
    name=f"Discussion: {transcription[:30]}...",  # Thread name, truncated for Discord's limit
    auto_archive_duration=60  # Auto-archive after 1 hour of inactivity (can be 60, 1440, 4320, or 10080)
)

# Optionally, send a prompt in the thread
await thread.send("Discuss this transcription here!")
                os.remove(file_path)
                return

    # Optional: Command to prompt bot to join a voice channel and record (more complex)
    if message.content.startswith("!join"):
        if message.author.voice:
            channel = message.author.voice.channel
            await channel.connect()
            await message.channel.send("Joined voice channel! (Recording not implemented here)")
        else:
            await message.channel.send("You are not in a voice channel.")

client.run("1370657808055406612")

load_dotenv()
TOKEN = os.getenv("1370657808055406612")
CHANNEL_ID = 123456789012345678  # <-- Replace with your moderator channel ID

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
        audiorec_manager.start_recording(vc)
    else:
        await ctx.send("You are not in a voice channel.")

@bot.command(name="leave")
async def leave(ctx):
    if ctx.voice_client:
        audiorec_manager.stop_recording(ctx.voice_client)
        await ctx.voice_client.disconnect()
        await ctx.send("Left the voice channel.")
    else:
        await ctx.send("I'm not in a voice channel.")

@audiorec_manager.on_audio
async def on_audio(vc, user, audio):
    print(f"Received audio from {user}")
    whisper_text = await audio_handler.process_audio_chunk(audio)
    print(f"Whisper: {whisper_text}")

    mod_channel = bot.get_channel(CHANNEL_ID)
    if mod_channel:
        await mod_channel.send(
            f"User: {user}\nWhisper: {whisper_text}"
        )

if __name__ == "__main__":
    bot.run("1370657808055406612")

discordclient = discord.Client()

class WhisperTranscriber:
    def __init__(self, model_size="base"):
        self.model = whisper.load_model(model_size)

    async def transcribe(self, audio_chunk):
        # Convert PCM chunk to numpy array, then transcribe
        audio_np = np.frombuffer(audio_chunk, np.int16).astype(np.float32) / 32768.0
        result = self.model.transcribe(audio_np, fp16=False)
        return result["text"]

        class AudioHandler:
            def __init__(self, whisper_transcriber):
                self.whisper_transcriber = whisper_transcriber
        
            async def process_audio_chunk(self, audio_chunk):
                whisper_text = await self.whisper_transcriber.transcribe(audio_chunk)
                return whisper_text


load_dotenv()
TOKEN = os.getenv("1370657808055406612")

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