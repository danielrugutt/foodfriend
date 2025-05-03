# FoodFriend
Search for recipes according to your diet, schedule meals, bookmark them, and more!

### Initial setup
Make sure Node and Python are installed on your machine first!
1. Clone the repo into your current directory
``` sh
git clone https://github.com/danielrugutt/foodfriend
```

2. Set up a virtual environment (lets you install packages for this project instead of system wide):
``` sh
python -m venv venv
```

2a. WINDOWS - Activate the virtual environment
``` sh
.\venv\Scripts\activate
```

2b. LINUX/MAC - Activate the virtual environment
``` sh
source venv/bin/activate
```

3. Install all python requirements
``` sh
python -m pip install -r requirements.txt
```

4. Install all frontend requirements
``` sh
npm install
```

5. Install firebase-tools, and follow all prompts afterwards
``` sh
npm install -g firebase-tools
```

6. Make .env & firebase-auth.json in the root directory, and download the keys from Sendto 

### To run
If using a venv and not in it, make sure to start it first.

WINDOWS - Activate the virtual environment
``` sh
.\venv\Scripts\activate
```

LINUX/MAC - Activate the virtual environment
``` sh
source venv/bin/activate
```

Then run it with this!
``` sh
python app.py
```

Then go to http://127.0.0.1:5000 to use a local version of FoodFriend.


If you'd like to run the test file instead, run with this:
``` sh
python test_foodfriend.py
``` 

### Contributors
- Van Anderson: Van-Anderson
- Nick Kolesar: Indigenous1151
- Daniel Rugutt: danielrugutt
- Natalie Simova: naaatami
- Noah Ludy: Nludy12

URL to the live website:  https://foodfriend-a774e.web.app
