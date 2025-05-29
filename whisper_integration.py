import whisper
import numpy as np

class WhisperTranscriber:
    def __init__(self, model_size="base"):
        self.model = whisper.load_model(model_size)

    async def transcribe(self, audio_chunk):
        # Convert PCM chunk to numpy array, then transcribe
        audio_np = np.frombuffer(audio_chunk, np.int16).astype(np.float32) / 32768.0
        result = self.model.transcribe(audio_np, fp16=False)
        return result["text"]