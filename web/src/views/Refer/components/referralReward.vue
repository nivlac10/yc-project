<template>
	<div class="referralReward">
		<invitation-information />
		<!-- <my-invite-bonus /> -->
		<extra-invitation-bonus />
		<lifetime-referral-bonus />
		<invitation-steps />
		<awards-already-received />
		<invitation-rules />
	</div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "@/store/index";
import { useI18n } from "vue-i18n";
import invitationInformation from "./invitationInformation.vue"
import myInviteBonus from "./myInviteBonus.vue";
import extraInvitationBonus from "./extraInvitationBonus.vue";
import lifetimeReferralBonus from "./lifetimeReferralBonus.vue"
import invitationSteps from "./invitationSteps.vue";
import invitationRules from "./invitationRules.vue"
import awardsAlreadyReceived from "./awardsAlreadyReceived.vue"
export default defineComponent({
	name: "referralReward",
	components: { invitationInformation, myInviteBonus, extraInvitationBonus, lifetimeReferralBonus, invitationSteps, invitationRules, awardsAlreadyReceived },
	setup() {
		const { proxy } = getCurrentInstance() as any;
		const router = useRouter();
		const { t } = useI18n();
		const store = useStore();
		const state = reactive({
		});
		return { ...toRefs(state), store, t, };
	},
});
</script>
<style  lang="scss" scoped>
.referralReward {}

@media (max-width: 768px) {}
</style>
  