// Tag filtering

function renderTagFilters(availableTags) {
    const container = document.getElementById("tag-filters");
    const allTags = ["All", ...availableTags];

    container.innerHTML = allTags
        .map(tag => {
            const active = AppState.selectedTag === tag ? "active" : "";
            return `<button class="tag-btn ${active}" data-tag="${tag}">${tag}</button>`;
        })
        .join("");

    // Event delegation
    container.onclick = (e) => {
        if (e.target.classList.contains("tag-btn")) {
            AppState.selectedTag = e.target.dataset.tag;
            applyFilter();
        }
    };
}

function applyFilter() {
    const tag = AppState.selectedTag;
    const filtered = tag === "All"
        ? AppState.currentPapers
        : AppState.currentPapers.filter(p => p.tags.includes(tag));

    renderPapers(filtered);

    const label = AppState.currentView
        ? AppState.currentView.id
        : "";
    renderPaperCount(filtered.length, label);

    // Update active button
    document.querySelectorAll(".tag-btn").forEach(btn => {
        btn.classList.toggle("active", btn.dataset.tag === tag);
    });
}
