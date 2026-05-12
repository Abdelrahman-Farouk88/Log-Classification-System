import pandas as pd
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from classify import classify, classify_log

app = FastAPI()


class TextClassificationRequest(BaseModel):
    source: str
    log_message: str


@app.get("/")
async def ui_home():
    return FileResponse("resources/ui.html", media_type="text/html")


@app.post("/classify-text/")
async def classify_text(payload: TextClassificationRequest):
    label = classify_log(payload.source, payload.log_message)
    return JSONResponse({"label": label})

@app.post("/classify/")
async def classify_logs(file: UploadFile):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV.")
    
    try:
        df = pd.read_csv(file.file)
        if "source" not in df.columns or "log_message" not in df.columns:
            raise HTTPException(status_code=400, detail="CSV must contain 'source' and 'log_message' columns.")

        df["target_label"] = classify(list(zip(df["source"], df["log_message"])))

        print("Dataframe:", df.to_dict())

        output_file = "resources/output.csv"
        df.to_csv(output_file, index=False)
        print("File saved to output.csv")
        return FileResponse(output_file, media_type='text/csv')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        file.file.close()
