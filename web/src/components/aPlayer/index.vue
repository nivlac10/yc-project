<template>
	<el-dialog v-model="dialogVisible" :show-close="false" :close-on-click-modal="false" :close-on-press-escape="false"
		:width="store.state.status.isPc ? '402px' : '100%'">
		<div class="audio">
			<div class="audio_title">
				<span>{{ t('aPlayer.Música') }}</span>
				<img src="@assets/images/public/Shutdownx.png" alt="" @click="store.state.music.musicShow = false">
			</div>
			<div class="audio_volume" v-if="store.state.status.isPc">
				<div class="audio_volume_name">{{ t('aPlayer.Música') }}</div>
				<div class="audio_volume_progress_rate">
					<el-slider v-model="store.state.music.audioVolume" @change="changeAudioVolume" />
				</div>
				<div class="audio_volume_img">
					<img v-if="store.state.music.audioVolume > 0" src="@assets/images/audio/yinliang.png" alt="">
					<img v-else src="@assets/images/audio/yinliang_false.png" alt="">
				</div>
			</div>
			<div class="audio_music">
				<div class="audio_music_name text_hiding">
					{{ store.state.music.audioUrlList[store.state.music.currentAudioIdx].name }}
				</div>
				<div class="audio_music_time">
					<div class="audio_music_time_current">{{ store.state.music.audioStart }}</div>
					<div class="audio_music_time_progress_rate">
						<el-slider v-model="store.state.music.audioDuration" :show-tooltip="false" show-input :debounce="10"
							size="small" @change="changeAudioDuration" />
					</div>
					<div class="audio_music_time_total">{{ store.state.music.duration }}</div>
				</div>
				<div class="audio_music_operate">
					<div class="audio_music_operate_mode" @click="changeAudioPlayStatus">
						<img :src="store.state.music.audioPlayStatusList[store.state.music.audioPlayStatus]['img']" alt="">
						<div>{{ store.state.music.audioPlayStatusList[store.state.music.audioPlayStatus]['title'] }}</div>
					</div>
					<div class="audio_music_operate_play">
						<img src="@assets/images/audio/shangyiqu.png" alt="" @click="chengeNextAudioPlay(0)">
						<img
							:src="store.state.music.audioStatus == 'play' ? getImageUrl('audio/bofangzhong.png') : getImageUrl('audio/zanting.png')"
							alt="" @click="playAudio">
						<img src="@assets/images/audio/xiayiqu.png" alt="" @click="chengeNextAudioPlay(1)">
					</div>
					<div class="audio_music_operate_num">
						<div>{{ store.state.music.audioUrlList.length || '--' }}</div>
						<div>{{ t('aPlayer.Transferido') }}</div>
					</div>
				</div>
			</div>
			<div class="audio_list">
				<ul>
					<li :class="{ active: store.state.music.currentAudioIdx == index }"
						v-for="(item, index) in store.state.music.audioUrlList" :key="index" @click="selectAudio(index)">
						<div>
							<img v-if="store.state.music.currentAudioIdx == index" src="@assets/images/audio/music_play.png" alt="">
							<span v-else>{{ index + 1 }}</span>
						</div>
						<div class="text_hiding">{{ item.name }}</div>
					</li>
				</ul>
			</div>
		</div>
	</el-dialog>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, ref, onMounted, nextTick, computed } from "vue";
import { useRouter } from "vue-router";
import { store as stores, useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import { getImageUrl } from "@/utils/baseFun";
import { mapGetters } from "vuex";

export default defineComponent({
	name: "about",
	setup() {
		const { proxy } = getCurrentInstance() as any;
		const router = useRouter();
		const { t } = useI18n();
		const store = useStore();
		const state = reactive({
			dialogVisible: true
		});

		// const { audioPlayStatusList } = mapGetters('musicModule', ['audioPlayStatusList'])

		onMounted(() => {
			nextTick(() => {
				// 设置播放音乐的位置
				if (document.querySelector('.audio_list ul')) {
					(document.querySelector('.audio_list ul') as any).scrollTo({
						top: parseInt(document.querySelector('.audio_list ul li')?.clientHeight as any) * store.state.music.currentAudioIdx,
						behavior: 'smooth'
					});
				}
			})
		})

		const audioRef: any = ref(null)

		// 修改下一首音频播放
		const chengeNextAudioPlay = (val: number) => {
			store.dispatch('music/setChengeNextAudioPlay', val)
		}

		// 播放暂停控制
		const playAudio = () => {
			store.dispatch('music/setPlayAudio')
		}

		/**
		 * @description: 修改音频播放时间
		 * @param {*} val 返回的百分比数值
		 * @return {*}
		 */
		const changeAudioDuration = (val: number) => {
			store.dispatch('music/setChangeAudioDuration', val)
		}
		/**
		 * @description: 修改音频音量
		 * @param {*} val 返回的百分比数值
		 * @return {*}
		 */
		const changeAudioVolume = (val: number) => {
			store.dispatch('music/setChangeAudioVolume')
		}

		// 更新进度条与当前播放时间
		const updateProgress = (e) => {
			store.dispatch('music/setUpdateProgress', e)
		}

		// 修改音频播放状态
		const changeAudioPlayStatus = () => {
			store.dispatch('music/setChangeAudioPlayStatus')
		}

		const selectAudio = (index: number) => {
			store.state.music.currentAudioIdx = index
			store.commit('music/playAudioFun', store.state.music.audioDom)
		}

		return {
			...toRefs(state), store, t, getImageUrl, updateProgress, audioRef, playAudio,
			changeAudioDuration, changeAudioVolume, changeAudioPlayStatus, chengeNextAudioPlay, selectAudio
		};
	},
});
</script>
<style  lang="scss" scoped>
.audio {
	width: 402px;
	user-select: none;
	padding: 10px 16px 20px 16px;
	background-color: #202431;
	border-radius: 12px;
	box-sizing: border-box;

	.audio_title {
		position: relative;
		padding: 20px 0;
		text-align: center;

		span {
			font-size: 18px;
			font-weight: 600;
			color: #FFFFFF;
		}

		img {
			cursor: pointer;
			position: absolute;
			top: 5px;
			right: 0;
			width: 20px;
		}
	}

	.audio_volume {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 18px;
		padding: 8px 16px;
		margin-bottom: 12px;
		background: #2F3445;
		border-radius: 8px;

		.audio_volume_name {
			font-size: 14px;
			color: #FFFFFF;
		}

		.audio_volume_progress_rate {
			width: 100%;

			:deep(.el-slider) {
				.el-slider__runway {
					height: 3px;
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
					width: 16px;
					height: 16px;
				}
			}
		}

		.audio_volume_img {
			img {
				width: 30px;
			}
		}
	}

	.audio_music {
		padding: 16px 12px;
		margin-bottom: 12px;
		background: #2F3445;
		border-radius: 8px;
		box-sizing: border-box;

		.audio_music_name {
			width: 100%;
			display: block !important;
			padding: 0 0 15px 0;
			text-align: center;
			white-space: nowrap;
			font-size: 14px;
			color: #FFFFFF;
		}

		.audio_music_time {
			display: flex;
			justify-content: space-between;
			align-items: center;
			gap: 16px;
			margin-bottom: 10px;
			font-size: 12px;
			color: #B2B6C5;

			.audio_music_time_current {}

			.audio_music_time_progress_rate {
				width: 100%;

				:deep(.el-slider) {
					.el-slider__runway {
						height: 3px;
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
						width: 16px;
						height: 16px;
					}
				}
			}

			.audio_music_time_total {}
		}

		.audio_music_operate {
			display: flex;
			align-items: center;
			justify-content: space-between;

			.audio_music_operate_mode {
				cursor: pointer;
				width: 20%;
				text-align: center;

				img {
					width: 24px;
				}

				div {
					font-size: 12px;
					color: #B2B6C5;
				}
			}

			.audio_music_operate_play {
				display: flex;
				align-items: center;
				gap: 40px;

				img {
					cursor: pointer;
					width: 24px;
					height: 24px;

					&:nth-child(2) {
						width: 42px;
						height: 42px;
					}
				}
			}

			.audio_music_operate_num {
				width: 20%;
				text-align: center;
				color: #B2B6C5;

				div:nth-child(1) {
					margin-bottom: 6px;
					font-size: 18px;
				}

				div:nth-child(2) {
					font-size: 12px;
				}
			}
		}
	}

	.audio_list {
		padding: 5px;
		background: #2F3445;
		border-radius: 8px;

		ul {
			height: 300px;
			overflow-y: scroll;

			li {
				cursor: pointer;
				display: flex;
				align-items: center;
				padding: 13px 10px;
				font-size: 13px;
				color: #B2B6C5;

				&:hover {
					color: #fff;
					background: rgba(32, 36, 49, 0.4);
					border-radius: 4px;
				}

				&.active {
					color: #fff;
					background: rgba(32, 36, 49, 0.4);
					border-radius: 4px;
				}

				div:nth-child(1) {
					margin-right: 10px;

					img {
						width: 12px;
						height: 12px;
					}
				}

				div:nth-child(2) {
					display: block !important;
					white-space: nowrap;
				}
			}
		}
	}
}

@media (max-width: 768px) {
	.audio {
		padding: 5px 10px;
		margin: 0 10px;
		width: calc(100% - 20px);

		.audio_title {
			padding: 10px 0 20px 0;

			span {
				font-size: 16px;
			}

			img {
				top: 5px;
			}
		}

		.audio_volume {
			padding: 5px;
			margin-bottom: 10px;

			.audio_volume_name {
				font-size: 12px;
			}

			.audio_volume_img {
				img {
					width: 25px;
				}
			}
		}

		.audio_music {
			padding: 5px;
			margin-bottom: 10px;

			.audio_music_name {
				padding: 5px 0 5px 0;
				text-align: center;
			}

			.audio_music_time {
				margin-bottom: 0px;
			}

			.audio_music_operate {
				.audio_music_operate_mode {
					width: 25%;
					text-align: center;

					img {
						width: 30px;
					}
				}

				.audio_music_operate_play {
					gap: 20px;

					img {
						width: 35px;
					}
				}

				.audio_music_operate_num {
					width: 25%;
				}
			}
		}

		.audio_list {
			padding: 10px;
			box-shadow: 0px 0px 12px rgba(0, 0, 0, .12);
			background-color: #2f3445;
			border-radius: 6px;

			ul {
				height: 300px;
				font-size: 12px;
			}
		}
	}
}
</style>
  