# Use an official Python runtime as an image
FROM python:3.9
ENV FLASK_APP app

# The EXPOSE instruction indicates the ports on which a container # # will listen for connections
# Since Flask apps listen to port 5000  by default, we expose it
EXPOSE 5000

# Sets the working directory for following COPY and CMD instructions
# Notice we haven’t created a directory by this name - this
# instruction creates a directory with this name if it doesn’t exist
WORKDIR /app

# install mariadb connector/c
RUN wget https://downloads.mariadb.com/MariaDB/mariadb_repo_setup
RUN echo "733cf126b03f73050e242102592658913d10829a5bf056ab77e7f864b3f8de1f  mariadb_repo_setup"     | sha256sum -c -
RUN chmod +x mariadb_repo_setup
RUN ./mariadb_repo_setup    --mariadb-server-version="mariadb-10.6"
RUN apt install libmariadb3 libmariadb-dev -y

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app
RUN pip install -r requirements.txt

# Load secrets
COPY .secrets_env_vars /app/.secrets_env_vars

COPY templates /app/templates

# Run app.py when the container launches
COPY app.py /app
# for debugging purposes only
# CMD ["sleep", "600"]
CMD ["flask", "run", "--host", "0.0.0.0"]
