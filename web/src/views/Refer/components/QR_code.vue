<template>
	<div class="QR_code_page_">
		<div class="logo">
			<!-- <img src="@assets/images/public/newLogo.png" alt="">
			<img src="@assets/images/refer/newRefer/logo_h.png" alt=""> -->
			<img :src="store.state.conf.all_conf.platform['platform_title_icon_url']" alt="">
		</div>
		<div class="code">
			<vueQr :text="inviteLink"></vueQr>
		</div>
		<div class="b_box">
			<div class="img_box">
				<img src="@assets/images/refer/newRefer/br.png" alt="">
				<img src="@assets/images/refer/newRefer/pix.png" alt="">
			</div>
			<p>De Brasileiros para Brasileiros!</p>
			<p>{{ store.state.conf.all_conf.platform['platform_path'] }}</p>
		</div>
	</div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, watch } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import vueQr from 'vue-qr/src/packages/vue-qr.vue'
import html2canvas from 'html2canvas'

export default defineComponent({
	name: "QR_code_page_",
	components: { vueQr },
	setup(props) {
		const { proxy } = getCurrentInstance() as any;
		const router = useRouter();
		const { t } = useI18n();
		const store = useStore();
		const state = reactive({
			inviteLink: store.state.conf.all_conf.share_conf['url'] + store.state.user.uid
		});

		const toSave = () => {
			const candom: any = document.querySelector(".QR_code_page_")
			html2canvas(candom).then((canvas) => {
				let saveUrl = canvas.toDataURL("image/png");    //将图片元素转成base64图片
				let aLink = document.createElement("a");
				let blob = base64ToBlob(saveUrl);    //将base64转成blob流
				let evt = document.createEvent("HTMLEvents");
				evt.initEvent("click", true, true);
				aLink.download = new Date().getTime() + ".png";
				aLink.href = URL.createObjectURL(blob);  //转成下载链接
				aLink.click();
			});
		};

		// 这里把图片转base64
		const base64ToBlob = (code: any) => {
			let parts = code.split(";base64,");
			let contentType = parts[0].split(":")[1];
			let raw = window.atob(parts[1]);
			let rawLength = raw.length;
			let uInt8Array = new Uint8Array(rawLength);
			for (let i = 0; i < rawLength; ++i) {
				uInt8Array[i] = raw.charCodeAt(i);
			}
			return new Blob([uInt8Array], { type: contentType });
		}

		return { ...toRefs(state), store, t, props, toSave };
	},
});
</script>
<style  lang="scss" scoped>
.QR_code_page_ {
	width: 375px;
	background: url(@assets/images/refer/newRefer/backdrop.png) no-repeat;
	background-size: 100% 100%;
	// border-radius: 12px;
	overflow: hidden;
	margin: 0;

	.logo {
		padding-top: 32px;

		img {
			display: block;
			margin: 0 auto;
		}

		img:nth-child(1) {
			width: auto;
		}

		img:nth-child(2) {
			width: 260px;
		}
	}

	.code {
		margin-bottom: 30px;
		text-align: center;

		img {
			width: 248px;
			height: 243px;
			border-radius: 12px;
		}
	}

	.b_box {
		padding: 30px 40px;
		background: #172035;
		box-sizing: border-box;
		// border-radius: 0px 0px 20px 20px;

		.img_box {
			display: flex;
			justify-content: space-between;

			img:nth-child(1) {
				width: 81px;
				height: 57px;
			}

			img:nth-child(2) {
				width: 170px;
				height: 57px;
			}
		}

		p {
			text-align: center;
			font-size: 20px;
			white-space: nowrap;
		}

		p:nth-last-child(2) {
			padding: 20px 0;
			color: #C3CFD9;
		}

		p:nth-last-child(1) {
			color: #63B6FF;
		}
	}
}

@media (max-width: 768px) {}
</style>
  