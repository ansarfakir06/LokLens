"""
LokLens — Backend REST API Server (app.py)
Tagline: A Lens Through Development

Purpose:
A lightweight, beginner-friendly Python Flask REST API server that provides
endpoints for states, administrations, election manifesto promises,
progress metrics, and official government sources.

Endpoints:
- GET /                         -> Serves frontend (index.html)
- GET /api/health               -> Server health check & DB status
- GET /api/states               -> List of all supported states
- GET /api/administrations      -> List of governments / administrations
- GET /api/promises             -> List promises (filters: ?state= &category= &search=)
- GET /api/promises/<promise_id>-> Retrieve detailed single promise
- GET /api/promises/<promise_id>/progress -> Retrieve scheme progress records
- GET /api/sources              -> List all documented government & manifesto sources
"""

import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import db

# Initialize Flask application
app = Flask(__name__, static_folder=".", static_url_path="")

# Enable Cross-Origin Resource Sharing (CORS) so frontend clients can call this API
CORS(app)

# ============================================================================
# 1. IN-MEMORY FALLBACK DATA STORE
# ============================================================================
# If MySQL is not yet configured or initialized, this store ensures the app
# runs smoothly without crashing while the student learns database setup!

STATES_FALLBACK = [
    {
        "id": "karnataka",
        "name": "Karnataka",
        "hasData": True,
        "guaranteeCount": 5,
        "activeAdministration": "Congress Government (2023–2028)"
    },
    {
        "id": "tamil-nadu",
        "name": "Tamil Nadu",
        "hasData": False,
        "guaranteeCount": 0,
        "message": "We have not yet compiled verified manifesto promises and government execution orders for Tamil Nadu. LokLens adheres to strict data verification rules and does not publish unverified or placeholder data."
    },
    {
        "id": "telangana",
        "name": "Telangana",
        "hasData": False,
        "guaranteeCount": 0,
        "message": "Manifesto data for Telangana is currently in the research pipeline. Official party manifestos and state government department budget reports are undergoing verification."
    },
    {
        "id": "andhra-pradesh",
        "name": "Andhra Pradesh",
        "hasData": False,
        "guaranteeCount": 0,
        "message": "Assembly election manifesto promises and implementation records for Andhra Pradesh are pending source compilation. Check back soon for verified records."
    },
    {
        "id": "maharashtra",
        "name": "Maharashtra",
        "hasData": False,
        "guaranteeCount": 0,
        "message": "Manifesto tracking records for Maharashtra are pending source documentation. We only publish records supported by downloadable official government gazettes."
    }
]

ADMINISTRATIONS_FALLBACK = [
    {
        "id": "karnataka-inc-2023",
        "stateId": "karnataka",
        "party": "Indian National Congress (INC)",
        "term": "2023–2028",
        "manifestoTitle": "Karnataka Congress Assembly Election Manifesto 2023",
        "subtitle": "5 Flagship Guarantees — Verified against Official Departmental Orders",
        "manifestoFile": "Assembly_Election_Karnataka_Manifesto_2023_241fdc08d0.pdf"
    }
]

PROMISES_FALLBACK = [
    {
        "id": "gruha-jyothi",
        "stateId": "karnataka",
        "administrationId": "karnataka-inc-2023",
        "name": "Gruha Jyothi",
        "kannadaName": "ಗೃಹ ಜ್ಯೋತಿ",
        "department": "Energy Department, Government of Karnataka",
        "governmentOrder": "G.O. EN 22 PSR 2023 (Dated: 05-06-2023)",
        "category": "energy",
        "categoryLabel": "⚡ Energy",
        "status": "delivered",
        "statusLabel": "Delivered / Active",
        "summary": "Up to 200 units of zero-cost electricity per month to eligible domestic households.",
        "manifestoQuote": "200 units of free electricity to all the houses.",
        "implementationDetails": "Sanctioned zero-cost domestic electricity up to a ceiling of 200 units per month for households across all state electricity supply companies (BESCOM, MESCOM, CESC, HESCOM, GESCOM). The monthly entitled quota is calculated based on each consumer's past 12-month average consumption plus an additional 10% entitlement buffer.",
        "eligibility": "All domestic LT-2 category electricity consumer accounts in Karnataka. Commercial and industrial connections are excluded.",
        "metrics": {
            "target": "Up to 200 units / month per domestic consumer account",
            "delivered": "Zero-bill benefit applied across 1.6+ crore domestic accounts",
            "metricType": "Power Consumption (kWh) & Consumer Accounts",
            "reportingPeriod": "Monthly billing cycles (Operational since August 2023)",
            "lastUpdated": "Karnataka Gazette & Energy Department (2024)",
            "progressModel": "Recurring Operational Benefit (Non-construction scheme)"
        },
        "dataNotes": "Electricity subsidy schemes represent ongoing monthly service benefits, not a one-time construction project. Progress is measured in beneficiary households receiving zero bills and subsidy amounts disbursed to electricity supply companies (ESCOMs). We do not display arbitrary completion percentages.",
        "sources": [
            {
                "id": "src-manifesto-2023",
                "title": "Karnataka Congress Assembly Election Manifesto 2023",
                "url": "Assembly_Election_Karnataka_Manifesto_2023_241fdc08d0.pdf",
                "type": "Official Election Manifesto",
                "publisher": "Karnataka Pradesh Congress Committee"
            },
            {
                "id": "src-energy-go-2023",
                "title": "Energy Department Government Order (G.O. EN 22 PSR 2023)",
                "url": "https://karnataka.gov.in",
                "type": "Official Government Order",
                "publisher": "Energy Department, Govt of Karnataka"
            }
        ]
    },
    {
        "id": "gruha-lakshmi",
        "stateId": "karnataka",
        "administrationId": "karnataka-inc-2023",
        "name": "Gruha Lakshmi",
        "kannadaName": "ಗೃಹ ಲಕ್ಷ್ಮಿ",
        "department": "Department of Women and Child Development",
        "governmentOrder": "G.O. WCD 90 MMB 2023 (Dated: 07-06-2023)",
        "category": "women",
        "categoryLabel": "👩 Women Welfare",
        "status": "delivered",
        "statusLabel": "Delivered / Active",
        "summary": "₹2,000 monthly direct financial assistance to the woman head of every family.",
        "manifestoQuote": "₹2,000 every month to each woman head of the family.",
        "implementationDetails": "Direct Benefit Transfer (DBT) of ₹2,000 deposited monthly directly into the Aadhaar-seeded bank account of the woman designated as head of the family on Antyodaya, BPL, and APL ration cards.",
        "eligibility": "Women recognized as head of household on Antyodaya Anna Yojana (AAY), BPL, and APL ration cards. Excludes income-tax payees and GST registrants.",
        "metrics": {
            "target": "₹2,000 / month per eligible family",
            "delivered": "Monthly DBT transfers to over 1.18 crore enrolled women heads",
            "metricType": "Direct Financial Assistance (DBT) & Enrolled Beneficiaries",
            "reportingPeriod": "Monthly disbursement rounds (Operational since August 2023)",
            "lastUpdated": "Women & Child Development Department (2024)",
            "progressModel": "Recurring Social Welfare Cash Transfer"
        },
        "dataNotes": "Cash transfers operate on recurring monthly payment cycles. Delivery is evaluated through bank disbursement success rates and verified ration-card linkages, not physical construction milestones.",
        "sources": [
            {
                "id": "src-manifesto-2023",
                "title": "Karnataka Congress Assembly Election Manifesto 2023",
                "url": "Assembly_Election_Karnataka_Manifesto_2023_241fdc08d0.pdf",
                "type": "Official Election Manifesto",
                "publisher": "Karnataka Pradesh Congress Committee"
            },
            {
                "id": "src-wcd-portal-2023",
                "title": "Women & Child Development Guidelines (G.O. WCD 90 MMB 2023)",
                "url": "https://karnataka.gov.in",
                "type": "Official Department Guidelines",
                "publisher": "Women & Child Development Dept"
            }
        ]
    },
    {
        "id": "anna-bhagya",
        "stateId": "karnataka",
        "administrationId": "karnataka-inc-2023",
        "name": "Anna Bhagya",
        "kannadaName": "ಅನ್ನ ಭಾಗ್ಯ",
        "department": "Department of Food, Civil Supplies and Consumer Affairs",
        "governmentOrder": "G.O. FCS 47 RPR 2023 (Dated: 08-07-2023)",
        "category": "food",
        "categoryLabel": "🌾 Food Security",
        "status": "adjusted",
        "statusLabel": "Partly Cash / Active",
        "summary": "10 kg free food grains per person per month for BPL families (delivered as 5 kg rice + ₹170 cash equivalent).",
        "manifestoQuote": "10 Kgs of food grains to every person in BPL family.",
        "implementationDetails": "The manifesto promised 10 kg of food grains per person per month. Due to initial procurement challenges in sourcing sufficient rice from the Food Corporation of India (FCI), the state government approved a policy adjustment to disburse cash compensation of ₹170 per person per month (at ₹34 per kg for 5 kg) directly via DBT alongside 5 kg physical grain.",
        "eligibility": "Every individual member listed on Antyodaya Anna Yojana (AAY) and Priority Household (BPL) ration cards in Karnataka.",
        "metrics": {
            "target": "10 kg food grains / person / month",
            "delivered": "5 kg physical rice + ₹170 cash equivalent per person via DBT",
            "metricType": "Food Grains (kg) & Direct Cash Compensation (₹)",
            "reportingPeriod": "Monthly fair-price shop allocations & DBT cycles",
            "lastUpdated": "Food & Civil Supplies Department (2024)",
            "progressModel": "Hybrid Food Security Allocation (Grain + Cash Equivalent)"
        },
        "dataNotes": "Status is transparently designated 'Partly Cash / Active'. LokLens does not mark this as 100% physically delivered in grain because the state government substituted 5 kg of grain with direct cash compensation due to supply-chain procurement realities.",
        "sources": [
            {
                "id": "src-manifesto-2023",
                "title": "Karnataka Congress Assembly Election Manifesto 2023",
                "url": "Assembly_Election_Karnataka_Manifesto_2023_241fdc08d0.pdf",
                "type": "Official Election Manifesto",
                "publisher": "Karnataka Pradesh Congress Committee"
            },
            {
                "id": "src-food-supplies-2023",
                "title": "Food, Civil Supplies and Consumer Affairs Government Order",
                "url": "https://ahara.kar.nic.in",
                "type": "Department Order",
                "publisher": "Food & Civil Supplies Dept"
            }
        ]
    },
    {
        "id": "yuvanidhi",
        "stateId": "karnataka",
        "administrationId": "karnataka-inc-2023",
        "name": "Yuvanidhi",
        "kannadaName": "ಯುವ ನಿಧಿ",
        "department": "Department of Skill Development, Entrepreneurship and Livelihood",
        "governmentOrder": "G.O. SDEL 57 TPE 2023 (Dated: 28-07-2023)",
        "category": "youth",
        "categoryLabel": "🎓 Youth & Jobs",
        "status": "delivered",
        "statusLabel": "Delivered / Active",
        "summary": "Monthly unemployment stipend: ₹3,000 for degree graduates, ₹1,500 for diploma holders.",
        "manifestoQuote": "₹3,000 per month for two years to unemployed graduates and ₹1,500 per month for two years to unemployed diploma holders.",
        "implementationDetails": "Direct financial allowance to unemployed graduates (₹3,000/mo) and diploma holders (₹1,500/mo) who graduated in 2022-2023 and remained unemployed 180 days after graduation. Paid for up to 24 months or until employment is found.",
        "eligibility": "Unemployed degree and diploma holders domiciled in Karnataka who passed in 2022-23 and are not enrolled in higher education or employed in the formal sector.",
        "metrics": {
            "target": "₹3,000 (Degree) / ₹1,500 (Diploma) monthly for up to 24 months",
            "delivered": "Monthly DBT allowance for verified applicants",
            "metricType": "Unemployment Financial Allowance & Verified Beneficiaries",
            "reportingPeriod": "Monthly disbursements (Operational since January 2024)",
            "lastUpdated": "Skill Development & Livelihood Dept (2024)",
            "progressModel": "Time-Bound Transitional Youth Support"
        },
        "dataNotes": "Beneficiaries must log into the Seva Sindhu portal each month to submit a self-declaration confirming their continued unemployment status and non-enrollment in higher studies.",
        "sources": [
            {
                "id": "src-manifesto-2023",
                "title": "Karnataka Congress Assembly Election Manifesto 2023",
                "url": "Assembly_Election_Karnataka_Manifesto_2023_241fdc08d0.pdf",
                "type": "Official Election Manifesto",
                "publisher": "Karnataka Pradesh Congress Committee"
            },
            {
                "id": "src-sevasindhu-2024",
                "title": "Skill Development Dept Order (SDEL 57 TPE 2023)",
                "url": "https://sevasindhuservices.karnataka.gov.in",
                "type": "Official Government Portal",
                "publisher": "Govt of Karnataka"
            }
        ]
    },
    {
        "id": "shakti",
        "stateId": "karnataka",
        "administrationId": "karnataka-inc-2023",
        "name": "Shakti",
        "kannadaName": "ಶಕ್ತಿ ಯೋಜನೆ",
        "department": "Transport Department, Government of Karnataka",
        "governmentOrder": "G.O. TD 59 TRM 2023 (Dated: 05-06-2023)",
        "category": "transport",
        "categoryLabel": "🚌 Transport",
        "status": "delivered",
        "statusLabel": "Delivered / Active",
        "summary": "Free zero-fare bus travel for women domiciled in Karnataka across state transport corporation buses.",
        "manifestoQuote": "Free travel to all women throughout the state in regular KSRTC / BMTC buses.",
        "implementationDetails": "Zero-fare public transit for women domiciled in Karnataka across all four state transport corporations (KSRTC, BMTC, NWKRTC, KKRTC) in city, ordinary, and express bus routes.",
        "eligibility": "All female and transgender citizens domiciled in Karnataka. Beneficiaries show a government-issued address ID to obtain zero-fare tickets.",
        "metrics": {
            "target": "100% free bus travel for women in ordinary & express state buses",
            "delivered": "Over 250+ crore zero-fare tickets issued across 4 RTCs",
            "metricType": "Passenger Trips & Corporation Reimbursements",
            "reportingPeriod": "Continuous (Operational since June 2023)",
            "lastUpdated": "Transport Department G.O. (2024)",
            "progressModel": "Ongoing Public Transit Subsidy"
        },
        "dataNotes": "Bus transit progress is measured through zero-fare passenger trips logged and state treasury corporation reimbursements, not physical infrastructure completion.",
        "sources": [
            {
                "id": "src-manifesto-2023",
                "title": "Karnataka Congress Assembly Election Manifesto 2023",
                "url": "Assembly_Election_Karnataka_Manifesto_2023_241fdc08d0.pdf",
                "type": "Official Election Manifesto",
                "publisher": "Karnataka Pradesh Congress Committee"
            },
            {
                "id": "src-ksrtc-order-2023",
                "title": "Transport Department Notification & Guidelines",
                "url": "https://ksrtc.in",
                "type": "Transport Corporation Order",
                "publisher": "Transport Department, Govt of Karnataka"
            }
        ]
    }
]

# ============================================================================
# 2. STATIC FRONTEND SERVING
# ============================================================================

@app.route("/")
def serve_index():
    """Serves the main frontend single-page dashboard."""
    return send_from_directory(".", "index.html")

@app.route("/<path:path>")
def serve_static_files(path):
    """Serves CSS, JS, PDFs, and assets."""
    if os.path.exists(path):
        return send_from_directory(".", path)
    return jsonify({"error": "File Not Found", "path": path}), 404

# ============================================================================
# 3. REST API ENDPOINTS
# ============================================================================

@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint to verify backend and database connection status."""
    db_connected = db.is_db_connected()
    return jsonify({
        "status": "healthy",
        "application": "LokLens — A Lens Through Development",
        "version": "1.0.0",
        "database": "mysql_connected" if db_connected else "in_memory_fallback",
        "environment": "development"
    }), 200

@app.route("/api/states", methods=["GET"])
def get_states():
    """Returns the list of all supported Indian states."""
    states = db.get_states()
    if states is None:
        states = STATES_FALLBACK

    return jsonify({
        "count": len(states),
        "states": states
    }), 200

@app.route("/api/administrations", methods=["GET"])
def get_administrations():
    """Returns governments / administrations."""
    state_id = request.args.get("state")
    admins = db.get_administrations(state_id)
    if admins is None:
        if state_id:
            admins = [a for a in ADMINISTRATIONS_FALLBACK if a["stateId"] == state_id]
        else:
            admins = ADMINISTRATIONS_FALLBACK

    return jsonify({"count": len(admins), "administrations": admins}), 200

@app.route("/api/promises", methods=["GET"])
def get_promises():
    """
    Returns manifesto promises with optional filtering.
    Query parameters:
    - ?state=karnataka
    - ?category=energy
    - ?search=electricity
    """
    state_filter = request.args.get("state", "karnataka").lower().strip()
    category_filter = request.args.get("category", "all").lower().strip()
    search_query = request.args.get("search", "").lower().strip()

    # 1. Check if state exists
    states = db.get_states() or STATES_FALLBACK
    state_record = next((s for s in states if s["id"] == state_filter), None)
    if not state_record:
        return jsonify({
            "error": "Invalid State",
            "message": f"State '{state_filter}' is not recognized."
        }), 400

    if not state_record["hasData"]:
        return jsonify({
            "state": state_record["name"],
            "hasData": False,
            "message": state_record.get("message", "Data pending verification."),
            "count": 0,
            "promises": []
        }), 200

    # 2. Try DB query first
    results = db.get_promises(state_filter, category_filter, search_query)

    # If DB not connected, use fallback store
    if results is None:
        results = [p for p in PROMISES_FALLBACK if p["stateId"] == state_filter]
        if category_filter and category_filter != "all":
            results = [p for p in results if p["category"] == category_filter]
        if search_query:
            results = [
                p for p in results
                if search_query in p["name"].lower()
                or search_query in p["manifestoQuote"].lower()
                or search_query in p["summary"].lower()
                or search_query in p["metrics"]["target"].lower()
            ]

    total_count = 5 if state_filter == "karnataka" else 0
    return jsonify({
        "state": state_record["name"],
        "hasData": True,
        "count": len(results),
        "totalGuarantees": total_count,
        "promises": results
    }), 200

@app.route("/api/promises/<string:promise_id>", methods=["GET"])
def get_promise_detail(promise_id):
    """Returns the full detailed profile of a single promise."""
    promise = db.get_promise_by_id(promise_id)
    
    if promise is False:
        return jsonify({
            "error": "Not Found",
            "message": f"Promise with ID '{promise_id}' was not found."
        }), 404

    if promise is None:
        # Fallback to in-memory list
        promise = next((p for p in PROMISES_FALLBACK if p["id"] == promise_id), None)
        if not promise:
            return jsonify({
                "error": "Not Found",
                "message": f"Promise with ID '{promise_id}' was not found."
            }), 404

    return jsonify(promise), 200

@app.route("/api/promises/<string:promise_id>/progress", methods=["GET"])
def get_promise_progress(promise_id):
    """Returns scheme progress, metrics, and reporting period for a promise."""
    promise = db.get_promise_by_id(promise_id)
    if promise is None or promise is False:
        promise = next((p for p in PROMISES_FALLBACK if p["id"] == promise_id), None)

    if not promise:
        return jsonify({
            "error": "Not Found",
            "message": f"Promise with ID '{promise_id}' was not found."
        }), 404

    return jsonify({
        "promiseId": promise["id"],
        "name": promise["name"],
        "status": promise["status"],
        "statusLabel": promise["statusLabel"],
        "metrics": promise["metrics"],
        "dataNotes": promise["dataNotes"]
    }), 200

@app.route("/api/sources", methods=["GET"])
def get_all_sources():
    """Returns a consolidated list of all documented sources."""
    sources = db.get_sources()
    if sources is None:
        sources = []
        seen = set()
        for promise in PROMISES_FALLBACK:
            for src in promise["sources"]:
                if src["id"] not in seen:
                    seen.add(src["id"])
                    sources.append(src)

    return jsonify({
        "count": len(sources),
        "sources": sources
    }), 200

# ============================================================================
# 4. ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint Not Found",
        "message": "The requested API endpoint does not exist."
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal Server Error",
        "message": "An unexpected error occurred on the server."
    }), 500

# ============================================================================
# 5. SERVER ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    db_mode = "MySQL (loklens_db)" if db.is_db_connected() else "In-Memory Fallback (Set .env for MySQL)"
    print("\n" + "="*60)
    print(" LokLens — A Lens Through Development")
    print(f" Database Mode: {db_mode}")
    print(" REST API Server running at: http://127.0.0.1:5000")
    print("="*60 + "\n")
    app.run(host="127.0.0.1", port=5000, debug=True)
