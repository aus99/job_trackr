Instructions to run Job Trackr

To run the Job Trackr locally, follow these steps:

1. First, clone the gitlab repository at https://git.cs.bham.ac.uk/projects-2023-24/aus135.
    
2. Open the repository using an IDE such as PyCharm or Visual Studio Code, with Python installed.
    
3. Navigate to the 'aus135' directory and create virtual environment using the command 'py -m venv .venv'.

4. Install Python 3 on your machine if you do not already have it at https://www.python.org/downloads/.
    
5. Activate the virtual machine using the command 'venv/Scripts/activate'. To deactivate it, run the command 'deactivate'(This step and previous   step will differ depending on the Operating system of your machine). 
    
6. Navigate to the 'jobtrackr_backend' directory and run the command 'python manage.py runserver' to start the backend.
    
7. Open another terminal, navigate to the 'jobtrackr_frontend' directory and run the command 'npm run serve' to start the frontend.
    
8. Go to  http://localhost:8080/ to start using Job Trackr!