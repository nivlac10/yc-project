import { get, post } from "@/utils/http";

export class LoginService {
	static login = (params?: object) => post('/user_phone_login', params);
	static register = (params?: object) => post('/user_phone_register', params);
	static getCode = (params?: object) => post('/send_phone_code', params);
	static user_forget_password = (params?: object) => post('/user_forget_password', params);
	static google_login = (params?: object) => post('/google_login', params);
	static facebook_login = (params?: object) => post('/facebook_login', params);
	static app_google_login = (params?: object) => post('/app_google_login', params);
	static user_email_login = (params?: object) => post('/user_email_login', params);
	static user_email_register = (params?: object) => post('/user_email_register', params);
	static send_email_code = (params?: object) => post('/send_email_code', params);
	static user_forget_email_password = (params?: object) => post('/user_forget_email_password', params);
	static verify_google_user = (params?: object) => post('/verify_google_user', params);
	static verify_facebook_user = (params?: object) => post('/verify_facebook_user', params);
	static user_verify_bind_pwd = (params?: object) => post('/user_verify_bind_pwd', params);
	
}
