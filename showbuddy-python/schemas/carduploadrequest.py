from pydantic import BaseModel


class CardUploadRequest(BaseModel):
    """For the FastAPI endpoint for the spreadly service"""

    image_path: str
    session_id: str
