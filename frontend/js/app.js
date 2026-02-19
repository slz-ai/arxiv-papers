// Main application - routing and page controller

async function init() {
    try {
        showLoading(true);
        AppState.index = await API.getIndex();
        renderSidebar(AppState.index, null);
        initI18n();
        handleRoute();
    } catch (err) {
        console.error("Failed to initialize:", err);
        document.getElementById("paper-list").innerHTML =
            '<p style="text-align:center;color:#999;padding:2rem;">Failed to load data. Please check data/index.json exists.</p>';
        showLoading(false);
    }
}

async function handleRoute() {
    const hash = location.hash.slice(1); // remove #

    if (hash.startsWith("/daily/")) {
        const date = hash.split("/")[2];
        await loadDailyPapers(date);
    } else if (hash.startsWith("/conference/")) {
        const confId = hash.split("/")[2];
        await loadConferencePapers(confId);
    } else {
        // Default: load most recent date
        if (AppState.index && AppState.index.available_dates.length > 0) {
            const latestDate = AppState.index.available_dates[0];
            location.hash = `/daily/${latestDate}`;
        } else {
            showLoading(false);
            document.getElementById("empty").style.display = "block";
        }
    }
}

async function loadDailyPapers(date) {
    showLoading(true);
    AppState.selectedTag = "All";

    try {
        const data = await API.getDailyPapers(date);
        AppState.currentPapers = data.papers;
        AppState.currentView = { type: "daily", id: date };

        renderSidebar(AppState.index, AppState.currentView);
        renderTagFilters(data.available_tags);
        renderPaperCount(data.paper_count, date);
        renderPapers(data.papers);
    } catch (err) {
        console.error(`Failed to load papers for ${date}:`, err);
        AppState.currentPapers = [];
        renderPapers([]);
    }

    showLoading(false);
}

async function loadConferencePapers(confId) {
    showLoading(true);
    AppState.selectedTag = "All";

    try {
        const data = await API.getConferencePapers(confId);
        AppState.currentPapers = data.papers;
        AppState.currentView = { type: "conference", id: confId };

        renderSidebar(AppState.index, AppState.currentView);
        renderTagFilters(data.available_tags);
        renderPaperCount(data.paper_count, data.conference);
        renderPapers(data.papers);
    } catch (err) {
        console.error(`Failed to load conference ${confId}:`, err);
        AppState.currentPapers = [];
        renderPapers([]);
    }

    showLoading(false);
}

// Listen for hash changes
window.addEventListener("hashchange", handleRoute);

// Initialize on load
document.addEventListener("DOMContentLoaded", init);
