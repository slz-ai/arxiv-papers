// Simple global state
const AppState = {
    index: null,
    currentPapers: [],
    filteredPapers: [],  // after tag filter
    currentView: null,   // { type: "daily", id: "2026-02-17" } or { type: "conference", id: "neurips_2025" }
    selectedTag: "All",
    lang: localStorage.getItem("lang") || "en",
    // Pagination
    page: 1,
    pageSize: 20,
};
