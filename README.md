# Flask api form angular / Assurance Prediction

# Créer un environnement virtuel
python -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
# if db.sqlite existe la supprimer
python
>>> from app import db
>>> db.create_all()
>>> exit()
python app.py

