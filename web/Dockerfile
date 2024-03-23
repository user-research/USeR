# pull official base image
FROM node:20-alpine

# set working directory
WORKDIR /usr/src/user

# install app dependencies
COPY package.json .
COPY package-lock.json .

RUN npm ci

COPY . .