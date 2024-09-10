FROM node:21 AS build
WORKDIR /app
COPY package.json ./
COPY package-lock.json ./
RUN npm install
COPY . .
RUN npm run build


FROM nginx:1.24
WORKDIR /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/templates/default.conf.template
COPY --from=build /app/dist /usr/share/nginx/html
ENV VITE_API_BASE_URL http://localhost:5000
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]