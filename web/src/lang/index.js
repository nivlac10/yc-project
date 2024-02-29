/*
 * @Author: wawodel 69891926+wawodel@users.noreply.github.com
 * @Date: 2023-06-08 16:39:47
 * @LastEditors: wawodel 69891926+wawodel@users.noreply.github.com
 * @LastEditTime: 2023-12-11 16:38:14
 * @FilePath: \web1.1\src\lang\index.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
import enLocale from './English.js'
import { createI18n } from 'vue-i18n'
import PortuguesLocale from './Portugues.js'
const messages = {
    EN: {
        ...enLocale
    },
    PT: {
        ...PortuguesLocale
    }
}
export default createI18n({
    locale: 'PT', 
    messages,
    legacy: false
})