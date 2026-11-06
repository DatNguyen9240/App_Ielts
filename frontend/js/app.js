/**
 * Smart Video Vocabulary & Flashcard App - Frontend Logic
 * Kết nối FastAPI Backend + HTML5 Video Seeking + 3D Flashcard Deck
 */

// ==================== STATE MANAGEMENT ====================
const state = {
    topics: [],
    activeTab: "my_videos", // "my_videos" hoặc topic object
    selectedTopic: "all",
    videos: [],
    currentVideo: null,
    flashcards: [],
    currentCardIndex: 0,
    isCardFlipped: false,
    searchDebounceTimer: null,
    watchingVideo: null,
    activeScanningTarget: null, // { type: "local" | "online", video: object }
    topicPagination: {
        active: false,
        query: "",
        topicTitle: "",
        page: 1,
        pageSize: 12,
        hasMore: true,
        isLoading: false,
        seenIds: new Set()
    },
    currentTopicVocabs: []
};

// ==================== DOM ELEMENTS ====================
const DOM = {
    // Tabs
    tabVideoBtn: document.getElementById("tabVideoBtn"),
    tabFlashcardBtn: document.getElementById("tabFlashcardBtn"),
    tabVideoSection: document.getElementById("tabVideoSection"),
    tabFlashcardSection: document.getElementById("tabFlashcardSection"),
    flashcardCountBadge: document.getElementById("flashcardCountBadge"),

    // Views
    myVideosView: document.getElementById("myVideosView"),
    topicDiscoveryView: document.getElementById("topicDiscoveryView"),
    topicDiscoveryTitle: document.getElementById("topicDiscoveryTitle"),
    topicVideosLoading: document.getElementById("topicVideosLoading"),
    topicVideosGrid: document.getElementById("topicVideosGrid"),
    topicInfiniteScrollArea: document.getElementById("topicInfiniteScrollArea"),
    infiniteScrollLoading: document.getElementById("infiniteScrollLoading"),
    loadMoreTopicVideosBtn: document.getElementById("loadMoreTopicVideosBtn"),
    infiniteScrollEnd: document.getElementById("infiniteScrollEnd"),
    refreshTopicVideosBtn: document.getElementById("refreshTopicVideosBtn"),
    openTopicVocabModalBtn: document.getElementById("openTopicVocabModalBtn"),
    backToMyVideosBtn: document.getElementById("backToMyVideosBtn"),
    youtubeSearchKeywordInput: document.getElementById("youtubeSearchKeywordInput"),
    youtubeSearchSubmitBtn: document.getElementById("youtubeSearchSubmitBtn"),

    // Topic Vocab Modal
    topicVocabModal: document.getElementById("topicVocabModal"),
    closeTopicVocabModalBtn: document.getElementById("closeTopicVocabModalBtn"),
    topicVocabModalTitle: document.getElementById("topicVocabModalTitle"),
    topicVocabModalSubtitle: document.getElementById("topicVocabModalSubtitle"),
    topicVocabFilterInput: document.getElementById("topicVocabFilterInput"),
    topicVocabCountBadge: document.getElementById("topicVocabCountBadge"),
    saveAllTopicVocabBtn: document.getElementById("saveAllTopicVocabBtn"),
    generateAiVocabBtn: document.getElementById("generateAiVocabBtn"),
    openAiKeySettingsBtn: document.getElementById("openAiKeySettingsBtn"),
    topicVocabCardsGrid: document.getElementById("topicVocabCardsGrid"),

    // Gemini AI Key Modal
    geminiKeyModal: document.getElementById("geminiKeyModal"),
    closeGeminiKeyModalBtn: document.getElementById("closeGeminiKeyModalBtn"),
    cancelGeminiKeyBtn: document.getElementById("cancelGeminiKeyBtn"),
    saveGeminiKeyBtn: document.getElementById("saveGeminiKeyBtn"),
    geminiApiKeyInput: document.getElementById("geminiApiKeyInput"),
    geminiKeyStatusText: document.getElementById("geminiKeyStatusText"),

    // Topic Tabs & Selects
    topicTabsContainer: document.getElementById("topicTabsContainer"),
    activeTopicBadge: document.getElementById("activeTopicBadge"),
    videoUrlTopicSelect: document.getElementById("videoUrlTopicSelect"),
    videoTopicSelect: document.getElementById("videoTopicSelect"),

    // Watch Online Video Modal
    watchVideoModal: document.getElementById("watchVideoModal"),
    closeWatchModalBtn: document.getElementById("closeWatchModalBtn"),
    watchModalTitle: document.getElementById("watchModalTitle"),
    watchIframe: document.getElementById("watchIframe"),
    watchModalImportBtn: document.getElementById("watchModalImportBtn"),
    watchModalDescBtn: document.getElementById("watchModalDescBtn"),
    watchModalSearchInput: document.getElementById("watchModalSearchInput"),
    watchModalSearchBtn: document.getElementById("watchModalSearchBtn"),
    watchModalSearchResults: document.getElementById("watchModalSearchResults"),
    watchSearchCountBadge: document.getElementById("watchSearchCountBadge"),
    watchModalInstantImportBtn: document.getElementById("watchModalInstantImportBtn"),

    // Video Player & Controls
    videoSelect: document.getElementById("videoSelect"),
    deleteCurrentVideoBtn: document.getElementById("deleteCurrentVideoBtn"),
    mainVideo: document.getElementById("mainVideo"),
    mainYoutubePlayer: document.getElementById("mainYoutubePlayer"),
    videoPlaceholder: document.getElementById("videoPlaceholder"),
    videoTitleDisplay: document.getElementById("videoTitleDisplay"),
    currentTimeDisplay: document.getElementById("currentTimeDisplay"),
    totalDurationDisplay: document.getElementById("totalDurationDisplay"),

    // Search
    vocabSearchInput: document.getElementById("vocabSearchInput"),
    clearSearchBtn: document.getElementById("clearSearchBtn"),
    searchResultCount: document.getElementById("searchResultCount"),
    searchResultsList: document.getElementById("searchResultsList"),

    // Flashcard Deck
    emptyFlashcardState: document.getElementById("emptyFlashcardState"),
    flashcardDeckContainer: document.getElementById("flashcardDeckContainer"),
    flashcardInner: document.getElementById("flashcardInner"),
    cardWord: document.getElementById("cardWord"),
    cardBackWord: document.getElementById("cardBackWord"),
    cardSentence: document.getElementById("cardSentence"),
    cardMeaning: document.getElementById("cardMeaning"),
    cardStatusBadge: document.getElementById("cardStatusBadge"),
    cardProgressText: document.getElementById("cardProgressText"),
    cardTimestampTag: document.getElementById("cardTimestampTag"),
    pronounceWordBtn: document.getElementById("pronounceWordBtn"),
    cardPlayVideoBtn: document.getElementById("cardPlayVideoBtn"),
    cardBackPlayVideoBtn: document.getElementById("cardBackPlayVideoBtn"),
    flipCardBtn: document.getElementById("flipCardBtn"),
    prevCardBtn: document.getElementById("prevCardBtn"),
    nextCardBtn: document.getElementById("nextCardBtn"),
    shuffleCardsBtn: document.getElementById("shuffleCardsBtn"),
    toggleMasteredBtn: document.getElementById("toggleMasteredBtn"),
    masteredBtnText: document.getElementById("masteredBtnText"),
    deleteCardBtn: document.getElementById("deleteCardBtn"),
    goBackToVideoBtn: document.getElementById("goBackToVideoBtn"),

    // Modals
    openUploadModalBtn: document.getElementById("openUploadModalBtn"),
    placeholderUploadBtn: document.getElementById("placeholderUploadBtn"),
    uploadModal: document.getElementById("uploadModal"),
    closeUploadModalBtn: document.getElementById("closeUploadModalBtn"),
    modalTabUrlBtn: document.getElementById("modalTabUrlBtn"),
    modalTabFileBtn: document.getElementById("modalTabFileBtn"),
    urlVideoForm: document.getElementById("urlVideoForm"),
    videoUrlInput: document.getElementById("videoUrlInput"),
    videoUrlTitleInput: document.getElementById("videoUrlTitleInput"),
    whisperUrlModelSelect: document.getElementById("whisperUrlModelSelect"),
    whisperModelFieldWrapper: document.getElementById("whisperModelFieldWrapper"),
    submitUrlBtn: document.getElementById("submitUrlBtn"),
    submitUrlBtnText: document.getElementById("submitUrlBtnText"),
    uploadVideoForm: document.getElementById("uploadVideoForm"),
    videoFileInput: document.getElementById("videoFileInput"),
    videoTitleInput: document.getElementById("videoTitleInput"),
    whisperModelSelect: document.getElementById("whisperModelSelect"),
    uploadProgressBox: document.getElementById("uploadProgressBox"),
    progressStatusText: document.getElementById("progressStatusText"),
    submitUploadBtn: document.getElementById("submitUploadBtn"),

    // Add Flashcard Modal
    flashcardModal: document.getElementById("flashcardModal"),
    closeFlashcardModalBtn: document.getElementById("closeFlashcardModalBtn"),
    cancelFcBtn: document.getElementById("cancelFcBtn"),
    saveFlashcardForm: document.getElementById("saveFlashcardForm"),
    fcWordInput: document.getElementById("fcWordInput"),
    fcMeaningInput: document.getElementById("fcMeaningInput"),
    meaningLoadingIndicator: document.getElementById("meaningLoadingIndicator"),
    meaningSuggestionsBox: document.getElementById("meaningSuggestionsBox"),
    meaningChipsContainer: document.getElementById("meaningChipsContainer"),
    fcSentenceInput: document.getElementById("fcSentenceInput"),
    fcSentenceTranslation: document.getElementById("fcSentenceTranslation"),
    fcSentenceTransText: document.getElementById("fcSentenceTransText"),
    fcVideoId: document.getElementById("fcVideoId"),
    fcStartTime: document.getElementById("fcStartTime"),
    fcEndTime: document.getElementById("fcEndTime"),
    fcTimestampBadge: document.getElementById("fcTimestampBadge"),
    fcVideoIdText: document.getElementById("fcVideoIdText"),

    // Replay Modal
    videoReplayModal: document.getElementById("videoReplayModal"),
    closeReplayModalBtn: document.getElementById("closeReplayModalBtn"),
    replayVideo: document.getElementById("replayVideo"),
    replaySentenceContext: document.getElementById("replaySentenceContext"),
    replayModalTitle: document.getElementById("replayModalTitle"),
    jumpToMainPlayerBtn: document.getElementById("jumpToMainPlayerBtn"),

    // Description Vocabulary Feature
    openDescVocabModalBtn: document.getElementById("openDescVocabModalBtn"),
    quickDescVocabBtn: document.getElementById("quickDescVocabBtn"),
    descVocabModal: document.getElementById("descVocabModal"),
    closeDescVocabModalBtn: document.getElementById("closeDescVocabModalBtn"),
    descVocabTextarea: document.getElementById("descVocabTextarea"),
    descInputContainer: document.getElementById("descInputContainer"),
    toggleDescExpandBtn: document.getElementById("toggleDescExpandBtn"),
    toggleDescExpandText: document.getElementById("toggleDescExpandText"),
    toggleDescExpandIcon: document.getElementById("toggleDescExpandIcon"),
    descSourceUrlNotice: document.getElementById("descSourceUrlNotice"),
    fetchPinnedCommentBtn: document.getElementById("fetchPinnedCommentBtn"),
    fetchDescFromYoutubeBtn: document.getElementById("fetchDescFromYoutubeBtn"),
    runScanDescBtn: document.getElementById("runScanDescBtn"),
    descScanLoading: document.getElementById("descScanLoading"),
    descResultsContainer: document.getElementById("descResultsContainer"),
    descScanStats: document.getElementById("descScanStats"),
    descScanCountBadge: document.getElementById("descScanCountBadge"),
    descMatchedList: document.getElementById("descMatchedList"),
};


// ==================== MODERN TOAST & CONFIRM DIALOG SYSTEM ====================

/**
 * Hiển thị thông báo Toast hiện đại thay thế cho browser alert()
 * @param {string} message - Nội dung thông báo
 * @param {"success" | "error" | "warning" | "info"} type - Phân loại
 * @param {number} duration - Thời gian hiển thị (ms)
 */
function showToast(message, type = "info", duration = 3500) {
    const container = document.getElementById("toastContainer");
    if (!container) return;

    const toast = document.createElement("div");
    toast.className = "toast-item flex items-center p-3.5 rounded-xl border shadow-lg text-xs font-medium space-x-3 transition-all";

    let bgBorderClass = "bg-white border-slate-200 text-slate-800 shadow-slate-200/50";
    let iconHtml = '<div class="w-6 h-6 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center flex-shrink-0"><i class="fa-solid fa-circle-info text-xs"></i></div>';

    if (type === "success") {
        bgBorderClass = "bg-white border-emerald-200 text-slate-800 shadow-emerald-500/10";
        iconHtml = '<div class="w-6 h-6 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center flex-shrink-0"><i class="fa-solid fa-check text-xs"></i></div>';
    } else if (type === "error") {
        bgBorderClass = "bg-white border-rose-200 text-slate-800 shadow-rose-500/10";
        iconHtml = '<div class="w-6 h-6 rounded-full bg-rose-100 text-rose-600 flex items-center justify-center flex-shrink-0"><i class="fa-solid fa-xmark text-xs"></i></div>';
    } else if (type === "warning") {
        bgBorderClass = "bg-white border-amber-200 text-slate-800 shadow-amber-500/10";
        iconHtml = '<div class="w-6 h-6 rounded-full bg-amber-100 text-amber-600 flex items-center justify-center flex-shrink-0"><i class="fa-solid fa-triangle-exclamation text-xs"></i></div>';
    }

    toast.className += " " + bgBorderClass;
    toast.innerHTML = `
        ${iconHtml}
        <div class="flex-1 leading-snug break-words">${message}</div>
        <button type="button" class="text-slate-400 hover:text-slate-600 p-1 rounded-md transition ml-1 flex-shrink-0">
            <i class="fa-solid fa-xmark text-xs"></i>
        </button>
    `;

    const closeBtn = toast.querySelector("button");
    const removeToast = () => {
        if (toast.classList.contains("toast-closing")) return;
        toast.classList.add("toast-closing");
        setTimeout(() => toast.remove(), 220);
    };

    closeBtn.onclick = removeToast;
    const timer = setTimeout(removeToast, duration);

    toast.onmouseenter = () => clearTimeout(timer);
    toast.onmouseleave = () => setTimeout(removeToast, 1500);

    container.appendChild(toast);
}

/**
 * Hiển thị hộp thoại xác nhận hiện đại thay thế cho confirm()
 * @param {Object} options
 * @param {string} options.title - Tiêu đề
 * @param {string} options.message - Nội dung
 * @param {string} [options.confirmText="Đồng ý"]
 * @param {string} [options.cancelText="Hủy bỏ"]
 * @param {"indigo" | "red"} [options.confirmColor="indigo"]
 * @param {string} [options.icon="fa-circle-question"]
 * @returns {Promise<boolean>}
 */
function showConfirm({
    title = "Xác nhận",
    message = "",
    confirmText = "Đồng ý",
    cancelText = "Hủy bỏ",
    confirmColor = "indigo",
    icon = "fa-circle-question"
} = {}) {
    return new Promise((resolve) => {
        const modal = document.getElementById("customConfirmModal");
        const titleEl = document.getElementById("confirmModalTitle");
        const msgEl = document.getElementById("confirmModalMessage");
        const iconWrapper = document.getElementById("confirmModalIconWrapper");
        const iconEl = document.getElementById("confirmModalIcon");
        const cancelBtn = document.getElementById("confirmCancelBtn");
        const okBtn = document.getElementById("confirmOkBtn");

        if (!modal || !okBtn || !cancelBtn) {
            resolve(window.confirm(`${title}\n\n${message}`));
            return;
        }

        titleEl.innerText = title;
        msgEl.innerText = message;
        cancelBtn.innerText = cancelText;
        okBtn.innerText = confirmText;

        if (confirmColor === "red") {
            okBtn.className = "px-4 py-2 bg-rose-600 hover:bg-rose-700 text-white text-xs font-bold rounded-xl shadow-md shadow-rose-600/30 transition";
            iconWrapper.className = "w-11 h-11 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center flex-shrink-0 text-xl shadow-inner";
        } else {
            okBtn.className = "px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold rounded-xl shadow-md shadow-indigo-600/30 transition";
            iconWrapper.className = "w-11 h-11 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center flex-shrink-0 text-xl shadow-inner";
        }

        iconEl.className = `fa-solid ${icon}`;

        const cleanup = (result) => {
            modal.classList.add("hidden");
            okBtn.onclick = null;
            cancelBtn.onclick = null;
            modal.onclick = null;
            window.removeEventListener("keydown", handleKey);
            resolve(result);
        };

        const handleKey = (e) => {
            if (e.key === "Escape") cleanup(false);
            if (e.key === "Enter") cleanup(true);
        };

        okBtn.onclick = () => cleanup(true);
        cancelBtn.onclick = () => cleanup(false);
        modal.onclick = (e) => {
            if (e.target === modal) cleanup(false);
        };
        window.addEventListener("keydown", handleKey);

        modal.classList.remove("hidden");
    });
}

// Ghi đè window.alert để triệt tiêu mọi alert() còn sót lại
window.alert = (msg) => showToast(String(msg), "info");


// ==================== HELPER FUNCTIONS ====================

/**
 * Định dạng số giây thành chuỗi mm:ss.s
 * @param {number} seconds 
 * @returns {string} ví dụ "02:14.5"
 */
function formatTime(seconds) {
    if (isNaN(seconds) || seconds < 0) return "00:00.0";
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    const ms = Math.floor((seconds % 1) * 10);
    return `${String(mins).padStart(2, "0")}:${String(secs).padStart(2, "0")}.${ms}`;
}

/**
 * Highlight từ khóa trong câu trích dẫn
 */
function highlightWordInText(sentence, wordToHighlight) {
    if (!wordToHighlight) return sentence;
    try {
        const regex = new RegExp(`(${wordToHighlight.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, "gi");
        return sentence.replace(regex, `<mark class="vocab-highlight">$1</mark>`);
    } catch (e) {
        return sentence;
    }
}


// ==================== API SERVICE ====================
// Cấu hình URL Backend:
// - Khi chạy Local hoặc Deploy trọn gói trên Railway: để trống ""
// - Khi Deploy Frontend trên Vercel: điền URL Railway của bạn (ví dụ: "https://my-app.up.railway.app")
const API_BASE_URL = window.API_BASE_URL || localStorage.getItem("API_BASE_URL") || "";

const API = {
    async fetchTopics() {
        try {
            const res = await fetch(`${API_BASE_URL}/api/topics`);
            if (!res.ok) return [];
            return await res.json();
        } catch (e) {
            console.warn("Lỗi tải chủ đề:", e);
            return [];
        }
    },

    async fetchTopicVideos(topicId) {
        try {
            const res = await fetch(`${API_BASE_URL}/api/topics/${topicId}/videos`);
            if (!res.ok) return { videos: [] };
            return await res.json();
        } catch (e) {
            console.warn("Lỗi tải video chủ đề:", e);
            return { videos: [] };
        }
    },

    async fetchVideos(topic = null) {
        let url = `${API_BASE_URL}/api/videos`;
        if (topic && topic !== "all") {
            url += `?topic=${encodeURIComponent(topic)}`;
        }
        const res = await fetch(url);
        if (!res.ok) throw new Error("Không thể tải danh sách video");
        return await res.json();
    },

    async deleteVideo(videoId) {
        const res = await fetch(`${API_BASE_URL}/api/videos/${videoId}`, {
            method: "DELETE"
        });
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw new Error(err.detail || "Không thể xóa video");
        }
        return await res.json();
    },

    async uploadVideo(formData) {
        const res = await fetch(`${API_BASE_URL}/api/videos/upload`, {
            method: "POST",
            body: formData
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || "Lỗi khi upload video");
        }
        return await res.json();
    },

    async processVideoFromUrl(data) {
        const res = await fetch(`${API_BASE_URL}/api/videos/from-url`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || "Lỗi khi tải video từ đường link");
        }
        return await res.json();
    },

    async searchWords(query, videoId = null) {
        let url = `${API_BASE_URL}/api/search?q=${encodeURIComponent(query)}`;
        if (videoId) url += `&video_id=${videoId}`;
        const res = await fetch(url);
        if (!res.ok) throw new Error("Lỗi khi tìm kiếm từ vựng");
        return await res.json();
    },

    async lookupWord(word, context = "") {
        try {
            const url = `${API_BASE_URL}/api/dictionary/lookup?word=${encodeURIComponent(word)}&context=${encodeURIComponent(context)}`;
            const res = await fetch(url);
            if (!res.ok) return null;
            return await res.json();
        } catch (e) {
            console.warn("Lỗi tra từ:", e);
            return null;
        }
    },

    async fetchFlashcards() {
        const res = await fetch(`${API_BASE_URL}/api/flashcards`);
        if (!res.ok) throw new Error("Không thể tải danh sách Flashcards");
        return await res.json();
    },

    async createFlashcard(data) {
        const res = await fetch(`${API_BASE_URL}/api/flashcards`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        if (!res.ok) throw new Error("Không thể tạo Flashcard");
        return await res.json();
    },

    async updateFlashcard(cardId, data) {
        const res = await fetch(`${API_BASE_URL}/api/flashcards/${cardId}`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        if (!res.ok) throw new Error("Không thể cập nhật Flashcard");
        return await res.json();
    },

    async deleteFlashcard(cardId) {
        const res = await fetch(`${API_BASE_URL}/api/flashcards/${cardId}`, {
            method: "DELETE"
        });
        if (!res.ok) throw new Error("Không thể xóa Flashcard");
        return await res.json();
    },

    async fetchVideoDescription(videoId) {
        try {
            const res = await fetch(`${API_BASE_URL}/api/videos/${videoId}/description`);
            if (!res.ok) return null;
            return await res.json();
        } catch (e) {
            console.warn("Lỗi tải description video:", e);
            return null;
        }
    },

    async scanDescriptionVocab(videoId, data = {}) {
        const res = await fetch(`${API_BASE_URL}/api/videos/${videoId}/description/scan`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw new Error(err.detail || "Không thể quét từ vựng description");
        }
        return await res.json();
    },

    async scanOnlineYoutubeVocab(data = {}) {
        const res = await fetch(`${API_BASE_URL}/api/youtube/scan-description`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw new Error(err.detail || "Không thể quét từ vựng video YouTube này");
        }
        return await res.json();
    },

    async searchYoutubeVideos(query, pageOrMaxResults = 1, maxResults = 12) {
        let page = 1;
        let limit = 12;
        if (typeof pageOrMaxResults === "object") {
            page = pageOrMaxResults.page || 1;
            limit = pageOrMaxResults.maxResults || 12;
        } else if (pageOrMaxResults > 10 && maxResults === 12) {
            limit = pageOrMaxResults;
            page = 1;
        } else {
            page = pageOrMaxResults;
            limit = maxResults;
        }
        const res = await fetch(`${API_BASE_URL}/api/youtube/search-videos?q=${encodeURIComponent(query)}&page=${page}&max_results=${limit}`);
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw new Error(err.detail || "Lỗi khi tìm kiếm video trên YouTube");
        }
        return await res.json();
    },

    async fetchTopicVocabularies(topicId) {
        const res = await fetch(`${API_BASE_URL}/api/topics/${topicId}/vocabularies`);
        if (!res.ok) throw new Error("Không thể tải danh sách từ vựng chủ đề");
        return await res.json();
    },

    async saveTopicVocabToFlashcard(data) {
        const res = await fetch(`${API_BASE_URL}/api/topics/vocabularies/save-flashcard`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        if (!res.ok) throw new Error("Không thể lưu từ vựng vào Flashcard");
        return await res.json();
    },

    async getAiConfig() {
        const res = await fetch(`${API_BASE_URL}/api/ai/config`);
        if (!res.ok) throw new Error("Không thể kiểm tra cấu hình AI");
        return await res.json();
    },

    async setAiConfig(apiKey) {
        const res = await fetch(`${API_BASE_URL}/api/ai/config`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ api_key: apiKey })
        });
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw new Error(err.detail || "Không thể lưu API Key");
        }
        return await res.json();
    },

    async generateAiTopicVocab(topicId) {
        const res = await fetch(`${API_BASE_URL}/api/topics/${topicId}/generate-ai-vocab`, {
            method: "POST",
            headers: { "Content-Type": "application/json" }
        });
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw new Error(err.detail || "Không thể sinh từ vựng bằng AI");
        }
        return await res.json();
    },

    async searchWordsInYoutube(youtubeId, query) {
        const res = await fetch(`${API_BASE_URL}/api/youtube/search-words`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ youtube_id: youtubeId, query: query })
        });
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw new Error(err.detail || "Không thể tìm từ vựng trong video này");
        }
        return await res.json();
    },

    async importOnlineYoutubeVideo(data) {
        const res = await fetch(`${API_BASE_URL}/api/youtube/import-online`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw new Error(err.detail || "Không thể nạp video YouTube online");
        }
        return await res.json();
    },

    async fetchPinnedComment(youtubeId) {
        const res = await fetch(`${API_BASE_URL}/api/youtube/${encodeURIComponent(youtubeId)}/pinned-comment`);
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw new Error(err.detail || "Không thể lấy bình luận ghim");
        }
        return await res.json();
    }
};


// ==================== TAB SWITCHING LOGIC ====================
function switchTab(tabName) {
    if (tabName === "video") {
        DOM.tabVideoBtn.className = "flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-200 bg-white text-indigo-600 shadow-sm";
        DOM.tabFlashcardBtn.className = "flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-200 text-slate-600 hover:text-slate-900";
        DOM.tabVideoSection.classList.remove("hidden");
        DOM.tabFlashcardSection.classList.add("hidden");
    } else {
        DOM.tabFlashcardBtn.className = "flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-200 bg-white text-indigo-600 shadow-sm";
        DOM.tabVideoBtn.className = "flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-200 text-slate-600 hover:text-slate-900";
        DOM.tabVideoSection.classList.add("hidden");
        DOM.tabFlashcardSection.classList.remove("hidden");
        loadFlashcardDeck();
    }
}


// ==================== TOPIC TABS & DISCOVERY LOGIC ====================

/**
 * Tải danh sách 16 chủ đề và khởi tạo thanh tabs & dropdowns
 */
async function loadTopics() {
    try {
        state.topics = await API.fetchTopics();
        populateTopicSelects();
        renderTopicTabs();
    } catch (e) {
        console.error("Lỗi khởi tạo chủ đề:", e);
    }
}

/**
 * Điền 16 chủ đề có đánh số vào các ô chọn trong modal upload
 */
function populateTopicSelects() {
    const selects = [DOM.videoUrlTopicSelect, DOM.videoTopicSelect];
    selects.forEach(select => {
        if (!select) return;
        select.innerHTML = "";
        state.topics.forEach(t => {
            const opt = document.createElement("option");
            opt.value = t.title;
            opt.textContent = t.title;
            select.appendChild(opt);
        });
    });
}

/**
 * Hiển thị thanh tabs: "📁 Video của tôi" + 16 chủ đề IELTS có đánh số
 */
function renderTopicTabs() {
    if (!DOM.topicTabsContainer) return;
    DOM.topicTabsContainer.innerHTML = "";

    // 1. Tab "📁 Video của tôi" (Nơi tra cứu từ vựng và xem video đã tải lên)
    const myTab = document.createElement("button");
    const isMyActive = state.activeTab === "my_videos";
    myTab.className = `whitespace-nowrap px-4 py-2 rounded-xl text-xs font-bold transition flex items-center space-x-1.5 ${
        isMyActive 
            ? "bg-indigo-600 text-white shadow-md shadow-indigo-100 ring-2 ring-indigo-400" 
            : "bg-slate-100 hover:bg-slate-200 text-slate-700"
    }`;
    myTab.innerHTML = `
        <i class="fa-solid fa-folder-open text-xs ${isMyActive ? 'text-white' : 'text-indigo-600'}"></i>
        <span>Video của tôi</span>
        <span class="ml-1 px-1.5 py-0.5 rounded-full text-[10px] ${isMyActive ? 'bg-indigo-800 text-white' : 'bg-slate-200 text-slate-700'}">${state.videos.length}</span>
    `;
    myTab.onclick = () => showMyVideosTab();
    DOM.topicTabsContainer.appendChild(myTab);

    // 2. 16 Tabs chủ đề có đánh số để người dùng tự do xem và khám phá video
    state.topics.forEach(t => {
        const tabBtn = document.createElement("button");
        const isActive = state.activeTab && state.activeTab.id === t.id;
        tabBtn.className = `whitespace-nowrap px-3.5 py-2 rounded-xl text-xs font-bold transition flex items-center space-x-1.5 ${
            isActive 
                ? "bg-indigo-600 text-white shadow-md shadow-indigo-100 ring-2 ring-indigo-400" 
                : "bg-slate-100 hover:bg-slate-200 text-slate-700"
        }`;
        // Hiển thị tiêu đề ngắn gọn có đánh số (ví dụ: "1. Work & Study")
        tabBtn.innerHTML = `<span>${t.id}. ${t.short_title}</span>`;
        tabBtn.title = t.title;
        tabBtn.onclick = () => showTopicDiscoveryTab(t);
        DOM.topicTabsContainer.appendChild(tabBtn);
    });
}

/**
 * Chuyển sang Tab "Video của tôi" (Tra cứu từ vựng & Player nội bộ)
 */
function showMyVideosTab() {
    state.activeTab = "my_videos";
    if (state.topicPagination) state.topicPagination.active = false;
    DOM.myVideosView.classList.remove("hidden");
    DOM.topicDiscoveryView.classList.add("hidden");
    if (DOM.topicInfiniteScrollArea) DOM.topicInfiniteScrollArea.classList.add("hidden");
    if (DOM.activeTopicBadge) {
        DOM.activeTopicBadge.innerText = `📁 Video của tôi (${state.videos.length} video)`;
    }
    renderTopicTabs();
}

// Bí danh để tương thích và an toàn tuyệt đối
const selectMyVideosTab = showMyVideosTab;

/**
 * Chuyển sang Tab Khám phá Video theo 1 trong 16 chủ đề IELTS
 */
async function showTopicDiscoveryTab(topic) {
    state.activeTab = topic;
    DOM.myVideosView.classList.add("hidden");
    DOM.topicDiscoveryView.classList.remove("hidden");

    if (DOM.topicDiscoveryTitle) {
        DOM.topicDiscoveryTitle.innerText = topic.title;
    }
    if (DOM.activeTopicBadge) {
        DOM.activeTopicBadge.innerText = `Chủ đề: ${topic.id}. ${topic.short_title}`;
    }
    renderTopicTabs();

    // Điền sẵn chủ đề này vào các ô chọn khi tải video
    if (DOM.videoUrlTopicSelect) DOM.videoUrlTopicSelect.value = topic.title;
    if (DOM.videoTopicSelect) DOM.videoTopicSelect.value = topic.title;

    await loadAndRenderTopicVideos(topic);
}

/**
 * Tải và hiển thị danh sách video thực tế trên YouTube theo chủ đề (hỗ trợ phân trang cuộn tiếp)
 */
async function loadAndRenderTopicVideos(topic) {
    if (!DOM.topicVideosGrid) return;
    DOM.topicVideosLoading.classList.remove("hidden");
    DOM.topicVideosGrid.innerHTML = "";
    if (DOM.topicInfiniteScrollArea) DOM.topicInfiniteScrollArea.classList.add("hidden");

    const topicQuery = topic.short_title || topic.title || "IELTS Speaking";

    // Khởi tạo trạng thái phân trang vô tận
    state.topicPagination = {
        active: true,
        query: topicQuery,
        topicTitle: topic.title,
        page: 1,
        pageSize: 12,
        hasMore: true,
        isLoading: false,
        seenIds: new Set()
    };

    try {
        // 1. Tải trước các video bài mẫu (hiển thị tức thì)
        const data = await API.fetchTopicVideos(topic.id);
        const curated = data.videos || [];
        if (curated.length > 0) {
            renderVideoCards(curated, topic.title, false);
        }

        // 2. Tự động tải đợt 1 từ YouTube theo chủ đề
        try {
            const res = await API.searchYoutubeVideos(topicQuery, 1, state.topicPagination.pageSize);
            const ytVideos = Array.isArray(res) ? res : (res.videos || []);
            const hasMore = Array.isArray(res) ? (ytVideos.length >= state.topicPagination.pageSize) : Boolean(res.has_more);
            state.topicPagination.hasMore = hasMore;

            if (ytVideos.length > 0) {
                renderVideoCards(ytVideos, topic.title, true);
            }
        } catch (eYt) {
            console.warn("Không thể tải thêm video YouTube tự động:", eYt);
        }

        DOM.topicVideosLoading.classList.add("hidden");

        if (state.topicPagination.seenIds.size === 0) {
            DOM.topicVideosGrid.innerHTML = `
                <div class="col-span-full py-12 text-center text-slate-400 bg-white rounded-2xl border border-slate-200 p-8 space-y-3">
                    <i class="fa-solid fa-video-slash text-4xl text-slate-300"></i>
                    <p class="text-sm font-semibold text-slate-700">Chưa tìm thấy video cho chủ đề này</p>
                    <p class="text-xs text-slate-400">Bạn có thể dán đường link video YouTube bất kỳ để thêm vào chủ đề này.</p>
                </div>
            `;
        } else {
            updateInfiniteScrollUI();
        }
    } catch (err) {
        console.error("Lỗi nạp video chủ đề:", err);
        DOM.topicVideosLoading.classList.add("hidden");
    }
}

/**
 * Hiển thị các thẻ video vào lưới Topic Grid với xử lý chống ảnh xám và các nút tác vụ
 * @param {Array} videos Danh sách video
 * @param {string} topicTitle Tiêu đề chủ đề hoặc truy vấn
 * @param {boolean} append Nối thêm vào cuối (dùng cho phân trang cuộn tiếp)
 */
function renderVideoCards(videos, topicTitle, append = false) {
    if (!DOM.topicVideosGrid) return;
    if (!append) {
        DOM.topicVideosGrid.innerHTML = "";
    }

    const fallbackImg = "https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=640&q=80";

    videos.forEach(v => {
        if (!v || !v.id) return;

        // Tránh trùng lặp video đã có trong danh sách
        if (state.topicPagination && state.topicPagination.seenIds) {
            if (state.topicPagination.seenIds.has(v.id)) return;
            state.topicPagination.seenIds.add(v.id);
        }

        const card = document.createElement("div");
        card.className = "bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm hover:shadow-md transition flex flex-col justify-between group";

        const mins = Math.floor(v.duration / 60);
        const secs = Math.floor(v.duration % 60);
        const durationStr = `${String(mins).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
        const thumbUrl = v.thumbnail || `https://i.ytimg.com/vi/${v.id}/hqdefault.jpg`;

        card.innerHTML = `
            <div>
                <div class="relative aspect-video bg-slate-900 overflow-hidden cursor-pointer watch-now-trigger">
                    <img 
                        src="${thumbUrl}" 
                        alt="${v.title}" 
                        loading="lazy" 
                        class="w-full h-full object-cover group-hover:scale-105 transition duration-300"
                        onload="if (this.naturalWidth === 120 && this.naturalHeight === 90) { this.src = '${fallbackImg}'; }"
                        onerror="if(!this.dataset.triedHq){this.dataset.triedHq='1'; this.src='https://i.ytimg.com/vi/${v.id}/hqdefault.jpg';} else { this.onerror=null; this.src='${fallbackImg}'; }"
                    >
                    <span class="absolute bottom-2 right-2 bg-black/80 text-white font-mono text-[11px] font-bold px-2 py-0.5 rounded-md">
                        ${durationStr}
                    </span>
                    <div class="absolute inset-0 bg-slate-950/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center text-white">
                        <div class="w-12 h-12 rounded-full bg-indigo-600/90 flex items-center justify-center shadow-lg">
                            <i class="fa-solid fa-play text-lg ml-0.5"></i>
                        </div>
                    </div>
                </div>
                <div class="p-4 space-y-2">
                    <div class="text-[11px] font-semibold text-indigo-600 truncate">
                        <i class="fa-brands fa-youtube mr-1 text-red-500"></i> ${v.channel}
                    </div>
                    <h4 class="text-sm font-bold text-slate-800 line-clamp-2 leading-snug group-hover:text-indigo-600 transition" title="${v.title}">
                        ${v.title}
                    </h4>
                </div>
            </div>
            <div class="p-3 pt-0 border-t border-slate-100 grid grid-cols-4 gap-1 mt-2">
                <button class="watch-btn py-2 px-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-[11px] font-semibold transition flex flex-col items-center justify-center" title="Xem video & Tìm từ trong phụ đề">
                    <i class="fa-solid fa-play text-[11px] text-indigo-600 mb-0.5"></i>
                    <span>Xem & Tìm</span>
                </button>
                <button class="topic-desc-btn py-2 px-1 bg-amber-50 hover:bg-amber-500 hover:text-white text-amber-800 rounded-xl text-[11px] font-bold transition flex flex-col items-center justify-center" title="Lấy từ vựng ở Description">
                    <i class="fa-solid fa-list-check text-[11px] text-amber-600 mb-0.5"></i>
                    <span>Từ vựng</span>
                </button>
                <button class="instant-import-btn py-2 px-1 bg-emerald-50 hover:bg-emerald-600 hover:text-white text-emerald-700 rounded-xl text-[11px] font-bold transition flex flex-col items-center justify-center" title="Lưu bài học Online (2s - 0MB tải)">
                    <i class="fa-solid fa-bolt text-[11px] text-emerald-600 mb-0.5"></i>
                    <span>Lưu 2s</span>
                </button>
                <button class="import-btn py-2 px-1 bg-indigo-50 hover:bg-indigo-600 hover:text-white text-indigo-700 rounded-xl text-[11px] font-bold transition flex flex-col items-center justify-center" title="Tải & học sâu bằng Whisper">
                    <i class="fa-solid fa-cloud-arrow-down text-[11px] text-indigo-500 mb-0.5"></i>
                    <span>Whisper</span>
                </button>
            </div>
        `;

        // Bấm xem video & tìm từ vựng trong bài nói
        card.querySelector(".watch-btn").onclick = () => openWatchVideoModal(v);
        card.querySelector(".watch-now-trigger").onclick = () => openWatchVideoModal(v);

        // Bấm lấy từ vựng ở description
        card.querySelector(".topic-desc-btn").onclick = () => openDescriptionVocabForOnlineVideo(v);

        // Bấm nạp tức thì bài học online (2 giây)
        card.querySelector(".instant-import-btn").onclick = () => triggerInstantImportOnlineVideo(v, topicTitle);

        // Bấm nhập video để Whisper tải và trích xuất offline
        card.querySelector(".import-btn").onclick = () => triggerImportTopicVideo(v, topicTitle);

        DOM.topicVideosGrid.appendChild(card);
    });
}

// ==================== BỘ TỪ VỰNG CHỦ ĐỀ CHUẨN NGỮ CẢNH (BAND 7.5 - 9.0) ====================

/**
 * Phát âm thanh bằng Web Speech API (chuẩn giọng bản ngữ Anh/Mỹ)
 */
function speakText(text, lang = "en-US") {
    if (!("speechSynthesis" in window)) {
        showToast("Trình duyệt không hỗ trợ phát âm tự động", "warning");
        return;
    }
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = lang;
    utterance.rate = 0.88; // Tốc độ tự nhiên, rõ ràng cho người học
    window.speechSynthesis.speak(utterance);
}

/**
 * Tô sáng từ vựng mục tiêu trong câu ngữ cảnh
 */
function highlightWordInSentence(sentence, targetWord) {
    if (!sentence || !targetWord) return sentence || "";
    const cleanWord = targetWord.trim().replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp(`(\\b${cleanWord}\\w*\\b)`, 'gi');
    return sentence.replace(regex, '<mark class="bg-amber-200 text-amber-950 font-bold px-1.5 py-0.5 rounded shadow-sm">$1</mark>');
}

/**
 * Mở Modal danh sách từ vựng & câu ngữ cảnh Band 7.5 - 9.0 cho chủ đề
 */
async function openTopicVocabModal(topic) {
    if (!topic || typeof topic !== "object") {
        showToast("Vui lòng chọn một chủ đề IELTS để xem từ vựng", "info");
        return;
    }

    if (!DOM.topicVocabModal) return;

    if (DOM.topicVocabModalTitle) {
        DOM.topicVocabModalTitle.innerText = `Bộ từ vựng: ${topic.title}`;
    }
    if (DOM.topicVocabModalSubtitle) {
        DOM.topicVocabModalSubtitle.innerText = `Các từ vựng học thuật, idioms & collocations đắt giá kèm câu ngữ cảnh thực tế cho chủ đề "${topic.short_title}"`;
    }
    if (DOM.topicVocabFilterInput) {
        DOM.topicVocabFilterInput.value = "";
    }

    DOM.topicVocabModal.classList.remove("hidden");
    if (DOM.topicVocabCardsGrid) {
        DOM.topicVocabCardsGrid.innerHTML = `
            <div class="col-span-full py-16 text-center text-slate-500 space-y-3">
                <i class="fa-solid fa-spinner fa-spin text-3xl text-indigo-600"></i>
                <p class="text-sm font-semibold">Đang tải danh sách từ vựng chuẩn ngữ cảnh...</p>
            </div>
        `;
    }

    try {
        const data = await API.fetchTopicVocabularies(topic.id);
        state.currentTopicVocabs = data.vocabularies || [];
        renderTopicVocabCards(state.currentTopicVocabs);
    } catch (err) {
        console.error("Lỗi tải từ vựng chủ đề:", err);
        if (DOM.topicVocabCardsGrid) {
            DOM.topicVocabCardsGrid.innerHTML = `
                <div class="col-span-full py-12 text-center text-rose-500 bg-rose-50 rounded-2xl border border-rose-200 p-6 space-y-2">
                    <i class="fa-solid fa-circle-exclamation text-3xl"></i>
                    <p class="text-sm font-bold">Không thể tải từ vựng: ${err.message}</p>
                </div>
            `;
        }
    }
}

/**
 * Hiển thị lưới thẻ từ vựng chủ đề kèm câu ngữ cảnh
 */
function renderTopicVocabCards(vocabs) {
    if (!DOM.topicVocabCardsGrid) return;
    DOM.topicVocabCardsGrid.innerHTML = "";

    if (DOM.topicVocabCountBadge) {
        DOM.topicVocabCountBadge.innerText = `${vocabs.length} từ vựng Band 8.0+`;
    }

    if (!vocabs || vocabs.length === 0) {
        DOM.topicVocabCardsGrid.innerHTML = `
            <div class="col-span-full py-12 text-center text-slate-400 bg-white rounded-2xl border border-slate-200 p-8 space-y-2">
                <i class="fa-solid fa-book-open text-3xl text-slate-300"></i>
                <p class="text-sm font-bold text-slate-600">Không tìm thấy từ vựng phù hợp</p>
                <p class="text-xs text-slate-400">Hãy thử xóa bộ lọc tìm kiếm để xem lại toàn bộ từ vựng.</p>
            </div>
        `;
        return;
    }

    vocabs.forEach(item => {
        const card = document.createElement("div");
        card.className = "bg-white rounded-2xl border border-slate-200/90 p-5 shadow-sm hover:shadow-md transition flex flex-col justify-between space-y-3.5 group";

        // Màu badge cho loại từ
        let badgeColor = "bg-indigo-50 text-indigo-700 border-indigo-200";
        const pos = (item.part_of_speech || "").toLowerCase();
        if (pos.includes("idiom")) {
            badgeColor = "bg-amber-50 text-amber-800 border-amber-200";
        } else if (pos.includes("collocation")) {
            badgeColor = "bg-purple-50 text-purple-700 border-purple-200";
        } else if (pos.includes("adj")) {
            badgeColor = "bg-emerald-50 text-emerald-700 border-emerald-200";
        }

        const highlightedSentence = highlightWordInSentence(item.context_sentence, item.word);

        const collocationsHtml = (item.collocations || []).map(c => `
            <span class="inline-block bg-slate-100 text-slate-600 text-[10px] font-medium px-2 py-0.5 rounded-md mr-1 mt-1">
                ${c}
            </span>
        `).join("");

        card.innerHTML = `
            <div class="space-y-2.5">
                <!-- Header Word & Phonetics -->
                <div class="flex items-start justify-between gap-2">
                    <div>
                        <div class="flex items-center space-x-2">
                            <h4 class="text-base font-extrabold text-slate-900 group-hover:text-indigo-600 transition tracking-tight">
                                ${item.word}
                            </h4>
                            <button type="button" class="speak-word-btn w-6 h-6 rounded-full bg-slate-100 hover:bg-indigo-100 text-slate-500 hover:text-indigo-600 flex items-center justify-center transition text-[11px]" title="Nghe phát âm từ này">
                                <i class="fa-solid fa-volume-high"></i>
                            </button>
                        </div>
                        <div class="flex items-center space-x-2 mt-0.5 text-xs text-slate-500">
                            <span class="font-mono text-slate-400">${item.phonetic || ""}</span>
                            <span class="border px-1.5 py-0.2 rounded text-[10px] font-bold uppercase ${badgeColor}">
                                ${item.part_of_speech || "Word"}
                            </span>
                        </div>
                    </div>
                    <button type="button" class="save-fc-btn px-2.5 py-1 bg-indigo-50 hover:bg-indigo-600 hover:text-white text-indigo-700 rounded-xl text-[11px] font-bold transition flex items-center space-x-1 border border-indigo-200 shadow-sm" title="Lưu từ này vào bộ thẻ Flashcard">
                        <i class="fa-regular fa-star text-xs"></i>
                        <span>Lưu thẻ</span>
                    </button>
                </div>

                <!-- Meaning -->
                <div class="text-xs font-semibold text-slate-800 leading-snug">
                    <span class="text-indigo-600 font-bold mr-1">✦</span> ${item.meaning}
                </div>

                <!-- Context Sentence Box -->
                <div class="bg-amber-50/60 rounded-xl p-3 border border-amber-200/70 space-y-1.5">
                    <div class="flex items-center justify-between text-[11px] font-bold text-amber-900">
                        <span class="flex items-center space-x-1">
                            <i class="fa-solid fa-quote-left text-amber-500 text-[10px]"></i>
                            <span>Ngữ cảnh IELTS Speaking thực tế:</span>
                        </span>
                        <button type="button" class="speak-sentence-btn text-amber-700 hover:text-amber-900 p-0.5 rounded transition" title="Nghe đọc toàn bộ câu ngữ cảnh">
                            <i class="fa-solid fa-volume-high text-xs"></i>
                        </button>
                    </div>
                    <p class="text-xs text-slate-800 leading-relaxed italic">
                        "${highlightedSentence}"
                    </p>
                    ${item.speaking_question ? `
                        <div class="text-[10px] text-amber-800/80 font-medium pt-1 border-t border-amber-200/60 flex items-center space-x-1">
                            <i class="fa-regular fa-lightbulb text-amber-600"></i>
                            <span><b>Gợi ý câu hỏi:</b> "${item.speaking_question}"</span>
                        </div>
                    ` : ""}
                </div>

                <!-- Collocations -->
                ${collocationsHtml ? `
                    <div class="pt-0.5">
                        <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Cụm từ hay gặp:</span>
                        <div class="flex flex-wrap">${collocationsHtml}</div>
                    </div>
                ` : ""}
            </div>

            <!-- Card Bottom Actions -->
            <div class="pt-2 border-t border-slate-100 flex items-center justify-between gap-2">
                <button type="button" class="find-in-video-btn text-xs font-semibold text-indigo-600 hover:text-indigo-800 hover:underline flex items-center space-x-1" title="Dò từ này trong bài nói của các video chủ đề">
                    <i class="fa-solid fa-magnifying-glass text-[11px]"></i>
                    <span>Dò trong video bài mẫu</span>
                </button>
                <button type="button" class="copy-sentence-btn text-xs text-slate-400 hover:text-slate-700 flex items-center space-x-1 transition" title="Sao chép câu ngữ cảnh">
                    <i class="fa-regular fa-copy text-xs"></i>
                    <span>Copy câu</span>
                </button>
            </div>
        `;

        // Sự kiện phát âm từ
        card.querySelector(".speak-word-btn").onclick = () => speakText(item.word);

        // Sự kiện phát âm toàn bộ câu ngữ cảnh
        card.querySelector(".speak-sentence-btn").onclick = () => speakText(item.context_sentence);

        // Sự kiện lưu vào Flashcard
        const saveBtn = card.querySelector(".save-fc-btn");
        saveBtn.onclick = () => saveTopicVocabItem(item, saveBtn);

        // Sự kiện copy câu ngữ cảnh
        card.querySelector(".copy-sentence-btn").onclick = async () => {
            try {
                await navigator.clipboard.writeText(item.context_sentence);
                showToast(`Đã sao chép câu ngữ cảnh của "${item.word}"!`, "success", 2000);
            } catch (e) {
                showToast("Không thể sao chép văn bản", "warning");
            }
        };

        // Sự kiện dò từ vựng trong video
        card.querySelector(".find-in-video-btn").onclick = () => {
            if (DOM.topicVocabModal) DOM.topicVocabModal.classList.add("hidden");
            showToast(`Đang tìm bài nói có chứa "${item.word}"...`, "info", 2500);
            const firstCardTrigger = document.querySelector(".watch-now-trigger");
            if (firstCardTrigger) {
                firstCardTrigger.click();
                setTimeout(() => {
                    if (DOM.watchModalSearchInput) {
                        DOM.watchModalSearchInput.value = item.word;
                        if (DOM.watchModalSearchBtn) DOM.watchModalSearchBtn.click();
                    }
                }, 400);
            } else {
                searchYoutubeVideosOnline(item.word);
            }
        };

        DOM.topicVocabCardsGrid.appendChild(card);
    });
}

/**
 * Lưu một từ vựng chủ đề vào bộ Flashcard
 */
async function saveTopicVocabItem(item, buttonEl) {
    try {
        const payload = {
            word: item.word,
            meaning: item.meaning,
            context_sentence: item.context_sentence,
            topic_id: state.activeTab && typeof state.activeTab === "object" ? state.activeTab.id : 1
        };

        const res = await API.saveTopicVocabToFlashcard(payload);

        if (buttonEl) {
            buttonEl.className = "px-2.5 py-1 bg-emerald-500 text-white rounded-xl text-[11px] font-bold transition flex items-center space-x-1 shadow-sm";
            buttonEl.innerHTML = `<i class="fa-solid fa-check text-xs"></i><span>Đã lưu</span>`;
        }

        // Cập nhật lại danh sách Flashcard ngầm
        try {
            state.flashcards = await API.fetchFlashcards();
            updateFlashcardBadgeCount();
        } catch (eFc) {
            console.warn("Lỗi tải lại flashcard:", eFc);
        }

        showToast(res.message || `Đã lưu từ "${item.word}" vào Flashcard!`, "success", 3000);
    } catch (err) {
        console.error("Lỗi lưu Flashcard từ vựng chủ đề:", err);
        showToast("Lỗi khi lưu Flashcard: " + err.message, "error");
    }
}

/**
 * Lưu toàn bộ từ vựng đang hiển thị vào Flashcard một chạm
 */
async function saveAllVisibleTopicVocabs() {
    if (!state.currentTopicVocabs || state.currentTopicVocabs.length === 0) {
        showToast("Không có từ vựng nào để lưu", "info");
        return;
    }

    let savedCount = 0;
    showToast(`Đang lưu ${state.currentTopicVocabs.length} từ vựng vào Flashcard...`, "info", 2000);

    for (const item of state.currentTopicVocabs) {
        try {
            const payload = {
                word: item.word,
                meaning: item.meaning,
                context_sentence: item.context_sentence,
                topic_id: state.activeTab && typeof state.activeTab === "object" ? state.activeTab.id : 1
            };
            await API.saveTopicVocabToFlashcard(payload);
            savedCount++;
        } catch (e) {
            console.warn("Lỗi lưu từ:", item.word, e);
        }
    }

    try {
        state.flashcards = await API.fetchFlashcards();
        updateFlashcardBadgeCount();
    } catch (eFc) {}

    // Đổi toàn bộ nút sang trạng thái Đã lưu
    document.querySelectorAll(".save-fc-btn").forEach(btn => {
        btn.className = "px-2.5 py-1 bg-emerald-500 text-white rounded-xl text-[11px] font-bold transition flex items-center space-x-1 shadow-sm";
        btn.innerHTML = `<i class="fa-solid fa-check text-xs"></i><span>Đã lưu</span>`;
    });

    showToast(`Đã lưu thành công ${savedCount} từ vựng kèm ngữ cảnh vào Flashcard!`, "success", 4000);
}

/**
 * Mở modal cấu hình Gemini API Key
 */
async function openGeminiKeyModal() {
    if (!DOM.geminiKeyModal) return;
    DOM.geminiKeyModal.classList.remove("hidden");
    if (DOM.geminiKeyStatusText) DOM.geminiKeyStatusText.innerText = "Đang kiểm tra key...";
    try {
        const cfg = await API.getAiConfig();
        if (cfg.has_key) {
            if (DOM.geminiKeyStatusText) {
                DOM.geminiKeyStatusText.innerHTML = `<span class="text-emerald-600 font-bold"><i class="fa-solid fa-check-circle mr-1"></i>Đã cấu hình (${cfg.masked_key})</span>`;
            }
        } else {
            if (DOM.geminiKeyStatusText) {
                DOM.geminiKeyStatusText.innerHTML = `<span class="text-amber-600 font-bold"><i class="fa-solid fa-circle-exclamation mr-1"></i>Chưa lưu API Key</span>`;
            }
        }
    } catch (e) {
        if (DOM.geminiKeyStatusText) DOM.geminiKeyStatusText.innerText = "Không thể kiểm tra trạng thái";
    }
}

/**
 * Đóng modal cấu hình Gemini API Key
 */
function closeGeminiKeyModal() {
    if (DOM.geminiKeyModal) DOM.geminiKeyModal.classList.add("hidden");
}

/**
 * Lưu Gemini API Key từ modal
 */
async function saveGeminiApiKeyFromModal() {
    const key = (DOM.geminiApiKeyInput?.value || "").trim();
    if (!key || key.length < 10) {
        showToast("Vui lòng nhập API Key hợp lệ (bắt đầu bằng AIza...)", "warning");
        return;
    }

    try {
        await API.setAiConfig(key);
        showToast("Đã lưu Google Gemini API Key thành công!", "success", 3000);
        closeGeminiKeyModal();
        if (DOM.geminiApiKeyInput) DOM.geminiApiKeyInput.value = "";
    } catch (err) {
        showToast("Lỗi khi lưu API Key: " + err.message, "error");
    }
}

/**
 * Kích hoạt AI tạo thêm từ vựng mới chuẩn Band 8.0+
 */
async function triggerGenerateAiVocab() {
    if (!state.activeTab || typeof state.activeTab !== "object") {
        showToast("Vui lòng chọn một chủ đề IELTS", "info");
        return;
    }

    // Kiểm tra xem đã có key chưa
    try {
        const cfg = await API.getAiConfig();
        if (!cfg.has_key) {
            showToast("Vui lòng nhập Gemini API Key miễn phí để AI sinh từ vựng", "warning", 4000);
            openGeminiKeyModal();
            return;
        }
    } catch (e) {}

    // Bật trạng thái loading trên nút
    const origBtnHtml = DOM.generateAiVocabBtn ? DOM.generateAiVocabBtn.innerHTML : "";
    if (DOM.generateAiVocabBtn) {
        DOM.generateAiVocabBtn.disabled = true;
        DOM.generateAiVocabBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin text-amber-300"></i><span>AI đang suy nghĩ...</span>`;
    }

    showToast(`AI đang phân tích chủ đề "${state.activeTab.short_title}" và tạo 8 từ vựng Band 8.0+...`, "info", 4500);

    try {
        const res = await API.generateAiTopicVocab(state.activeTab.id);
        state.currentTopicVocabs = res.vocabularies || [];
        renderTopicVocabCards(state.currentTopicVocabs);
        showToast(res.message || "Đã tạo thành công 8 từ vựng mới bằng AI!", "success", 4000);
    } catch (err) {
        console.error("Lỗi AI sinh từ vựng:", err);
        showToast("Lỗi AI sinh từ vựng: " + err.message, "error", 5000);
        if (err.message && err.message.toLowerCase().includes("key")) {
            openGeminiKeyModal();
        }
    } finally {
        if (DOM.generateAiVocabBtn) {
            DOM.generateAiVocabBtn.disabled = false;
            DOM.generateAiVocabBtn.innerHTML = origBtnHtml;
        }
    }
}

/**
 * Tìm kiếm video thực tế trên YouTube theo từ khóa tùy thích (hỗ trợ phân trang cuộn tiếp)
 */
async function searchYoutubeVideosOnline(query) {
    const cleanQ = (query || "").trim();
    if (!cleanQ) {
        showToast("Vui lòng nhập từ khóa tìm kiếm trên YouTube", "warning");
        return;
    }

    if (!DOM.topicVideosGrid) return;
    DOM.topicVideosLoading.classList.remove("hidden");
    DOM.topicVideosGrid.innerHTML = "";
    if (DOM.topicInfiniteScrollArea) DOM.topicInfiniteScrollArea.classList.add("hidden");

    if (DOM.topicDiscoveryTitle) {
        DOM.topicDiscoveryTitle.innerText = `Kết quả tìm kiếm YouTube: "${cleanQ}"`;
    }

    state.topicPagination = {
        active: true,
        query: cleanQ,
        topicTitle: cleanQ,
        page: 1,
        pageSize: 12,
        hasMore: true,
        isLoading: false,
        seenIds: new Set()
    };

    try {
        const res = await API.searchYoutubeVideos(cleanQ, 1, state.topicPagination.pageSize);
        DOM.topicVideosLoading.classList.add("hidden");

        const ytVideos = Array.isArray(res) ? res : (res.videos || []);
        const hasMore = Array.isArray(res) ? (ytVideos.length >= state.topicPagination.pageSize) : Boolean(res.has_more);
        state.topicPagination.hasMore = hasMore;

        if (!ytVideos || ytVideos.length === 0) {
            DOM.topicVideosGrid.innerHTML = `
                <div class="col-span-full py-12 text-center text-slate-400 bg-white rounded-2xl border border-slate-200 p-8 space-y-3">
                    <i class="fa-brands fa-youtube text-4xl text-red-400"></i>
                    <p class="text-sm font-semibold text-slate-700">Không tìm thấy video nào trên YouTube cho "${cleanQ}"</p>
                    <p class="text-xs text-slate-400">Hãy thử nhập từ khóa ngắn hơn như "IELTS Speaking Part 1" hoặc "Band 9 Sample".</p>
                </div>
            `;
            return;
        }

        renderVideoCards(ytVideos, cleanQ, false);
        updateInfiniteScrollUI();
    } catch (err) {
        console.error("Lỗi tìm kiếm YouTube:", err);
        DOM.topicVideosLoading.classList.add("hidden");
        showToast(`Không thể tìm kiếm video trên YouTube: ${err.message}`, "error");
    }
}

/**
 * Cập nhật giao diện thanh trạng thái cuộn trang vô tận
 */
function updateInfiniteScrollUI() {
    if (!DOM.topicInfiniteScrollArea) return;
    if (!state.topicPagination || !state.topicPagination.active) {
        DOM.topicInfiniteScrollArea.classList.add("hidden");
        return;
    }

    DOM.topicInfiniteScrollArea.classList.remove("hidden");

    if (state.topicPagination.isLoading) {
        if (DOM.infiniteScrollLoading) DOM.infiniteScrollLoading.classList.remove("hidden");
        if (DOM.loadMoreTopicVideosBtn) DOM.loadMoreTopicVideosBtn.classList.add("hidden");
        if (DOM.infiniteScrollEnd) DOM.infiniteScrollEnd.classList.add("hidden");
    } else if (state.topicPagination.hasMore) {
        if (DOM.infiniteScrollLoading) DOM.infiniteScrollLoading.classList.add("hidden");
        if (DOM.loadMoreTopicVideosBtn) DOM.loadMoreTopicVideosBtn.classList.remove("hidden");
        if (DOM.infiniteScrollEnd) DOM.infiniteScrollEnd.classList.add("hidden");
    } else {
        if (DOM.infiniteScrollLoading) DOM.infiniteScrollLoading.classList.add("hidden");
        if (DOM.loadMoreTopicVideosBtn) DOM.loadMoreTopicVideosBtn.classList.add("hidden");
        if (DOM.infiniteScrollEnd) DOM.infiniteScrollEnd.classList.remove("hidden");
    }
}

/**
 * Tải thêm đợt video tiếp theo khi người dùng cuộn xuống dưới
 */
async function loadMoreTopicVideos() {
    if (!state.topicPagination || !state.topicPagination.active) return;
    if (state.topicPagination.isLoading || !state.topicPagination.hasMore) return;

    state.topicPagination.isLoading = true;
    updateInfiniteScrollUI();

    const nextPage = state.topicPagination.page + 1;
    const query = state.topicPagination.query;
    const topicTitle = state.topicPagination.topicTitle;

    try {
        const res = await API.searchYoutubeVideos(query, nextPage, state.topicPagination.pageSize);
        const ytVideos = Array.isArray(res) ? res : (res.videos || []);
        const hasMore = Array.isArray(res) ? (ytVideos.length >= state.topicPagination.pageSize) : Boolean(res.has_more);

        state.topicPagination.page = nextPage;
        state.topicPagination.hasMore = hasMore;

        if (ytVideos.length > 0) {
            renderVideoCards(ytVideos, topicTitle, true);
        } else {
            state.topicPagination.hasMore = false;
        }
    } catch (err) {
        console.warn("Lỗi tải thêm video khi cuộn:", err);
        state.topicPagination.hasMore = false;
    } finally {
        state.topicPagination.isLoading = false;
        updateInfiniteScrollUI();
    }
}

/**
 * Khởi tạo tính năng tự động tải thêm khi cuộn (IntersectionObserver + Scroll fallback)
 */
function initTopicInfiniteScroll() {
    if (!DOM.topicInfiniteScrollArea) return;

    // 1. Tự động kích hoạt khi cuộn đến gần cuối trang (IntersectionObserver)
    if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver((entries) => {
            const entry = entries[0];
            if (entry && entry.isIntersecting) {
                if (state.topicPagination && state.topicPagination.active && state.topicPagination.hasMore && !state.topicPagination.isLoading) {
                    loadMoreTopicVideos();
                }
            }
        }, {
            root: null,
            rootMargin: "350px", // Kích hoạt sớm trước 350px để cuộn mượt mà không phải chờ
            threshold: 0.05
        });

        observer.observe(DOM.topicInfiniteScrollArea);
    }

    // 2. Nút bấm xem thêm trực tiếp
    if (DOM.loadMoreTopicVideosBtn) {
        DOM.loadMoreTopicVideosBtn.addEventListener("click", () => {
            loadMoreTopicVideos();
        });
    }

    // 3. Fallback theo dõi sự kiện window scroll
    window.addEventListener("scroll", () => {
        if (!state.topicPagination || !state.topicPagination.active || !state.topicPagination.hasMore || state.topicPagination.isLoading) {
            return;
        }
        if (DOM.topicDiscoveryView && DOM.topicDiscoveryView.classList.contains("hidden")) {
            return;
        }
        const scrollPosition = window.innerHeight + window.scrollY;
        const threshold = document.documentElement.scrollHeight - 400;
        if (scrollPosition >= threshold) {
            loadMoreTopicVideos();
        }
    }, { passive: true });
}

/**
 * Nạp nhanh video YouTube làm bài học Online chỉ trong 1-2 giây (0MB tải về)
 */
async function triggerInstantImportOnlineVideo(video, topicTitle) {
    try {
        showToast(`Đang nạp bài học online "${video.title}"...`, "info", 2000);
        const newVid = await API.importOnlineYoutubeVideo({
            url_or_id: video.id,
            title: video.title,
            topic: topicTitle || "General"
        });
        showToast(`🎉 Đã nạp thành công bài học "${newVid.title}"!`, "success", 4000);
        await loadVideos();
        switchTab("video");
        showMyVideosTab();
        selectVideo(newVid.id);
    } catch (err) {
        console.error("Lỗi nạp bài học online:", err);
        showToast(`Không thể nạp bài học: ${err.message}`, "error", 4000);
    }
}

/**
 * Mở modal xem video YouTube trực tiếp & hỗ trợ tìm kiếm từ vựng trong bài nói
 */
function openWatchVideoModal(video) {
    state.watchingVideo = video;
    if (DOM.watchModalTitle) DOM.watchModalTitle.innerText = video.title;
    if (DOM.watchIframe) DOM.watchIframe.src = `https://www.youtube.com/embed/${video.id}?autoplay=1`;

    // Reset thanh tìm kiếm từ vựng trong modal
    if (DOM.watchModalSearchInput) DOM.watchModalSearchInput.value = "";
    if (DOM.watchSearchCountBadge) DOM.watchSearchCountBadge.classList.add("hidden");
    if (DOM.watchModalSearchResults) {
        DOM.watchModalSearchResults.classList.add("hidden");
        DOM.watchModalSearchResults.innerHTML = "";
    }

    if (DOM.watchVideoModal) DOM.watchVideoModal.classList.remove("hidden");
}

/**
 * Đóng modal xem video YouTube
 */
function closeWatchVideoModal() {
    if (DOM.watchIframe) DOM.watchIframe.src = "";
    if (DOM.watchVideoModal) DOM.watchVideoModal.classList.add("hidden");
}

/**
 * Tìm kiếm từ vựng trực tiếp trong bài nói của video YouTube (Dùng phụ đề YouTube - Không cần tải file)
 */
async function executeInVideoSearch(query) {
    if (!state.watchingVideo) return;
    const cleanQ = (query || "").trim();
    if (!cleanQ) {
        if (DOM.watchModalSearchResults) DOM.watchModalSearchResults.classList.add("hidden");
        if (DOM.watchSearchCountBadge) DOM.watchSearchCountBadge.classList.add("hidden");
        return;
    }

    if (DOM.watchModalSearchResults) {
        DOM.watchModalSearchResults.classList.remove("hidden");
        DOM.watchModalSearchResults.innerHTML = `
            <div class="py-4 text-center text-slate-400 text-xs flex items-center justify-center space-x-2">
                <i class="fa-solid fa-spinner fa-spin text-indigo-400"></i>
                <span>Đang dò từ "${cleanQ}" trong bài nói của video...</span>
            </div>
        `;
    }

    try {
        const res = await API.searchWordsInYoutube(state.watchingVideo.id, cleanQ);
        const results = res.results || [];

        if (DOM.watchSearchCountBadge) {
            DOM.watchSearchCountBadge.innerText = `${results.length} kết quả`;
            DOM.watchSearchCountBadge.classList.remove("hidden");
        }

        if (results.length === 0) {
            DOM.watchModalSearchResults.innerHTML = `
                <div class="p-3 text-center text-slate-400 text-xs bg-slate-950 rounded-lg border border-slate-800">
                    Không tìm thấy từ "<strong>${cleanQ}</strong>" trong bài nói video này. Hãy thử từ khóa khác!
                </div>
            `;
            return;
        }

        DOM.watchModalSearchResults.innerHTML = "";
        results.forEach(item => {
            const row = document.createElement("div");
            row.className = "p-2.5 bg-slate-950 hover:bg-slate-900 border border-slate-800 rounded-lg flex items-center justify-between gap-3 text-xs text-white transition";

            const highlightedText = highlightWordInText(item.context_sentence, item.matched_word);
            const timeFormatted = formatTime(item.sentence_start_time);

            row.innerHTML = `
                <div class="flex-1 min-w-0 space-y-1">
                    <p class="text-slate-200 line-clamp-2 leading-relaxed">"${highlightedText}"</p>
                    ${item.vietnamese_meaning ? `
                        <p class="text-[11px] text-amber-400/90 font-medium truncate">
                            <i class="fa-solid fa-language mr-1"></i> ${item.vietnamese_meaning}
                        </p>
                    ` : ""}
                </div>
                <div class="flex items-center space-x-1.5 flex-shrink-0">
                    <button class="seek-yt-btn px-2.5 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-xs font-mono font-bold transition flex items-center space-x-1" title="Tua video tới câu này">
                        <i class="fa-solid fa-play text-[10px]"></i>
                        <span>${timeFormatted}</span>
                    </button>
                    <button class="fc-yt-btn px-2.5 py-1.5 bg-slate-800 hover:bg-amber-600 hover:text-white text-amber-300 rounded-lg text-xs font-bold transition flex items-center space-x-1" title="Thêm từ này vào Flashcard">
                        <i class="fa-solid fa-plus text-[10px]"></i>
                        <span>Thẻ</span>
                    </button>
                </div>
            `;

            // Bấm tua video YouTube trong iframe
            row.querySelector(".seek-yt-btn").onclick = () => {
                if (DOM.watchIframe && state.watchingVideo) {
                    DOM.watchIframe.src = `https://www.youtube.com/embed/${state.watchingVideo.id}?start=${Math.floor(item.sentence_start_time)}&autoplay=1`;
                }
            };

            // Bấm thêm Flashcard
            row.querySelector(".fc-yt-btn").onclick = () => {
                openAddFlashcardModal({
                    word: item.matched_word,
                    meaning: item.vietnamese_meaning || "",
                    context_sentence: item.context_sentence,
                    video_id: state.currentVideo ? state.currentVideo.id : 1,
                    start_time: item.sentence_start_time,
                    end_time: item.sentence_end_time
                });
            };

            DOM.watchModalSearchResults.appendChild(row);
        });

    } catch (err) {
        console.error("Lỗi tìm từ trong video YouTube:", err);
        if (DOM.watchModalSearchResults) {
            DOM.watchModalSearchResults.innerHTML = `
                <div class="p-2.5 text-center text-rose-400 text-xs bg-slate-950 rounded-lg border border-slate-800">
                    ${err.message || "Không thể tìm từ vựng trong video này."}
                </div>
            `;
        }
    }
}

/**
 * Tự động tải video từ danh mục chủ đề và chạy Whisper để đưa vào "Video của tôi"
 */
async function triggerImportTopicVideo(video, topicTitle) {
    const ok = await showConfirm({
        title: "Học từ vựng từ Video mẫu",
        message: `Hệ thống sẽ tải video và dùng Whisper bóc tách mốc thời gian từng từ cho bài thi:\n"${video.title}".\n\n(Quá trình xử lý sẽ mất khoảng 1-2 phút)`,
        confirmText: "Bắt đầu học ngay",
        confirmColor: "indigo",
        icon: "fa-wand-magic-sparkles"
    });
    if (!ok) return;

    closeWatchVideoModal();

    // Mở modal upload để hiển thị tiến trình
    DOM.uploadModal.classList.remove("hidden");
    DOM.uploadProgressBox.classList.remove("hidden");
    DOM.progressStatusText.innerText = `Đang tải video & Whisper đang trích xuất từng từ cho: "${video.title}"...`;
    DOM.submitUrlBtn.disabled = true;

    try {
        const uploaded = await API.processVideoFromUrl({
            url: video.url,
            title: video.title,
            topic: topicTitle,
            model_name: "base"
        });
        showToast(`Đã trích xuất xong từ vựng cho video "${uploaded.title}"!`, "success", 4500);
        DOM.uploadModal.classList.add("hidden");
        // Nạp lại danh sách video của tôi và chuyển sang xem ngay
        await loadVideos();
        showMyVideosTab();
        selectVideo(uploaded.id);
    } catch (err) {
        showToast("Lỗi khi xử lý video: " + err.message, "error", 5000);
    } finally {
        DOM.uploadProgressBox.classList.add("hidden");
        DOM.submitUrlBtn.disabled = false;
    }
}


// ==================== VIDEO PLAYER & SEARCH LOGIC ====================

/**
 * Tải danh sách video của tôi và cập nhật dropdown
 */
async function loadVideos() {
    try {
        state.videos = await API.fetchVideos();
        DOM.videoSelect.innerHTML = "";

        if (state.videos.length === 0) {
            DOM.videoSelect.innerHTML = `<option value="">-- Chưa có video nào (Hãy dán link hoặc chọn chủ đề) --</option>`;
            DOM.videoPlaceholder.classList.remove("hidden");
            DOM.videoTitleDisplay.innerText = "Tiêu đề: Chưa có video";
            DOM.currentTimeDisplay.innerText = "00:00.0";
            DOM.totalDurationDisplay.innerText = "00:00.0";
            DOM.mainVideo.removeAttribute("src");
            DOM.mainVideo.load();
            renderTopicTabs();
            return;
        }

        state.videos.forEach(vid => {
            const opt = document.createElement("option");
            opt.value = vid.id;
            opt.textContent = `[${vid.topic || 'General'}] ${vid.title} (${Math.round(vid.duration)}s)`;
            DOM.videoSelect.appendChild(opt);
        });

        // Chọn video đầu tiên nếu chưa có
        if (!state.currentVideo || !state.videos.some(v => v.id === state.currentVideo.id)) {
            selectVideo(state.videos[0].id);
        }

        renderTopicTabs();
    } catch (e) {
        console.error("Lỗi nạp video:", e);
    }
}

/**
 * Chọn video để phát
 */
function selectVideo(videoId) {
    const vid = state.videos.find(v => v.id === Number(videoId));
    if (!vid) return;

    state.currentVideo = vid;
    DOM.videoSelect.value = vid.id;
    DOM.videoPlaceholder.classList.add("hidden");
    DOM.videoTitleDisplay.innerText = `Tiêu đề: ${vid.title}`;
    DOM.totalDurationDisplay.innerText = formatTime(vid.duration);

    const isYoutubeEmbed = vid.filepath && (vid.filepath.includes("youtube.com/embed") || vid.filepath.includes("youtu.be"));

    if (isYoutubeEmbed && DOM.mainYoutubePlayer) {
        // Tắt HTML5 video player và chuyển sang iframe YouTube
        DOM.mainVideo.classList.add("hidden");
        DOM.mainVideo.pause();
        DOM.mainVideo.removeAttribute("src");
        DOM.mainYoutubePlayer.classList.remove("hidden");
        DOM.mainYoutubePlayer.src = `${vid.filepath}?enablejsapi=1`;
    } else {
        // HTML5 Video player thông thường
        if (DOM.mainYoutubePlayer) {
            DOM.mainYoutubePlayer.classList.add("hidden");
            DOM.mainYoutubePlayer.src = "";
        }
        DOM.mainVideo.classList.remove("hidden");
        const fullVideoUrl = vid.filepath.startsWith("http") ? vid.filepath : `${API_BASE_URL}${vid.filepath}`;
        DOM.mainVideo.src = fullVideoUrl;
        DOM.mainVideo.load();
    }

    // Nếu đang có từ khóa tìm kiếm, tự động tìm kiếm trên video mới
    const query = DOM.vocabSearchInput.value.trim();
    if (query) {
        triggerSearch(query);
    }
}

/**
 * Tua video đến mốc thời gian chính xác (Core Feature 1)
 */
function seekVideo(timeInSeconds, shouldPlay = true) {
    const targetTime = Math.max(0, parseFloat(timeInSeconds));
    const isYoutubeEmbed = state.currentVideo && state.currentVideo.filepath && (state.currentVideo.filepath.includes("youtube.com/embed") || state.currentVideo.filepath.includes("youtu.be"));

    if (isYoutubeEmbed && DOM.mainYoutubePlayer) {
        DOM.currentTimeDisplay.innerText = formatTime(targetTime);
        const baseUrl = state.currentVideo.filepath.split("?")[0];
        DOM.mainYoutubePlayer.src = `${baseUrl}?start=${Math.floor(targetTime)}&autoplay=${shouldPlay ? 1 : 0}`;
        if (window.innerWidth < 1024) {
            DOM.mainYoutubePlayer.scrollIntoView({ behavior: "smooth", block: "center" });
        }
        return;
    }

    if (!DOM.mainVideo.src) return;
    DOM.mainVideo.currentTime = targetTime;
    
    if (shouldPlay) {
        DOM.mainVideo.play().catch(err => console.log("User interaction required for autoplay:", err));
    }

    // Cuộn nhẹ lên video player nếu đang xem trên màn hình nhỏ
    if (window.innerWidth < 1024) {
        DOM.mainVideo.scrollIntoView({ behavior: "smooth", block: "center" });
    }
}

/**
 * Xử lý tìm kiếm từ vựng với Debounce
 */
function triggerSearch(query) {
    if (!query || query.length < 2) {
        DOM.clearSearchBtn.classList.add("hidden");
        DOM.searchResultCount.innerText = "Nhập từ để tìm kiếm các câu phát âm";
        DOM.searchResultsList.innerHTML = `
            <div class="h-full flex flex-col items-center justify-center text-center text-slate-400 p-6">
                <i class="fa-solid fa-magnifying-glass text-4xl mb-3 text-slate-300"></i>
                <p class="text-sm font-medium text-slate-600">Tìm kiếm từ vựng bất kỳ</p>
                <p class="text-xs text-slate-400 mt-1">Hệ thống sẽ quét từng mốc thời gian của Whisper và hiển thị ngữ cảnh câu nói.</p>
            </div>
        `;
        return;
    }

    DOM.clearSearchBtn.classList.remove("hidden");
    DOM.searchResultCount.innerHTML = `<i class="fa-solid fa-spinner fa-spin mr-1"></i> Đang tìm kiếm...`;

    clearTimeout(state.searchDebounceTimer);
    state.searchDebounceTimer = setTimeout(async () => {
        try {
            const videoId = state.currentVideo ? state.currentVideo.id : null;
            const results = await API.searchWords(query, videoId);
            renderSearchResults(results, query);
        } catch (err) {
            console.error("Lỗi tìm kiếm:", err);
            DOM.searchResultCount.innerText = "Có lỗi xảy ra khi tìm kiếm";
        }
    }, 300);
}

/**
 * Hiển thị danh sách kết quả tìm kiếm kèm câu chứa từ vựng & nút tua video
 */
function renderSearchResults(results, query) {
    DOM.searchResultCount.innerText = `Tìm thấy ${results.length} kết quả phù hợp`;
    DOM.searchResultsList.innerHTML = "";

    if (results.length === 0) {
        DOM.searchResultsList.innerHTML = `
            <div class="h-full flex flex-col items-center justify-center text-center text-slate-400 p-6">
                <i class="fa-regular fa-face-frown text-4xl mb-3 text-slate-300"></i>
                <p class="text-sm font-semibold text-slate-600">Không tìm thấy từ "${query}"</p>
                <p class="text-xs text-slate-400 mt-1">Hãy thử tìm dạng từ nguyên thể hoặc một từ khác trong video.</p>
            </div>
        `;
        return;
    }

    results.forEach(item => {
        const card = document.createElement("div");
        card.className = "p-3.5 bg-slate-50 hover:bg-indigo-50/40 rounded-xl border border-slate-200 transition group space-y-2";

        const highlightedSentence = highlightWordInText(item.context_sentence, query);

        card.innerHTML = `
            <div class="flex items-center justify-between text-xs">
                <span class="inline-flex items-center space-x-1 font-mono font-semibold text-indigo-700 bg-indigo-100/70 px-2 py-0.5 rounded">
                    <i class="fa-regular fa-clock text-[10px]"></i>
                    <span>${formatTime(item.word_start_time)}</span>
                </span>
                <span class="text-[11px] text-slate-400 truncate max-w-[150px]">${item.video_title}</span>
            </div>

            <p class="text-xs sm:text-sm text-slate-700 leading-relaxed italic">
                "${highlightedSentence}"
            </p>

            <div class="flex items-center justify-end space-x-2 pt-1 border-t border-slate-200/60">
                <button class="seek-btn px-2.5 py-1.5 bg-white hover:bg-indigo-600 hover:text-white border border-slate-200 hover:border-indigo-600 rounded-lg text-xs font-semibold text-slate-700 transition flex items-center space-x-1">
                    <i class="fa-solid fa-play text-[10px]"></i>
                    <span>Phát đoạn này</span>
                </button>
                <button class="add-fc-btn px-2.5 py-1.5 bg-indigo-50 hover:bg-indigo-600 hover:text-white border border-indigo-200 hover:border-indigo-600 rounded-lg text-xs font-semibold text-indigo-700 transition flex items-center space-x-1">
                    <i class="fa-solid fa-star text-[10px] text-amber-500 group-hover:text-amber-300"></i>
                    <span>+ Flashcard</span>
                </button>
            </div>
        `;

        // Sự kiện: Bấm vào kết quả -> Tua video chính xác đến khoảnh khắc đó
        card.querySelector(".seek-btn").addEventListener("click", () => {
            // Nếu kết quả thuộc video khác, chuyển video trước
            if (state.currentVideo && state.currentVideo.id !== item.video_id) {
                selectVideo(item.video_id);
                setTimeout(() => seekVideo(item.word_start_time), 300);
            } else {
                seekVideo(item.word_start_time);
            }
        });

        // Sự kiện: Thêm vào Flashcard
        card.querySelector(".add-fc-btn").addEventListener("click", () => {
            openAddFlashcardModal(item, query);
        });

        DOM.searchResultsList.appendChild(card);
    });
}


// ==================== FLASHCARD DECK & STUDY LOGIC ====================

/**
 * Tải toàn bộ Flashcards từ database và hiển thị
 */
async function loadFlashcardDeck() {
    try {
        state.flashcards = await API.fetchFlashcards();
        updateFlashcardBadgeCount();

        if (state.flashcards.length === 0) {
            DOM.emptyFlashcardState.classList.remove("hidden");
            DOM.flashcardDeckContainer.classList.add("hidden");
            return;
        }

        DOM.emptyFlashcardState.classList.add("hidden");
        DOM.flashcardDeckContainer.classList.remove("hidden");

        if (state.currentCardIndex >= state.flashcards.length) {
            state.currentCardIndex = 0;
        }

        renderCurrentFlashcard();
    } catch (e) {
        console.error("Lỗi nạp flashcard:", e);
    }
}

/**
 * Hiển thị thẻ Flashcard tại vị trí hiện tại (Mặt trước & Mặt sau)
 */
function renderCurrentFlashcard() {
    if (state.flashcards.length === 0) return;

    const card = state.flashcards[state.currentCardIndex];
    state.isCardFlipped = false;
    DOM.flashcardInner.classList.remove("is-flipped");

    // Tiến trình thẻ
    DOM.cardProgressText.innerText = `Thẻ ${state.currentCardIndex + 1} / ${state.flashcards.length}`;

    // Cập nhật mặt trước
    DOM.cardWord.innerText = card.word;
    DOM.cardSentence.innerHTML = highlightWordInText(card.context_sentence, card.word);
    DOM.cardTimestampTag.innerText = formatTime(card.start_time);
    
    // Trạng thái thẻ
    if (card.status === "mastered") {
        DOM.cardStatusBadge.className = "px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-700";
        DOM.cardStatusBadge.innerText = "Đã thuộc";
        DOM.masteredBtnText.innerText = "Học lại thẻ này";
    } else {
        DOM.cardStatusBadge.className = "px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-700";
        DOM.cardStatusBadge.innerText = "Đang học";
        DOM.masteredBtnText.innerText = "Đánh dấu đã thuộc";
    }

    // Cập nhật mặt sau
    DOM.cardBackWord.innerText = card.word;
    DOM.cardMeaning.innerText = card.meaning;
}

/**
 * Cập nhật số đếm badge Flashcard trên thanh điều hướng
 */
function updateFlashcardBadgeCount() {
    DOM.flashcardCountBadge.innerText = state.flashcards.length;
}

/**
 * Lật thẻ Flashcard (3D flip animation)
 */
function toggleFlipCard() {
    state.isCardFlipped = !state.isCardFlipped;
    if (state.isCardFlipped) {
        DOM.flashcardInner.classList.add("is-flipped");
    } else {
        DOM.flashcardInner.classList.remove("is-flipped");
    }
}

/**
 * Xem lại đoạn video gốc từ Flashcard (Core Feature 2)
 */
function replayFlashcardVideo(card) {
    if (!card) return;

    // Thiết lập video cho Replay Modal
    DOM.replayModalTitle.innerText = `Ngữ cảnh: "${card.word}" trong "${card.video_title || 'Video'}"`;
    DOM.replaySentenceContext.innerHTML = highlightWordInText(card.context_sentence, card.word);
    
    // Tìm video trong state hoặc lấy từ card
    const targetVideo = state.videos.find(v => v.id === card.video_id);
    let rawVideoUrl = targetVideo ? targetVideo.filepath : `/uploads/${card.video_filename}`;
    const videoUrl = rawVideoUrl.startsWith("http") ? rawVideoUrl : `${API_BASE_URL}${rawVideoUrl}`;

    DOM.replayVideo.src = videoUrl;
    DOM.videoReplayModal.classList.remove("hidden");

    // Khi video sẵn sàng, tua đến đúng khoảnh khắc nhân vật phát âm từ
    DOM.replayVideo.onloadedmetadata = () => {
        // Lùi lại 0.5s trước mốc để người học nghe rõ trọn vẹn ngữ cảnh
        const seekTime = Math.max(0, card.start_time - 0.5);
        DOM.replayVideo.currentTime = seekTime;
        DOM.replayVideo.play().catch(e => console.log(e));
    };

    // Nút "Mở trên Player chính": Chuyển sang Tab 1 và nhảy đến mốc thời gian
    DOM.jumpToMainPlayerBtn.onclick = () => {
        DOM.replayVideo.pause();
        DOM.videoReplayModal.classList.add("hidden");
        switchTab("video");
        selectVideo(card.video_id);
        setTimeout(() => {
            seekVideo(card.start_time);
        }, 300);
    };
}

/**
 * Phát âm từ vựng bằng Web Speech API
 */
function pronounceCurrentWord() {
    if (state.flashcards.length === 0) return;
    const card = state.flashcards[state.currentCardIndex];
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(card.word);
        utterance.lang = "en-US";
        utterance.rate = 0.9;
        window.speechSynthesis.speak(utterance);
    }
}


// ==================== MODAL HANDLERS ====================

async function openAddFlashcardModal(item, queryWord) {
    const targetWord = (item.matched_word || queryWord || "").trim();
    DOM.fcWordInput.value = targetWord;
    DOM.fcMeaningInput.value = "";
    DOM.fcSentenceInput.value = item.context_sentence;
    DOM.fcVideoId.value = item.video_id;
    DOM.fcStartTime.value = item.word_start_time;
    DOM.fcEndTime.value = item.word_end_time;
    DOM.fcTimestampBadge.innerText = formatTime(item.word_start_time);
    DOM.fcVideoIdText.innerText = `#${item.video_id} - ${item.video_title}`;

    // Reset trạng thái gợi ý
    DOM.meaningSuggestionsBox.classList.add("hidden");
    DOM.meaningChipsContainer.innerHTML = "";
    DOM.fcSentenceTranslation.classList.add("hidden");
    DOM.fcSentenceTransText.innerText = "";
    DOM.meaningLoadingIndicator.classList.remove("hidden");

    DOM.flashcardModal.classList.remove("hidden");

    // Tự động gọi API tra cứu nghĩa tiếng Việt và gợi ý từ đồng nghĩa
    try {
        const dictData = await API.lookupWord(targetWord, item.context_sentence);
        if (dictData) {
            // Tự động điền nghĩa chính vào ô nhập
            if (dictData.primary_meaning) {
                DOM.fcMeaningInput.value = dictData.primary_meaning;
            }

            // Hiển thị các nút gợi ý nghĩa (Chips) để bấm chọn nhanh
            if (dictData.suggestions && dictData.suggestions.length > 0) {
                DOM.meaningChipsContainer.innerHTML = "";
                dictData.suggestions.forEach(suggestion => {
                    const chip = document.createElement("button");
                    chip.type = "button";
                    chip.className = "px-2.5 py-1 bg-indigo-50 hover:bg-indigo-600 hover:text-white text-indigo-700 text-xs font-semibold rounded-lg border border-indigo-200 hover:border-indigo-600 transition flex items-center space-x-1";
                    chip.innerHTML = `<span>${suggestion}</span>`;
                    chip.onclick = () => {
                        DOM.fcMeaningInput.value = suggestion;
                        DOM.fcMeaningInput.focus();
                    };
                    DOM.meaningChipsContainer.appendChild(chip);
                });
                DOM.meaningSuggestionsBox.classList.remove("hidden");
            }

            // Hiển thị bản dịch của câu ngữ cảnh
            if (dictData.sentence_translation) {
                DOM.fcSentenceTransText.innerText = dictData.sentence_translation;
                DOM.fcSentenceTranslation.classList.remove("hidden");
            }
        }
    } catch (err) {
        console.warn("Không thể nạp gợi ý nghĩa:", err);
    } finally {
        DOM.meaningLoadingIndicator.classList.add("hidden");
        DOM.fcMeaningInput.focus();
    }
}


// ==================== DESCRIPTION VOCABULARY SCANNING ====================

/**
 * Mở modal Quét từ vựng từ Description của video hiện tại (Video của tôi)
 */
async function openDescriptionVocabModal() {
    if (!state.currentVideo) {
        showToast("Vui lòng chọn 1 video trước khi quét description!", "warning");
        return;
    }

    state.activeScanningTarget = {
        type: "local",
        video: state.currentVideo
    };

    DOM.descVocabModal.classList.remove("hidden");
    DOM.descScanLoading.classList.add("hidden");

    // Hiển thị thông báo link nguồn nếu có
    if (state.currentVideo.source_url) {
        DOM.descSourceUrlNotice.innerText = `Nguồn: ${state.currentVideo.source_url}`;
        DOM.fetchDescFromYoutubeBtn.classList.remove("hidden");
    } else {
        DOM.descSourceUrlNotice.innerText = "";
        DOM.fetchDescFromYoutubeBtn.classList.add("hidden");
    }

    // Nạp description đã lưu (hoặc lấy từ server)
    try {
        const descData = await API.fetchVideoDescription(state.currentVideo.id);
        if (descData && descData.description) {
            DOM.descVocabTextarea.value = descData.description;
            state.currentVideo.description = descData.description;
            if (descData.source_url) state.currentVideo.source_url = descData.source_url;
        } else if (state.currentVideo.description) {
            DOM.descVocabTextarea.value = state.currentVideo.description;
        } else {
            DOM.descVocabTextarea.value = "";
        }
    } catch (e) {
        DOM.descVocabTextarea.value = state.currentVideo.description || "";
    }

    // Tự động quét nếu đã có nội dung description
    if (DOM.descVocabTextarea.value.trim().length > 10) {
        await executeDescriptionScan();
    }
}

/**
 * Mở modal Quét từ vựng từ Description cho Video YouTube trong Tab Chủ đề IELTS
 */
async function openDescriptionVocabForOnlineVideo(video) {
    if (!video) return;

    state.activeScanningTarget = {
        type: "online",
        video: video
    };

    DOM.descVocabModal.classList.remove("hidden");
    DOM.descScanLoading.classList.remove("hidden");
    DOM.descMatchedList.innerHTML = "";
    DOM.descScanCountBadge.classList.add("hidden");
    DOM.descSourceUrlNotice.innerText = `YouTube: ${video.channel} - ${video.title}`;
    DOM.fetchDescFromYoutubeBtn.classList.remove("hidden");
    DOM.descVocabTextarea.value = "Đang tải mô tả và phụ đề từ YouTube...";
    DOM.runScanDescBtn.disabled = true;

    try {
        const result = await API.scanOnlineYoutubeVocab({
            youtube_id: video.id,
            url: video.url,
            title: video.title
        });

        DOM.descVocabTextarea.value = result.description || "";
        renderDescriptionScanResults(result);
    } catch (err) {
        showToast("Lỗi khi quét từ vựng YouTube: " + err.message, "error", 5000);
        DOM.descScanLoading.classList.add("hidden");
        DOM.descMatchedList.innerHTML = `
            <div class="py-10 text-center text-slate-400 bg-slate-50/70 rounded-2xl border border-dashed border-slate-200 p-6 space-y-2">
                <i class="fa-solid fa-triangle-exclamation text-3xl text-amber-500"></i>
                <p class="text-xs font-semibold text-slate-700">Chưa thể quét tự động từ vựng cho video này</p>
                <p class="text-[11px] text-slate-400 max-w-md mx-auto">Bạn có thể tự dán danh sách từ vào ô mô tả bên trên rồi bấm "Dò từ vựng trong video".</p>
            </div>
        `;
    } finally {
        DOM.runScanDescBtn.disabled = false;
    }
}

/**
 * Đóng modal Description
 */
function closeDescriptionVocabModal() {
    DOM.descVocabModal.classList.add("hidden");
}

/**
 * Thực hiện gọi API quét từ vựng trong description và đối chiếu với video
 */
async function executeDescriptionScan() {
    const isOnline = state.activeScanningTarget && state.activeScanningTarget.type === "online";
    if (!isOnline && !state.currentVideo) return;

    const descText = DOM.descVocabTextarea.value.trim();
    if (!descText) {
        showToast("Vui lòng nhập hoặc dán nội dung mô tả video (description)!", "warning");
        DOM.descVocabTextarea.focus();
        return;
    }

    DOM.descScanLoading.classList.remove("hidden");
    DOM.descMatchedList.innerHTML = "";
    DOM.runScanDescBtn.disabled = true;

    try {
        let result;
        if (isOnline) {
            const target = state.activeScanningTarget.video;
            result = await API.scanOnlineYoutubeVocab({
                youtube_id: target.id,
                url: target.url,
                title: target.title,
                custom_description: descText
            });
        } else {
            result = await API.scanDescriptionVocab(state.currentVideo.id, {
                description_text: descText,
                source_url: state.currentVideo.source_url || null
            });
        }

        renderDescriptionScanResults(result);
    } catch (err) {
        showToast("Lỗi khi quét từ vựng description: " + err.message, "error", 5000);
        DOM.descScanLoading.classList.add("hidden");
    } finally {
        DOM.runScanDescBtn.disabled = false;
    }
}

/**
 * Render danh sách thẻ từ vựng đã dò tìm được từ description
 */
function renderDescriptionScanResults(result) {
    DOM.descScanLoading.classList.add("hidden");
    const list = result.matched_vocab || [];
    const isOnline = state.activeScanningTarget && state.activeScanningTarget.type === "online";
    const targetVideo = isOnline ? state.activeScanningTarget.video : state.currentVideo;

    DOM.descScanCountBadge.innerText = `${list.length} từ vựng`;
    DOM.descScanCountBadge.classList.remove("hidden");
    DOM.descScanStats.innerHTML = `
        <i class="fa-solid fa-spell-check text-indigo-600"></i>
        <span>Tìm thấy <b>${list.length}</b> từ vựng xuất hiện trong video:</span>
    `;

    if (list.length === 0) {
        DOM.descMatchedList.innerHTML = `
            <div class="py-10 text-center text-slate-400 bg-slate-50/70 rounded-2xl border border-dashed border-slate-200 p-6 space-y-2">
                <i class="fa-regular fa-face-meh text-3xl text-slate-300"></i>
                <p class="text-xs font-semibold text-slate-700">Chưa tìm thấy từ nào trong description xuất hiện trong bài nói này</p>
                <p class="text-[11px] text-slate-400 max-w-md mx-auto">Bạn có thể tự tay gõ hoặc dán thêm các từ vựng vào ô mô tả bên trên rồi bấm "Dò từ vựng trong video".</p>
            </div>
        `;
        return;
    }

    DOM.descMatchedList.innerHTML = "";
    list.forEach((item, index) => {
        const card = document.createElement("div");
        card.className = "bg-white p-4 rounded-xl border border-slate-200 hover:border-indigo-300 hover:shadow-md transition space-y-2.5";

        const escapedWord = item.word.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
        const highlightRegex = new RegExp(`(${escapedWord})`, "gi");
        const highlightedSentence = item.context_sentence.replace(highlightRegex, `<mark class="vocab-highlight">$1</mark>`);

        let descDefHtml = "";
        if (item.definition_in_desc) {
            descDefHtml = `<div class="text-[11px] text-slate-500 italic bg-slate-50 px-2.5 py-1 rounded-lg border border-slate-100 flex items-center space-x-1.5"><i class="fa-solid fa-quote-left text-[10px] text-indigo-400"></i><span>${item.definition_in_desc}</span></div>`;
        }

        let vnMeaningHtml = "";
        if (item.vietnamese_meaning) {
            vnMeaningHtml = `<span class="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200"><i class="fa-solid fa-language mr-1"></i>${item.vietnamese_meaning}</span>`;
        }

        card.innerHTML = `
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-1 border-b border-slate-100">
                <div class="flex items-center space-x-2">
                    <span class="w-6 h-6 rounded-lg bg-indigo-50 text-indigo-700 font-bold text-xs flex items-center justify-center flex-shrink-0">${index + 1}</span>
                    <h4 class="text-sm font-extrabold text-indigo-600">${item.word}</h4>
                    ${vnMeaningHtml}
                </div>
                <div class="flex items-center space-x-2 text-xs">
                    <span class="text-slate-400 text-[11px]"><i class="fa-solid fa-clock text-slate-400 mr-1"></i>${formatTime(item.sentence_start_time)}</span>
                    ${item.occurrences_count > 1 ? `<span class="bg-amber-50 text-amber-700 border border-amber-200 px-2 py-0.5 rounded text-[10px] font-bold">${item.occurrences_count} lần nói</span>` : ''}
                </div>
            </div>
            ${descDefHtml}
            <div class="text-xs text-slate-700 leading-relaxed bg-slate-50/50 p-2.5 rounded-xl border border-slate-100">
                "${highlightedSentence}"
            </div>
            <div class="flex items-center justify-end space-x-2 pt-1">
                <button class="jump-sentence-btn px-3 py-1.5 bg-slate-100 hover:bg-indigo-600 hover:text-white text-slate-700 rounded-xl text-xs font-semibold transition flex items-center space-x-1">
                    <i class="fa-solid fa-play text-[10px]"></i>
                    <span>Nghe đoạn này (${formatTime(item.sentence_start_time)})</span>
                </button>
                <button class="add-fc-btn px-3 py-1.5 bg-indigo-50 hover:bg-indigo-600 hover:text-white text-indigo-700 rounded-xl text-xs font-bold border border-indigo-200 hover:border-indigo-600 transition flex items-center space-x-1">
                    <i class="fa-solid fa-plus text-[10px]"></i>
                    <span>Thêm Flashcard</span>
                </button>
            </div>
        `;

        // Bấm nghe đoạn này
        card.querySelector(".jump-sentence-btn").onclick = () => {
            if (isOnline) {
                DOM.watchModalTitle.innerText = `${targetVideo.title} (tại ${formatTime(item.sentence_start_time)})`;
                DOM.watchIframe.src = `https://www.youtube.com/embed/${targetVideo.id}?start=${Math.floor(item.sentence_start_time)}&autoplay=1`;
                DOM.watchVideoModal.classList.remove("hidden");
                DOM.descVocabModal.classList.add("hidden");
                showToast(`Đang phát YouTube tại mốc ${formatTime(item.sentence_start_time)}`, "info", 3000);
            } else {
                seekVideo(item.sentence_start_time, true);
                showToast(`Đang phát đoạn chứa từ "${item.word}" (${formatTime(item.sentence_start_time)})`, "info", 2500);
            }
        };

        // Bấm thêm Flashcard
        card.querySelector(".add-fc-btn").onclick = () => {
            const vidId = isOnline ? 0 : (targetVideo.id || 0);
            openAddFlashcardModal({
                matched_word: item.word,
                context_sentence: item.context_sentence,
                video_id: vidId,
                video_title: targetVideo.title,
                word_start_time: item.word_start_time || item.sentence_start_time,
                word_end_time: item.word_end_time || item.sentence_end_time
            }, item.word);

            if (item.vietnamese_meaning) {
                DOM.fcMeaningInput.value = item.vietnamese_meaning;
            }
        };

        DOM.descMatchedList.appendChild(card);
    });
}


// ==================== EVENT LISTENERS SETUP ====================
function setupEventListeners() {
    // Tab switching
    DOM.tabVideoBtn.addEventListener("click", () => switchTab("video"));
    DOM.tabFlashcardBtn.addEventListener("click", () => switchTab("flashcard"));
    DOM.goBackToVideoBtn.addEventListener("click", () => switchTab("video"));

    // Video selector
    DOM.videoSelect.addEventListener("change", (e) => {
        if (e.target.value) selectVideo(e.target.value);
    });

    // Nút xóa video đang chọn
    if (DOM.deleteCurrentVideoBtn) {
        DOM.deleteCurrentVideoBtn.addEventListener("click", async () => {
            if (!state.currentVideo) {
                showToast("Chưa có video nào để xóa!", "warning");
                return;
            }
            const ok = await showConfirm({
                title: "Xác nhận xóa Video",
                message: `Bạn có chắc chắn muốn xóa video này khỏi kho bài học không?\n\n"${state.currentVideo.title}"\n\n(Toàn bộ câu phụ đề và mốc từ vựng của video này sẽ được dọn dẹp sạch sẽ)`,
                confirmText: "Xóa video",
                confirmColor: "rose",
                icon: "fa-solid fa-trash-can"
            });
            if (!ok) return;

            try {
                const vidTitle = state.currentVideo.title;
                await API.deleteVideo(state.currentVideo.id);
                showToast(`Đã xóa video "${vidTitle}" thành công!`, "success", 3000);
                state.currentVideo = null;
                await loadVideos();
                showMyVideosTab();
            } catch (err) {
                showToast("Lỗi khi xóa video: " + err.message, "error", 4000);
            }
        });
    }

    // Time update listener on main player
    DOM.mainVideo.addEventListener("timeupdate", () => {
        DOM.currentTimeDisplay.innerText = formatTime(DOM.mainVideo.currentTime);
    });

    // Search input
    DOM.vocabSearchInput.addEventListener("input", (e) => {
        triggerSearch(e.target.value.trim());
    });

    DOM.clearSearchBtn.addEventListener("click", () => {
        DOM.vocabSearchInput.value = "";
        triggerSearch("");
        DOM.vocabSearchInput.focus();
    });

    // Flashcard Deck Interactions
    DOM.flashcardInner.addEventListener("click", (e) => {
        // Tránh kích hoạt lật thẻ nếu đang click vào nút phát video hoặc phát âm
        if (e.target.closest("button")) return;
        toggleFlipCard();
    });
    DOM.flipCardBtn.addEventListener("click", toggleFlipCard);

    // Bấm Space để lật thẻ
    window.addEventListener("keydown", (e) => {
        if (e.code === "Space" && !DOM.tabFlashcardSection.classList.contains("hidden")) {
            // Không lật nếu đang gõ trong input/textarea
            if (["INPUT", "TEXTAREA"].includes(document.activeElement.tagName)) return;
            e.preventDefault();
            toggleFlipCard();
        }
    });

    // Điều hướng thẻ
    DOM.prevCardBtn.addEventListener("click", () => {
        if (state.flashcards.length === 0) return;
        state.currentCardIndex = (state.currentCardIndex - 1 + state.flashcards.length) % state.flashcards.length;
        renderCurrentFlashcard();
    });

    DOM.nextCardBtn.addEventListener("click", () => {
        if (state.flashcards.length === 0) return;
        state.currentCardIndex = (state.currentCardIndex + 1) % state.flashcards.length;
        renderCurrentFlashcard();
    });

    DOM.shuffleCardsBtn.addEventListener("click", () => {
        if (state.flashcards.length <= 1) return;
        // Thuật toán xáo trộn Fisher-Yates
        for (let i = state.flashcards.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [state.flashcards[i], state.flashcards[j]] = [state.flashcards[j], state.flashcards[i]];
        }
        state.currentCardIndex = 0;
        renderCurrentFlashcard();
    });

    // Nút xem lại video gốc trên Flashcard
    DOM.cardPlayVideoBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        const card = state.flashcards[state.currentCardIndex];
        replayFlashcardVideo(card);
    });
    DOM.cardBackPlayVideoBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        const card = state.flashcards[state.currentCardIndex];
        replayFlashcardVideo(card);
    });

    // Phát âm từ
    DOM.pronounceWordBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        pronounceCurrentWord();
    });

    // Đánh dấu đã thuộc / đang học
    DOM.toggleMasteredBtn.addEventListener("click", async () => {
        if (state.flashcards.length === 0) return;
        const card = state.flashcards[state.currentCardIndex];
        const newStatus = card.status === "mastered" ? "learning" : "mastered";
        try {
            await API.updateFlashcard(card.id, { status: newStatus });
            card.status = newStatus;
            renderCurrentFlashcard();
            showToast(newStatus === "mastered" ? `Đã đánh dấu thuộc từ "${card.word}"!` : `Đã chuyển "${card.word}" về đang học`, "success", 2500);
        } catch (e) {
            showToast("Lỗi khi cập nhật trạng thái thẻ", "error");
        }
    });

    // Xóa thẻ Flashcard
    DOM.deleteCardBtn.addEventListener("click", async () => {
        if (state.flashcards.length === 0) return;
        const card = state.flashcards[state.currentCardIndex];
        const ok = await showConfirm({
            title: "Xác nhận xóa Flashcard",
            message: `Bạn có chắc chắn muốn xóa thẻ từ vựng "${card.word}" không?\nThao tác này không thể hoàn tác.`,
            confirmText: "Xóa thẻ",
            confirmColor: "red",
            icon: "fa-trash-can"
        });
        if (!ok) return;

        try {
            const deletedWord = card.word;
            await API.deleteFlashcard(card.id);
            state.flashcards.splice(state.currentCardIndex, 1);
            if (state.currentCardIndex >= state.flashcards.length) {
                state.currentCardIndex = Math.max(0, state.flashcards.length - 1);
            }
            updateFlashcardBadgeCount();
            if (state.flashcards.length === 0) {
                DOM.emptyFlashcardState.classList.remove("hidden");
                DOM.flashcardDeckContainer.classList.add("hidden");
            } else {
                renderCurrentFlashcard();
            }
            showToast(`Đã xóa thẻ từ vựng "${deletedWord}"`, "info", 3000);
        } catch (e) {
            showToast("Lỗi khi xóa Flashcard: " + e.message, "error");
        }
    });

    // Khi người dùng chỉnh sửa từ vựng trong Modal -> Tự động cập nhật gợi ý nghĩa mới
    let wordLookupTimer = null;
    DOM.fcWordInput.addEventListener("input", (e) => {
        const newWord = e.target.value.trim();
        if (!newWord || newWord.length < 2) return;
        clearTimeout(wordLookupTimer);
        wordLookupTimer = setTimeout(async () => {
            DOM.meaningLoadingIndicator.classList.remove("hidden");
            try {
                const dictData = await API.lookupWord(newWord, DOM.fcSentenceInput.value);
                if (dictData && dictData.suggestions && dictData.suggestions.length > 0) {
                    DOM.meaningChipsContainer.innerHTML = "";
                    dictData.suggestions.forEach(suggestion => {
                        const chip = document.createElement("button");
                        chip.type = "button";
                        chip.className = "px-2.5 py-1 bg-indigo-50 hover:bg-indigo-600 hover:text-white text-indigo-700 text-xs font-semibold rounded-lg border border-indigo-200 hover:border-indigo-600 transition flex items-center space-x-1";
                        chip.innerHTML = `<span>${suggestion}</span>`;
                        chip.onclick = () => {
                            DOM.fcMeaningInput.value = suggestion;
                            DOM.fcMeaningInput.focus();
                        };
                        DOM.meaningChipsContainer.appendChild(chip);
                    });
                    DOM.meaningSuggestionsBox.classList.remove("hidden");
                }
            } catch (err) {
                console.warn(err);
            } finally {
                DOM.meaningLoadingIndicator.classList.add("hidden");
            }
        }, 400);
    });

    // Form thêm Flashcard
    DOM.saveFlashcardForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const payload = {
            word: DOM.fcWordInput.value.trim(),
            meaning: DOM.fcMeaningInput.value.trim(),
            context_sentence: DOM.fcSentenceInput.value.trim(),
            video_id: parseInt(DOM.fcVideoId.value),
            start_time: parseFloat(DOM.fcStartTime.value),
            end_time: parseFloat(DOM.fcEndTime.value)
        };

        try {
            const newCard = await API.createFlashcard(payload);
            state.flashcards.unshift(newCard);
            updateFlashcardBadgeCount();
            DOM.flashcardModal.classList.add("hidden");
            showToast(`Đã thêm từ "${payload.word}" vào bộ Flashcard thành công!`, "success", 3500);
        } catch (err) {
            showToast("Không thể lưu Flashcard: " + err.message, "error");
        }
    });

    // Modal đóng / mở
    const closeModal = (modal) => modal.classList.add("hidden");
    DOM.openUploadModalBtn.addEventListener("click", () => DOM.uploadModal.classList.remove("hidden"));
    DOM.placeholderUploadBtn.addEventListener("click", () => DOM.uploadModal.classList.remove("hidden"));
    DOM.closeUploadModalBtn.addEventListener("click", () => closeModal(DOM.uploadModal));
    document.querySelectorAll(".cancelModalBtn").forEach(btn => {
        btn.addEventListener("click", () => closeModal(DOM.uploadModal));
    });

    // Chuyển đổi giữa 2 tab trong Modal: Dán Link vs Tải File
    DOM.modalTabUrlBtn.addEventListener("click", () => {
        DOM.modalTabUrlBtn.className = "py-2 rounded-lg bg-white text-indigo-600 shadow-sm flex items-center justify-center space-x-1.5 transition";
        DOM.modalTabFileBtn.className = "py-2 rounded-lg text-slate-600 hover:text-slate-900 flex items-center justify-center space-x-1.5 transition";
        DOM.urlVideoForm.classList.remove("hidden");
        DOM.uploadVideoForm.classList.add("hidden");
    });

    DOM.modalTabFileBtn.addEventListener("click", () => {
        DOM.modalTabFileBtn.className = "py-2 rounded-lg bg-white text-indigo-600 shadow-sm flex items-center justify-center space-x-1.5 transition";
        DOM.modalTabUrlBtn.className = "py-2 rounded-lg text-slate-600 hover:text-slate-900 flex items-center justify-center space-x-1.5 transition";
        DOM.uploadVideoForm.classList.remove("hidden");
        DOM.urlVideoForm.classList.add("hidden");
    });

    DOM.closeFlashcardModalBtn.addEventListener("click", () => closeModal(DOM.flashcardModal));
    DOM.cancelFcBtn.addEventListener("click", () => closeModal(DOM.flashcardModal));

    DOM.closeReplayModalBtn.addEventListener("click", () => {
        DOM.replayVideo.pause();
        closeModal(DOM.videoReplayModal);
    });

    // Topic Discovery & Watch Modal Event Listeners
    if (DOM.closeWatchModalBtn) {
        DOM.closeWatchModalBtn.addEventListener("click", closeWatchVideoModal);
    }
    if (DOM.watchVideoModal) {
        DOM.watchVideoModal.addEventListener("click", (e) => {
            if (e.target === DOM.watchVideoModal) closeWatchVideoModal();
        });
    }
    if (DOM.backToMyVideosBtn) {
        DOM.backToMyVideosBtn.addEventListener("click", showMyVideosTab);
    }
    if (DOM.refreshTopicVideosBtn) {
        DOM.refreshTopicVideosBtn.addEventListener("click", () => {
            if (state.activeTab && typeof state.activeTab === "object") {
                loadAndRenderTopicVideos(state.activeTab);
            }
        });
    }
    if (DOM.openTopicVocabModalBtn) {
        DOM.openTopicVocabModalBtn.addEventListener("click", () => {
            if (state.activeTab && typeof state.activeTab === "object") {
                openTopicVocabModal(state.activeTab);
            } else if (state.topics && state.topics.length > 0) {
                openTopicVocabModal(state.topics[0]);
            } else {
                showToast("Vui lòng chọn một chủ đề IELTS", "info");
            }
        });
    }
    if (DOM.closeTopicVocabModalBtn) {
        DOM.closeTopicVocabModalBtn.addEventListener("click", () => {
            if (DOM.topicVocabModal) DOM.topicVocabModal.classList.add("hidden");
        });
    }
    if (DOM.topicVocabModal) {
        DOM.topicVocabModal.addEventListener("click", (e) => {
            if (e.target === DOM.topicVocabModal) {
                DOM.topicVocabModal.classList.add("hidden");
            }
        });
    }
    if (DOM.topicVocabFilterInput) {
        DOM.topicVocabFilterInput.addEventListener("input", (e) => {
            const q = (e.target.value || "").trim().toLowerCase();
            if (!state.currentTopicVocabs) return;
            if (!q) {
                renderTopicVocabCards(state.currentTopicVocabs);
            } else {
                const filtered = state.currentTopicVocabs.filter(item => 
                    (item.word && item.word.toLowerCase().includes(q)) ||
                    (item.meaning && item.meaning.toLowerCase().includes(q)) ||
                    (item.context_sentence && item.context_sentence.toLowerCase().includes(q))
                );
                renderTopicVocabCards(filtered);
            }
        });
    }
    if (DOM.saveAllTopicVocabBtn) {
        DOM.saveAllTopicVocabBtn.addEventListener("click", saveAllVisibleTopicVocabs);
    }
    if (DOM.generateAiVocabBtn) {
        DOM.generateAiVocabBtn.addEventListener("click", triggerGenerateAiVocab);
    }
    if (DOM.openAiKeySettingsBtn) {
        DOM.openAiKeySettingsBtn.addEventListener("click", openGeminiKeyModal);
    }
    if (DOM.closeGeminiKeyModalBtn) {
        DOM.closeGeminiKeyModalBtn.addEventListener("click", closeGeminiKeyModal);
    }
    if (DOM.cancelGeminiKeyBtn) {
        DOM.cancelGeminiKeyBtn.addEventListener("click", closeGeminiKeyModal);
    }
    if (DOM.saveGeminiKeyBtn) {
        DOM.saveGeminiKeyBtn.addEventListener("click", saveGeminiApiKeyFromModal);
    }
    if (DOM.geminiKeyModal) {
        DOM.geminiKeyModal.addEventListener("click", (e) => {
            if (e.target === DOM.geminiKeyModal) closeGeminiKeyModal();
        });
    }
    if (DOM.watchModalImportBtn) {
        DOM.watchModalImportBtn.addEventListener("click", () => {
            if (state.watchingVideo && state.activeTab) {
                const topicTitle = typeof state.activeTab === "object" ? state.activeTab.title : "General";
                triggerImportTopicVideo(state.watchingVideo, topicTitle);
            }
        });
    }
    if (DOM.watchModalDescBtn) {
        DOM.watchModalDescBtn.addEventListener("click", () => {
            if (state.watchingVideo) {
                openDescriptionVocabForOnlineVideo(state.watchingVideo);
            }
        });
    }
    if (DOM.watchModalInstantImportBtn) {
        DOM.watchModalInstantImportBtn.addEventListener("click", () => {
            if (state.watchingVideo) {
                const topicTitle = typeof state.activeTab === "object" ? state.activeTab.title : "General";
                triggerInstantImportOnlineVideo(state.watchingVideo, topicTitle);
                closeWatchVideoModal();
            }
        });
    }
    if (DOM.watchModalSearchBtn) {
        DOM.watchModalSearchBtn.addEventListener("click", () => {
            if (DOM.watchModalSearchInput) executeInVideoSearch(DOM.watchModalSearchInput.value);
        });
    }
    if (DOM.watchModalSearchInput) {
        DOM.watchModalSearchInput.addEventListener("keydown", (e) => {
            if (e.key === "Enter") {
                e.preventDefault();
                executeInVideoSearch(DOM.watchModalSearchInput.value);
            }
        });
    }

    // Dynamic YouTube Search in Topic Discovery
    if (DOM.youtubeSearchSubmitBtn) {
        DOM.youtubeSearchSubmitBtn.addEventListener("click", () => {
            if (DOM.youtubeSearchKeywordInput) searchYoutubeVideosOnline(DOM.youtubeSearchKeywordInput.value);
        });
    }
    if (DOM.youtubeSearchKeywordInput) {
        DOM.youtubeSearchKeywordInput.addEventListener("keydown", (e) => {
            if (e.key === "Enter") {
                e.preventDefault();
                searchYoutubeVideosOnline(DOM.youtubeSearchKeywordInput.value);
            }
        });
    }
    document.querySelectorAll(".yt-quick-tag").forEach(tag => {
        tag.addEventListener("click", () => {
            const query = tag.innerText.trim();
            if (DOM.youtubeSearchKeywordInput) DOM.youtubeSearchKeywordInput.value = query;
            searchYoutubeVideosOnline(query);
        });
    });

    // Radio switcher for Online (2s) vs Whisper in URL Modal
    document.querySelectorAll("input[name='urlImportMode']").forEach(radio => {
        radio.addEventListener("change", (e) => {
            const mode = e.target.value;
            if (mode === "online") {
                if (DOM.whisperModelFieldWrapper) DOM.whisperModelFieldWrapper.classList.add("hidden");
                if (DOM.submitUrlBtnText) DOM.submitUrlBtnText.innerText = "Thêm bài học Online (2s)";
            } else {
                if (DOM.whisperModelFieldWrapper) DOM.whisperModelFieldWrapper.classList.remove("hidden");
                if (DOM.submitUrlBtnText) DOM.submitUrlBtnText.innerText = "Tải về & Xử lý Whisper";
            }
        });
    });

    // Description Vocabulary Event Listeners
    if (DOM.openDescVocabModalBtn) {
        DOM.openDescVocabModalBtn.addEventListener("click", openDescriptionVocabModal);
    }
    if (DOM.quickDescVocabBtn) {
        DOM.quickDescVocabBtn.addEventListener("click", openDescriptionVocabModal);
    }
    if (DOM.closeDescVocabModalBtn) {
        DOM.closeDescVocabModalBtn.addEventListener("click", closeDescriptionVocabModal);
    }
    if (DOM.descVocabModal) {
        DOM.descVocabModal.addEventListener("click", (e) => {
            if (e.target === DOM.descVocabModal) closeDescriptionVocabModal();
        });
    }
    if (DOM.runScanDescBtn) {
        DOM.runScanDescBtn.addEventListener("click", executeDescriptionScan);
    }
    if (DOM.fetchDescFromYoutubeBtn) {
        DOM.fetchDescFromYoutubeBtn.addEventListener("click", async () => {
            const isOnline = state.activeScanningTarget && state.activeScanningTarget.type === "online";
            const target = isOnline ? state.activeScanningTarget.video : state.currentVideo;

            if (!target || (!target.source_url && !target.url && !target.id)) {
                showToast("Video này không có link YouTube gốc!", "warning");
                return;
            }
            showToast("Đang tải lại mô tả từ YouTube...", "info", 2000);
            try {
                if (isOnline) {
                    await openDescriptionVocabForOnlineVideo(target);
                } else {
                    const descData = await API.fetchVideoDescription(target.id);
                    if (descData && descData.description) {
                        DOM.descVocabTextarea.value = descData.description;
                        target.description = descData.description;
                        showToast("Đã cập nhật mô tả từ YouTube!", "success", 2500);
                        await executeDescriptionScan();
                    } else {
                        showToast("Không tìm thấy mô tả trên YouTube cho video này", "warning");
                    }
                }
            } catch (err) {
                showToast("Lỗi khi tải mô tả: " + err.message, "error");
            }
        });
    }
    if (DOM.fetchPinnedCommentBtn) {
        DOM.fetchPinnedCommentBtn.addEventListener("click", async () => {
            const isOnline = state.activeScanningTarget && state.activeScanningTarget.type === "online";
            const target = isOnline ? state.activeScanningTarget.video : state.currentVideo;

            let youtubeId = null;
            if (isOnline && target) {
                youtubeId = target.id;
            } else if (target && target.source_url) {
                const m = target.source_url.match(/(?:v=|\/v\/|youtu\.be\/|\/embed\/|\/shorts\/)([A-Za-z0-9_-]{11})/);
                if (m) youtubeId = m[1];
            } else if (target && target.filepath && target.filepath.includes("youtube.com/embed/")) {
                const m = target.filepath.match(/\/embed\/([A-Za-z0-9_-]{11})/);
                if (m) youtubeId = m[1];
            }

            if (!youtubeId) {
                showToast("Video này không có link YouTube để lấy bình luận!", "warning");
                return;
            }

            showToast("Đang tìm bình luận được ghim từ YouTube...", "info", 2000);
            try {
                const commentData = await API.fetchPinnedComment(youtubeId);
                const pinnedText = commentData.combined_text || commentData.pinned_comment || commentData.uploader_comment;

                if (pinnedText) {
                    const currentText = DOM.descVocabTextarea.value.trim();
                    const banner = `\n\n📌 [BÌNH LUẬN ĐƯỢC GHIM TỪ TÁC GIẢ]:\n${pinnedText}`;
                    DOM.descVocabTextarea.value = currentText ? `${currentText}${banner}` : pinnedText;

                    showToast("📌 Đã nạp bình luận được ghim! Đang dò từ vựng...", "success", 2500);
                    await executeDescriptionScan();
                } else {
                    showToast("Video này không có bình luận nào được ghim từ tác giả.", "warning", 3500);
                }
            } catch (err) {
                showToast("Lỗi khi lấy bình luận ghim: " + err.message, "error", 4000);
            }
        });
    }
    if (DOM.toggleDescExpandBtn) {
        DOM.toggleDescExpandBtn.addEventListener("click", () => {
            const isHidden = DOM.descInputContainer.classList.contains("hidden");
            if (isHidden) {
                DOM.descInputContainer.classList.remove("hidden");
                DOM.toggleDescExpandText.innerText = "Thu gọn";
                DOM.toggleDescExpandIcon.className = "fa-solid fa-chevron-up text-[10px]";
            } else {
                DOM.descInputContainer.classList.add("hidden");
                DOM.toggleDescExpandText.innerText = "Mở rộng";
                DOM.toggleDescExpandIcon.className = "fa-solid fa-chevron-down text-[10px]";
            }
        });
    }

    // Phím Escape để đóng tất cả các modal đang mở
    window.addEventListener("keydown", (e) => {
        if (e.key === "Escape") {
            closeWatchVideoModal();
            closeDescriptionVocabModal();
            closeModal(DOM.uploadModal);
            closeModal(DOM.flashcardModal);
            if (DOM.topicVocabModal) DOM.topicVocabModal.classList.add("hidden");
            closeGeminiKeyModal();
            DOM.replayVideo.pause();
            closeModal(DOM.videoReplayModal);
        }
    });

    // 1. Xử lý tải video tự động từ Link (URL / YouTube / TikTok...)
    DOM.urlVideoForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const url = DOM.videoUrlInput.value.trim();
        if (!url) {
            showToast("Vui lòng dán đường link video hợp lệ!", "warning");
            return;
        }

        const mode = document.querySelector("input[name='urlImportMode']:checked")?.value || "online";
        const title = DOM.videoUrlTitleInput.value.trim() || null;
        const topic = DOM.videoUrlTopicSelect ? DOM.videoUrlTopicSelect.value : null;

        // Bật trạng thái đang tải & disable button
        DOM.uploadProgressBox.classList.remove("hidden");
        DOM.submitUrlBtn.disabled = true;
        DOM.submitUrlBtn.classList.add("opacity-50");

        if (mode === "online") {
            DOM.progressStatusText.innerText = "Đang lấy phụ đề chính thức & lập chỉ mục từ vựng (khoảng 2 giây)...";
            try {
                const uploadedVideo = await API.importOnlineYoutubeVideo({
                    url_or_id: url,
                    title: title,
                    topic: topic
                });
                showToast(`🎉 Nạp bài học Online "${uploadedVideo.title}" thành công!`, "success", 4000);
                DOM.uploadModal.classList.add("hidden");
                DOM.urlVideoForm.reset();
                // Nạp lại danh sách video và tự động chọn video vừa nạp
                await loadVideos();
                switchTab("video");
                showMyVideosTab();
                selectVideo(uploadedVideo.id);
            } catch (err) {
                showToast("Lỗi khi nạp bài học online: " + err.message, "error", 5000);
            } finally {
                DOM.uploadProgressBox.classList.add("hidden");
                DOM.submitUrlBtn.disabled = false;
                DOM.submitUrlBtn.classList.remove("opacity-50");
            }
        } else {
            // Chế độ tải file MP4 về máy và phân tích bằng Whisper
            const payload = {
                url: url,
                title: title,
                topic: topic,
                model_name: DOM.whisperUrlModelSelect.value
            };

            DOM.progressStatusText.innerText = "Đang tải video từ link & Whisper đang trích xuất từng từ...";
            try {
                const uploadedVideo = await API.processVideoFromUrl(payload);
                showToast(`Tải và xử lý video "${uploadedVideo.title}" thành công!`, "success", 4000);
                DOM.uploadModal.classList.add("hidden");
                DOM.urlVideoForm.reset();
                // Nạp lại danh sách video và tự động chọn video vừa tải về
                await loadVideos();
                switchTab("video");
                showMyVideosTab();
                selectVideo(uploadedVideo.id);
            } catch (err) {
                showToast("Lỗi khi xử lý video từ link: " + err.message, "error", 5000);
            } finally {
                DOM.uploadProgressBox.classList.add("hidden");
                DOM.submitUrlBtn.disabled = false;
                DOM.submitUrlBtn.classList.remove("opacity-50");
            }
        }
    });

    // 2. Upload Video Form từ file máy tính
    DOM.uploadVideoForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const file = DOM.videoFileInput.files[0];
        if (!file) {
            showToast("Vui lòng chọn 1 file video!", "warning");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);
        formData.append("title", DOM.videoTitleInput.value.trim());
        formData.append("topic", DOM.videoTopicSelect ? DOM.videoTopicSelect.value : "");
        formData.append("model_name", DOM.whisperModelSelect.value);

        // Hiển thị trạng thái đang xử lý
        DOM.uploadProgressBox.classList.remove("hidden");
        DOM.progressStatusText.innerText = "Đang tải file lên & Whisper đang trích xuất từng từ...";
        DOM.submitUploadBtn.disabled = true;
        DOM.submitUploadBtn.classList.add("opacity-50");

        try {
            const uploadedVideo = await API.uploadVideo(formData);
            showToast(`Xử lý video "${uploadedVideo.title}" hoàn tất!`, "success", 4000);
            DOM.uploadModal.classList.add("hidden");
            DOM.uploadVideoForm.reset();
            // Nạp lại danh sách video và tự động chọn video vừa upload
            await loadVideos();
            selectVideo(uploadedVideo.id);
        } catch (err) {
            showToast("Lỗi khi xử lý video: " + err.message, "error", 5000);
        } finally {
            DOM.uploadProgressBox.classList.add("hidden");
            DOM.submitUploadBtn.disabled = false;
            DOM.submitUploadBtn.classList.remove("opacity-50");
        }
    });
}


// ==================== INITIALIZATION ====================
document.addEventListener("DOMContentLoaded", async () => {
    setupEventListeners();
    initTopicInfiniteScroll();
    await loadTopics();
    await loadVideos();
    // Tải trước số lượng flashcard để hiển thị badge
    try {
        state.flashcards = await API.fetchFlashcards();
        updateFlashcardBadgeCount();
    } catch (e) {
        console.warn("Chưa nạp được flashcard lúc khởi động:", e);
    }
});

