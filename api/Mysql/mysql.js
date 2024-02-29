const { mysqlConf } = require('./../DBconfig')
const mysql = require('mysql2/promise');
const dbConfig = {
    host: mysqlConf.DBHOST,
    user: mysqlConf.DBUSER,
    password: mysqlConf.DBPWD,
    database: mysqlConf.DBNAME,
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0,
    timezone: 'local', // 设置时区为本地时区
};
class MySQLDatabase {
    // 链接配置

    constructor() {
        // 创建连接池
    }

    async getOne(sql, values = []) {
        const pool = mysql.createPool(dbConfig);
        let data = null
        try {
            // 执行查询
            const [results, fields] = await pool.query(sql, values);
            if (results) {
                // console.log(results);
                if (results[0]) {
                    data = results[0]
                }
            }
        } catch (error) {
            console.error('执行查询时出错: ', error);
            throw error;
        }
        this.close(pool)
        return data;
    }
    async getAll(sql, values = []) {
        let data = null
        const pool = mysql.createPool(dbConfig);
        try {
            // 执行查询
            const [results, fields] = await pool.query(sql, values);
            if (results) {
                // console.log(results);
                data = results
            }
        } catch (error) {
            console.error('执行查询时出错: ', error);
            throw error;
        }
        this.close(pool)
        return data;
    }
    async awaitSql(sql, values = []) {
        let data = null
        const pool = mysql.createPool(dbConfig);
        try {
            // 执行查询
            const [results, fields] = await pool.query(sql, values);
            if (results) {
                // console.log(results,fields);
                data = results.affectedRows
                this.close(pool)
                return data;
            }
        } catch (error) {
            console.error('执行时出错: ', error);
            throw error;
        }
        this.close(pool)
        return data;
    }
    async sql(sql, values = []) {
        let data = null
        const pool = mysql.createPool(dbConfig);
        try {
            // 执行查询
            pool.query(sql, values).then((results, fields) => {
                if (results) {
                    // console.log(results);
                    data = results.affectedRows
                }
                this.close(pool)
                return data;
            }).catch(() => {
                this.close(pool)
                return data;
            });
        } catch (error) {
            this.close(pool)
            console.error('执行时出错: ', error);
            throw error;
        }
    }
    async affairs(sqlList) {
        let data = false
        let connection;
        try {
            const pool = mysql.createPool(dbConfig);
            // 从连接池中获取连接
            connection = await pool.getConnection();

            // 开始事务
            await connection.beginTransaction();
            for (let i = 0; i < sqlList.length; i++) {
                const sql = sqlList[i];

                await connection.query(sql, null);
            }
            // 执行事务中的 SQL 查询
            // 提交事务
            await connection.commit();
        } catch (error) {
            // 如果发生错误，回滚事务
            if (connection) {
                data = false
                await connection.rollback();
            }

            console.error('事务失败:', error.message);
        } finally {
            // 释放连接
            if (connection) {
                connection.release();
            }
        }
        data = true
        return data
    }
    close(pool) {
        try {
            // 关闭连接池
            pool.end();
            // console.log('数据库连接池已关闭。');
        } catch (error) {
            console.error('关闭连接池时出错: ', error);
            throw error;
        }
    }
}

module.exports = MySQLDatabase