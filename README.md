# python-docker

A fetch receipt processor Python assignment.

## Docker specification
1.) Application Environment - Python <br />
2.) Python version - 3.9.12 <br />
3.) Port to listen on -  6055 <br />
4.) Command to run the flask app - <br /> ```python3 -m flask run --host=0.0.0.0 --port=6055```
<br />
Dependencies can be found in the requirements.txt file.

The Dockerfile and compose.yaml file is already present in the repo. To build and run the Python Docker application directly - <br />
```docker compose up --build``` <br />
Go to the home page - http://127.0.0.1:6055/ 
The above url will redirect to the - http://127.0.0.1:6055/receipts/process . We can input the JSON data in the textbox and submit it with the 'POST' request. Correct submission will result in Receipt ID response. This is the first API - process receipts call. (PS:  Save the receipts ID) <br />
Next, in order to know the points, go to link - http://127.0.0.1:6055/receipts/{id}/points . In place of {id}, use the id you got as response to above request. This link will send a 'GET' request and output total points rewarded. This is the second API - get points call. <br />

To stop the application - <br />
```docker compose down```



<br />
The application has been tested in the MacOS (Apple Silicon M1 chip). 
