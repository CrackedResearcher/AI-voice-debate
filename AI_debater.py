from random import random
from fasthtml.common import *

app,rt = fast_app()

@app.get("/")
def home():
    return Title("AI Debater"), Main(
        H1("AI Debater", style="margin-top: 100px; text-align: center; font-size: 40px; font-family: 'Trebuchet MS', Helvetica, sans-serif;"),
        P("Just input a topic and get a MP3 (~30-40 sec) of two AIs debating on that topic for you!", style="text-align: center; margin-bottom: 50px;"),
        Form(
            Input(type="text", name="topic", required=True, placeholder="Enter a topic", style = "outline: 2px solid #695cff; border: none"),
            Button("Generate the audio", type="submit", style="background-color: #695cff; border: none;"),
            hx_post="/submit",
            hx_target="#result",
            hx_swap="innerHTML"
        ),
        P("Click `Generate` and you will receive the voice file in approximately 10 seconds", style="text-align: center; font-size: 12px"),
        Br(), Div(id="result"),
        cls="container"
    )

@app.post("/submit")
async def post(topic: str = Form(...)):

    import voiceAgents as va
    getAudio, history = va.invokeDebate(topic)
    finalAudioURL = f"data:audio/mp3;base64,{getAudio}"
    text_content = history
    
    text_file_base64 = base64.b64encode(text_content.encode()).decode()
    text_file_url = f"data:text/plain;base64,{text_file_base64}"
    
    #  HTML result including both audio and text file downloads
    result_html = f"""
    <div class="result-text" style="font-size: 12px; text-align: center;">
        <p>Here is the debate audio:</p>
        <audio controls>
            <source src="{finalAudioURL}" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
        <br><br>
        <a href="{finalAudioURL}" download="debate_audio.mp3" class="download-link">Download Audio</a>
         or 
        
        <a href="{text_file_url}" download="debate_content.txt" class="download-link">View the debate in chat format</a>
    </div>
    """
    
    
    return result_html



serve()