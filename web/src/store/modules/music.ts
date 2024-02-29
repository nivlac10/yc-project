import { Module } from 'vuex';
import { musicState, RootStateTypes } from '@/store/interface/index';
import { getImageUrl } from '@/utils/baseFun';
import i18n from '@/lang/index.js'
import { computed } from "vue";
/**
 * @description: 音频播放时间换算
 * @param {*} time 音频当前播放时间，单位秒
 * @return {*}
 */
const transTime = (time: string) => {
	var duration = parseInt(time);
	var minute: any = parseInt((duration / 60).toString());
	var sec = (duration % 60) + "";
	var isM0 = ":";
	if (minute === 0) minute = "00";
	else if (minute < 10) minute = "0" + minute;

	if (sec.length === 1) sec = "0" + sec;

	return minute + isM0 + sec;
}

const musicModule: Module<musicState, RootStateTypes> = {
	namespaced: true,
	state: {
		musicShow: false,
		audioDom: '',
		audioUrl: '', // 音频地址
		currentAudioIdx: 0, // 当前播放音频的索引
		audioUrlList: [], // 音频列表
		audioVolume: 100, // 音量
		audioDuration: 0, // 音频当前播放时间 百分比
		audioStart: "00:00", // 音频当前播放时间 时间格式
		duration: "00:00", // 音频总时间
		audioStatus: 'pause', // 音频状态
		audioPlayStatus: 0, // 音频播放状态
		audioPlayStatusList: [
			{ title: 'asdfsd', img: getImageUrl('audio/liebiaoxunhuan.png') },
			{ title: computed(() => i18n.global.t("aPlayer.Aleatório")).value, img: getImageUrl('audio/suijibofang.png') },
			{ title: computed(() => i18n.global.t("aPlayer.Repetir")).value, img: getImageUrl('audio/danquxunhuan.png') },
		],
	},
	getters: {
		audioPlayStatusList(state) {
			return state.audioPlayStatusList
		}
	},
	mutations: {
		// 设置播放音频模式
		getPlayAudioMode(state: any, data: number) {
			// 列表循环播放
			if (state.audioPlayStatus == 0) {
				if (state.currentAudioIdx + 1 == state.audioUrlList.length) state.currentAudioIdx = 0
				else state.currentAudioIdx += 1
				// 随机播放
			} else if (state.audioPlayStatus == 1) {
				state.currentAudioIdx = Math.round(Math.random() * (state.audioUrlList.length - 1))
			} else if (state.audioPlayStatus == 2) {

			}
		},
		// 修改下一首音频播放
		chengeNextAudioPlay(state: any, data: number) {
			if (data == 0) {
				if (state.currentAudioIdx == 0) state.currentAudioIdx = state.audioUrlList.length - 1
				else state.currentAudioIdx -= 1
			} else {
				if (state.currentAudioIdx + 1 == state.audioUrlList.length) state.currentAudioIdx = 0
				else state.currentAudioIdx += 1
			}
		},
		/**
		 * @description: 播放音频方法
		 * @return {*} data 音频dom
		 */
		playAudioFun(state: any, data: any) {
			// 设置播放地址
			data.src = state.audioUrl = state.audioUrlList[state.currentAudioIdx].path
			setTimeout(() => {
				// 设置播放音乐的位置
				if (document.querySelector('.audio_list ul')) {
					(document.querySelector('.audio_list ul') as any).scrollTo({
						top: parseInt(document.querySelector('.audio_list ul li')?.clientHeight as any) * state.currentAudioIdx,
						behavior: 'smooth'
					});
				}
				state.audioStatus = "play";
				data.play();
			}, 100);
		},
		// 播放暂停控制
		playAudio(state: any, data: any) {
			if (data.paused) {
				data.play();
				state.audioStatus = "play";
			} else {
				data.pause();
				state.audioStatus = "pause";
			}
		},
		// 修改音频播放时间
		changeAudioDuration(state: any, data: any) {
			let wdiv = 100;
			// 只有音乐开始播放后才可以调节，已经播放过但暂停了的也可以
			let ratemin = data / wdiv;
			let rate = ratemin * 100;
			state.audioDuration = rate;
			state.audioDom.currentTime = state.audioDom.duration * ratemin;
		},
		// 修改音频音量
		changeAudioVolume(state: any, data: any) {
			let audio = state.audioDom;
			audio.volume = state.audioVolume / 100;
		},
		// 更新进度条与当前播放时间
		updateProgress(state: any, data: any) {
			var value = data.target.currentTime / data.target.duration;
			if (data.target.currentTime === data.target.duration) {
				state.audioStatus = "pause";
			}
			state.audioDuration = value * 100
			state.audioStart = transTime(state.audioDom.currentTime)
		},
		// 修改音频播放状态
		changeAudioPlayStatus(state: any, data: any) {
			switch (state.audioPlayStatus) {
				case 0:
					state.audioPlayStatus = 1
					break;
				case 1:
					state.audioPlayStatus = 2
					break;
				case 2:
					state.audioPlayStatus = 0
					break;
				default:
					break;
			}
		}
	},
	actions: {
		// 修改下一首音频播放
		async setChengeNextAudioPlay({ commit, state }, data: number) {
			// 获取音频播放状态
			if (state.audioPlayStatus == 0 || state.audioPlayStatus == 2) commit('chengeNextAudioPlay', data);
			else commit('getPlayAudioMode', data);
			commit('playAudioFun', state.audioDom)
		},
		// 播放暂停控制
		async setPlayAudio({ commit, state }, data: any) {
			commit('playAudio', state.audioDom);
		},
		// 设置播放音频模式 音乐结束时调用的
		async setPlayAudioMode({ commit, state }, data: any) {
			commit('getPlayAudioMode', data);
			commit('playAudioFun', state.audioDom)
		},
		// 修改音频播放时间
		async setChangeAudioDuration({ commit }, data: any) {
			commit('changeAudioDuration', data);
		},
		// 修改音频播放时间
		async setChangeAudioVolume({ commit }, data: any) {
			commit('changeAudioVolume', data);
		},
		// 更新进度条与当前播放时间
		async setUpdateProgress({ commit, state }, data: any) {
			commit('updateProgress', data);
		},
		// 修改音频播放状态
		async setChangeAudioPlayStatus({ commit, state }, data: any) {
			commit('changeAudioPlayStatus', data);
		},
	},
};

export default musicModule;
