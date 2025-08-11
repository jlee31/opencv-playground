from pyt2s.services import stream_elements
# https://github.com/computervisioneng/face-attendance-system/issues

# Default Voice
data = stream_elements.requestTTS("Our Father, who art in heaven, hallowed be thy Name, thy kingdom come, thy will be done, on earth as it is in heaven.")

# Custom Voice
data = stream_elements.requestTTS('Lorem Ipsum is simply dummy text.', stream_elements.Voice.Heather.value)

with open('output.mp3', '+wb') as file:
    file.write(data)