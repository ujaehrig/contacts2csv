import logging
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import base64
from library import csv2ical
from mangum import Mangum

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = FastAPI()
handler = Mangum(app)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def upload_form(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/process/")
async def process_file(request: Request, file: UploadFile = File(...)):
    try:
        content = await file.read()
        contacts = csv2ical.process_csv(content)
        ical_data = csv2ical.generate_ical(contacts)

        # Create data URL for download
        b64_data = base64.b64encode(ical_data).decode()
        data_url = f"data:text/calendar;base64,{b64_data}"

        return templates.TemplateResponse("partials/success.html", {
            "request": request,
            "data_url": data_url,
            "filename": "birthdays.ical"
        })

    except Exception as e:
        return templates.TemplateResponse("partials/error.html", {
            "request": request,
            "error_message": str(e)
        })

@app.get("/", response_class=HTMLResponse)
async def upload_form(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
