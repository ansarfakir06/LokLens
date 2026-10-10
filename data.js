/**
 * LokLens — Trustworthy Civic Data Store (data.js)
 * 
 * Purpose:
 * Stores thoroughly documented manifesto promises, on-ground implementation records,
 * and official government citations for the Karnataka Congress 2023 Assembly Election.
 * 
 * Data Integrity Principles (Section 7 & 8):
 * 1. Schemes are tracked using appropriate metrics (DBT amounts, power units, bus trips),
 *    NOT forced into generic construction percentages.
 * 2. Original manifesto promises are preserved verbatim.
 * 3. Clear citations to Departmental Government Orders (G.O.) and Gazettes.
 * 4. Transparent notes explaining policy adjustments (e.g. Anna Bhagya's grain+cash formula).
 */

const LOKLENS_DATA = {
    states: {
        "karnataka": {
            id: "karnataka",
            name: "Karnataka",
            administration: "Government of Karnataka (16th Legislative Assembly)",
            party: "Indian National Congress (INC)",
            term: "2023–2028",
            manifestoTitle: "Karnataka Congress Assembly Election Manifesto 2023",
            subtitle: "5 Flagship Guarantees — Verified against Official Departmental Orders",
            hasData: true,
            promises: [
                {
                    id: "gruha-jyothi",
                    name: "Gruha Jyothi",
                    kannadaName: "ಗೃಹ ಜ್ಯೋತಿ",
                    department: "Energy Department, Government of Karnataka",
                    governmentOrder: "G.O. EN 22 PSR 2023 (Dated: 05-06-2023)",
                    category: "energy",
                    categoryLabel: "⚡ Energy",
                    status: "delivered",
                    statusLabel: "Delivered / Active",
                    summary: "Up to 200 units of zero-cost electricity per month to eligible domestic households.",
                    manifestoQuote: "200 units of free electricity to all the houses.",
                    implementationDetails: "Sanctioned zero-cost domestic electricity up to a ceiling of 200 units per month for households across all state electricity supply companies (BESCOM, MESCOM, CESC, HESCOM, GESCOM). The monthly entitled quota is calculated based on each consumer's past 12-month average consumption plus an additional 10% entitlement buffer. If consumption remains within this entitled quota and under 200 units, the consumer receives a zero electricity bill.",
                    eligibility: "All domestic LT-2 category electricity consumer accounts in Karnataka. Commercial and industrial connections are excluded.",
                    metrics: {
                        target: "Up to 200 units / month per domestic consumer account",
                        delivered: "Zero-bill benefit applied across 1.6+ crore domestic accounts",
                        metricType: "Power Consumption (kWh) & Consumer Accounts",
                        reportingPeriod: "Monthly billing cycles (Operational since August 2023)",
                        lastUpdated: "Karnataka Gazette & Energy Department (2024)",
                        progressModel: "Recurring Operational Benefit (Non-construction scheme)"
                    },
                    dataNotes: "Electricity subsidy schemes represent ongoing monthly service benefits, not a one-time construction project. Progress is measured in beneficiary households receiving zero bills and subsidy amounts disbursed to electricity supply companies (ESCOMs). We do not display arbitrary completion percentages.",
                    sources: [
                        {
                            title: "Karnataka Congress Assembly Election Manifesto 2023",
                            url: "Assembly_Election_Karnataka_Manifesto_2023_241fdc08d0.pdf",
                            type: "Official Election Manifesto",
                            publisher: "Karnataka Pradesh Congress Committee (KPCC)"
                        },
                        {
                            title: "Energy Department Government Order (G.O. EN 22 PSR 2023)",
                            url: "https://karnataka.gov.in",
                            type: "Official Government Order",
                            publisher: "Energy Department, Govt of Karnataka"
                        },
                        {
                            title: "Seva Sindhu Citizen Services Portal — Gruha Jyothi Guidelines",
                            url: "https://sevasindhuservices.karnataka.gov.in",
                            type: "Citizen Services Portal",
                            publisher: "Centre for e-Governance, Karnataka"
                        }
                    ]
                },
                {
                    id: "gruha-lakshmi",
                    name: "Gruha Lakshmi",
                    kannadaName: "ಗೃಹ ಲಕ್ಷ್ಮಿ",
                    department: "Department of Women and Child Development",
                    governmentOrder: "G.O. WCD 90 MMB 2023 (Dated: 07-06-2023)",
                    category: "women",
                    categoryLabel: "👩 Women Welfare",
                    status: "delivered",
                    statusLabel: "Delivered / Active",
                    summary: "₹2,000 monthly direct financial assistance to the woman head of every family.",
                    manifestoQuote: "₹2,000 every month to each woman head of the family.",
                    implementationDetails: "Direct Benefit Transfer (DBT) of ₹2,000 deposited monthly directly into the Aadhaar-seeded bank account of the woman designated as head of the family on Antyodaya, BPL, and APL ration cards. The scheme is designed to enhance financial autonomy and support household living expenditures.",
                    eligibility: "Women recognized as head of household on Antyodaya Anna Yojana (AAY), Below Poverty Line (BPL), and Above Poverty Line (APL) ration cards. Excludes women or their spouses who are income-tax assessees or GST registrants.",
                    metrics: {
                        target: "₹2,000 / month per eligible family",
                        delivered: "Monthly DBT transfers to over 1.18 crore enrolled women heads",
                        metricType: "Direct Financial Assistance (DBT) & Enrolled Beneficiaries",
                        reportingPeriod: "Monthly disbursement rounds (Operational since August 2023)",
                        lastUpdated: "Women & Child Development Department (2024)",
                        progressModel: "Recurring Social Welfare Cash Transfer"
                    },
                    dataNotes: "Cash transfers operate on recurring monthly payment cycles. Delivery is evaluated through bank disbursement success rates and verified ration-card linkages, not physical construction milestones.",
                    sources: [
                        {
                            title: "Karnataka Congress Assembly Election Manifesto 2023",
                            url: "Assembly_Election_Karnataka_Manifesto_2023_241fdc08d0.pdf",
                            type: "Official Election Manifesto",
                            publisher: "Karnataka Pradesh Congress Committee"
                        },
                        {
                            title: "Department of Women and Child Development Guidelines (G.O. WCD 90 MMB 2023)",
                            url: "https://karnataka.gov.in",
                            type: "Official Department Guidelines",
                            publisher: "Women & Child Development Dept"
                        },
                        {
                            title: "Karnataka Direct Benefit Transfer (DBT) Portal Records",
                            url: "https://dbt.karnataka.gov.in",
                            type: "State DBT Monitoring Portal",
                            publisher: "Finance Department, Govt of Karnataka"
                        }
                    ]
                },
                {
                    id: "anna-bhagya",
                    name: "Anna Bhagya",
                    kannadaName: "ಅನ್ನ ಭಾಗ್ಯ",
                    department: "Department of Food, Civil Supplies and Consumer Affairs",
                    governmentOrder: "G.O. FCS 47 RPR 2023 (Dated: 08-07-2023)",
                    category: "food",
                    categoryLabel: "🌾 Food Security",
                    status: "adjusted",
                    statusLabel: "Partly Cash / Active",
                    summary: "10 kg free food grains per person per month for BPL families (delivered as 5 kg rice + ₹170 cash equivalent).",
                    manifestoQuote: "10 Kgs of food grains to every person in BPL family.",
                    implementationDetails: "The manifesto promised 10 kg of food grains per person per month. The Government of India already provides 5 kg of free rice per beneficiary under the National Food Security Act (NFSA / PMGKAY). The state promised an additional 5 kg. Due to initial procurement challenges in sourcing sufficient rice from the Food Corporation of India (FCI) and other state governments, the Karnataka cabinet approved a policy adjustment to disburse cash compensation of ₹170 per person per month (at ₹34 per kg for 5 kg) directly to beneficiaries' bank accounts via DBT alongside 5 kg physical grain.",
                    eligibility: "Every individual member listed on Antyodaya Anna Yojana (AAY) and Priority Household (BPL) ration cards in Karnataka.",
                    metrics: {
                        target: "10 kg food grains / person / month",
                        delivered: "5 kg physical rice + ₹170 cash equivalent per person via DBT",
                        metricType: "Food Grains (kg) & Direct Cash Compensation (₹)",
                        reportingPeriod: "Monthly fair-price shop allocations & DBT cycles",
                        lastUpdated: "Food & Civil Supplies Department (2024)",
                        progressModel: "Hybrid Food Security Allocation (Grain + Cash Equivalent)"
                    },
                    dataNotes: "Status is transparently designated 'Partly Cash / Active'. LokLens does not mark this as 100% physically delivered in grain because the state government substituted 5 kg of grain with direct cash compensation due to supply-chain procurement realities.",
                    sources: [
                        {
                            title: "Karnataka Congress Assembly Election Manifesto 2023",
                            url: "Assembly_Election_Karnataka_Manifesto_2023_241fdc08d0.pdf",
                            type: "Official Election Manifesto",
                            publisher: "Karnataka Pradesh Congress Committee"
                        },
                        {
                            title: "Food, Civil Supplies and Consumer Affairs Government Order",
                            url: "https://ahara.kar.nic.in",
                            type: "Department Order",
                            publisher: "Food & Civil Supplies Dept, Karnataka"
                        },
                        {
                            title: "State Food Commission Annual Report & PDS Bulletin",
                            url: "https://ahara.kar.nic.in",
                            type: "Public Distribution System Bulletin",
                            publisher: "Govt of Karnataka"
                        }
                    ]
                },
                {
                    id: "yuvanidhi",
                    name: "Yuvanidhi",
                    kannadaName: "ಯುವ ನಿಧಿ",
                    department: "Department of Skill Development, Entrepreneurship and Livelihood",
                    governmentOrder: "G.O. SDEL 57 TPE 2023 (Dated: 28-07-2023)",
                    category: "youth",
                    categoryLabel: "🎓 Youth & Jobs",
                    status: "delivered",
                    statusLabel: "Delivered / Active",
                    summary: "Monthly unemployment stipend: ₹3,000 for degree graduates and ₹1,500 for diploma holders for up to 2 years.",
                    manifestoQuote: "₹3,000 per month for two years to unemployed graduates and ₹1,500 per month for two years to unemployed diploma holders.",
                    implementationDetails: "Financial allowance of ₹3,000/month for degree holders and ₹1,500/month for diploma holders who graduated in the academic year 2022-2023 and remain unemployed 180 days after completion of studies. Allowance is provided for a maximum duration of 24 months, or until the candidate obtains formal employment or enters self-employment, whichever is earlier.",
                    eligibility: "Unemployed degree and diploma holders domiciled in Karnataka who passed in 2022-23 and are not enrolled in higher education or employed in the formal/informal sector.",
                    metrics: {
                        target: "₹3,000 (Degree) / ₹1,500 (Diploma) monthly for up to 24 months",
                        delivered: "Direct monthly stipend transferred to verified applicant accounts",
                        metricType: "Unemployment Financial Allowance & Verified Beneficiaries",
                        reportingPeriod: "Monthly disbursements (Operational since January 2024)",
                        lastUpdated: "Skill Development & Livelihood Dept (2024)",
                        progressModel: "Time-Bound Transitional Youth Support"
                    },
                    dataNotes: "Beneficiaries must log into the Seva Sindhu portal each month to submit a self-declaration confirming their continued unemployment status and non-enrollment in further degree programs.",
                    sources: [
                        {
                            title: "Karnataka Congress Assembly Election Manifesto 2023",
                            url: "Assembly_Election_Karnataka_Manifesto_2023_241fdc08d0.pdf",
                            type: "Official Election Manifesto",
                            publisher: "Karnataka Pradesh Congress Committee"
                        },
                        {
                            title: "Department of Skill Development Scheme Notification (SDEL 57 TPE 2023)",
                            url: "https://sevasindhuservices.karnataka.gov.in",
                            type: "Official Government Order",
                            publisher: "Skill Development Dept, Govt of Karnataka"
                        },
                        {
                            title: "Yuva Nidhi Seva Sindhu Application & Verification Portal",
                            url: "https://sevasindhuservices.karnataka.gov.in",
                            type: "Official Application Portal",
                            publisher: "Govt of Karnataka"
                        }
                    ]
                },
                {
                    id: "shakti",
                    name: "Shakti",
                    kannadaName: "ಶಕ್ತಿ ಯೋಜನೆ",
                    department: "Transport Department, Government of Karnataka",
                    governmentOrder: "G.O. TD 59 TRM 2023 (Dated: 05-06-2023)",
                    category: "transport",
                    categoryLabel: "🚌 Transport",
                    status: "delivered",
                    statusLabel: "Delivered / Active",
                    summary: "Free zero-fare bus travel for women domiciled in Karnataka across state transport corporations.",
                    manifestoQuote: "Free travel to all women throughout the state in regular KSRTC / BMTC buses.",
                    implementationDetails: "Zero-fare public transit for women and transgender citizens domiciled in Karnataka across all four state transport corporations: Karnataka State Road Transport Corporation (KSRTC), Bengaluru Metropolitan Transport Corporation (BMTC), North Western Karnataka Road Transport Corporation (NWKRTC), and Kalyana Karnataka Road Transport Corporation (KKRTC). The scheme applies to city, ordinary, and express services, while excluding luxury and air-conditioned buses (e.g., Rajahamsa, Vajra, Airavat, Flybus).",
                    eligibility: "All female and transgender citizens domiciled in Karnataka. Beneficiaries show a government-issued photo identity card with Karnataka domicile address to obtain zero-fare tickets.",
                    metrics: {
                        target: "100% free travel for women in ordinary & express state buses",
                        delivered: "Over 250+ crore zero-fare passenger trips logged across 4 RTCs",
                        metricType: "Zero-Fare Passenger Trips & State Reimbursements",
                        reportingPeriod: "Continuous operational transit (Active since June 11, 2023)",
                        lastUpdated: "Transport Department & RTC Bulletins (2024)",
                        progressModel: "Ongoing Public Transit Subsidy"
                    },
                    dataNotes: "Public transit progress is evaluated by counting zero-fare passenger trips issued by conductors and state government treasury reimbursements paid to transport corporations, not physical infrastructure completion.",
                    sources: [
                        {
                            title: "Karnataka Congress Assembly Election Manifesto 2023",
                            url: "Assembly_Election_Karnataka_Manifesto_2023_241fdc08d0.pdf",
                            type: "Official Election Manifesto",
                            publisher: "Karnataka Pradesh Congress Committee"
                        },
                        {
                            title: "Transport Department Government Order (G.O. TD 59 TRM 2023)",
                            url: "https://ksrtc.in",
                            type: "Official Government Order",
                            publisher: "Transport Department, Govt of Karnataka"
                        },
                        {
                            title: "Karnataka State Transport Corporations Operational Reports",
                            url: "https://transport.karnataka.gov.in",
                            type: "Corporation Ridership Reports",
                            publisher: "KSRTC, BMTC, NWKRTC, KKRTC"
                        }
                    ]
                }
            ]
        },
        "tamil-nadu": {
            id: "tamil-nadu",
            name: "Tamil Nadu",
            hasData: false,
            message: "We have not yet compiled verified manifesto promises and government execution orders for Tamil Nadu. LokLens adheres to strict data verification rules and does not publish unverified or placeholder data."
        },
        "telangana": {
            id: "telangana",
            name: "Telangana",
            hasData: false,
            message: "Manifesto data for Telangana is currently in the research pipeline. Official party manifestos and state government department budget reports are undergoing verification."
        },
        "andhra-pradesh": {
            id: "andhra-pradesh",
            name: "Andhra Pradesh",
            hasData: false,
            message: "Assembly election manifesto promises and implementation records for Andhra Pradesh are pending source compilation. Check back soon for verified records."
        },
        "maharashtra": {
            id: "maharashtra",
            name: "Maharashtra",
            hasData: false,
            message: "Manifesto tracking records for Maharashtra are pending source documentation. We only publish records supported by downloadable official government gazettes."
        }
    }
};
