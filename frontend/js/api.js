// Data fetching layer - loads JSON files from data/ directory
const API = {
    // Auto-detect: ./data (production) or ../data (local dev)
    dataBase: null,

    async _resolveBase() {
        if (this.dataBase) return;
        try {
            const resp = await fetch("./data/index.json", { method: "HEAD" });
            this.dataBase = resp.ok ? "./data" : "../data";
        } catch (e) {
            this.dataBase = "../data";
        }
    },

    async getIndex() {
        await this._resolveBase();
        const resp = await fetch(`${this.dataBase}/index.json`);
        if (!resp.ok) throw new Error("Failed to load index");
        return resp.json();
    },

    async getDailyPapers(date) {
        await this._resolveBase();
        const resp = await fetch(`${this.dataBase}/daily/${date}.json`);
        if (!resp.ok) throw new Error(`No papers for ${date}`);
        return resp.json();
    },

    async getConferencePapers(confId) {
        await this._resolveBase();
        const resp = await fetch(`${this.dataBase}/conferences/${confId}.json`);
        if (!resp.ok) throw new Error(`No data for conference ${confId}`);
        return resp.json();
    },
};
