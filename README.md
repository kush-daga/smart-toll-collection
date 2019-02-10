# smart-toll-collection

This is a computer vision project aiming in helping reduce traffic at the toll booths.

#PROBLEM
The problem that we aim to address is the increasing amount of traffic in the tolls, even after the introduction of
fasTag in India, still there is alot of traffic jams as there are only two lanes in most places and many non fasTag users
also enter the lanes. We are proposing a solution to silve this issue.

#Technology Used
We are using Flask combined with openCV and libraries like numpy to identify the license plates and recognize the characters of the plate.
Right now we are using stock photos for testing out our application which you can input in line 38 in Main.py in app/views/ml/.

#Installation

1. Clone this repo and make a virtualenv if you wish to, im using python3 in this project.
2. Then install the requirements via "pip install -r requirements.txt" command.
3. Run the run.py file and open the localhost:4000 page on your browser. (python run.py OR python3 run.py)
4. After the installation you will notice three images showing basic steps of image processing, click the pic and enter any key to continue.
5. Open the browser and see the result, you will see the identified plate number shown.

# For a smaple form we are proposing to use viist localhost:4000/form

Visit the website for more information after running it locally.

Screenshots :
![Alt text](relative/screesnhots/1.png)(?raw=true "Title")
