/**
 * LokLens — Automated Frontend & Data Integrity Test (test_frontend.js)
 * 
 * Tests:
 * 1. Checks that index.html contains all necessary DOM hooks
 * 2. Validates LOKLENS_DATA schema (all 5 guarantees, metrics, sources)
 * 3. Verifies local manifesto PDF exists and is readable
 */

const fs = require("fs");
const path = require("path");

function runFrontendTests() {
    console.log("============================================================");
    console.log(" LokLens — Frontend & Civic Data Integrity Tests");
    console.log("============================================================\n");

    let passed = 0;
    let failed = 0;

    function assert(condition, message) {
        if (condition) {
            console.log(`✓ PASS: ${message}`);
            passed++;
        } else {
            console.error(`✗ FAIL: ${message}`);
            failed++;
        }
    }

    // Test 1: Verify index.html exists and has critical DOM IDs
    const indexPath = path.join(__dirname, "index.html");
    assert(fs.existsSync(indexPath), "index.html exists");
    
    const indexHTML = fs.readFileSync(indexPath, "utf-8");
    const requiredIDs = [
        "state-select",
        "search-input",
        "promise-grid",
        "loading-state",
        "empty-state",
        "promise-modal",
        "modal-close-btn",
        "modal-category",
        "modal-status",
        "modal-promise-name",
        "modal-dept",
        "modal-manifesto-quote",
        "modal-implementation-text",
        "modal-eligibility-text",
        "modal-metric-target",
        "modal-metric-delivery",
        "modal-metric-type",
        "modal-metric-updated",
        "modal-metric-model",
        "modal-data-notes",
        "modal-sources-list"
    ];

    requiredIDs.forEach(id => {
        assert(indexHTML.includes(`id="${id}"`), `index.html contains element #${id}`);
    });

    // Test 2: Verify data.js schema and contents
    const dataPath = path.join(__dirname, "data.js");
    assert(fs.existsSync(dataPath), "data.js exists");

    const dataContent = fs.readFileSync(dataPath, "utf-8");
    assert(dataContent.includes("const LOKLENS_DATA"), "data.js exports LOKLENS_DATA");

    // Load data in sandboxed scope
    const vm = require("vm");
    const sandbox = {};
    vm.createContext(sandbox);
    const data = vm.runInContext(dataContent + "; LOKLENS_DATA;", sandbox);

    assert(data && data.states, "LOKLENS_DATA contains states dictionary");
    assert(data.states.karnataka, "Karnataka state record exists");
    assert(data.states.karnataka.promises.length === 5, "Karnataka contains exactly 5 guarantees");

    const guaranteeIds = ["gruha-jyothi", "gruha-lakshmi", "anna-bhagya", "yuvanidhi", "shakti"];
    guaranteeIds.forEach(gid => {
        const p = data.states.karnataka.promises.find(item => item.id === gid);
        assert(p !== undefined, `Guarantee '${gid}' exists in dataset`);
        assert(p && p.manifestoQuote && p.manifestoQuote.length > 5, `'${gid}' has manifesto quote`);
        assert(p && p.department && p.department.length > 5, `'${gid}' has verified department`);
        assert(p && p.metrics && p.metrics.metricType, `'${gid}' has appropriate metric type`);
        assert(p && p.sources && p.sources.length > 0, `'${gid}' has documented sources`);
    });

    // Test 3: Verify Manifesto PDF exists and is non-empty
    const pdfPath = path.join(__dirname, "Assembly_Election_Karnataka_Manifesto_2023_241fdc08d0.pdf");
    assert(fs.existsSync(pdfPath), "Official Manifesto PDF exists on disk");
    const pdfStats = fs.statSync(pdfPath);
    assert(pdfStats.size > 1000000, `Manifesto PDF is valid file size (${(pdfStats.size / (1024*1024)).toFixed(1)} MB)`);

    console.log(`\nResults: ${passed} Passed, ${failed} Failed.`);
    if (failed > 0) {
        process.exit(1);
    }
}

runFrontendTests();
