FROM node:16-alpine

WORKDIR /app
COPY package.json .
RUN npm install
COPY . .

ENV VITE_API_URL=http://localhost:8000

ENV NODE_ENV production
RUN npm run build

EXPOSE 4173
CMD ["npm", "run", "preview"]
