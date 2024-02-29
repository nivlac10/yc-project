/**
 * 关于时间工具类
 */
class Time {
	/**
	 * 获取当前日期
	 * @return {Date} 当前日期对象
	 */
	static get_today() {
		return new Date();
	}

	/**
	 * 格式化日期为 "YYYY-MM-DD"
	 * @param {Date} date - 要格式化的日期对象
	 * @returns {string} - 格式化后的日期字符串
	 */
	static formatDate(date) {
		date = new Date(date);
		const year = date.getFullYear();
		const month = String(date.getMonth() + 1).padStart(2, '0');
		const day = String(date.getDate()).padStart(2, '0');
		return `${year}-${month}-${day}`;
	}
	/**
 * 格式化日期为 "YYYY-MM-DD-HH:mm:ss"
 * @param {Date} date - 要格式化的日期对象
 * @returns {string} - 格式化后的日期字符串
 */
	static formatDateHms(date) {
		date = new Date(date)
		const year = date.getFullYear();
		const month = String(date.getMonth() + 1).padStart(2, '0');
		const day = String(date.getDate()).padStart(2, '0');
		const hours = String(date.getHours()).padStart(2, '0');
		const minutes = String(date.getMinutes()).padStart(2, '0');
		const seconds = String(date.getSeconds()).padStart(2, '0');
		return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
	}


	/**
	 * 获取今天日期 y-m-d
	 * @return {string} 今天日期 y-m-d 格式
	 */
	static get_today_ymd() {
		const todayTime = this.formatDate(this.get_today());
		// console.log(todayTime);
		return todayTime;
	}

	/**
	 * 获取今天星期几的数字
	 * @return {number} 星期数 （0-6，0表示星期日，1表示星期一）
	 */
	static get_weekday() {
		const today = this.get_today();
		const dayOfWeek = today.getDay();
		return dayOfWeek;
	}

	/**
		* 获取昨天日期 
		* @return {string} 昨天日期  y-m-d格式
		*/
	static get_yesterday() {
		const yesterday = new Date();
		yesterday.setDate(yesterday.getDate() - 1);
		return this.formatDate(yesterday);
	}

	/**
	 * 获取前几天的日期
	 * @param {number} front_int  前几天
	 * @return {string} 前几天的日期 y-m-d格式
	 */
	static get_front_day(front_int) {
		const targetDate = new Date();
		targetDate.setDate(targetDate.getDate() - front_int);
		return this.formatDate(targetDate);
	}

	/**
		 * 获取前几天的日期的时分秒
		 * @param {number} front_int  前几天
		 * @return {string} 前几天的日期 d_h_s格式
		 */
	static get_front_day_h_s(front_int) {
		const targetDate = new Date();
		targetDate.setDate(targetDate.getDate() - front_int);

		const year = targetDate.getFullYear();
		const month = String(targetDate.getMonth() + 1).padStart(2, '0');
		const day = String(targetDate.getDate()).padStart(2, '0');
		const hours = String(targetDate.getHours()).padStart(2, '0');
		const minutes = String(targetDate.getMinutes()).padStart(2, '0');
		const seconds = String(targetDate.getSeconds()).padStart(2, '0');

		return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
	}


	/**
	 * 获取几天后的日期
	 * @param {number} back_int  几天后
	 * @return {string} 几天后的日期 Y-m-d 格式
	 */
	static get_back_day(back_int) {
		const targetDate = new Date();
		targetDate.setDate(targetDate.getDate() + back_int);

		const year = targetDate.getFullYear();
		const month = String(targetDate.getMonth() + 1).padStart(2, '0');
		const day = String(targetDate.getDate()).padStart(2, '0');

		return `${year}-${month}-${day}`;
	}

	/**
* 获取过去七天的日期
* @return {string} 过去七天的日期 Y-m-d 格式
*/
	static get_sevenday() {
		const targetDate = new Date();
		targetDate.setDate(targetDate.getDate() - 6);

		const year = targetDate.getFullYear();
		const month = String(targetDate.getMonth() + 1).padStart(2, '0');
		const day = String(targetDate.getDate()).padStart(2, '0');

		return `${year}-${month}-${day}`;
	}

	/**
* 获取本周第一天的日期
* @return {string} 本周第一天的日期 Y-m-d 格式
*/
	static get_this_week_start() {
		const targetDate = new Date();
		const dayOfWeek = targetDate.getDay();
		const difference = (dayOfWeek + 6) % 7;
		targetDate.setDate(targetDate.getDate() - difference);

		const year = targetDate.getFullYear();
		const month = String(targetDate.getMonth() + 1).padStart(2, '0');
		const day = String(targetDate.getDate()).padStart(2, '0');

		return `${year}-${month}-${day}`;
	}

	/**
* 获取上周第一天的日期
* @return {string} 上周第一天的日期 Y-m-d 格式
*/
	static get_last_week_start() {
		const targetDate = new Date();
		const dayOfWeek = targetDate.getDay();
		const difference = (dayOfWeek + 6) % 7;  // 修正本周开始是星期一的问题
		const daysToSubtract = dayOfWeek === 0 ? 6 : dayOfWeek - 1;  // 修正如果今天是星期天的情况

		targetDate.setDate(targetDate.getDate() - daysToSubtract - 7);  // 减去7天以获取上周

		const year = targetDate.getFullYear();
		const month = String(targetDate.getMonth() + 1).padStart(2, '0');
		const day = String(targetDate.getDate()).padStart(2, '0');

		return `${year}-${month}-${day}`;
	}

	/**
* 获取上周最后一天的日期
* @return {string} 上周最后一天的日期 Y-m-d 格式
*/
	static get_last_week_end() {
		const targetDate = new Date();
		const dayOfWeek = targetDate.getDay();
		const difference = (dayOfWeek + 6) % 7;  // 修正本周开始是星期一的问题
		const daysToSubtract = dayOfWeek === 0 ? 7 : dayOfWeek;  // 修正如果今天是星期天的情况

		targetDate.setDate(targetDate.getDate() - daysToSubtract);

		const year = targetDate.getFullYear();
		const month = String(targetDate.getMonth() + 1).padStart(2, '0');
		const day = String(targetDate.getDate()).padStart(2, '0');

		return `${year}-${month}-${day}`;
	}

	/**
		 * 获取下周一的日期
		 * @return {Date} 下周一的日期对象
		 */
	static get_next_week_monday() {
		const targetDate = new Date();
		const dayOfWeek = targetDate.getDay();
		const daysToAdd = dayOfWeek === 0 ? 1 : 8 - dayOfWeek;  // 修正如果今天是星期天的情况

		targetDate.setDate(targetDate.getDate() + daysToAdd);

		return targetDate;
	}
	/**
	 * 获取下个月一号的日期
	 * @return {Date} 下个月一号的日期对象
	 */
	static get_next_month_one() {
		const today = new Date();
		const firstDay = new Date(today.getFullYear(), today.getMonth() + 1, 1);
		return firstDay.toLocaleString();
	}

	/**
* 根据日期获取当天凌晨时间戳
* @param {Date} date - 要获取凌晨时间的日期对象
* @return {number} 当天凌晨的时间戳
*/
	static get_day_zero_time(date) {
		if (!date) {
			return null;
		}
		date = new Date(date)
		const dateZero = new Date(date);
		dateZero.setHours(0, 0, 0, 0);

		return dateZero.toLocaleString();
	}

	/**
* 获取当前时间到明日凌晨零点还有多少秒
* @return {number} 到明日凌晨零点的剩余秒数
*/
	static get_yesterday_zero_time() {
		// 获取当前时间
		const currentTime = new Date();
		// 获取明天的日期
		const tomorrow = new Date(currentTime);
		tomorrow.setDate(currentTime.getDate() + 1);
		tomorrow.setHours(0, 0, 0, 0);

		// 计算时间差并转换为秒数
		const timeDifference = tomorrow - currentTime;
		const secondsUntilMidnight = timeDifference / 1000;

		return secondsUntilMidnight;
	}

	/**
* 获取这月开始第一天
* @return {Date} 这个月开始的日期对象
*/
	static getThisMonthStart() {
		const today = new Date();
		const thisMonthStart = new Date(today.getFullYear(), today.getMonth(), 1);

		return thisMonthStart.toLocaleString();
	}

	/**
	 * 获取上月最后一天
	 * @return {Date} 上个月最后一天的日期对象
	 */
	static get_last_month_end() {
		const today = new Date();
		const thisMonthStart = new Date(today.getFullYear(), today.getMonth(), 1);
		const lastMonthEnd = new Date(thisMonthStart - 1);

		return lastMonthEnd.toLocaleString();
	}

	/**
	 * 获取上月开始第一天
	 * @return {Date} 上个月开始的日期对象
	 */
	static get_last_month_start() {
		const today = new Date();
		const thisMonthStart = new Date(today.getFullYear(), today.getMonth(), 1);
		const lastMonthEnd = new Date(thisMonthStart - 1);
		const lastMonthStart = new Date(lastMonthEnd.getFullYear(), lastMonthEnd.getMonth(), 1);

		return lastMonthStart.toLocaleString();
	}

	/**
* 获取前30天
* @return {Date} 30天前的日期对象
*/
	static getLastThirtyDays() {
		const today = new Date();
		const lastThirtyDays = new Date(today - 30 * 24 * 60 * 60 * 1000);

		return lastThirtyDays.toLocaleString();
	}

	/**
	 * 获取前60天
	 * @return {Date} 60天前的日期对象
	 */
	static getLastSixtyDays() {
		const today = new Date();
		const lastSixtyDays = new Date(today - 60 * 24 * 60 * 60 * 1000);

		return lastSixtyDays.toLocaleString();
	}

	/**
* 将时间戳转换为日期字符串（年月日时分秒）。
* @param {number} timestamp - 要转换的时间戳
* @returns {string} - 转换后的日期字符串
*/
	static int_day(timestamp) {
		// 使用 JavaScript 的 Date 对象进行时间戳转换
		const date = new Date(timestamp * 1000);

		// 格式化日期字符串
		const formattedDate = date.toLocaleString('en-US', { timeZone: 'UTC' }); // 替换 'en-US' 为你的语言环境

		return formattedDate;
	}

	/**
* 将时间戳转换为日期字符串（年月日）。
* @param {number} timestamp - 要转换的时间戳
* @returns {string} - 转换后的日期字符串
*/
	static int_ymd(timestamp) {
		// 使用 JavaScript 的 Date 对象进行时间戳转换
		const date = new Date(timestamp * 1000);

		// 获取年、月、日
		const year = date.getFullYear();
		const month = String(date.getMonth() + 1).padStart(2, '0'); // 月份从 0 开始，因此需要加 1
		const day = String(date.getDate()).padStart(2, '0');

		// 拼接日期字符串
		const formattedDate = `${year}-${month}-${day}`;

		return formattedDate;
	}

	/**
* 将时间戳转换为日期字符串（年月日时分秒）。
* @param {number} timestamp - 要转换的时间戳
* @returns {string} - 转换后的日期字符串
*/
	static int_ymds(timestamp) {
		// 使用 JavaScript 的 Date 对象进行时间戳转换
		const date = new Date(timestamp * 1000);

		// 获取年、月、日、时、分、秒
		const year = date.getFullYear();
		const month = String(date.getMonth() + 1).padStart(2, '0'); // 月份从 0 开始，因此需要加 1
		const day = String(date.getDate()).padStart(2, '0');
		const hours = String(date.getHours()).padStart(2, '0');
		const minutes = String(date.getMinutes()).padStart(2, '0');
		const seconds = String(date.getSeconds()).padStart(2, '0');

		// 拼接日期字符串
		const formattedDate = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;

		return formattedDate;
	}

	/**
* 将日期字符串转换为时间戳。
* @param {string} day - 要转换的日期字符串（格式为 'YYYY-MM-DD'）
* @returns {number} - 转换后的时间戳（以秒为单位）
*/
	static day_int(day) {
		// 使用 JavaScript 的 Date 对象和 getTime() 方法进行转换
		const timestamp = new Date(day).getTime() / 1000;

		return timestamp;
	}

	/**
* 将带有时分秒的日期字符串转换为时间戳。
* @param {string} day - 要转换的日期字符串（格式为 'YYYY-MM-DD HH:mm:ss'）
* @returns {number} - 转换后的时间戳（以秒为单位）
*/
	static days_int(day) {
		// 使用 JavaScript 的 Date 对象和 getTime() 方法进行转换
		const timestamp = new Date(day).getTime() / 1000;

		return timestamp;
	}

	/**
* 计算当前时间距离 00:00 还有多少秒。
* @returns {number} - 剩余秒数
*/
	static get_rest_time() {
		const now = new Date();
		const today_begin = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 0, 0, 0);
		const tomorrow_begin = new Date(today_begin);
		tomorrow_begin.setDate(today_begin.getDate() + 1);

		const rest_seconds = Math.floor((tomorrow_begin - now) / 1000); // 将毫秒转换为秒

		return rest_seconds;
	}

	/**
 * 获取指定年月的第一天和最后一天日期
 * @param {number} year - 年份，默认为当前年份
 * @param {number} month - 月份，默认为当前月份
 * @returns {Object} 包含第一天和最后一天日期的对象
 */
	static getMonthFirstDayAndLastDay(year, month) {
		const currentDate = new Date();
		year = year || currentDate.getFullYear();
		month = month || currentDate.getMonth() + 1;

		const firstDay = new Date(year, month - 1, 1);
		const lastDay = new Date(year, month, 0);

		// 转换为字符串
		const formattedFirstDay = this.formatDate(firstDay);
		const formattedLastDay = this.formatDate(lastDay);

		return {
			firstDay: formattedFirstDay,
			lastDay: formattedLastDay
		};
	}

	/**
* 根据创建时间计算距离当前时间的相对时间
* @param {Date} createTime - 创建时间的日期对象
* @returns {string} 相对时间字符串
*/
	static formatTime(createTime) {
		const createTimeTimestamp = Math.floor(createTime / 1000);
		const currentTime = Math.floor(Date.now() / 1000);
		const timeDifference = currentTime - createTimeTimestamp;

		if (timeDifference / 60 < 1) {
			return '刚刚';
		} else if (timeDifference / 60 < 60) {
			return `${Math.floor(timeDifference / 60)}分钟前`;
		} else if (timeDifference / 60 / 60 < 24) {
			return `${Math.floor(timeDifference / 60 / 60)}小时前`;
		} else if (timeDifference / 86400 < 30) {
			return `${Math.floor(timeDifference / 86400)}天前`;
		} else if (timeDifference / 86400 / 30 < 12) {
			return `${Math.floor(timeDifference / 86400 / 30)}月前`;
		} else {
			return '1年前';
		}
	}

	/**
	 * 判断两个日期是否相同
	 * @param {string} ymd1 - 第一个日期字符串（格式：YYYY-MM-DD）
	 * @param {string} ymd2 - 第二个日期字符串（格式：YYYY-MM-DD）
	 * @returns {number} - 相同返回1，不同返回0
	 */
	static judgeDateSame(ymd1, ymd2) {
		let flag = 0;
		if (ymd1 === ymd2) {
			flag = 1;
		}
		return flag;
	}

/**	
 * 获取本周是今年的第几周
 * 
 * @returns {number} 本周是今年的第几周
 */
	static get_how_year_week() {
		let today = new Date();
		let year = today.getFullYear();
		let firstDayOfYear = new Date(year, 0, 1);
		let daysSinceStart = Math.floor((today - firstDayOfYear) / (24 * 60 * 60 * 1000));
		let weekNumber = Math.ceil((today.getDay() + 1 + daysSinceStart) / 7);
		return weekNumber;
	}



}

// 导出工具类
module.exports = Time;

// let time = new Time();
// console.log(123, Time.formatDateHms(new Date('2023-06-28 21:32:55')));

