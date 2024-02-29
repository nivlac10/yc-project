<template>
    <div class="fbAndGoogle">
        <div class="title">
            <img src="../../../assets/images/public/popover_return.png" alt="" @click="close">
            <span>{{ t('login.ACCOUNTLOGINSETUP') }}</span>
        </div>
        <div v-show="isOtp">
            <div class="item" @click="fbLogin">
                <img src="../../../assets/images/login/Facebook.png" alt="">
                <span>{{ t('login.Facebookaccounthasbeen') }}</span>
                <img src="../../../assets/images/public/arrow_right.png" alt="">
            </div>

            <div class="item" @click="">
                <img src="@assets/images/login/Google.png" alt="" />
                <!-- googleLogin -->
                <div class="google_max_box">
                    <div id="g_id_onload"
                        data-client_id="916158791940-haoduo5h3ns6hig87itgmactgi2t0fo0.apps.googleusercontent.com"
                        data-context="signin" data-ux_mode="popup" data-callback="handleCredential"
                        data-auto_prompt="false"></div>

                </div>
                <div class="google_login_box">
                    <div style="   opacity: 0; position: absolute; top:0;left 0;  width:100%;" class="g_id_signin"
                        data-type="icon" data-shape="rectangular" data-theme="filled_blue" data-text="signin_with"
                        data-size="" data-logo_alignment="left" data-width="100%">
                    </div>

                </div>


                <span>{{ t('login.Googleaccounthasbeen') }}</span>
                <img src="../../../assets/images/public/arrow_right.png" alt="">
            </div>
            <p class="font">{{ t('login.ItwillbechangedtoPHONEorEMAILon') }} <span>{{ t('login.Avoidlosing') }}</span></p>
        </div>
        <div class="fbAndGoogleLogin" v-show="!isOtp">
            <div class="item2" v-show="(type == 'fb')">
                <img src="../../../assets/images/login/Facebook.png" alt="">
                <span>{{ t('login.Facebookaccounthasbeen') }}</span>
            </div>
            <div class="item2" v-show="(type == 'gg')">
                <img src="../../../assets/images/login/Google.png" alt="">
                <span>{{ t('login.Googleaccounthasbeen') }}</span>
            </div>
            <el-form ref="formRef" :model="validateForm" label-width="0" :rules="rules" class="demo-ruleForm">
                <el-form-item label="" prop="phone">
                    <div class="input_box input_box_phone">
                        <div class="input_box_l input_box_l_phone">
                            <span>+{{ t("base.countryCode") }}</span>
                            <img src="@assets/images/public/down_arrow.png" alt="" />
                        </div>
                        <el-input v-model="validateForm.phone" :placeholder="t('login.EnterPhoneNumber')" />
                    </div>
                </el-form-item>
                <el-form-item label="" prop="password">
                    <div class="input_box input_box_password">
                        <div class="input_box_l">
                            <img src="@assets/images/login/lock.png" alt="" />
                        </div>
                        <el-input v-model="validateForm.password" type="password" :placeholder="t('login.EnterPassword')"
                            show-password />
                    </div>
                </el-form-item>
                <el-form-item label="" prop="otp">
                    <div class="input_box input_box_code">
                        <div class="input_box_l">
                            <img src="@assets/images/login/shield.png" alt="" />
                        </div>
                        <el-input v-model="validateForm.otp" :placeholder="t('login.EnterVerificationCode')" />
                        <div class="sl_box_shadow" @click="getCode">
                            <span v-if="codeTime == 0">{{ t("login.CODE") }}</span>
                            <el-countdown title="" format="ss" :value="codeTime" @finish="finish" v-else />
                        </div>
                    </div>
                </el-form-item>

            </el-form>
            <div class="btn" @click="setPwd">{{ t('login.setUP') }} </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, computed } from "vue";
import { useI18n } from "vue-i18n";
import { debounce } from "@/utils/baseFun";
import { UserService } from "@/api/user";
import { useStore } from "@/store/index";
import { LoginService } from "@/api/login";
import { SuccessNotiFun } from "@/utils/baseFun";
const store = useStore();


const emit = defineEmits(["def"])
const { t } = useI18n();
let type = ref('');
let isOtp = ref(true);
let validateForm = reactive({
    phone: "",
    password: "",
    otp: "",
});
let verify_token = ref();
let countryCode = computed(() => t("base.countryCode"));// 国家区号

let googleToken = ref();
let fbToken = ref();


const setPwd = (() => {
    store.dispatch('status/setLoadingShow', true)
    LoginService.user_verify_bind_pwd({ phone: countryCode.value + validateForm.phone, password: validateForm.password, otp: validateForm.otp, verify_token: verify_token.value }).then((res) => {
        if (res.data.code == 1) {
            SuccessNotiFun(t('login.bindingsuccessful'))
            close();
        }
    })
    store.dispatch('status/setLoadingShow', false)
})


const close = () => {
    if (isOtp.value == false) {
        isOtp.value = true
    } else {
        emit('def', false);
    }
};
const formRef = ref();



const tofbAndGoogleLogin = (data) => {

    isOtp.value = false;
    type.value = data;
    console.log(type.value == 'gg');
};
const validatePass = (rule, value, callback) => {
    if (value === "") {
        callback(new Error(t("login.EnterPassword")));
    } else {
        if (validateForm.password !== "") {
            if (!formRef.value) return;
            formRef.value.validateField("checkPass", () => null);
        }
        callback();
    }
};

const rules = reactive({
    phone: [
        {
            // validator: validatePhone,
            required: true,
            message: t("login.EnterPhoneNumber"),
            trigger: "blur",
        },
    ],
    password: [{ validator: validatePass, trigger: "blur" }],
    otp: [
        {
            required: true,
            message: t("login.EnterVerificationCode"),
            trigger: "blur",
        },
    ],
});
let codeTime = ref(0);
// 验证码结束
const finish = () => {
    codeTime.value = 0;
};
// 获取验证码
const getCode = () => {
    store.dispatch('status/setLoadingShow', true)
    if (
        validateForm.phone == "" ||
        codeTime.value != 0 ||
        validateForm.password == ""
    )
        return;
    const fun = () => {
        UserService.send_phone_code({
            phone: countryCode.value + validateForm.phone,
        }).then((res) => {
            if (res.data.code == 1) codeTime.value = Date.now() + 1000 * 60;
        });
        store.dispatch('status/setLoadingShow', false)
    };
    debounce(fun);
};

// @ts-ignore：
window.googleOrFb = 'google';

//fb js
const scriptFB = document.createElement("script");
scriptFB.src = "https://connect.facebook.net/en_US/sdk.js";
document.body.appendChild(scriptFB);
//google js
const script = document.createElement("script");
script.src = "https://accounts.google.com/gsi/client";
document.body.appendChild(script);

function fbLogin() {
    store.dispatch('status/setLoadingShow', true);
    // (window as any).fbAsyncInit();

    // @ts-ignore：
    FB.init({
        appId: "271631798860673", // 应用编号 3460020840937747
        autoLogAppEvents: true,
        cookie: true,
        xfbml: true,
        email: true,
        version: "v16.0",
    });

    // @ts-ignore：
    // 检查用户登录状态
    window.FB.getLoginStatus(function (response) {

        let code = localStorage.getItem("code") || "0";
        let cid = localStorage.getItem("c") || 1;
        if (response.status !== "connected") {

            // 未登录，fb会让用户登录
            window.FB.login((res) => {
                // 不管用户有没有登录都会有res
                window.FB.api(
                    "/me",
                    { fields: "email,name" },
                    function (response) {
                        //获取用户头像
                        window.FB.api(
                            response.id + "/picture",
                            "GET",
                            { redirect: "false", scope: 'email' },
                            function (pic) {
                                const data = {
                                    face_id: response.id,
                                    face_name: response.name,
                                    face_email: response.email,
                                    face_img: "0",
                                    code: code,
                                    cid: cid,
                                };


                                if (response.id) {
                                    facebookPost(data);
                                }
                            }
                        );
                    }
                );
            });
        } else {
            // 已登录过，fb直接返回response
            window.FB.api(
                "/me",
                { fields: "email,name" },
                function (response) {
                    //获取用户头像
                    window.FB.api(
                        response.id + "/picture",
                        "GET",
                        { redirect: "false", scope: 'email' },
                        function (pic) {
                            const data = {
                                face_id: response.id,
                                face_name: response.name,
                                face_email: response.email,
                                face_img: "0",
                                code: code,
                                cid: cid,
                            };
                            if (response.id) {
                                facebookPost(data);
                            }
                        }
                    );
                }
            );
        }

    });

    store.dispatch('status/setLoadingShow', false)
};

window.fbAsyncInit = async function fbAsyncInit() {
    // @ts-ignore：
};

function facebookPost(data) {
    store.dispatch('status/setLoadingShow', true)
    debounce(() => {
        LoginService.verify_facebook_user({ face_id: data.face_id }).then((res) => {
            console.log(res);
            if (res.data.code == 1) {
                verify_token.value = res.data.token;
                tofbAndGoogleLogin('fb')
            }
            store.dispatch('status/setLoadingShow', false)
        })


    })
}

//谷歌登录
window.handleCredential = function handleCredentialResponse(
    response
) {
    store.dispatch('status/setLoadingShow', true)
    // 获取回调响应的凭证数据 然后拿这个凭证给后台，后台jwt进行解析获取登录信息
    let response_code = response.credential;
    debounce(async () => {
        let res = await LoginService.verify_google_user({ google_token: response_code });
        console.log(res);
        if (res.data.code == 1) {
            verify_token.value = res.data.token;
            tofbAndGoogleLogin('gg');
        }
        store.dispatch('status/setLoadingShow', false)
    })

};


</script>

<style lang="scss" scoped>
.google_login_box {
    position: absolute;
    top: 0;
    width: 100%;
    height: 60px;
    opacity: 0;

    :deep(.nsm7Bb-HzV7m-LgbsSe.Bz112c-LgbsSe) {
        width: 100%;
        height: 60px;
    }
}

.fbAndGoogle {
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100%;
    width: 100%;

    .title {
        display: flex;
        align-items: center;
        margin-bottom: 30px;
        width: 100%;

        img {
            width: 42px;
            height: 42px;
            margin-right: 15px;
        }

        span {
            color: #FBD31E;
            font-size: 18px;
            font-weight: Bold;
        }

    }

    .item {
        // width: 100%;
        height: 60px;
        background: #45475B;
        border-radius: 12px;
        cursor: pointer;
        display: flex;
        // justify-content: center;
        justify-content: space-between;
        align-items: center;
        padding: 0 30px;
        margin-bottom: 20px;
        position: relative;
        .google_max_box{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
        }
        img {
            width: 31.69px;
            height: 31.69px;
        }

        span {
            // text-align: center;
            font-size: 12px;
            line-height: 14px;
            color: #C3CFD9;
            white-space: pre-wrap;
            margin: 0 10px;
        }
    }

    .item>img:nth-child(4) {
        width: 21.69px;
        height: 21.69px;
    }

    .font {
        color: #C3CFD9;
        font-size: 12px;
        line-height: 14px;

        span {
            color: #DEA541;
        }
    }

    .fbAndGoogleLogin {
        display: flex;
        flex-direction: column;
        justify-content: center;
        width: 100%;

        .item2 {
            border: 1.32px solid #53535C;
            border-radius: 12px;
            cursor: pointer;
            width: calc(100% - 20px);
            height: 60px;
            padding: 0 10px;
            margin-bottom: 20px;
            display: flex;
            justify-content: center;
            align-items: center;

            img {
                width: 31.69px;
                height: 31.69px;
            }

            span {
                text-align: center;
                font-size: 12px;
                line-height: 14px;
                color: #C3CFD9;
                white-space: pre-wrap;
                margin: 0 10px;
            }
        }
    }

    .btn {
        width: 100%;
        height: 50px;
        border-radius: 10px;
        background: #CA2E46;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 19px;
        line-height: 22px;
        font-weight: bold;
        color: #FFFFFF;
        box-shadow: inset 0px 6px 6px 0px rgba(207, 51, 78, 0.54), inset 2px -6px 6px 0px rgba(207, 51, 78, 0.58), inset -5px 0px 8px 0px rgba(207, 51, 78, 0.67), inset 0px -9px 11px 0px #CF334E, inset 0px -2px 0px 0px rgba(140, 27, 42, 0.8);
    }
}
</style>