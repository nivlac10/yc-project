<template>
    <div class="index">
        <el-card v-if="noUidShow">
            <div class="noUidBox">
                <h1> 请输入用户ID</h1>
                <div>
                    <el-input v-model="uid" placeholder="请输入用户UID" style="width: 200px;" clearable />

                    <el-button type="primary" @click="jumpUid">查询</el-button>
                </div>

            </div>
        </el-card>
        <el-card v-else class="user_info">
            <!-- 用户表头 -->
            <el-page-header :icon="null">
                <template #content>
                    <div class="flex items-center">
                        <el-avatar :size="32" class="mr-3"
                            src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" />
                        <span class="text-sm font-600 mr-3"> 用户信息 </span>
                        <span class="text-sm mr-2" style="color: var(--el-text-color-regular)">
                            uid: {{ userInfo['data'] ? userInfo['data'].uid : '' }}
                        </span>
                        <el-tag v-if="is_black == false">正常用户</el-tag>
                        <el-tag class="ml-2" type="danger" v-if="is_black == true">黑名单用户</el-tag>

                    </div>
                </template>
                <template #extra>
                    <div class="flex items-center gap2" v-permission="['1']">

                        <el-button>Print</el-button>
                        <el-button type="primary">Edit</el-button>
                    </div>
                </template>
            </el-page-header>
            <!-- 用户信息 -->
            <el-skeleton class="mt-7" v-if="!dataLoadState" :rows="15" animated />
            <el-tabs v-else v-model="activeName" class="demo-tabs">
                <el-tab-pane label="基本信息" name="0">
                    <userDataTable @loadUserInfo="loadUserInfo()" v-if="activeName == '0'" :data="userInfo['data']"></userDataTable>
                </el-tab-pane>
                <el-tab-pane label="团队" name="1">
                    <userTeamDetails v-if="activeName == '1'" :data="userInfo['data']"></userTeamDetails>
                </el-tab-pane>
                <el-tab-pane label="VIP详情" name="2">

                    <userVipDetails v-if="activeName == '2'" :data="userInfo['data']"></userVipDetails>
                </el-tab-pane>
                <el-tab-pane label="余额日志" name="3">
                    <balanceLog v-if="activeName == '3'" :userIDShow="false" :uid="uid"></balanceLog>
                </el-tab-pane>
                <el-tab-pane label="充值日志" name="4">
                    <payList v-if="activeName == '4'" :userIDShow="false" :uid="uid"></payList>
                </el-tab-pane>
                <el-tab-pane label="提现日志" name="5">
                    <withdrawalList v-if="activeName == '5'" :userIDShow="false" :uid="uid"></withdrawalList>
                </el-tab-pane>
                <el-tab-pane label="游戏记录" name="6">
                    <gameRecord v-if="activeName == '6'" :userIDShow="false" :uid="uid"></gameRecord>
                </el-tab-pane>
            </el-tabs>
        </el-card>

    </div>
</template>
<script lang="ts">
import { reactive, toRefs, getCurrentInstance, defineComponent } from "vue";
import userDataTable from "./userInfoCom/userDataTable.vue";
import userTeamDetails from "./userInfoCom/userTeamDetails.vue";
import userVipDetails from "./userInfoCom/userVipDetails.vue";
import { recharge_user_detail_post } from "@/api/userManagenment/index.ts";
import { useRoute } from "vue-router";
import { WarningNotiFun, goToUserInfo } from "@/utils/baseFun";
import balanceLog from "./balanceLog.vue";
import payList from "@/views/paymentManagement/payList.vue";
import withdrawalList from "@/views/paymentManagement/withdrawalList.vue";
import gameRecord from "@/views/gameManagement/gameRecord.vue";
export default defineComponent({
    name: "index",
    components: { userDataTable, userTeamDetails, userVipDetails, balanceLog, payList, withdrawalList, gameRecord },

    setup() {
        const route = useRoute()
        const state = reactive({
            activeName: '0',
            userInfo: {
            },
            is_black: false,
            size: '',
            dataLoadState: false,
            noUidShow: true,
            uid: route.params.uid
        });
        function loadUserInfo() {
            if (state.uid != ":uid") {
                state.noUidShow = false
                recharge_user_detail_post({ uid: state.uid }).then((res) => {
                    state.dataLoadState = true
                    state.userInfo = res
                    if (state.userInfo['data']) {
                        state.noUidShow = false
                        route.params.uid = state.uid

                        state.is_black = state.userInfo['data']['is_black']
                    }
                    else {
                        state.noUidShow = true
                        WarningNotiFun("请输入正确的用户ID")
                    }
                })
            } else {
                state.uid = ""
                state.noUidShow = true
            }
        }
        loadUserInfo()
        function jumpUid() {
            if (state.uid) {
                loadUserInfo()
            }
        }

        return { ...toRefs(state), jumpUid,loadUserInfo };
    },
});
</script>
<style  lang="scss" scoped>
.index {
    padding: 5px;
}

:deep(.el-page-header__back) {
    display: none !important;
}

:deep(.el-divider) {
    display: none !important;
}

:deep(.el-page-header__left) {
    margin: 0;
}

:deep(.el-card__body) {
    padding: 10px;
}

.noUidBox {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 10px;
    width: 100%;
    height: 80vh;

    div {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    span {
        font-size: 15px;
        font-weight: 600;
    }
}
</style>
  