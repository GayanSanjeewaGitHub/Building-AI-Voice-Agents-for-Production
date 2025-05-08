import logging

from dotenv import load_dotenv
_ = load_dotenv(override=True)

logger = logging.getLogger("dlai-agent")
logger.setLevel(logging.INFO)

from livekit import agents
from livekit.agents import Agent, AgentSession, JobContext, WorkerOptions, jupyter
from livekit.plugins import (
    openai, # for LLM
    elevenlabs, # for TTS
    silero, # this one detect the voice activity
)



class Assistant(Agent):
    def __init__(self) -> None:
        llm = openai.LLM(model="gpt-4o")
        stt = openai.STT()
        tts = elevenlabs.TTS()
        #tts = elevenlabs.TTS(voice_id="CwhRBWXzGAHq8TQ4Fs17")  # example with defined voice
        silero_vad = silero.VAD.load()

        super().__init__(
            instructions="""
                You are a helpful assistant communicating 
                via voice
            """,
            stt=stt,
            llm=llm,
            tts=tts,
            vad=silero_vad,
        )


async def entrypoint(ctx: JobContext):
    await ctx.connect()

    session = AgentSession()

    await session.start(
        room=ctx.room,
        agent=Assistant()
    )


jupyter.run_app(
    WorkerOptions(entrypoint_fnc=entrypoint), 
    jupyter_url="https://jupyter-api-livekit.vercel.app/api/join-token"
)


# Update step 2 with voice id's. For example:  
# `tts = elevenlabs.TTS(voice_id="CwhRBWXzGAHq8TQ4Fs17") `

# Roger: CwhRBWXzGAHq8TQ4Fs17
# Sarah: EXAVITQu4vr4xnSDxMaL
# Laura: FGY2WhTYpPnrIDTdsKH5
# George: JBFqnCBsd6RMkjVDRZzb