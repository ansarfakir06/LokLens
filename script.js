/**
 * LokLens — Stage 3 Full-Stack Application Logic (script.js)
 * 
 * Purpose:
 * Connects the UI to our Python Flask REST API backend (`/api/...`).
 * Includes intelligent graceful fallback to `LOKLENS_DATA` (data.js) when running
 * in standalone file mode.
 * 
 * Beginner-friendly highlights:
 * - Uses modern `async / await` and the `fetch()` API
 * - Clean Separation of Concerns: API Service -> State Management -> DOM Rendering
 * - Full explanations for technical interviews
 */

// ============================================================================
// 1. APPLICATION STATE
// ============================================================================
const appState = {
    selectedState: "karnataka",
    selectedCategory: "all",
    searchQuery: "",
    isApiConnected: false,   // Tracks if Python Flask backend is reachable
    cachedPromises: []       // Holds active list of promises
};

// ============================================================================
// 2. DOM ELEMENT REFERENCES
// ============================================================================

// Controls
const stateSelect = document.getElementById("state-select");
const searchInput = document.getElementById("search-input");
const filterPills = document.querySelectorAll(".filter-pill");

// Section headers & status counters
const sectionTitle = document.getElementById("section-title");
const sectionSubtitle = document.getElementById("section-subtitle");
const metaTagGuarantees = document.querySelector(".manifesto-meta .meta-tag:first-child");
const connectionIndicator = document.querySelector(".status-indicator");

// Containers
const promiseGrid = document.getElementById("promise-grid");
const loadingState = document.getElementById("loading-state");
const emptyState = document.getElementById("empty-state");
const emptyTitle = emptyState.querySelector(".empty-title");
const emptyMessage = emptyState.querySelector(".empty-message");

// Modal Elements
const modal = document.getElementById("promise-modal");
const modalCloseBtn = document.getElementById("modal-close-btn");
const modalFooterClose = document.getElementById("modal-footer-close");
const modalCategory = document.getElementById("modal-category");
const modalStatus = document.getElementById("modal-status");
const modalPromiseName = document.getElementById("modal-promise-name");
const modalDept = document.getElementById("modal-dept");
const modalManifestoQuote = document.getElementById("modal-manifesto-quote");
const modalImplementationText = document.getElementById("modal-implementation-text");
const modalEligibilityText = document.getElementById("modal-eligibility-text");
const modalMetricTarget = document.getElementById("modal-metric-target");
const modalMetricDelivery = document.getElementById("modal-metric-delivery");
const modalMetricType = document.getElementById("modal-metric-type");
const modalMetricUpdated = document.getElementById("modal-metric-updated");
const modalMetricModel = document.getElementById("modal-metric-model");
const modalDataNotes = document.getElementById("modal-data-notes");
const modalSourcesList = document.getElementById("modal-sources-list");

// ============================================================================
// 3. API SERVICE LAYER (Client -> Flask Backend)
// ============================================================================

/**
 * Checks if the Flask backend server is alive by hitting /api/health.
 */
async function checkBackendHealth() {
    try {
        const response = await fetch("/api/health");
        if (response.ok) {
            const data = await response.json();
            appState.isApiConnected = true;
            updateConnectionUI(true);
            console.log("Connected to Flask Backend:", data);
        } else {
            appState.isApiConnected = false;
            updateConnectionUI(false);
        }
    } catch (error) {
        // When opening index.html directly via file:// or without Flask
        appState.isApiConnected = false;
        updateConnectionUI(false);
        console.log("Flask backend not detected. Operating in Local Verified Mode.");
    }
}

/**
 * Updates the navbar badge to show whether Flask API is connected.
 */
function updateConnectionUI(connected) {
    if (!connectionIndicator) return;

    if (connected) {
        connectionIndicator.innerHTML = `
            <span class="pulse-dot" style="background:#38BDF8; box-shadow:0 0 8px #38BDF8;"></span>
            Flask API Connected
        `;
        connectionIndicator.style.borderColor = "rgba(56, 189, 248, 0.4)";
        connectionIndicator.style.color = "#38BDF8";
        connectionIndicator.style.background = "rgba(56, 189, 248, 0.1)";
    } else {
        connectionIndicator.innerHTML = `
            <span class="pulse-dot"></span>
            Verified Source Mode
        `;
        connectionIndicator.style.borderColor = "rgba(16, 185, 129, 0.25)";
        connectionIndicator.style.color = "#34D399";
        connectionIndicator.style.background = "rgba(16, 185, 129, 0.1)";
    }
}

/**
 * Fetches promises from Flask REST API endpoint (/api/promises).
 * Returns parsed JSON or throws an error.
 */
async function fetchPromisesFromAPI(stateId, category, search) {
    const params = new URLSearchParams({
        state: stateId,
        category: category,
        search: search
    });

    const response = await fetch(`/api/promises?${params.toString()}`);
    if (!response.ok) {
        throw new Error(`API HTTP Error: ${response.status}`);
    }
    return await response.json();
}

/**
 * Fetches a single promise's full detail from /api/promises/<id>.
 */
async function fetchPromiseDetailFromAPI(promiseId) {
    const response = await fetch(`/api/promises/${promiseId}`);
    if (!response.ok) {
        throw new Error(`API HTTP Error: ${response.status}`);
    }
    return await response.json();
}

// ============================================================================
// 4. HTML CARD BUILDER
// ============================================================================

function createPromiseCardHTML(promise) {
    return `
        <article class="promise-card" data-id="${promise.id}" data-category="${promise.category}">
            <div class="card-header">
                <span class="badge category-badge ${promise.category}">
                    ${promise.categoryLabel}
                </span>
                <span class="badge status-badge ${promise.status}">
                    ${promise.statusLabel}
                </span>
            </div>
            
            <h3 class="promise-title">${promise.name}</h3>
            
            <p class="promise-manifesto-text">
                "${promise.manifestoQuote}"
            </p>
            
            <div class="card-metric-preview">
                <div class="metric-label">Key Metric</div>
                <div class="metric-value">${promise.metrics.target}</div>
            </div>
            
            <div class="card-footer">
                <span class="source-hint">${promise.metrics.metricType.split('/')[0].trim()}</span>
                <button class="view-detail-btn" type="button" aria-label="View details for ${promise.name}">
                    View Progress & Sources <span aria-hidden="true">→</span>
                </button>
            </div>
        </article>
    `;
}

// ============================================================================
// 5. RENDERING PIPELINE
// ============================================================================

/**
 * Main render function: fetches data from Flask if connected, or uses local data.js.
 */
async function renderApp(showLoading = false) {
    if (showLoading) {
        promiseGrid.style.display = "none";
        emptyState.style.display = "none";
        loadingState.style.display = "flex";
    }

    try {
        if (appState.isApiConnected) {
            // === PATH A: LIVE FLASK REST API ===
            const apiResult = await fetchPromisesFromAPI(
                appState.selectedState,
                appState.selectedCategory,
                appState.searchQuery
            );

            loadingState.style.display = "none";

            if (!apiResult.hasData) {
                sectionTitle.textContent = apiResult.state;
                sectionSubtitle.textContent = "Data undergoing official verification.";
                if (metaTagGuarantees) metaTagGuarantees.textContent = "0 Verified";
                showEmptyState("Data Not Available Yet", apiResult.message);
                return;
            }

            sectionTitle.textContent = "Karnataka Congress Manifesto 2023";
            sectionSubtitle.textContent = "The 5 Flagship Guarantees announced in the 2023 Assembly Election.";
            
            appState.cachedPromises = apiResult.promises;
            renderCardsList(apiResult.promises, apiResult.totalGuarantees);

        } else {
            // === PATH B: LOCAL DATA STORE FALLBACK ===
            const currentState = LOKLENS_DATA.states[appState.selectedState];

            if (showLoading) {
                await new Promise(r => setTimeout(r, 200));
            }
            loadingState.style.display = "none";

            if (!currentState || !currentState.hasData) {
                sectionTitle.textContent = currentState ? currentState.name : "State";
                sectionSubtitle.textContent = "Data undergoing official verification.";
                if (metaTagGuarantees) metaTagGuarantees.textContent = "0 Verified";
                showEmptyState("Data Not Available Yet", currentState ? currentState.message : "Not available");
                return;
            }

            sectionTitle.textContent = currentState.manifestoTitle;
            sectionSubtitle.textContent = currentState.subtitle;

            // Filter locally
            const query = appState.searchQuery.toLowerCase().trim();
            const category = appState.selectedCategory;

            const filtered = currentState.promises.filter(promise => {
                const matchesCategory = (category === "all" || promise.category === category);
                const text = `${promise.name} ${promise.manifestoQuote} ${promise.summary} ${promise.metrics.target}`.toLowerCase();
                const matchesSearch = (query === "" || text.includes(query));
                return matchesCategory && matchesSearch;
            });

            appState.cachedPromises = currentState.promises;
            renderCardsList(filtered, currentState.promises.length);
        }

    } catch (err) {
        console.error("Render error:", err);
        loadingState.style.display = "none";
        showEmptyState("Connection Notice", "Operating in offline source verification mode.");
    }
}

/**
 * Injects filtered cards into the grid or renders empty search state.
 */
function renderCardsList(promises, totalCount) {
    if (metaTagGuarantees) {
        metaTagGuarantees.textContent = `${promises.length} of ${totalCount} Guarantees`;
    }

    if (promises.length === 0) {
        showEmptyState(
            "No Matching Promises Found",
            `No guarantees match "${appState.searchQuery}" under this category. Try clearing your search keyword.`
        );
        return;
    }

    emptyState.style.display = "none";
    promiseGrid.style.display = "grid";
    promiseGrid.innerHTML = promises.map(createPromiseCardHTML).join("");
}

function showEmptyState(title, message) {
    promiseGrid.style.display = "none";
    loadingState.style.display = "none";
    emptyState.style.display = "block";
    emptyTitle.textContent = title;
    emptyMessage.textContent = message;
}

// ============================================================================
// 6. MODAL DIALOG CONTROLLER
// ============================================================================

async function openModal(promiseId) {
    let promise = null;

    if (appState.isApiConnected) {
        try {
            promise = await fetchPromiseDetailFromAPI(promiseId);
        } catch (e) {
            console.warn("Could not fetch promise from API, checking cache", e);
        }
    }

    // Fallback to cache / local data
    if (!promise) {
        const currentState = LOKLENS_DATA.states[appState.selectedState];
        if (currentState && currentState.promises) {
            promise = currentState.promises.find(p => p.id === promiseId);
        }
    }

    if (!promise) return;

    // Badges & Names
    modalCategory.textContent = promise.categoryLabel;
    modalCategory.className = `badge category-badge ${promise.category}`;
    modalStatus.textContent = promise.statusLabel;
    modalStatus.className = `badge status-badge ${promise.status}`;
    modalPromiseName.textContent = promise.kannadaName ? `${promise.name} (${promise.kannadaName})` : promise.name;

    if (modalDept) {
        const deptInfo = [];
        if (promise.department) deptInfo.push(promise.department);
        if (promise.governmentOrder) deptInfo.push(promise.governmentOrder);
        modalDept.textContent = deptInfo.join(" • ");
    }

    // Manifesto Quote & Implementation
    modalManifestoQuote.textContent = `"${promise.manifestoQuote}"`;
    modalImplementationText.textContent = promise.implementationDetails;

    if (modalEligibilityText) {
        modalEligibilityText.textContent = promise.eligibility || "Eligible citizens of Karnataka meeting departmental verification standards.";
    }

    // Metrics Grid
    modalMetricTarget.textContent = promise.metrics.target;
    modalMetricDelivery.textContent = promise.metrics.delivered;
    modalMetricType.textContent = promise.metrics.metricType;
    modalMetricUpdated.textContent = promise.metrics.lastUpdated;

    if (modalMetricModel) {
        modalMetricModel.textContent = promise.metrics.progressModel || "Operational Service Delivery (Recurring Benefit)";
    }

    // Data Transparency Note
    modalDataNotes.textContent = promise.dataNotes;

    // Sources List
    modalSourcesList.innerHTML = promise.sources.map(src => `
        <li>
            <a href="${src.url}" target="_blank" rel="noopener noreferrer">
                <div style="display:flex; flex-direction:column; gap:2px; text-align:left;">
                    <span style="font-weight: 600;">📄 ${src.title}</span>
                    <span style="font-size: 11.5px; opacity: 0.75;">${src.publisher ? src.publisher + ' • ' : ''}${src.type}</span>
                </div>
                <span aria-hidden="true" style="margin-left: auto; font-size: 14px; opacity: 0.7;">↗</span>
            </a>
        </li>
    `).join("");

    modal.classList.add("active");
    modal.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
}

function closeModal() {
    modal.classList.remove("active");
    modal.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
}

// ============================================================================
// 7. EVENT LISTENERS
// ============================================================================

// State dropdown
stateSelect.addEventListener("change", (e) => {
    appState.selectedState = e.target.value;
    appState.searchQuery = "";
    searchInput.value = "";
    appState.selectedCategory = "all";
    filterPills.forEach(pill => {
        pill.classList.toggle("active", pill.getAttribute("data-category") === "all");
    });
    renderApp(true);
});

// Category filter pills
filterPills.forEach(pill => {
    pill.addEventListener("click", () => {
        filterPills.forEach(p => p.classList.remove("active"));
        pill.classList.add("active");
        appState.selectedCategory = pill.getAttribute("data-category");
        renderApp(false);
    });
});

// Live search input
searchInput.addEventListener("input", (e) => {
    appState.searchQuery = e.target.value;
    renderApp(false);
});

// Event delegation on cards grid
promiseGrid.addEventListener("click", (e) => {
    const card = e.target.closest(".promise-card");
    if (card) {
        const promiseId = card.getAttribute("data-id");
        openModal(promiseId);
    }
});

// Modal close triggers
modalCloseBtn.addEventListener("click", closeModal);
modalFooterClose.addEventListener("click", closeModal);

modal.addEventListener("click", (e) => {
    if (e.target === modal) closeModal();
});

document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal.classList.contains("active")) {
        closeModal();
    }
});

// ============================================================================
// 8. APP INITIALIZATION
// ============================================================================
(async function init() {
    await checkBackendHealth();
    await renderApp(false);
})();
