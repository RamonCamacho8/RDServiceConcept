FROM node:16-alpine

WORKDIR /app
COPY client/package.json .
RUN npm install
COPY client/ .

ENV NODE_ENV production
RUN npm run build

EXPOSE 3000
CMD ["npm", "run", "preview"]