// Simple global state
const AppState = {
    index: null,
    currentPapers: [],
    currentView: null,   // { type: "daily", id: "2026-02-17" } or { type: "conference", id: "neurips_2025" }
    selectedTag: "All",
    lang: localStorage.getItem("lang") || "en",
};
