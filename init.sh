# Venv
venv_folder="venv"
if [ ! -d "$venv_folder" ]
then
    echo "Venv Directory doesn't exist. Creating now"
    python3 -m venv venv
    echo "Venv Directory created"
else
    echo "Venv Directory exists"
fi
# Result Directory
if [ ! -d "./KsdNaverOCRServer/result" ]
then
    echo "result Directory doesn't exist. Creating now"
    mkdir ./KsdNaverOCRServer/result
    echo "result Directory created"
else
    echo "result Directory exists"
fi


# python3 -m pip install virtualenv
source venv/bin/activate
pip3 install -r requirements.txt
uvicorn KsdNaverOCRServer.main:app --reload --host 0.0.0.0 --port 8000
