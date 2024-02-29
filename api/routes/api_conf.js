const RKEY = require('../RKEY')
var express = require('express');
var router = express.Router();
const userDataUtil = require('../utils/userDataUtil');
const redis = require('../Redis/index')

router.all('/api/get_conf', async (req, res) => {
    const data = {
        code: 0,
        // vip配置
        vip_conf: [],
        // 活动
        activity: [],
        // 公告
        notice_list: [],
        // 轮播图
        banner: [],
        // TG频道地址
        tg_channel_url: '',
        // 支付配置
        pay_conf: {

        },
        // 分享配置
        share_conf: {},
        // 平台名称以及图标配置
        platform: {
            platform_min_icon_url: '',
            platform_title_icon_url: '',
            platform_path: '',
            platform_url: '',
            platform_title: '',
            platform_livechat_id: ''
        },
        // 音乐数组
        music_list: [],
        // 游戏列表版本号
        game_data_version: 0,
        // 货币符号
        currency: "",
        // 安卓下载地址
        android_url: '',
        // 活动弹窗列表
        san_plate_alert_list: [],
        // 邀请活动赠送
        invit_recharge_gift: ''
    }
    try {
        await get_all_conf(data)
    } catch (error) {
        console.log(error);
    }
    res.send(data);
    return;

})

async function get_all_conf(data) {
    try {

        // 获取vip配置
        data.vip_conf = await get_redis_conf(RKEY.SAN_GAME_VIP_LV_LIST)
        // 获取活动配置
        data.activity = await get_redis_conf(RKEY.SAN_GAME_NEW_ACTIVITY_CONF)
        // 获取公告配置
        data.notice_list = await get_redis_conf(RKEY.SAN_GAME_NEW_NOTICE_CONF)
        // 获取轮播图配置
        data.banner = await get_redis_conf(RKEY.SAN_GAME_BANNER_LIST)
        // 游戏列表版本号
        data.game_data_version = await redis.get(RKEY.GAME_DATA_VERSION)
        // 支付配置
        // 获取支付简介
        // data.pay_conf.activity_slogan = await this.get_redis_conf("san_recharge_activity_slogan")
        // 默认支付金额
        data.pay_conf.default_money = await hget_redis_conf(RKEY.SAN_GAME_ALL_CONF, "default_money")
        // 获取支付挡位列表
        data.pay_conf.pay_money_list = await getPayMoneyList()
        // 获取最大最小 充值提现金额
        data.pay_conf.min_recharge_money = await hget_redis_conf(RKEY.SAN_GAME_ALL_CONF, "min_recharge_money")
        data.pay_conf.max_recharge_money = await hget_redis_conf(RKEY.SAN_GAME_ALL_CONF, "max_recharge_money")
        data.pay_conf.min_withdraw_money = await hget_redis_conf(RKEY.SAN_GAME_ALL_CONF, "min_withdraw_money")
        data.pay_conf.max_withdraw_money = await hget_redis_conf(RKEY.SAN_GAME_ALL_CONF, "max_withdraw_money")
        data.pay_conf.min_withdraw_commission = await hget_redis_conf(RKEY.SAN_GAME_ALL_CONF, "min_withdraw_commission")
        // 获取tg社群链接
        data.tg_channel_url = await hget_redis_conf(RKEY.SAN_GAME_ALL_CONF, "tg_channel_url")
        // 分享配置
        data.share_conf.url = await hget_redis_conf(RKEY.SAN_GAME_ALL_CONF, 'copy_link')
        data.share_conf.detail = await hget_redis_conf(RKEY.SAN_GAME_ALL_CONF, 'share_detail')
        data.share_conf.title = await hget_redis_conf(RKEY.SAN_GAME_ALL_CONF, 'share_title')
        data.share_conf.share_contact_email = await hget_redis_conf(RKEY.SAN_GAME_ALL_CONF, 'share_contact_email')
        // 货币符号
        data.currency = await hget_redis_conf(RKEY.SAN_GAME_ALL_CONF, 'currency')
        // 安卓下载地址
        data.android_url = await hget_redis_conf(RKEY.SAN_GAME_ALL_CONF, 'android_url')
        // 货币符号
        data.san_plate_alert_list = await get_redis_conf('san_plate_alert_list')
        // 资源地址
        const resource_host = await hget_redis_conf(RKEY.SAN_GAME_ALL_CONF, RKEY.CDN_HOST)
        // 平台配置
        data.platform.platform_min_icon_url = resource_host + await hget_redis_conf(RKEY.SAN_GAME_ALL_CONF, 'platform_min_icon_url')
        data.platform.platform_title_icon_url = resource_host + await hget_redis_conf(RKEY.SAN_GAME_ALL_CONF, 'platform_title_icon_url')
        data.platform.platform_path = await hget_redis_conf(RKEY.SAN_GAME_ALL_CONF, 'platform_path')
        data.platform.platform_url = await hget_redis_conf(RKEY.SAN_GAME_ALL_CONF, 'platform_url')
        data.platform.platform_title = await hget_redis_conf(RKEY.SAN_GAME_ALL_CONF, 'platform_title')
        data.platform.platform_livechat_id = await hget_redis_conf(RKEY.SAN_GAME_ALL_CONF, 'platform_livechat_id')
        // 邀请首充赠送金额
        data.invit_recharge_gift = await hget_redis_conf(RKEY.SAN_GAME_ALL_CONF, 'invit_recharge_gift')
        data.music_list = await get_music_list(resource_host)
        data.code = 1
    } catch (error) {
        console.log(error);
    }

}
// 获取redis get配置
async function get_redis_conf(redisKey) {
    let data = await redis.get(redisKey)
    return data ? JSON.parse(data) : []
}

// 获取redis hget配置
async function hget_redis_conf(redisKey, minKey) {
    let data = await redis.hget(redisKey, minKey)
    return data ? data : null
}

async function getPayMoneyList() {
    const payMoneyStr = await redis.hget(RKEY.SAN_GAME_ALL_CONF, 'pay_money_list') ||
        "100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000";
    const payMoneyList = payMoneyStr.split(",").map(Number);
    return payMoneyList;
}

  // 获取音乐列表
  async function get_music_list(resource_host) {
    const music_list = [
        {
            'name': 'ADEUS - Mari Fernandez (Áudio Oficial)_A7bstHh6S_8',
            'path': 'ADEUS - Mari Fernandez (Áudio Oficial)_A7bstHh6S_8.mp3'
        },
        {
            'name': 'Ainda_Gosto_de_Você_Já_Era_Sorriso_Maroto,_Ludmilla,_Belo_Sorriso',
            'path': 'Ainda_Gosto_de_Você_Já_Era_Sorriso_Maroto,_Ludmilla,_Belo_Sorriso.mp3'
        },
        {
            'name': 'Ana Castela - Solteiro Forçado (Áudio MP3)',
            'path': 'Ana Castela - Solteiro Forçado (Áudio MP3).mp3'
        },
        {
            'name': 'Bom Não, Morena - Zé Vaqueiro e Matheus Vini_sdiKMI2LVb8',
            'path': 'Bom Não, Morena - Zé Vaqueiro e Matheus Vini_sdiKMI2LVb8.mp3'
        },
        {
            'name': 'Cafézin de Vó  - Ávine Vinny e João Gomes_-47K7KhcWGQ',
            'path': 'Cafézin de Vó  - Ávine Vinny e João Gomes_-47K7KhcWGQ.mp3'
        },
        { 'name': 'Cêis Não Bebe Não_ (Ao Vivo)_lVbnO4HWdIw', 'path': 'Cêis Não Bebe Não_ (Ao Vivo)_lVbnO4HWdIw.mp3' },
        {
            'name': 'Di Propósito, Leo Santana - VáPurMim (Ao Vivo)_Gk7uMqGS6mU',
            'path': 'Di Propósito, Leo Santana - VáPurMim (Ao Vivo)_Gk7uMqGS6mU.mp3'
        },
        {
            'name': 'Diego_&_Victor_Hugo,_Bruno_&_Marrone_Facas_Ao_Vivo_VntVkQRaAS8',
            'path': 'Diego_&_Victor_Hugo,_Bruno_&_Marrone_Facas_Ao_Vivo_VntVkQRaAS8.mp3'
        },
        {
            'name': 'Diego_&_Victor_Hugo,_Jorge_&_Mateus_Beijo_de_Glicose_Todo_Dia_Uma',
            'path': 'Diego_&_Victor_Hugo,_Jorge_&_Mateus_Beijo_de_Glicose_Todo_Dia_Uma.mp3'
        },
        {
            'name': 'Diego_e_Victor_Hugo,_Henrique_&_Juliano_Calafrio_DVD_Sem_Contraindicação',
            'path': 'Diego_e_Victor_Hugo,_Henrique_&_Juliano_Calafrio_DVD_Sem_Contraindicação.mp3'
        },
        {
            'name': 'Diego_e_Victor_Hugo,_Luan_Pereira_Pirulito_Vermelho_Clipe_Oficial',
            'path': 'Diego_e_Victor_Hugo,_Luan_Pereira_Pirulito_Vermelho_Clipe_Oficial.mp3'
        },
        {
            'name': 'Dilsinho - Diferentão (Clipe Oficial)_3mVs1SInmb0',
            'path': 'Dilsinho - Diferentão (Clipe Oficial)_3mVs1SInmb0.mp3'
        },
        { 'name': 'Dilsinho - Duas (Ao Vivo)_cANKLcbqr_I', 'path': 'Dilsinho - Duas (Ao Vivo)_cANKLcbqr_I.mp3' },
        {
            'name': 'Dilsinho - Ele ou Eu (Ao Vivo)_P--t5uBv3C8',
            'path': 'Dilsinho - Ele ou Eu (Ao Vivo)_P--t5uBv3C8.mp3'
        },
        {
            'name': 'Dilsinho,_Henrique_&_Juliano_Sogra_DVD_Open_House_Ao_Vivo_p1mhzgVWFzg',
            'path': 'Dilsinho,_Henrique_&_Juliano_Sogra_DVD_Open_House_Ao_Vivo_p1mhzgVWFzg.mp3'
        },
        {
            'name': 'Di_Propósito,_Rodriguinho_Querendo_Mais_Ao_Vivo_8WtdD1QP2IM',
            'path': 'Di_Propósito,_Rodriguinho_Querendo_Mais_Ao_Vivo_8WtdD1QP2IM.mp3'
        },
        {
            'name': 'Ela_Sorriso_Maroto,_Ferrugem_Sorriso_Eu_Gosto_No_Pagode_CgkLC1mcCE0',
            'path': 'Ela_Sorriso_Maroto,_Ferrugem_Sorriso_Eu_Gosto_No_Pagode_CgkLC1mcCE0.mp3'
        },
        {
            'name': 'Grupo_Menos_é_Mais_e_Matheus_Fernandes_Lapada_Dela_Lyric_Vídeo_0XaZGK47AcY',
            'path': 'Grupo_Menos_é_Mais_e_Matheus_Fernandes_Lapada_Dela_Lyric_Vídeo_0XaZGK47AcY.mp3'
        },
        { 'name': 'Guilherme e Benuto - POEIRÃO (DVD)', 'path': 'Guilherme e Benuto - POEIRÃO (DVD).mp3' },
        {
            'name': 'Guilherme_&_Benuto,_Os_Barões_da_Pisadinha_Faxina_Alguém_Aí_Me_Chama',
            'path': 'Guilherme_&_Benuto,_Os_Barões_da_Pisadinha_Faxina_Alguém_Aí_Me_Chama.mp3'
        },
        {
            'name': 'Guilherme_e_Benuto,_Ana_Castela_e_Adriano_Rhod_Duas_Três_Áudio_Oficial',
            'path': 'Guilherme_e_Benuto,_Ana_Castela_e_Adriano_Rhod_Duas_Três_Áudio_Oficial.mp3'
        },
        {
            'name': 'Guilherme_e_Benuto,_Matheus_&_Kauan_Esse_B_O_É_Meu_DVD_Deu_Rolo',
            'path': 'Guilherme_e_Benuto,_Matheus_&_Kauan_Esse_B_O_É_Meu_DVD_Deu_Rolo.mp3'
        },
        {
            'name': 'Guilherme_e_Benuto,_Simone_Mendes_Manda_um_Oi_DVD_Deu_Rolo_de_Novo',
            'path': 'Guilherme_e_Benuto,_Simone_Mendes_Manda_um_Oi_DVD_Deu_Rolo_de_Novo.mp3'
        },
        {
            'name': 'Guilherme_e_Benuto,_Wesley_Safadão_Milionário_DVD_Deu_Rolo_de_Novo',
            'path': 'Guilherme_e_Benuto,_Wesley_Safadão_Milionário_DVD_Deu_Rolo_de_Novo.mp3'
        },
        {
            'name': 'Guilherme_e_Benuto_feat_@HugoeGuilhermeOficial_Haja_Colírio_DVD',
            'path': 'Guilherme_e_Benuto_feat_@HugoeGuilhermeOficial_Haja_Colírio_DVD.mp3'
        },
        {
            'name': 'Guilherme_e_Benuto_feat_Xand_Avião_Assunto_Delicado_DVD_Deu_Rolo',
            'path': 'Guilherme_e_Benuto_feat_Xand_Avião_Assunto_Delicado_DVD_Deu_Rolo.mp3'
        },
        {
            'name': 'Guilherme_e_Benuto_Pulei_Na_Piscina_DVD_DRIVE_IN_360_1Ji48IQkIxQ',
            'path': 'Guilherme_e_Benuto_Pulei_Na_Piscina_DVD_DRIVE_IN_360_1Ji48IQkIxQ.mp3'
        },
        { 'name': 'Gusttavo Lima -  Fala Mal de Mim (Áudio)', 'path': 'Gusttavo Lima -  Fala Mal de Mim (Áudio).mp3' },
        {
            'name': 'Gusttavo Lima - Bloqueado (Letra_Lyrics)_FLxRLpyMsKw',
            'path': 'Gusttavo Lima - Bloqueado (Letra_Lyrics)_FLxRLpyMsKw.mp3'
        },
        {
            'name': 'Gusttavo Lima - Desejo Imortal (Áudio Oficial)_Np_pOs_YV04',
            'path': 'Gusttavo Lima - Desejo Imortal (Áudio Oficial)_Np_pOs_YV04.mp3'
        },
        {
            'name': 'Gusttavo_Lima_Canudinho_Part_Ana_Castela_Letra_TULeErLOLyY',
            'path': 'Gusttavo_Lima_Canudinho_Part_Ana_Castela_Letra_TULeErLOLyY.mp3'
        },
        {
            'name': 'Gusttavo_Lima_Cara_da_Derrota_Ao_Vivo_em_Goiânia_Nosy_f5WOBk',
            'path': 'Gusttavo_Lima_Cara_da_Derrota_Ao_Vivo_em_Goiânia_Nosy_f5WOBk.mp3'
        },
        {
            'name': 'Gusttavo_Lima_Compensa_DVD_Paraíso_Particular_XjoW45h0Hzw',
            'path': 'Gusttavo_Lima_Compensa_DVD_Paraíso_Particular_XjoW45h0Hzw.mp3'
        },
        {
            'name': 'Gusttavo_Lima_Mala_dos_Porta_Mala_part_Matheus_e_Kauan_DVD_Paraíso',
            'path': 'Gusttavo_Lima_Mala_dos_Porta_Mala_part_Matheus_e_Kauan_DVD_Paraíso.mp3'
        },
        {
            'name': 'Gusttavo_Lima_Oficializar_Part_Maiara_&_Maraisa_DVD_Paraíso_Particular',
            'path': 'Gusttavo_Lima_Oficializar_Part_Maiara_&_Maraisa_DVD_Paraíso_Particular.mp3'
        },
        {
            'name': 'Gusttavo_Lima_Oi_Vida_part_Wesley_Safadão_DVD_Paraíso_Particular',
            'path': 'Gusttavo_Lima_Oi_Vida_part_Wesley_Safadão_DVD_Paraíso_Particular.mp3'
        },
        {
            'name': 'Gusttavo_Lima_Saudade_da_Minha_Vida_Ao_Vivo_no_Buteco_São_Paulo',
            'path': 'Gusttavo_Lima_Saudade_da_Minha_Vida_Ao_Vivo_no_Buteco_São_Paulo.mp3'
        },
        {
            'name': 'Gusttavo_Lima_Solteiro_Frustrado_#Embaixador15Anos_KWp54ZJ2Q0E',
            'path': 'Gusttavo_Lima_Solteiro_Frustrado_#Embaixador15Anos_KWp54ZJ2Q0E.mp3'
        },
        {
            'name': 'Gusttavo_Lima_Termina_Comigo_Antes_Ao_Vivo_em_Porto_Alegre_rTJSWmgbVwA',
            'path': 'Gusttavo_Lima_Termina_Comigo_Antes_Ao_Vivo_em_Porto_Alegre_rTJSWmgbVwA.mp3'
        },
        {
            'name': 'HALLS_NA_LINGUA_Kadu_Martins_Não_sei_o_que_é,_só_sei_que_é_bom_fEs4cs2p7',
            'path': 'HALLS_NA_LINGUA_Kadu_Martins_Não_sei_o_que_é,_só_sei_que_é_bom_fEs4cs2p7.mp3'
        },
        {
            'name': "Israel_&_Rodolffo,_Mari_Fernandez_Seu_Brilho_Sumiu_Let's_Bora_Áudio",
            'path': "Israel_&_Rodolffo,_Mari_Fernandez_Seu_Brilho_Sumiu_Let's_Bora_Áudio.mp3"
        },
        {
            'name': 'Kaique_&_Felipe_Bailarina_feat_Guilherme_&_Benuto_e_MC_Livinho_HqS',
            'path': 'Kaique_&_Felipe_Bailarina_feat_Guilherme_&_Benuto_e_MC_Livinho_HqS.mp3'
        },
        {
            'name': 'Luan Santana - AMBIENTE ERRADO (LUAN CITY 2.0)_-JBsQjMynbM',
            'path': 'Luan Santana - AMBIENTE ERRADO (LUAN CITY 2.0)_-JBsQjMynbM.mp3'
        },
        {
            'name': 'Luan Santana - MEIO TERMO (LUAN CITY 2.0)_6Pix8tMSN6g',
            'path': 'Luan Santana - MEIO TERMO (LUAN CITY 2.0)_6Pix8tMSN6g.mp3'
        },
        {
            'name': 'Luan Santana - MULHER SEGURA (LUAN CITY 2.0)_XJQUyfPYQNs',
            'path': 'Luan Santana - MULHER SEGURA (LUAN CITY 2.0)_XJQUyfPYQNs.mp3'
        },
        {
            'name': 'Luan Santana - SEM SENTIMENTO (Luan City 2.0)_g2v_IPQRz_c',
            'path': 'Luan Santana - SEM SENTIMENTO (Luan City 2.0)_g2v_IPQRz_c.mp3'
        },
        {
            'name': 'Luan_Pereira_ft_@GustavoMioto_Moletom_Oficial_P4E831Xqs1c',
            'path': 'Luan_Pereira_ft_@GustavoMioto_Moletom_Oficial_P4E831Xqs1c.mp3'
        },
        {
            'name': 'Luan_Santana_+_Simone_Mendes_NOSSA_DISTÂNCIA_Brahma_tgdErmnUlkM',
            'path': 'Luan_Santana_+_Simone_Mendes_NOSSA_DISTÂNCIA_Brahma_tgdErmnUlkM.mp3'
        },
        {
            'name': 'Luan_Santana_ABALO_EMOCIONAL_Baixinha_Invocada_LUAN_CITY_cPGKKktrObc',
            'path': 'Luan_Santana_ABALO_EMOCIONAL_Baixinha_Invocada_LUAN_CITY_cPGKKktrObc.mp3'
        },
        {
            'name': 'Luan_Santana_ERRO_PLANEJADO_feat_Henrique_e_Juliano_LUAN_CITY_apPxQOfh0ek',
            'path': 'Luan_Santana_ERRO_PLANEJADO_feat_Henrique_e_Juliano_LUAN_CITY_apPxQOfh0ek.mp3'
        },
        {
            'name': 'Luan_Santana_feat_Luísa_Souza_Coração_Cigano_áudio_oficial_mv6SNRJsphs',
            'path': 'Luan_Santana_feat_Luísa_Souza_Coração_Cigano_áudio_oficial_mv6SNRJsphs.mp3'
        },
        {
            'name': 'Marcos_&_Belutti,_@GuilhermeeBenuto_Cê_Namora_Eu_Quebra_Cabeça_4zEMivRdsPU',
            'path': 'Marcos_&_Belutti,_@GuilhermeeBenuto_Cê_Namora_Eu_Quebra_Cabeça_4zEMivRdsPU.mp3'
        },
        {
            'name': 'Marcos_&_Belutti,_João_Gomes_Saudade_Digitando_Quebra_Cabeça_ImLfYwrz',
            'path': 'Marcos_&_Belutti,_João_Gomes_Saudade_Digitando_Quebra_Cabeça_ImLfYwrz.mp3'
        },
        {
            'name': 'Mari_Fernandez,_MC_Ryan_SP_e_MC_Daniel_Love_Absurdo_Vídeo_Oficial',
            'path': 'Mari_Fernandez,_MC_Ryan_SP_e_MC_Daniel_Love_Absurdo_Vídeo_Oficial.mp3'
        },
        {
            'name': 'Mari_Fernandez_PODE_APOSTAR_feat_Xand_Avião_DVD_Ao_Vivo_em_Fortaleza',
            'path': 'Mari_Fernandez_PODE_APOSTAR_feat_Xand_Avião_DVD_Ao_Vivo_em_Fortaleza.mp3'
        },
        {
            'name': 'Marília Mendonça - Leão - Decretos Reais_tI55Zu9uZEM',
            'path': 'Marília Mendonça - Leão - Decretos Reais_tI55Zu9uZEM.mp3'
        },
        {
            'name': 'MC Lipi - Anota Aí (Love Funk) DJ Guh Mix_tnyJXbPrGN8',
            'path': 'MC Lipi - Anota Aí (Love Funk) DJ Guh Mix_tnyJXbPrGN8.mp3'
        },
        {
            'name': 'Ombrim_Ai_Que_Delícia_o_Verão_Marina_Sena,_Chicão_do_Piseiro,_Roni',
            'path': 'Ombrim_Ai_Que_Delícia_o_Verão_Marina_Sena,_Chicão_do_Piseiro,_Roni.mp3'
        },
        {
            'name': 'Os_Barões_da_Pisadinha,_Diego_&_Victor_Hugo_Não_Deixa_Eu_Saber_Clipe',
            'path': 'Os_Barões_da_Pisadinha,_Diego_&_Victor_Hugo_Não_Deixa_Eu_Saber_Clipe.mp3'
        },
        {
            'name': 'Os_Barões_da_Pisadinha_Aí_Eu_Chorei_Vestido_da_Shein_Ao_Vivo_n17D8aXOflc',
            'path': 'Os_Barões_da_Pisadinha_Aí_Eu_Chorei_Vestido_da_Shein_Ao_Vivo_n17D8aXOflc.mp3'
        },
        {
            'name': 'PARADA_LOUCA_VAI_BEBÊ_ME_PEDE_PRA_FAZER_MARI_FERNANDEZ_&_MARCYNHO',
            'path': 'PARADA_LOUCA_VAI_BEBÊ_ME_PEDE_PRA_FAZER_MARI_FERNANDEZ_&_MARCYNHO.mp3'
        },
        {
            'name': 'Paulo e Nathan - Feat.  Lauana Prado - Juvenil_hs3_q-FnTiI',
            'path': 'Paulo e Nathan - Feat.  Lauana Prado - Juvenil_hs3_q-FnTiI.mp3'
        },
        {
            'name': 'Paulo_e_Nathan_Acabei_de_Terminar_Part_Hugo_e_Guilherme_DVD_Nunca',
            'path': 'Paulo_e_Nathan_Acabei_de_Terminar_Part_Hugo_e_Guilherme_DVD_Nunca.mp3'
        },
        {
            'name': 'SARRADINHA - Mari Fernandez e Mc Pedrinho_oqjPVinBg38',
            'path': 'SARRADINHA - Mari Fernandez e Mc Pedrinho_oqjPVinBg38.mp3'
        },
        {
            'name': 'Turma do Pagode - Alô Ex (Ao Vivo)_cgis-mIhAcQ',
            'path': 'Turma do Pagode - Alô Ex (Ao Vivo)_cgis-mIhAcQ.mp3'
        },
        {
            'name': 'Turma do Pagode - Só um Pagode (Ao Vivo)_sJuLi84tZy8',
            'path': 'Turma do Pagode - Só um Pagode (Ao Vivo)_sJuLi84tZy8.mp3'
        },
        {
            'name': 'Yasmin_Santos,_Diego_&_Victor_Hugo_Principalmente_Pessoas_6kxyKhJwL8w',
            'path': 'Yasmin_Santos,_Diego_&_Victor_Hugo_Principalmente_Pessoas_6kxyKhJwL8w.mp3'
        },
        { 'name': 'ZÉ VAQUEIRO - COLADIN (MP3 - AUDIOPLAY)', 'path': 'ZÉ VAQUEIRO - COLADIN (MP3 - AUDIOPLAY).mp3' }
    ]
    for (let i = 0; i < music_list.length; i++) {
        const element = music_list[i];
        element.path = resource_host + 'music/' + element.path
    }
    return music_list
}




module.exports = router;