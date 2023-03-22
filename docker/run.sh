docker run -v  $(pwd)/..:/ws \
           --name cs-251-project-maestro \
           -i -t -p 8888:8888 ghjeong12/maestro-micro2020-tutorial \
           /bin/bash