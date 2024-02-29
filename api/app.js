var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var morgan = require('morgan');
// 域资源共享模块
const cors = require('cors');
// 文件写入模块
const fs = require('fs');
// 创建一个日志文件
const logFilePath = path.join(__dirname, 'logs', 'access.log');
const accessLogStream = fs.createWriteStream(logFilePath, { flags: 'a' });
const redis = require('./Redis/index')


var app = express();
// 添加中间件以解析 x-www-form-urlencoded 格式的请求体
app.use(express.urlencoded({ extended: true }));

// 使用中间件来获取用户真实 IP 地址
app.use((req, res, next) => {
  // 尝试获取 X-Real-IP 头部
  const realIp = req.headers['x-real-ip'];
  // 如果 X-Real-IP 头部不存在，尝试获取 X-Forwarded-For 头部
  // X-Forwarded-For 头部可能包含多个 IP 地址，取第一个作为真实 IP
  if (!realIp) {
    const forwardedFor = req.headers['x-forwarded-for'];
    if (forwardedFor) {
      const ipArray = forwardedFor.split(',');
      realIp = ipArray[0].trim();
    }
  }

  // 将真实 IP 存储在 req.realIp 中，以便后续路由使用
  req.realIp = realIp || req.connection.remoteAddress;
  next();
});

// 防抖
app.use(async (req, res, next) => {
  const ip = req.realIp; // 假设你已经从用户登录信息中提取了唯一标识符
  // 检查缓存中是否存在用户标识符，如果存在则表示已经在处理中
  const currentPath = req.url;
  const redisKey = ip + '_' + currentPath
  if (await redis.get("wait:" + redisKey)) {
    res.send({ code: 40 });
  } else {

    await redis.setex("wait:" + redisKey, 10, '1'); // 设置过期时间为10秒

    // 执行下一个中间件或路由处理程序
    next();
    // 标记用户标识符为处理中
    // 处理完成后清除标记
    await redis.del("wait:" + redisKey);
  }
});

// 使用morgan中间件，将日志记录到文件中
app.use(morgan('tiny', { stream: accessLogStream }));
// 设置跨域
app.use(cors());
// app.use((req, res, next) => {
//   res.header('Access-Control-Allow-Origin', '*');
//   res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization');
//   res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
//   res.header('Access-Control-Allow-Credentials', 'true');
//   next();
// });
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());






// 导入路由
// 测试
var usersRouter = require('./routes/users');
app.use('/users', usersRouter);

// 登录注册
var apiLogin = require('./routes/api_login')
app.use('/', apiLogin);
// 配置
var apiConf = require('./routes/api_conf')
app.use('/', apiConf);
// 首页
var home = require('./routes/api_home')
app.use('/', home);
// 兑换码
var apiGiveCode = require('./routes/api_give_code')
app.use('/', apiGiveCode);
// 补给箱
var apiLossMoneyBonus = require('./routes/api_loss_money_bonus')
app.use('/', apiLossMoneyBonus);
// 邀请奖金
var apiInviteTask = require('./routes/api_invite_task')
app.use('/', apiInviteTask);
// 旋转转盘
var apiRollerMoney = require('./routes/api_roller_money')
app.use('/', apiRollerMoney);
// 充值签到
var apiSign = require('./routes/api_sign')
app.use('/', apiSign);
// 获取游戏链接
var api_game = require('./routes/api_game')
app.use('/', api_game);
// 用户订单查询
var apiUserOrders = require('./routes/api_user_orders')
app.use('/', apiUserOrders);
// refer团队信息
var apiUserReferRecord = require('./routes/api_user_refer_record')
app.use('/', apiUserReferRecord);
// 用户
var apiUser = require('./routes/api_user')
app.use('/', apiUser);
// PG操作
//var game_pg = require('./routes/game_pg')
//app.use('/', game_pg);
// VIP
var api_vip_reward = require('./routes/api_vip_reward')
app.use('/', api_vip_reward);
// 支付
var apiPay = require('./routes/api_pay')
app.use('/', apiPay);
// 充值成就
var api_recharge_achieve_bonus = require('./routes/api_recharge_achieve_bonus')
app.use('/', api_recharge_achieve_bonus)
// 发送验证码
var senMsg = require('./routes/sen_msg')
app.use('/', senMsg)
// 获取游戏反水列表
var api_rebate = require('./routes/api_rebate');
app.use('/', api_rebate)
// 提现
var apiWithdrawal = require('./routes/api_withdrawal')
app.use('/', apiWithdrawal)

// sailspay回调
//var order_callback_sailspay = require('./routes/order_callback_sailspay')
//app.use('/', order_callback_sailspay)

// PG操作
var { router_pg_sw } = require('./routes/game_pg_sw')
app.use('/', router_pg_sw);

//Dove Cash
var api_Dove_Cash = require('./routes/api_Dove_Cash')
app.use('/', api_Dove_Cash);







// catch 404 and forward to error handler
app.use((req, res, next) => {
  res.status(404).send("404 Not Found");
});

// error handler
app.use(function (err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};
  // render the error page
  res.status(err.status || 500);
  res.render('error');
});
// 在应用关闭时关闭 Redis 客户端
app.on('close', () => {
});
module.exports = app;
