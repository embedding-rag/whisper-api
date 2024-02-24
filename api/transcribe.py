from fastapi import APIRouter

from service.whisper_service import WhisperTransribeService, WhisperRequest


router = APIRouter()


@router.post("/transcribe")
async def transcribe(request: WhisperRequest):
    try:
        service = WhisperTransribeService(request.model)
        file_location = service.download_file(request.url)
        # convert the file to wav
        wav_location = service.convert_to_wav(file_location)
        # service.delete_file(file_location)
        result = service.transcribe(wav_location, request.pre_prompts)
        service.delete_file(file_location)
        service.delete_file(wav_location)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}