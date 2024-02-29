// // 引入 crypto 模块用于计算 MD5
// const crypto = require("crypto");

// function generateSortedQueryString(params, secretKey) {
//   // 1. 将参数名按照 ASCII 码从小到大排序
//   const sortedKeys = Object.keys(params).sort();

//   // 2. 构建键值对字符串
//   const keyValuePairs = sortedKeys
//     .filter(key => params[key] !== null && params[key] !== undefined && params[key] !== "")
//     .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`);

//   // 3. 使用 & 符号连接键值对字符串
//   const queryString = keyValuePairs.join("&");

//   // 4. 在 data 最后拼接上 &key={Secret key}
//   const dataString = queryString + `&key=${encodeURIComponent(secretKey)}`;

//   return dataString;
// }

// function calculateMD5(data) {
//   // 5. 对 data 进行 MD5 运算得到 sign 值
//   const md5 = crypto.createHash("md5");
//   md5.update(data, "utf8");
//   return md5.digest("hex");
// }

// // 示例参数集合
// const params = {
//   mchNo: "bingwin777",
//   time: "2023-12-10 16:56:31",
//   fee: "100",
//   orderNo: "2023-12-10 16:56:3180732",
//   type: "gcash",
//   notifyUrl: "https://api.1winpg.com/api/do_pay_notify_manage",
//   backUrl: "https://www.1winpg.com",
//   notifytype: "json"
// }

// // 示例 Secret Key
// const secretKey = "450EBA72EB7746748C1A7BB7B1FC8443";

// // 生成排序后的 URL 键值对字符串
// const sortedQueryString = generateSortedQueryString(params, secretKey);

// // 计算 MD5 签名
// const sign = calculateMD5(sortedQueryString);

// console.log(sign);



console.log(Math.floor(Date.now()))