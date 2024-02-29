/*
 * @Author: wawodel 69891926+wawodel@users.noreply.github.com
 * @Date: 2023-12-04 17:55:16
 * @LastEditors: wawodel 69891926+wawodel@users.noreply.github.com
 * @LastEditTime: 2023-12-04 18:00:28
 * @FilePath: \Node-admin\express-admin\ecosystem.config.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
module.exports = {
    apps: [
        {
            name: "1winpg",
            script: "./bin/www",
            instances: "max",
            // exec_mode: "cluster",
            log_file: "./logs/access.log",
            error_file: "./logs/error.log",
            out_file: "./logs/out.log", // 重定向标准输出到文件
            merge_logs: true,
            env: {
                PORT: 5000, // Specify the port you want to use
                NODE_ENV: "production", // You can set other environment variables here
            },
        }
    ]
};
