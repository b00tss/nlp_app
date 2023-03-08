# NLP_APP

This repository holds the code to start topic modeling  web application. The web application is created with django and the source files are in the  **webapp** folder. You can start the app locally by building and running the docker application. The web applications uses a machine learning model which is created with the scripts in **ml_scripts** folder.

## Running the docker

Make sure to have a local installation of docker, and execute the build scripts with:

    ./build.sh
You can now run the application with the run script:

    ./run.sh
You can visit the app in your browser on the following url:

    172.0.0.0.1:8000
Use the following predefined user to login:

**username:** testApp

**password:** this2pass
