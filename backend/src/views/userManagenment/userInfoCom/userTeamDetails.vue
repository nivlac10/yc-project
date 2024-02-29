<template>
    <div>
        <el-radio-group v-model="size">
            <el-radio label="large">大号</el-radio>
            <el-radio label="default">默认</el-radio>
            <el-radio label="small">小号</el-radio>
        </el-radio-group>
        <el-descriptions :column="isPc ? 4 : 1" :size="size" class="mt-2" direction="vertical" border title="团队信息">
            <!-- 人数 -->
            <el-descriptions-item label="团队总人数">{{ user_info['team_user_num'] }}</el-descriptions-item>
            <el-descriptions-item label="一级人数">{{ user_info['team_one_user_num'] }}</el-descriptions-item>
            <el-descriptions-item label="二级人数">{{ user_info['team_two_user_num'] }}</el-descriptions-item>
            <el-descriptions-item label="三级人数">{{ user_info['team_three_user_num'] }}</el-descriptions-item>
            <!-- 充值 -->
            <el-descriptions-item label="团队总充值">{{ user_info['team_one_recharge'] + user_info['team_two_recharge'] +
                user_info['team_three_recharge'] }}</el-descriptions-item>
            <el-descriptions-item label="一级充值">{{ user_info['team_one_recharge'] }}</el-descriptions-item>
            <el-descriptions-item label="二级充值">{{ user_info['team_two_recharge'] }}</el-descriptions-item>
            <el-descriptions-item label="三级充值">{{ user_info['team_three_recharge'] }}</el-descriptions-item>
            <!-- 打码 -->
            <el-descriptions-item label="团队总打码">{{ user_info['team_one_bet'] + user_info['team_two_bet'] +
                user_info['team_three_bet'] }}</el-descriptions-item>
            <el-descriptions-item label="一级打码">{{ user_info['team_one_bet'] }}</el-descriptions-item>
            <el-descriptions-item label="二级打码">{{ user_info['team_two_bet'] }}</el-descriptions-item>
            <el-descriptions-item label="三级打码">{{ user_info['team_three_bet'] }}</el-descriptions-item>
            <!-- 佣金详情 -->
            <el-descriptions-item label="邀请佣金">{{ user_info['share_task_brokerage'] + user_info['share_recharge_brokerage']
            }}</el-descriptions-item>
            <el-descriptions-item label="一级打码返佣">{{ user_info['bet_brokerage_one_money'] }}</el-descriptions-item>
            <el-descriptions-item label="二级打码返佣">{{ user_info['bet_brokerage_two_money'] }}</el-descriptions-item>
            <el-descriptions-item label="三级打码返佣">{{ user_info['bet_brokerage_three_money'] }}</el-descriptions-item>

            <el-descriptions-item label="首充佣金">{{ user_info['share_recharge_brokerage'] }}</el-descriptions-item>
            <el-descriptions-item label="邀请任务佣金">{{ user_info['share_task_brokerage'] }}</el-descriptions-item>
        </el-descriptions>
        <el-card class="mt-3">
            <div class="from_box">
                <datetime @def="timeChange"></datetime>
                <div>
                    <el-select v-model="searchForm.users_level" class="m-2" placeholder="全部">
                        <el-option v-for="item in level" :label="item['label']" :value="item['value']" />
                    </el-select>
                    <el-select v-model="searchForm.first_recharge" class="m-2" placeholder="全部">
                        <el-option v-for="item in first_recharge" :label="item['label']" :value="item['value']" />
                    </el-select>
                    <el-button type="primary" @click="searchData">搜索</el-button>
                </div>
                <div class="total_box">

                    <el-button type="success">充提差:{{ tableTotal['total_money_withdraw'] }}</el-button>

                    <el-button type="success">充值金额:{{ tableTotal['total_money'] }}</el-button>

                    <el-button type="success">提现金额:{{ tableTotal['total_withdraw'] }}</el-button>

                    <el-button type="success">新增人数:{{ tableTotal['count'] }}</el-button>

                    <el-button type="success">余额:{{ tableTotal['money'] }}</el-button>

                    <el-button type="success">充值人数:{{ tableTotal['first_recharge'] }}</el-button>

                </div>
            </div>

        </el-card>
        <el-card class="mt-3">
            <el-table v-loading="loading" :data="tableData" style="width: 100%">
                <el-table-column prop="add_time" label="注册时间" header-align="center" :align="'center'" sortable />
                <el-table-column prop="uid" label="用户id" header-align="center" :align="'center'">
                    <template #default="scope">
                        <el-button type="primary" @click="goToUserInfo(scope.row.uid)" style="width: 100%;">{{
                            `${scope.row.uid}(${scope.row.nickname})` }}</el-button>
                    </template>
                </el-table-column>
                <el-table-column prop="total_money" label="充值" header-align="center" :align="'center'" sortable>
                </el-table-column>
                <el-table-column prop="total_withdraw" label="提现" header-align="center" :align="'center'" sortable>
                </el-table-column>
                <el-table-column prop="total_shu_ying" label="总押分" header-align="center" :align="'center'" sortable>
                </el-table-column>
                <el-table-column prop="total_real_shu_ying" label="实际输赢" header-align="center" :align="'center'" sortable>
                </el-table-column>
                <el-table-column prop="money" label="余额" header-align="center" :align="'center'" sortable>
                </el-table-column>
                <el-table-column prop="total_money" label="等级" header-align="center" :align="'center'" sortable>

                    <template #default="scope">
                        <span style="color: red;" v-if="scope.row.level == 1"> 一级</span>
                        <span style="color:blue;" v-if="scope.row.level == 2"> 二级</span>
                        <span style="color: green;" v-if="scope.row.level == 3"> 三级</span>
                    </template>
                </el-table-column>
            </el-table>
        </el-card>
        <el-card uno-margin-top>
            <div class="pager-wrapper">
                <pagination :pageForm="pageForm" @def="getData" />
            </div>
        </el-card>
    </div>
</template>
  
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent, computed } from "vue";
import { storeToRefs } from "pinia";
import confStore from "@/store/modules/conf";
import { goToUserInfo } from "@/utils/baseFun";
import datetime from "@/components/datetime/index.vue";
import { play_promotion_list } from "@/api/userManagenment/index"
import pagination from "@/components/pagination/index.vue"
export default defineComponent({
    name: "index",
    components: {
        datetime, pagination
    },
    props: {
        data: {
            // type:
        }
    },
    setup(props) {
        const store = confStore();
        let { isPc } = storeToRefs(store);
        const state = reactive({
            loading: false, // table loading
            size: 'default',
            user_info: props.data,
            timeArr: [],
            tableData: [
            ],
            pageForm: {
                page: 1,
                limit: 20,
                total: 0
            },
            tableTotal: {

            },
            searchForm: {
                uid: props.data['uid'],//用户id
                users_level: null,//下级等级
                first_recharge: null,//是否首充
                stime: null,
                etime: null,

            },
            level: [
                { label: '下级等级', value: null },
                { label: '一级', value: '1' },
                { label: '二级', value: '2' },
                { label: '三级', value: '3' }
            ],
            first_recharge: [
                { label: '是否充值', value: null },
                { label: '是', value: '1' },
                { label: '否', value: '0' },
            ],

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
        const timeChange = (time) => {
            state.timeArr = time
            getData()

        }
        const getData = () => {
            state.loading = true
            state.searchForm.stime = state.timeArr ? state.timeArr[0] : ''
            state.searchForm.etime = state.timeArr ? state.timeArr[1] : ''
            play_promotion_list({ page: state.pageForm.page, limit: state.pageForm.limit, ...state.searchForm }).then(res => {
                state.pageForm.total = res.count
                state.tableData = res.data;
                state.tableTotal = res.total;
                state.loading = false
            })
        }
        // 搜索数据
        const searchData = () => {
            state.pageForm.page = 1;
            getData();// 获取数据
        }
        return { ...toRefs(state), iconStyle, storeToRefs, props, isPc, goToUserInfo, timeChange, getData, searchData };
    },
});
</script>
<style lang="scss" scoped>
.from_box {
    width: 900px;
}

.total_box {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

@media (max-width:750px) {
    .from_box {
        width: 100%;
    }
}
</style>
  
  