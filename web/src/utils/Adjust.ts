
// 注册
export function register_adjust(email, phone) {
    //@ts-ignore
    Adjust.trackEvent({
        // other initialisation options go here
        eventToken: 'g1cl7w', // 注册
    });
    //@ts-ignore
    fbq('track', 'CompleteRegistration');
    if (localStorage.getItem('kwai_pixel') != "477914035590803478") {

        // @ts-ignore
        kwaiq.instance(localStorage.getItem('kwai_pixel')).track('completeRegistration')  // kwai注册
    }

    if (localStorage.getItem('kwai_pixel') == "477914035590803478") {

        //@ts-ignore
        kwaiq.instance(localStorage.getItem('kwai_pixel')).track("purchase")  //  kwai首充
    }
    //appAf上报
    appFlyerEvent('af_complete_registration', `${email, phone}`);
}
// 充值
export function rechage_adjust(money) {
    let first_rechage = localStorage.getItem("first_rechage") || 0
    if (first_rechage == 0) {
        //@ts-ignore
        Adjust.trackEvent({
            eventToken: 'q5amvw', // 首充
        });
        //@ts-ignore
        fbq('track', 'Purchase', { currency: "BRL", value: money });
        localStorage.setItem("first_rechage", '1')

        if (localStorage.getItem('kwai_pixel') != "477914035590803478") {
            //@ts-ignore
            kwaiq.instance(localStorage.getItem('kwai_pixel')).track("purchase")  //  kwai首充
        } else {
            //@ts-ignore
            kwaiq.instance(localStorage.getItem('kwai_pixel')).track('addToCart')  //  kwai首充
        }
        //appAf上报
        appFlyerEvent('af_purchase', `${money},RBL`);
    } else {

    }
}

//加入购物车
export function add_shopping_cart() {
    //@ts-ignore
    kwaiq.instance(localStorage.getItem('kwai_pixel')).track('addToCart');
}

//登录成功统一上报事件
export function signReport() {
    //appAf上报
    appFlyerEvent('af_login', "");
}



//埋点
export function appFlyerEvent(key, value) {
    // (window as any).alert(JSON.stringify(text));
    // alert(JSON.stringify(text));
    try {
        //@ts-ignore
        window.Native.sendEventCustom(key, value);
    } catch (error) {
        // alert(JSON.stringify(error))
        // console.log(error);
    }


}