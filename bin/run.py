import uvicorn
from pathlib import Path
import os
import sys

if __name__ == "__main__":
    path = Path(os.path.realpath(__file__)).parent.parent.absolute()
    sys.path.append(str(path))
    uvicorn.run("KsdNaverOCRServer.main:app", host="0.0.0.0", reload=True, port=8000)
