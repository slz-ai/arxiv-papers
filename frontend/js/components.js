// UI rendering functions

function renderSidebar(index, currentView) {
    // Conferences
    const confList = document.getElementById("conference-list");
    confList.innerHTML = index.available_conferences
        .map(conf => {
            const active = currentView && currentView.type === "conference" && currentView.id === conf.id;
            return `<li><a href="#/conference/${conf.id}" class="${active ? 'active' : ''}">${conf.name}</a></li>`;
        })
        .join("");

    // Dates
    const dateList = document.getElementById("date-list");
    dateList.innerHTML = index.available_dates
        .map(d => {
            const active = currentView && currentView.type === "daily" && currentView.id === d;
            return `<li><a href="#/daily/${d}" class="${active ? 'active' : ''}">${d}</a></li>`;
        })
        .join("");
}

function renderPaperCount(count, label) {
    document.getElementById("paper-count").textContent =
        `Showing ${count} papers for ${label}`;
}

function renderPaperCard(paper) {
    const authorStr = paper.authors.slice(0, 5).join(", ") +
        (paper.authors.length > 5 ? ` et al.` : "");

    const tags = paper.tags
        .map(t => `<span class="paper-tag">${t}</span>`)
        .join("");

    return `
        <div class="paper-card">
            <div class="paper-title">
                <a href="${paper.arxiv_url}" target="_blank" rel="noopener">${paper.title}</a>
            </div>
            <div class="paper-tags">${tags}</div>
            <div class="paper-authors">${authorStr}</div>
            <div class="paper-abstract">${paper.abstract}</div>
            <div class="paper-links">
                <a href="${paper.pdf_url}" target="_blank" rel="noopener">[PDF]</a>
                <a href="${paper.arxiv_url}" target="_blank" rel="noopener">[arXiv]</a>
            </div>
        </div>
    `;
}

function renderPapers(papers) {
    const list = document.getElementById("paper-list");
    const empty = document.getElementById("empty");

    if (papers.length === 0) {
        list.innerHTML = "";
        empty.style.display = "block";
    } else {
        empty.style.display = "none";
        list.innerHTML = papers.map(renderPaperCard).join("");
    }
}

function showLoading(show) {
    document.getElementById("loading").style.display = show ? "block" : "none";
    if (show) {
        document.getElementById("paper-list").innerHTML = "";
        document.getElementById("empty").style.display = "none";
    }
}
