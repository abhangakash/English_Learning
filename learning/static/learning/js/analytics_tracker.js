/**
 * analytics_tracker.js (v2 - Improved)
 * Robust tracking for the 30-day English Learning journey.
 */

(function() {
    // 1. Identify Page Context
    const level = document.querySelector('meta[name="analytics-level"]')?.content || 'unknown';
    const day = document.querySelector('meta[name="analytics-day"]')?.content || '0';
    const stage = document.querySelector('meta[name="analytics-stage"]')?.content || 'daily_learning';
    const STORAGE_KEY = `analytics_${level}_day${day}_${stage}`;

    // 2. Initialize Analytics Object (with Persistence)
    function getInitialAnalytics() {
        const saved = localStorage.getItem(STORAGE_KEY);
        if (saved) {
            try {
                return JSON.parse(saved);
            } catch (e) { console.error("Error loading analytics from storage:", e); }
        }

        return {
            level: level,
            day_number: parseInt(day),
            stage: stage,
            started_at: new Date().toISOString(),
            total_time_spent_seconds: 0,
            total_sections: 0,
            sections_completed: 0,
            completed_sections: [], // Tracking unique section IDs
            total_attempts: 0,
            total_correct_attempts: 0,
            total_wrong_attempts: 0,
            overall_accuracy: 0,
            activity_data: {
                listening: { audio_listen_time_seconds: 0, recording_attempts: 0, quiz_attempts: 0, correct_attempts: 0, wrong_attempts: 0, time_spent_seconds: 0 },
                speaking: { recording_attempts: 0, recording_duration_seconds: 0, valid_recording_count: 0, failed_recording_count: 0, time_spent_seconds: 0 },
                reading: { check_attempts: 0, correct_attempts: 0, wrong_attempts: 0, correct_clicks: 0, wrong_clicks: 0, time_spent_seconds: 0 },
                writing: { input_count: 0, word_count: 0, character_count: 0, check_attempts: 0, correct_attempts: 0, wrong_attempts: 0, time_spent_seconds: 0 },
                vocabulary: { total_words: 0, total_listens: 0, word_repetitions: {}, time_spent_seconds: 0 },
                grammar: { check_attempts: 0, correct_attempts: 0, wrong_attempts: 0, time_spent_seconds: 0 },
                game: { check_attempts: 0, correct_attempts: 0, wrong_attempts: 0, time_spent_seconds: 0 }
            }
        };
    }

    window.dayAnalytics = getInitialAnalytics();
    let analyticsDirty = false;
    let lastTick = Date.now();
    let activeSection = null;

    // --- Core Helpers ---

    function markDirty() {
        analyticsDirty = true;
        saveLocalAnalytics();
    }

    function saveLocalAnalytics() {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(window.dayAnalytics));
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    async function saveAnalyticsToServer(isFinal = false) {
        if (!analyticsDirty && !isFinal) return;

        try {
            // Update accuracy
            if (window.dayAnalytics.total_attempts > 0) {
                window.dayAnalytics.overall_accuracy = (window.dayAnalytics.total_correct_attempts / window.dayAnalytics.total_attempts) * 100;
            }

            const response = await fetch('/learning/api/save-day-analytics/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(window.dayAnalytics)
            });
            
            if (response.ok) {
                analyticsDirty = false;
            }
        } catch (err) {
            console.error('Failed to save analytics to server:', err);
        }
    }

    function markSectionComplete(sectionKey, buttonId) {
        if (!window.dayAnalytics.completed_sections.includes(buttonId)) {
            window.dayAnalytics.completed_sections.push(buttonId);
            window.dayAnalytics.sections_completed = window.dayAnalytics.completed_sections.length;
            markDirty();
        }
    }

    function addAttempt(sectionKey, completeBtnId) {
        window.dayAnalytics.total_attempts++;
        if (window.dayAnalytics.activity_data[sectionKey].check_attempts !== undefined) {
            window.dayAnalytics.activity_data[sectionKey].check_attempts++;
        } else if (sectionKey === 'listening') {
            window.dayAnalytics.activity_data.listening.quiz_attempts++;
        }
        
        // Use button state for better accuracy detection
        setTimeout(() => {
            const completeBtn = document.getElementById(completeBtnId);
            const isCorrect = completeBtn && !completeBtn.disabled;
            
            if (isCorrect) {
                window.dayAnalytics.total_correct_attempts++;
                window.dayAnalytics.activity_data[sectionKey].correct_attempts++;
            } else {
                window.dayAnalytics.total_wrong_attempts++;
                window.dayAnalytics.activity_data[sectionKey].wrong_attempts++;
            }
            markDirty();
        }, 500); // Wait for page logic to process
    }

    // --- Specialized Tracking ---

    // 1. Better Audio Tracking
    let lastAudioTime = 0;
    function trackAudio(audioElement) {
        audioElement.addEventListener('play', () => { 
            activeSection = 'listening';
            lastAudioTime = audioElement.currentTime;
        });
        audioElement.addEventListener('timeupdate', () => {
            const current = audioElement.currentTime;
            const delta = current - lastAudioTime;
            if (delta > 0 && delta < 2) { // Ignore seeking jumps
                window.dayAnalytics.activity_data.listening.audio_listen_time_seconds += delta;
                markDirty();
            }
            lastAudioTime = current;
        });
    }

    // 2. Speaking Duration Tracking
    let recordStartTime = null;
    function startRecordTimer() {
        recordStartTime = Date.now();
        window.dayAnalytics.activity_data.speaking.recording_attempts++;
        markDirty();
    }
    function stopRecordTimer() {
        if (recordStartTime) {
            const duration = (Date.now() - recordStartTime) / 1000;
            window.dayAnalytics.activity_data.speaking.recording_duration_seconds += duration;
            window.dayAnalytics.activity_data.speaking.valid_recording_count++;
            recordStartTime = null;
            markDirty();
        }
    }

    // --- Initialize Listeners ---

    document.addEventListener('DOMContentLoaded', () => {
        // Track sections available
        const possibleSectionIds = ['listening-card', 'speaking-card', 'reading-card', 'writing-card', 'vocabulary-card', 'grammar-card', 'game-card'];
        window.dayAnalytics.total_sections = possibleSectionIds.filter(id => document.getElementById(id)).length;

        // Listening
        const audio = document.getElementById('listeningAudio');
        if (audio) trackAudio(audio);

        const listenRec = document.getElementById('listeningRecordBtn') || document.getElementById('authorityRecordBtn');
        if (listenRec) listenRec.addEventListener('click', startRecordTimer);
        const listenStop = document.getElementById('listeningStopBtn') || document.getElementById('authorityStopBtn');
        if (listenStop) listenStop.addEventListener('click', stopRecordTimer);

        const checkListen = document.getElementById('checkListeningWorkBtn');
        if (checkListen) checkListen.addEventListener('click', () => addAttempt('listening', 'completeListeningBtn'));

        // Speaking
        ['speakingRecordBtn', 'speakingRecordBtn1', 'speakingRecordBtn2', 'speakingRecordBtn3'].forEach(id => {
            const btn = document.getElementById(id);
            if (btn) btn.addEventListener('click', startRecordTimer);
        });
        ['speakingStopBtn', 'speakingStopBtn1', 'speakingStopBtn2', 'speakingStopBtn3'].forEach(id => {
            const btn = document.getElementById(id);
            if (btn) btn.addEventListener('click', stopRecordTimer);
        });

        // Reading (support all levels)
        ['checkUnderlinesBtn', 'checkCirclesBtn', 'checkReadingBtn', 'checkTask3Btn', 'validateAdvancedReading'].forEach(id => {
            const btn = document.getElementById(id);
            if (btn) btn.addEventListener('click', () => addAttempt('reading', 'completeReadingBtn'));
        });

        // Writing
        const checkWriting = document.getElementById('checkWritingBtn');
        if (checkWriting) {
            checkWriting.addEventListener('click', () => {
                const inputs = document.querySelectorAll('#writing-card input[type="text"], #writing-card textarea');
                let wordCount = 0;
                let charCount = 0;
                inputs.forEach(i => {
                    const val = i.value.trim();
                    if (val) {
                        wordCount += val.split(/\s+/).length;
                        charCount += val.length;
                    }
                });
                window.dayAnalytics.activity_data.writing.input_count = inputs.length;
                window.dayAnalytics.activity_data.writing.word_count = wordCount;
                window.dayAnalytics.activity_data.writing.character_count = charCount;
                addAttempt('writing', 'completeWritingBtn');
            });
        }

        // Vocabulary
        document.querySelectorAll('.vocab-audio-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const word = btn.getAttribute('data-word');
                window.dayAnalytics.activity_data.vocabulary.total_listens++;
                window.dayAnalytics.activity_data.vocabulary.word_repetitions[word] = (window.dayAnalytics.activity_data.vocabulary.word_repetitions[word] || 0) + 1;
                markDirty();
            });
        });
        const vocabTable = document.querySelector('.vocab-table');
        if (vocabTable) {
            window.dayAnalytics.activity_data.vocabulary.total_words = vocabTable.querySelectorAll('tbody tr').length;
        }

        // Grammar
        const checkGrammar = document.getElementById('checkGrammarBtn');
        if (checkGrammar) checkGrammar.addEventListener('click', () => addAttempt('grammar', 'completeGrammarBtn'));

        // Game
        const checkGame = document.getElementById('checkGameBtn');
        if (checkGame) checkGame.addEventListener('click', () => addAttempt('game', 'completeGameBtn'));

        // Section Completion Buttons
        const completeMapping = [
            { id: 'completeListeningBtn', key: 'listening' },
            { id: 'completeSpeakingBtn', key: 'speaking' },
            { id: 'completeReadingBtn', key: 'reading' },
            { id: 'completeWritingBtn', key: 'writing' },
            { id: 'completeVocabularyBtn', key: 'vocabulary' },
            { id: 'completeGrammarBtn', key: 'grammar' },
            { id: 'completeGameBtn', key: 'game' }
        ];

        completeMapping.forEach(item => {
            const btn = document.getElementById(item.id);
            if (btn) {
                btn.addEventListener('click', () => {
                    markSectionComplete(item.key, item.id);
                    saveAnalyticsToServer();
                });
            }
        });

        // Day Complete
        const dayComplete = document.getElementById('dayCompleteBtn');
        if (dayComplete) {
            dayComplete.addEventListener('click', async (e) => {
                // Ensure final data is sent before leaving
                await saveAnalyticsToServer(true);
                // Clear local storage for this day after successful completion? 
                // Better to keep it as a backup for a while or clear it here.
                // localStorage.removeItem(STORAGE_KEY);
            });
        }
    });

    // Global Time Ticker
    setInterval(() => {
        const now = Date.now();
        const delta = Math.floor((now - lastTick) / 1000);
        if (delta >= 1) {
            window.dayAnalytics.total_time_spent_seconds += delta;
            // Track active section timer
            const cards = ['listening', 'speaking', 'reading', 'writing', 'vocabulary', 'grammar', 'game'];
            cards.forEach(key => {
                const card = document.getElementById(`${key}-card`);
                if (card && card.getBoundingClientRect().top < window.innerHeight && card.getBoundingClientRect().bottom > 0) {
                    window.dayAnalytics.activity_data[key].time_spent_seconds += delta;
                }
            });
            lastTick = now;
            saveLocalAnalytics(); // Sync to local storage frequently
        }
    }, 1000);

    // Heartbeat Server Sync (only if dirty)
    setInterval(() => saveAnalyticsToServer(), 30000);

})();
