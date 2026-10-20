/**
 * toolkit_tracker.js (v3 - Final)
 * Tracking system for Advanced Communicator's Toolkit tools 1-8.
 * Stores dynamic tool data in localStorage and sends it to Django.
 */

(function () {
    const STORAGE_KEY = "advanced_toolkit_progress_global";
    const START_KEY = "advanced_toolkit_started_at";

    const TOOL_KEYS = [
        "tool1_grammar_hacks",
        "tool2_power_word",
        "tool3_word_search",
        "tool4_idiom_challenge",
        "tool5_grammar_detective",
        "tool6_word_association",
        "tool7_sentence_transform",
        "tool8_register_remix"
    ];

    let toolkitDirty = false;

    // 1. Persist Start Time
    function getStoredStartTime() {
        let startedAt = localStorage.getItem(START_KEY);
        if (!startedAt) {
            startedAt = new Date().toISOString();
            localStorage.setItem(START_KEY, startedAt);
        }
        return startedAt;
    }

    function getDefaultAnalytics() {
        return {
            toolkit_started_at: getStoredStartTime(),
            toolkit_completed: false,
            toolkit_total_tools_completed: 0,
            toolkit_score: 0,
            advanced_toolkit_data: {}
        };
    }

    // 2. Initialize from Storage
    function loadToolkitAnalytics() {
        const saved = localStorage.getItem(STORAGE_KEY);
        if (!saved) {
            return getDefaultAnalytics();
        }

        try {
            const parsed = JSON.parse(saved);
            return {
                ...getDefaultAnalytics(),
                ...parsed,
                advanced_toolkit_data: parsed.advanced_toolkit_data || {}
            };
        } catch (e) {
            console.warn("Toolkit analytics cache corrupted. Resetting.");
            return getDefaultAnalytics();
        }
    }

    window.toolkitAnalytics = loadToolkitAnalytics();

    function calculateToolkitSummary() {
        const data = window.toolkitAnalytics.advanced_toolkit_data || {};

        const completedCount = TOOL_KEYS.filter(key => {
            return data[key] && data[key].completed === true;
        }).length;

        window.toolkitAnalytics.toolkit_total_tools_completed = completedCount;
        window.toolkitAnalytics.toolkit_completed = (completedCount === 8);
        window.toolkitAnalytics.toolkit_score = Math.round((completedCount / 8) * 100);
    }

    function saveLocalToolkitAnalytics() {
        calculateToolkitSummary();
        localStorage.setItem(STORAGE_KEY, JSON.stringify(window.toolkitAnalytics));
        toolkitDirty = true;
    }

    // 3. Helper: Get CSRF Token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === name + "=") {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // 4. Save to Backend
    async function saveToolkitAnalytics(force = false) {
        if (!toolkitDirty && !force) return;

        try {
            calculateToolkitSummary();

            const response = await fetch("/learning/api/save-advanced-toolkit/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify(window.toolkitAnalytics)
            });

            if (response.ok) {
                toolkitDirty = false;
            }
        } catch (err) {
            console.error("Failed to save toolkit analytics:", err);
        }
    }

    // 5. Tool Data Modifiers
    function updateCurrentToolData(partialData) {
        const toolKey = document.querySelector('meta[name="tool-key"]')?.content;
        if (!toolKey) return;

        const existing = window.toolkitAnalytics.advanced_toolkit_data[toolKey] || {};

        window.toolkitAnalytics.advanced_toolkit_data[toolKey] = {
            ...existing,
            ...partialData,
            visited: true,
            last_updated_at: new Date().toISOString()
        };

        saveLocalToolkitAnalytics();
    }

    function markCurrentToolCompleted(extraData = {}) {
        updateCurrentToolData({
            ...extraData,
            completed: true,
            completed_at: new Date().toISOString()
        });

        saveToolkitAnalytics(true);
    }

    // 6. Generic Data Detection
    function detectKnownToolData() {
        const toolKey = document.querySelector('meta[name="tool-key"]')?.content;
        if (!toolKey) return;

        let data = { visited: true };

        // Detection based on common project variables
        if (typeof window.masteredHacks !== "undefined") {
            data.hacks_mastered_count = Array.isArray(window.masteredHacks) ? window.masteredHacks.length : Object.keys(window.masteredHacks || {}).length;
        }
        if (typeof window.powerWordsHeard !== "undefined") {
            data.power_words_heard_count = Array.isArray(window.powerWordsHeard) ? window.powerWordsHeard.length : Object.keys(window.powerWordsHeard || {}).length;
        }
        if (typeof window.foundWords !== "undefined") {
            data.words_found = Array.isArray(window.foundWords) ? window.foundWords.length : Object.keys(window.foundWords || {}).length;
        }
        if (typeof window.userAssociations !== "undefined") {
            data.total_attempted = Array.isArray(window.userAssociations) ? window.userAssociations.length : Object.keys(window.userAssociations || {}).length;
        }
        if (typeof window.answers !== "undefined") {
            data.answers_count = Array.isArray(window.answers) ? window.answers.length : Object.keys(window.answers || {}).length;
        }

        updateCurrentToolData(data);
    }

    // 7. Lifecycle Hooks
    document.addEventListener("DOMContentLoaded", function () {
        const toolNumber = document.querySelector('meta[name="tool-number"]')?.content;
        const toolKey = document.querySelector('meta[name="tool-key"]')?.content;

        if (!toolNumber || !toolKey) return;

        updateCurrentToolData({
            tool_number: Number(toolNumber),
            visited: true,
            session_started_at: new Date().toISOString()
        });

        // Trigger detection on interactions
        document.addEventListener("click", () => setTimeout(detectKnownToolData, 500));
        document.addEventListener("input", () => setTimeout(detectKnownToolData, 500));
        document.addEventListener("change", () => setTimeout(detectKnownToolData, 500));

        // Periodic Sync
        setInterval(() => saveToolkitAnalytics(), 30000);

        // Final Save
        window.addEventListener("beforeunload", function () {
            detectKnownToolData();
            if (navigator.sendBeacon) {
                calculateToolkitSummary();
                const blob = new Blob([JSON.stringify(window.toolkitAnalytics)], { type: "application/json" });
                // Note: CSRF might fail with sendBeacon unless endpoint is exempt or token is in URL
                navigator.sendBeacon("/learning/api/save-advanced-toolkit/", blob);
            } else {
                saveToolkitAnalytics(true);
            }
        });
    });

    // Expose Helpers to window for tool scripts to call
    window.updateCurrentToolData = updateCurrentToolData;
    window.markCurrentToolCompleted = markCurrentToolCompleted;
    window.saveToolkitAnalytics = saveToolkitAnalytics;

})();
