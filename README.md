
Instructions:

set your google api key as an enviroment variable called "GOOGLE_API_KEY"
python -m venv venv (in the main directory if needed.)
venv\scripts\activate (to go into the virtual enviroment)
pip install -r requirements.txt (Install the nessesary requirements and dependencies.)
create a /data/input_pdfs folder for input pdfs.
python src/app.py (to run the app.)

make sure you put your pdf files in the /data/input_pdfs folder, then type in the essay question or topic.

Should now print out the original file name, page number, and the quote that the model selected.


TODO:

allow the user to input how many quotes they want, 1, 5, 10, 15... etc.
Allow users to upload files rather than having to place them in the /data/input_pdfs folder
