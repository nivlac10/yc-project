
// 验证用户token中间件
const redis = require('../Redis/index')

const auth = async (req, res, next) => {
    req.uid = 0
    let user_token = req.body?.token || '';
    if (user_token === '') {
        // console.log(req.body);
        user_token = req.headers['token'] || '';
        if (user_token === '') {
            return next();
        }
    }
    const token_key = 'user_login_token_' + String(user_token);
    const con = await redis.get(token_key);
    if (con === null) {
        return next();
    }
    const only_key = 'only_user_' + String(con);
    const data = await redis.get(only_key);
    if (data === null) {
        return next();
    }
    if (data !== String(user_token)) {
        return next();
    }
    req.uid = con; // 设置 uid 到上下文中
    next();
}

module.exports = auth
