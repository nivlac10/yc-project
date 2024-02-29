const RKEY = require('../RKEY')
var express = require('express');
var router = express.Router();
const userDataUtil = require('../utils/userDataUtil');
const redis = require('../Redis/index')
const axios = require('axios');
const { SESClient, SendEmailCommand } = require("@aws-sdk/client-ses");
const constant = require('../constant')
/* const sesClient = new SESClient({
    region: '', // 替换为你的 AWS 区域
    credentials: {
        accessKeyId: '', // 替换为你的 AWS Access Key ID
        secretAccessKey: '', // 替换为你的 AWS Secret Access Key
    },
}); */
const SMS_CONF = {
    'lcyz': {
        'name': '创蓝云智',
        'func': chuan_lang_yun_zhi
    },
}


// 发送手机短信验证码

router.all("/api/send_phone_code", async (req, res) => {
    let data = {}
    data['code'] = 0
    data['msg'] = 'fail in send'
    try {
        let phone = req.body.phone.replace(/\s/g, '')
        console.log(phone);
        if (await redis.get('send_sms_' + String(phone))) {
            data['msg'] = 'The verification code has been sent. Please try again later'
            data['code'] = 1
            return res.send(data)
        }
        let sms_key = await redis.hget('san_game_all_conf', 'sms_conf')
        let flag = false
        let num = 0
        if (sms_key) {
            let smsData = await SMS_CONF[sms_key]['func'](phone)
            flag = smsData[0]
            num = smsData[1]
            if (!flag) {
                return res.send(data)
            }
        }
        redis.setex(String(phone), 300, String(num))
        redis.setex('send_sms_' + String(phone), 60, '1')
        data['code'] = 1
        data['msg'] = 'success'
        return res.send(data)
    } catch (error) {
        console.log(error);
    }
})

// 发送邮箱验证码
router.all("/api/send_email_code", async (req, res) => {
    let data = {}
    data['code'] = 0
    data['msg'] = 'fail in send'
    try {
        const email = req.body.email.replace(/\s/g, '')
        if (await redis.get('send_sms_' + email)) {
            data['msg'] = 'The verification code has been sent. Please try again later'
            data['code'] = 1
            return res.send(data)
        }
        const num = Math.floor(Math.random() * (9999 - 1000 + 1) + 1000);
        send_verification_code(email, num)
        redis.setex(String(email), 300, String(num))
        redis.setex('send_sms_' + String(email), 60, '1')
        data['code'] = 1
        data['msg'] = 'success'
        return res.send(data)
    } catch (error) {
        console.log(error);
    }
})


// 发送手机验证码
async function chuan_lang_yun_zhi(mobile) {
    const num = Math.floor(Math.random() * (9999 - 1000 + 1) + 1000);
    const codeTemplate = (await redis.hget('san_game_all_conf', 'code_template')) || '';

    let smsCodeTemplate;
    if (codeTemplate) {
        smsCodeTemplate = JSON.parse(codeTemplate);
    } else {
        return [false, num];
    }

    smsCodeTemplate = smsCodeTemplate['lcyz'];

    const data = {
        account: constant.CHUANG_LANG_YUN_ZHI_ACCOUNT,
        password: constant.CHUANG_LANG_YUN_ZHI_PASSWORD,
        msg: smsCodeTemplate.replace('<code>', String(num)),
        mobile: String(mobile),
    };
    console.log(data);
    const url = '';
    try {
        const response = await axios.post(url, data, {
            headers: {
                'Content-Type': 'application/json',
            },
            timeout: 10000,
        });
        console.log(response.data);
        const flag = String(response.data.code) === '0';
        return [flag, num];
    } catch (error) {
        console.error('Error sending request:', error.message);
        return [false, num];
    }
}



// 发送验证码邮件函数
const send_verification_code = async (recipientEmail, code) => {
    // 邮件参数
    const params = {
        Source: '', // 发送者邮箱
        Destination: {
            ToAddresses: [recipientEmail], // 接收者邮箱
        },
        Message: {
            Subject: {
                Data: 'Verification Code', // 邮件主题
            },
            Body: {
                Text: {
                    Data: `Your verification code is: ${code}`, // 邮件正文
                },
            },
        },
    };

    try {
        // 使用 SES 客户端发送邮件
        const command = new SendEmailCommand(params);
        const result = await sesClient.send(command);

        console.log('Email sent successfully:', result.MessageId);
        return true;
    } catch (error) {
        console.error('Error sending email:', error.message);
        return false;
    }
};


module.exports = router