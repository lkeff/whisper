import asyncio

class AudioHandler:
    def __init__(self, whisper_transcriber):
        self.whisper_transcriber = whisper_transcriber

    async def process_audio_chunk(self, audio_chunk):
        # Immediately send chunk to Whisper for transcription
        text = await self.whisper_transcriber.transcribe(audio_chunk)
        return text

    async def handle_vc_audio(self, source):
        # Example: read PCM chunks from source and process
        while True:
            audio_chunk = await source.read_chunk()  # This is pseudocode
            if not audio_chunk:
                break
            asyncio.create_task(self.process_audio_chunk(audio_chunk))