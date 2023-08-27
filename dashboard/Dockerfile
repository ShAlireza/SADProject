FROM node:16.15.0 as builder

WORKDIR /app

COPY package*.json ./

RUN npm install 

COPY . .

RUN npm run generate

FROM docker.io/nginx:1.22.0 as production-stage

COPY --from=builder /app/dist /usr/share/nginx/html

RUN sed -i 's/#error_page  404/error_page  404/g' /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

