<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-button type="primary" @click="showPop(true, 'add')">添加模块</el-button>
    </el-card>
    <el-card class="box-card" uno-margin-top>
      <el-table :data="tableData" style="width: 100%" v-loading="loading">
        <el-table-column prop="cid" label="ID" header-align="center" :align="'center'" sortable />
        <el-table-column prop="class_name" label="Name" header-align="center" :align="'center'" />
        <el-table-column prop="c_index" label="排序" header-align="center" :align="'center'" sortable />
        <el-table-column prop="add_time" label="时间" header-align="center" :align="'center'" sortable />
        <el-table-column fixed="right" label="操作" header-align="center" :align="'center'">
          <template #default="scope">
            <el-button link type="primary" size="small" @click="showPop(true, 'update', scope.row)">编辑</el-button>
            <el-button link type="primary" size="small" @click="deleteModule(scope.row.cid)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <el-dialog v-model="isShowPop" title="新增模块" :draggable="true">
      <div uno-flex-center uno-padding-20 uno-pop-item>
        <span> 模块名称：</span>
        <el-input v-model="moduleName" placeholder="请输入模块名称" clearable style="width: 80%;" />
      </div>
      <div uno-flex-center uno-padding-20 uno-pop-item>
        <span> 图片名称：</span>
        <el-input v-model="moduleIcon" placeholder="请输入模块图标" clearable style="width: 80%; " />
      </div>
      <div uno-flex-center uno-padding-20 uno-pop-item>
        <span> 排序：</span>
        <el-input v-model="moduleIndex" placeholder="请输入模块排序" clearable style="width: 80%; " />
      </div>
      <div uno-flex-center uno-padding-20 uno-pop-item>
        <span> 组件名：</span>
        <el-input v-model="componentsName" placeholder="请输入组件名" clearable style="width: 80%; " />
      </div>
      <div uno-flex-center uno-padding-20 uno-pop-item>
        <span> 路由地址：</span>
        <el-input v-model="routerName" placeholder="请输入路由地址" clearable style="width: 80%; " />
      </div>
      <div uno-padding-20 class="btns">
        <el-button type="primary" @click="popBtnClick">{{ addOrupdate == 'add' ? '立即添加' : '立即跟新' }}</el-button>
        <el-button @click="showPop(false)">取消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup >

import { ref ,reactive} from "vue";
import { useRouter } from "vue-router"
import { get_power_class_post, add_power_class_post, delete_power_class, power_class_detail_post } from "@/api/SystemManagement/module";
import { toRefs } from "vue";

const router = useRouter();
let tableData = ref([]);
let loading = ref(false);
//pop
let isShowPop = ref(false);
let addOrupdate = ref();
let moduleName = ref('');
let moduleIcon = ref('');
let moduleIndex = ref('');
let componentsName = ref('');
let routerName = ref('');
let row = ref();

const getData = async () => {
  loading.value = true;
  const { data } = await get_power_class_post({});
  tableData.value = data;
  loading.value = false;
  // console.log(data);
}

getData();

const showPop = (is: boolean, type?: string, rowData?) => {
  addOrupdate.value = type ?? 'add';
  if (row) row.value = rowData;
  isShowPop.value = is;
}

const popBtnClick = () => {
  if (addOrupdate.value == 'add') addModule();
  else updataModule();
}

const addModule = async () => {
  const data = await add_power_class_post({ class_name: moduleName.value, class_icon: moduleIcon.value, c_index: moduleIndex.value });
  console.log(data);
  if (data.status == 1) {
    await getData();
    isShowPop.value = false;
  }

}

const deleteModule = async (cid) => {
  let data = await delete_power_class({ cid });
  if (data.status == 1) {
    await getData();
  }
}

const updataModule = async () => {
  const data = await power_class_detail_post({ class_name: moduleName.value, class_icon: moduleIcon.value, c_index: moduleIndex.value, cid: row.value.cid });
  if (data.status == 1) {
    await getData();
    isShowPop.value = false;
  }
}
</script>

<style lang="scss" scoped>
.item {}

.btns {
  display: flex;
  justify-content: center;
}
</style>

