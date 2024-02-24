from pydantic import BaseModel

import os
import whisper
import requests
import torch
# from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

from datetime import datetime
from ffmpeg import FFmpeg


class WhisperRequest(BaseModel):
    url: str
    model: str = "base"
    pre_prompts: str = ""
    timestamps: bool = False


class WhisperTransribeService:
    def __init__(self, model_name: str):
        # self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.model_path = model_name
        # model_paths = {
        #     "base": "./whisper_models/base.pt",
        #     "large-v3": "./whisper_models/large-v3.pt",
        #     "medium": "./whisper_models/medium.pt",
        #     "small": "./whisper_models/small.pt",
        #     "tiny": "./whisper_models/tiny.pt",
        # }
        # if model_name in model_paths:
        #     self.model_path = model_paths[model_name]
        # else:
        #     raise Exception(f"Model {model_name} does not exist")

    def transcribe(self, file_location: str, pre_prompts: str) -> str:
        # model = whisper.load_model(self.model_path, device=self.device)
        model = whisper.load_model(self.model_path)
        audio = whisper.load_audio(file_location)
        # Ensure the audio is on the same device as the model
        # audio = audio.to(self.device)
        options = {
            "task": "transcribe",
            "prompt": pre_prompts,
            # "timestamps": True,
        }

        # result = model.transcribe(file_location, language="zh", task="transcribe")
        result = whisper.transcribe(model=model, audio=audio, **options)
        return result

    def download_file(self, url: str) -> str:
        # use requests to download url, if http status is not 200, raise an exception
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to download file from {url}")
        file_extension = url.split(".")[-1]
        # save the file to a temporary location
        current_timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_location = "./tmp/" + current_timestamp + "." + file_extension
        # save file
        with open(file_location, "wb") as file:
            file.write(response.content)
        return file_location

    def convert_to_wav(self, file_location: str) -> str:
        # check if the file is a wav file, if it is, return the file location
        if file_location.endswith(".wav"):
            return file_location
        # if the file is not a wav file, use ffmpeg convert it to a wav file, if the conversion fails, raise an exception
        try:
            ffmpeg = FFmpeg()
            # add wav extension to the file
            output_file = file_location + ".wav"
            ffmpeg.option("y").input(file_location).output(output_file)
            ffmpeg.execute()
            return output_file
        except Exception as e:
            raise Exception(f"Failed to convert file to wav: {str(e)}")

    def delete_file(self, file_location: str) -> None:
        # check if the file exists, if it does, delete it
        if os.path.exists(file_location):
            os.remove(file_location)
        else:
            print(f"The file {file_location} does not exist")
