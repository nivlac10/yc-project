<template>
    <div class="certificate">
        <div class="head">
            <img src="@/assets/images/footer/GC_icon.png" alt="">
            <p>VISIT GAMING CURACAO</p>
        </div>
        <div class="body">
            <div class="card">
                <img src="@/assets/images/Certificate/GC@2x.png" alt="">
                <div class="font">
                    Licensee:
                </div>
                <p class="fontP">Flag Bearer Technology Private Limited</p>
                <div class="title2">
                    <div>
                        <p>{{ store.state.conf.all_conf.platform['platform_url'] }}</p>
                        <img src="@/assets/images/Certificate/correct@2x.png" alt="">
                    </div>


                    VERIFIED
                </div>
                <p class="font2">
                    The above Casino or Sportsbook is licensed and authorized by the Goverment of Curacao and
                    operates under the Master License otGaming Services Provider, N.V. #365/JAZ as an Information Service
                    Provider. They have passed all comoliance and are legallyauthorized to conduct gaming operations forall
                    games of chance and wagering.
                </p>
                <div class="cardBottom">
                    <div class="title">
                        <div class="img1">
                            <img src="@/assets/images/Certificate/Maskgroup@2x.png" alt="">
                            <div class="fontItem">
                                <p>License</p>
                                <span>GLH-</span>
                                <span>OCCHKTW0701062022</span>
                            </div>

                        </div>
                        <div class="img2">
                            <img src="@/assets/images/Certificate/Maskgroup@2x.png" alt="">
                            <div class="fontItem">
                                <p>Website</p>
                                <span>{{ store.state.conf.all_conf.platform['platform_url'] }}</span>
                            </div>


                        </div>
                        <div class="img1">
                            <img src="@/assets/images/Certificate/Maskgroup@2x.png" alt="">
                            <div class="fontItem">
                                <p>Licensee </p>
                                <span>GLH-</span>
                                <span>Flag Bearer Technology Private Limited</span>
                            </div>

                        </div>
                    </div>
                </div>
            </div>
            <img src="@/assets/images/Certificate/Maskgroup.png" alt="" class="titleImg">
            <p class="bottomP">Gaming Curacao licensing and supervision conducted by Gaming Services Provider NV, as
                authorised by the
                Government of Curacao under National Decree No 14, dated 18 August 1998.</p>
            <p class="bottomP">Under this license, apart from its own diligence and legalities, the license holder is not
                authorized to
                offer its services in the territories of Aruba, Bonaire, Curaçao, France, Netherlands, Australia, UK, Spain,
                Saba, Statia, St Martin, USA, or any other jurisdiction that the Central Government of Curaçao (formerly the
                Netherlands Antilles) deems online gambling illegal or are blacklisted.
            </p>
            <p class="bottomP">Copyright © 2020 Gaming Curacao.</p>
            <img src="@/assets/images/Certificate/DMCA1@2x.png" alt="" class="bottomImg">
        </div>

    </div>
</template>

<script setup lang="ts">
import { useStore } from '@/store/index';

const store = useStore();
</script>

<style scoped lang="scss">
.certificate {
    width: 100%;

    .head {
        width: 100%;
        background: #fff;
        height: 80px;
        display: grid;
        justify-items: center;
        align-items: center;
        grid-template-columns: repeat(2, 1fr);
        box-shadow: 0px 4px 0px 0px #E3E3E3;

        p {
            color: #898989;
            font-size: 15px;
            font-weight: 500;
        }
    }

    .body {
        width: 100%;
        background: linear-gradient(to bottom, #EFEFEF 0%, #EFEFEF 50%, #F6F6F6 50%, #F6F6F6 100%);
        display: flex;
        justify-content: center;
        flex-direction: column;
        align-items: center;

        .card {
            margin-top: 100px;
            width: 1200px;
            height: 920px;
            background: #FCFCFC;
            box-shadow: 5px 13px 33px 0px #161616;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 10px;

            img {
                width: 837.39px;
                height: 333.95px;
            }

            .font {
                width: 100%;
                text-align: left;
            }

            p {
                color: #000000;
                font-size: 19.5px;
                line-height: 23px;
                border-bottom: #000000 2px solid;
            }

            .title2 {
                display: flex;
                align-items: center;
                font-size: 19.5px;
                line-height: 22.85px;
                margin-top: 18px;
                margin-left: -150px;

                div {
                    display: flex;
                    align-items: center;
                    font-size: 19.5px;
                    line-height: 22.85px;
                }

                img {
                    width: 52px;
                    height: 44px;
                }

                p {
                    font-size: 19.5px;
                    line-height: 22.85px;
                    font-weight: 400;
                    border-bottom: #000000 2px solid;
                }

            }

            .font2 {
                font-size: 19.5px;
                line-height: 22.85px;
                padding-bottom: 10px;
                border-bottom: #9A9A9A 2px solid;

            }

            .cardBottom {
                background: #1B1C1F;
                width: 99%;
                height: 368px;
                margin-top: 33px;
            }

            .cardBottom {
                // height: 292px;
                padding: 96px 335px 0 300px;
                box-sizing: border-box;

                img {
                    width: 29px;
                    height: 29px;
                }

                .title {
                    color: #fff;
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    align-items: flex-start;
                    row-gap: 50px;
                }

                .img1 {
                    display: flex;
                    align-items: flex-start;
                }

                .img2 {
                    margin-left: 228px;
                    display: flex;
                    align-items: flex-start;
                }

                .fontItem {
                    margin-left: 10px;

                    p {
                        color: #FFFFFF;
                        font-size: 19.5px;
                        line-height: 22.85px;
                        border: none;
                    }

                    span {
                        font-size: 16px;
                        line-height: 18.75px;
                        color: #7C7C7C;
                    }
                }
            }
        }

        .titleImg {
            margin-top: 143px;

            width: 64px;
            height: 60px;

        }

        .bottomP {
            margin-top: 30px;
            color: #333333;
            font-size: 13.5px;
            line-height: 15.82px;
            width: 683.14px;
            text-align: center;
        }

        .bottomImg {
            width: 60px;
            margin-top: 50px;
            margin-bottom: 298px;
        }
    }

}

@media (max-width: 768px) {
    .certificate {
        .head {
            height: 65px;

            p {
                display: none;
            }

            img {
                width: 184px;
            }
        }

        .body {
            .card {
                width: 264px;
                height: 100%;

                img {
                    width: 194px;
                    height: 70px;
                    margin-bottom: 25px;
                }

                .font {
                    font-size: 19.5px;
                }

                .fontP {
                    border: none;
                    text-decoration: underline;
                    text-align: center;

                }

                .title2 {
                    margin: 0;
                    flex-direction: column;
                    margin-bottom: 31px;
                }

                .cardBottom {
                    padding: 0;
                    height: 100%;

                    .title {
                        display: flex;
                        flex-direction: column;
                        padding: 85px 30px;
                    }

                    .img2 {
                        margin: 0;
                    }

                    .img1 {
                        width: 100%;
                    }

                }
            }

            .bottomP {
                width: 90%;
                margin-left: 5%;
            }

            .bottomImg {
                margin-bottom: 70px;
            }
        }

    }

}</style>