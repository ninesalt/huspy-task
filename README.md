# huspy-task

To get started just `docker-compose up`. Additionally you can change the flag passed to the entrypoint script to `--prod`  in the docker compose file to run gunicorn instead of the default dev server. 

To run the tests, you can exec into the container and just run `pytest`