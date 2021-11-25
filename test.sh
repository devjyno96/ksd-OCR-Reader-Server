venv_folder="venv"

if [ ! -d "$venv_folder" ]
then
    echo "Venv Directory doesn't exist. Creating now"
    python3 -m venv venv
    echo "Venv Directory created"
else
    echo "Venv Directory exists"
fi

# python3 -m pip install virtualenv
source venv/bin/activate

python3 KsdNaverOCRServer/tests/main.py