# Flask-Headline-App

## Steps to Launch the App
1. Install Python3.
```
sudo yum install -y python3
```

2. Download app from Github
```
wget https://github.com/SQLConjuror/headlines/archive/refs/heads/master.zip

unzip master.zip

cd headlines-master
```

3. Install & Create virtual environment.
```
pip3 install virtualenv
python3 -m venv venv
```

4. Activate the virtual environment.
```
source venv/bin/activate
```

5. Install Flask.
```
pip3 install flask
```

6. Upgrade pip 
```
pip install --upgrade pip
```

7. Install required packages
```
pip3 install -r app/requirements.txt
```

8. Run app
```
python3 run.py
```

9. Go to your browser and view the app
<serverIP/hostname>:5000
