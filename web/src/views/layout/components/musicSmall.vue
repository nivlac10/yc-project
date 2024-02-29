<template>
	<div class="musicSmall">
		<div class="music_name text_hiding">
			{{ store.state.conf.all_conf['music_list'][store.state.music.currentAudioIdx].name }}
		</div>
		<div class="audio_music_time_progress_rate">
			<el-slider v-model="store.state.music.audioDuration" :show-tooltip="false" show-input :debounce="10" size="small"
				@change="changeAudioDuration" />
		</div>
		<div class="img_list">
			<img :src="store.state.music.audioPlayStatusList[store.state.music.audioPlayStatus]['img']" alt=""
				@click="changeAudioPlayStatus">
			<img src="@assets/images/audio/shangyiqu.png" alt="" @click="chengeNextAudioPlay(0)">
			<img
				:src="store.state.music.audioStatus == 'play' ? getImageUrl('audio/bofangzhong.png') : getImageUrl('audio/zanting.png')"
				alt="" @click="playAudio">
			<img src="@assets/images/audio/xiayiqu.png" alt="" @click="chengeNextAudioPlay(1)">
			<img src="@assets/images/audio/bofangliebiao.png" alt="" @click="changeMusicShow">
		</div>
	</div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import { getImageUrl } from "@/utils/baseFun";
export default defineComponent({
	name: "musicSmall",
	setup() {
		const { proxy } = getCurrentInstance() as any;
		const router = useRouter();
		const { t } = useI18n();
		const store = useStore();
		const state = reactive({
		});

		/**
		 * @description: 修改音频播放时间
		 * @param {*} val 返回的百分比数值
		 * @return {*}
		 */
		const changeAudioDuration = (val: number) => {
			store.dispatch('music/setChangeAudioDuration', val)
		}

		// 修改下一首音频播放
		const chengeNextAudioPlay = (val: number) => {
			store.dispatch('music/setChengeNextAudioPlay', val)
		}

		// 播放暂停控制
		const playAudio = () => {
			store.dispatch('music/setPlayAudio')
		}

		// 修改音频播放状态
		const changeAudioPlayStatus = () => {
			store.dispatch('music/setChangeAudioPlayStatus')
		}

		// 显示音频组件
		const changeMusicShow = () => {
			store.state.music.musicShow = true
			if (!store.state.status.isPc) store.state.status.sidebarIsShow = false
		}

		return { ...toRefs(state), store, t, getImageUrl, changeAudioDuration, chengeNextAudioPlay, playAudio, changeAudioPlayStatus, changeMusicShow };
	},
});
</script>
<style  lang="scss" scoped>
.musicSmall {
	position: relative;
	margin-top: 33px;
	padding: 11px 17px;
	background: #2F3445;
	border-radius: 4px;

	&::after {
		content: "";
		position: absolute;
		top: -16.6px;
		left: 0;
		width: 100%;
		border-top: 1px solid #585E77;
	}

	.music_name {
		margin-bottom: 5px;
		display: block !important;
		text-align: center;
		font-size: 12px;
		color: #B2B6C5;
	}

	.audio_music_time_progress_rate {
		width: 100%;

		:deep(.el-slider) {
			.el-slider__runway {
				height: 1px;
				margin-right: 0;

				.el-slider__bar {
					height: 100%;
				}
			}

			.el-input-number {
				display: none;
			}

			.el-slider__button {
				transform: translateY(-2px);
				border: none;
				width: 8px;
				height: 8px;
			}
		}
	}

	.img_list {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 10px;

		img {
			cursor: pointer;
			display: block;
			width: 20px;

			&:nth-child(3) {
				width: 34px;
			}
		}
	}
}

@media (max-width: 768px) {}
</style>
  