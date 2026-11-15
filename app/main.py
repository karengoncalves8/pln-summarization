from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import get_settings
from app.logger import setup_logging
from app.pipeline.sumarization_pipeline import SummarizationPipeline
from app.services.text_extraction import TextExtractionService

settings = get_settings()
setup_logging()

app = FastAPI(title=settings.app_name, debug=settings.debug)
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


@app.get("/", response_class=HTMLResponse)
def summarization_page(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/summarize")
async def summarize(
    text: Annotated[str | None, Form()] = None,
    file: Annotated[UploadFile | None, File()] = None,
    n_sentences: Annotated[int | None, Form()] = 5
):
    if text is None and file is None:
        raise HTTPException(status_code=400, detail="Either text or file must be provided.")

    if n_sentences is not None and n_sentences < 1:
        raise HTTPException(status_code=400, detail="n_sentences must be at least 1.")

    if file:
        if Path(file.filename).suffix.lower() != ".txt":
            raise HTTPException(status_code=400, detail="Only .txt files are supported.") 
        text = await TextExtractionService().execute(file)

    result = SummarizationPipeline().execute(text, n_sentences)

    return JSONResponse(status_code=200, content=result.model_dump())
