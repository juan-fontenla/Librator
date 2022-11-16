FROM node:14.15.5-slim

RUN mkdir -p /app/client

WORKDIR /app/client

RUN apt update && apt -y upgrade && apt -y install curl git

# Downloading and installing NVM
RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.39.1/install.sh | bash

# Installing NVM version, removing node_modules (to force refresh dependencies),
# .... installing node dependencies and building the product in the dist folder
CMD /bin/bash -l -c "nvm install $(cat .nvmrc);" \ "nvm use;" && npm install && npm run serve
