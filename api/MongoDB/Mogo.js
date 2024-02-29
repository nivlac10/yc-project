const { MongoClient } = require('mongodb');
const { mongoConf } = require('./../DBconfig')
class MongoDB {
    static async connectToMongoDB() {
        try {
            const client = await MongoClient.connect(mongoConf.URL, { useNewUrlParser: true, useUnifiedTopology: true });
            const db = client.db(mongoConf.dbName);
            return db;
        } catch (error) {
            console.error('Failed to connect to MongoDB:', error);
            throw error;
        }
    }

    static async insertOne(tablename, tableinfo) {
        const db = await this.connectToMongoDB();
        const collection = db.collection(tablename);
        const document = tableinfo;

        const result = await collection.insertOne(document);

        // 关闭连接
        db.client.close();

        return result.insertedCount; // 返回插入的行数
    }

    static async get(tablename, query, page, pageSize) {
        const db = await this.connectToMongoDB();
        const collection = db.collection(tablename);

        // 分页逻辑
        const skipAmount = (page - 1) * pageSize;

        // 执行查询
        const cursor = collection.find(query).skip(skipAmount).limit(pageSize);

        // 将查询结果转为数组
        const result = await cursor.toArray();

        // 在这里可以对查询结果进行处理

        // console.log('Query Result:', result);

        // 关闭连接
        db.client.close();

        return result;
    }

    static async updateOne(tablename, query, update) {
        const db = await this.connectToMongoDB();
        const collection = db.collection(tablename);

        const result = await collection.updateOne(query, { $set: update });

        // 关闭连接
        db.client.close();

        return result.modifiedCount; // 返回修改的行数
    }

    static async deleteOne(tablename, query) {
        const db = await this.connectToMongoDB();
        const collection = db.collection(tablename);

        const result = await collection.deleteOne(query);

        // 关闭连接
        db.client.close();

        return result.deletedCount; // 返回删除的行数
    }
}

module.exports = MongoDB