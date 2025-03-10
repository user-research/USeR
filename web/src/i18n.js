import i18next from 'i18next'
import { initReactI18next } from 'react-i18next'
import common_en from "./translations/en/common.json";

// https://www.codeandweb.com/babeledit/tutorials/how-to-translate-your-react-app-with-react-i18next

i18next
    .use(initReactI18next)
    .init({
        interpolation: { escapeValue: false },  // React already does escaping
        lng: 'en',                              // language to use
        resources: {
            en: {
                common: common_en               // 'common' is our custom namespace
            },
        },
});