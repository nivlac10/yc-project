<template>
    <div class="user_info_max_box">
        <el-radio-group v-model="size">
            <el-radio label="large">大号</el-radio>
            <el-radio label="default">默认</el-radio>
            <el-radio label="small">小号</el-radio>
        </el-radio-group>
        <el-descriptions :column="isPc ? 4 : 1" :size="size" class="mt-2" direction="vertical" border title="基本信息">
            <el-descriptions-item label="用户名">{{ user_info.nickname }}</el-descriptions-item>
            <el-descriptions-item label="手机号">{{ user_info.phone }}</el-descriptions-item>
            <el-descriptions-item label="邮箱">{{ user_info.email }}</el-descriptions-item>
            <el-descriptions-item label="渠道">{{ user_info.cname }}</el-descriptions-item>
            <el-descriptions-item label="VIP等级">{{ user_info.vip_lv }} / {{ user_info.vip_low_lv }}</el-descriptions-item>
            <el-descriptions-item label="邀请人ID">
                <el-tag @click="goToUserInfo(user_info.parent_id)" class="ml-3">{{ user_info.parent_id ? user_info.parent_id
                    : "无"
                }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="邀请人上级ID">
                <el-tag @click="goToUserInfo(user_info.super_id)" class="ml-3">{{ user_info.super_id ? user_info.super_id :
                    "无"
                }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="邀请人上上级ID">
                <el-tag @click="goToUserInfo(user_info.super_parent_id)" class="ml-3">{{ user_info.super_parent_id ?
                    user_info.super_parent_id : "无" }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="注册时间">{{ user_info.add_time }}</el-descriptions-item>
            <el-descriptions-item label="登录时间">{{ user_info.login_time }}</el-descriptions-item>
            <el-descriptions-item label="在线游戏">
                {{ user_info.flag }}
                <el-tag @click="" class="ml-3" v-if="user_info.cur_gameid > 0">下线</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="SBO余额">
                {{ user_info.SBO_money }}
                <el-tag @click="" class="ml-3" v-if="user_info.SBO_money > 0">转出</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="白名单" class="withdraw_str">
                <el-select v-model="withdraw_type" class="m-1" placeholder='' @change="change_withdraw_type()">
                    <el-option v-for="item in type_list" :label="item['label']" :value="item['val']" :key="item" />
                </el-select>
            </el-descriptions-item>
            <el-descriptions-item label="CPF">{{ user_info.CPF ? user_info.CPF : "未填写" }}</el-descriptions-item>
            <el-descriptions-item label="提款姓名">{{ user_info.username ? user_info.username : "未填写" }}</el-descriptions-item>
        </el-descriptions>
        <el-descriptions :column="isPc ? 4 : 1" :size="size" class="mt-2" direction="vertical" border title="钱包信息">
            <el-descriptions-item label="当前余额">{{ user_info.money }}</el-descriptions-item>
            <el-descriptions-item label="总充值">{{ user_info.total_money }}</el-descriptions-item>
            <el-descriptions-item label="总提现">{{ user_info.total_withdraw }}</el-descriptions-item>
            <el-descriptions-item label="充提差">{{ user_info.total_money - user_info.total_withdraw }}</el-descriptions-item>
            <el-descriptions-item label="剩余打码量">{{ user_info.remain_code_amount }}</el-descriptions-item>
            <el-descriptions-item label="总压分">{{ user_info.total_bet }}</el-descriptions-item>
            <el-descriptions-item label="总赢分">{{ user_info.total_shu_ying }}</el-descriptions-item>

            <el-descriptions-item label="实际输赢">


                <div style="display: flex; align-items: center; justify-content: space-between;"><span>{{
                    user_info.total_shu_ying - user_info.total_bet }}</span>
                    <el-button @click="heshi()" type="primary">核实SBO输赢</el-button>
                </div>
            </el-descriptions-item>
            <el-descriptions-item label="剩余佣金">{{ user_info.commission }}</el-descriptions-item>
            <el-descriptions-item label="总佣金">{{ user_info.total_commission }}</el-descriptions-item>
        </el-descriptions>
        <el-descriptions :column="isPc ? 4 : 1" :size="size" class="mt-2" direction="vertical" border title="赠送数据">
            <el-descriptions-item label="总赠送">{{ user_info.give_money }}</el-descriptions-item>
            <el-descriptions-item label="首充">{{ user_info.first_recharge_give }}</el-descriptions-item>
            <el-descriptions-item label="每日首充">{{ user_info.day_first_recharge_give }}</el-descriptions-item>
            <el-descriptions-item label="日签到">{{ user_info.sign_bonus }}</el-descriptions-item>
            <el-descriptions-item label="补给箱">{{ user_info.loss_bonus }}</el-descriptions-item>
            <el-descriptions-item label="转轮赠送">{{ user_info.roller_money }}</el-descriptions-item>
            <el-descriptions-item label="优惠券">{{ user_info.give_code_money }}</el-descriptions-item>
            <el-descriptions-item label="下载apk赠送">{{ user_info.download_bonus }}</el-descriptions-item>
            <el-descriptions-item label="系统赠送">{{ user_info.system_give }}</el-descriptions-item>
            <el-descriptions-item label="充值成就">{{ user_info.recharge_achieve }}</el-descriptions-item>
            <el-descriptions-item label="打码反水">{{ user_info.vip_count }}</el-descriptions-item>
        </el-descriptions>
    </div>
</template>
<script>
import { reactive, toRefs, getCurrentInstance, defineComponent, computed } from "vue";
import { storeToRefs } from "pinia";
import confStore from "@/store/modules/conf";
import { goToUserInfo } from "@/utils/baseFun"
import { user_sbo_bet_log_heshi, withdraw_type_post } from "@/api/userManagenment/index"
import { ElLoading } from 'element-plus'
export default defineComponent({
    name: "index",
    props: {
        data: {
            // type:
        }
    },
    setup(props, { emit }) {
        const store = confStore();
        let { isPc } = storeToRefs(store);
        const state = reactive({
            size: '',
            user_info: props.data,
            type_list: [
                { val: 0, label: '正常' },
                { val: 1, label: '审核' },
                { val: 2, label: '白名单' }
            ],
            withdraw_type: props.data.withdraw_type
        });
        // 切换table文字大小
        const iconStyle = computed(() => {
            const marginMap = {
                large: '8px',
                default: '6px',
                small: '4px',
            }
            return {
                marginRight: marginMap[state.size] || marginMap.default,
            }
        })
        const heshi = () => {
            const loading = ElLoading.service({
                lock: true,
                text: 'Loading',
                background: 'rgba(0, 0, 0, 0.7)',
            })
            user_sbo_bet_log_heshi({ uid: state.user_info.uid }).then((res) => {
                emit("loadUserInfo")
                loading.close()
            })
        }
        const change_withdraw_type = () => {
            console.log(state.withdraw_type)
            withdraw_type_post({ withdraw_type: state.withdraw_type, uid: state.user_info.uid }).then((res) => { })
        }
        return { ...toRefs(state), iconStyle, storeToRefs, props, isPc, goToUserInfo, heshi, change_withdraw_type };
    },
});
</script>
<style  lang= scss  scoped>
.user_info_max_box {}

.el-descriptions {
    margin-top: 20px;
}

.cell-item {
    display: flex;
    align-items: center;
}
</style>
  