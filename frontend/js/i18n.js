// Bilingual support (EN/CN)
const TRANSLATIONS = {
    en: {
        conferences: "Conferences",
        archives: "Archives",
        no_papers: "No papers found.",
        showing: "Showing",
        papers_for: "papers for",
    },
    zh: {
        conferences: "会议",
        archives: "日期归档",
        no_papers: "暂无论文。",
        showing: "显示",
        papers_for: "篇论文，日期",
    },
};

function t(key) {
    return TRANSLATIONS[AppState.lang][key] || key;
}

function applyI18n() {
    document.querySelectorAll("[data-i18n]").forEach(el => {
        el.textContent = t(el.dataset.i18n);
    });
}

function initI18n() {
    const btn = document.getElementById("lang-toggle");
    btn.textContent = AppState.lang === "en" ? "中文" : "EN";

    btn.onclick = () => {
        AppState.lang = AppState.lang === "en" ? "zh" : "en";
        localStorage.setItem("lang", AppState.lang);
        btn.textContent = AppState.lang === "en" ? "中文" : "EN";
        applyI18n();
    };

    applyI18n();
}
