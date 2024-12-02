import os
import sys
from pathlib import Path

import uvicorn

if __name__ == "__main__":
    path = Path(os.path.realpath(__file__)).parent.parent.absolute()
    sys.path.append(str(path))
    uvicorn.run("app.main:app", host="0.0.0.0", reload=True, port=8000)
