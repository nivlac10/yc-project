// redisClient.js
const { redisConf } = require('./../DBconfig')
const Redis = require('ioredis');
const redisClient = new Redis({
    host: redisConf.HOST,  // Redis 服务器地址
    port: redisConf.PORT,  // Redis 服务器端口，默认是 6379
    db: redisConf.DB
});

module.exports = redisClient;
