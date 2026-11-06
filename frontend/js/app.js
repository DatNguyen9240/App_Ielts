/**
 * Smart Video Vocabulary & Flashcard App - Frontend Logic
 * Kết nối FastAPI Backend + HTML5 Video Seeking + 3D Flashcard Deck
 */

// ==================== STATE MANAGEMENT ====================
const state = {
    topics: [],
    selectedTopic: "all",
    videos: [],
    currentVideo: null,
    flashcards: [],
    currentCardIndex: 0,
    isCardFlipped: false,
    searchDebounceTimer: null,
};

// ==================== DOM ELEMENTS ====================
const DOM = {
    // Tabs
    tabVideoBtn: document.getElementById("tabVideoBtn"),
    tabFlashcardBtn: document.getElementById("tabFlashcardBtn"),
    tabVideoSection: document.getElementById("tabVideoSection"),
    tabFlashcardSection: document.getElementById("tabFlashcardSection"),
    flashcardCountBadge: document.getElementById("flashcardCountBadge"),

    // Topic Tabs & Selects
    topicTabsContainer: document.getElementById("topicTabsContainer"),
    activeTopicBadge: document.getElementById("activeTopicBadge"),
    videoUrlTopicSelect: document.getElementById("videoUrlTopicSelect"),
    videoTopicSelect: document.getElementById("videoTopicSelect"),

    // Video Player & Controls
    videoSelect: document.getElementById("videoSelect"),
    mainVideo: document.getElementById("mainVideo"),
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
    submitUrlBtn: document.getElementById("submitUrlBtn"),
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
};


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

    async fetchVideos(topic = null) {
        let url = `${API_BASE_URL}/api/videos`;
        if (topic && topic !== "all") {
            url += `?topic=${encodeURIComponent(topic)}`;
        }
        const res = await fetch(url);
        if (!res.ok) throw new Error("Không thể tải danh sách video");
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


// ==================== TOPIC TABS & FILTERING ====================

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
 * Hiển thị thanh tabs 16 chủ đề IELTS có đánh số
 */
function renderTopicTabs() {
    if (!DOM.topicTabsContainer) return;
    DOM.topicTabsContainer.innerHTML = "";

    // 1. Tab Tất cả
    const allTab = document.createElement("button");
    const isAllActive = state.selectedTopic === "all";
    allTab.className = `whitespace-nowrap px-3.5 py-1.5 rounded-xl text-xs font-bold transition flex items-center space-x-1.5 ${
        isAllActive 
            ? "bg-indigo-600 text-white shadow-md shadow-indigo-100" 
            : "bg-slate-100 hover:bg-slate-200 text-slate-700"
    }`;
    allTab.innerHTML = `<i class="fa-solid fa-sparkles text-[10px]"></i><span>Tất cả</span>`;
    allTab.onclick = () => selectTopicFilter("all");
    DOM.topicTabsContainer.appendChild(allTab);

    // 2. 16 Tabs chủ đề có đánh số
    state.topics.forEach(t => {
        const tabBtn = document.createElement("button");
        const isActive = state.selectedTopic === t.title;
        tabBtn.className = `whitespace-nowrap px-3 py-1.5 rounded-xl text-xs font-bold transition flex items-center space-x-1.5 ${
            isActive 
                ? "bg-indigo-600 text-white shadow-md shadow-indigo-100 ring-2 ring-indigo-300" 
                : "bg-slate-100 hover:bg-slate-200 text-slate-700"
        }`;
        // Hiển thị tiêu đề ngắn gọn có đánh số (ví dụ: "1. Work & Study")
        tabBtn.innerHTML = `<span>${t.id}. ${t.short_title}</span>`;
        tabBtn.title = t.title;
        tabBtn.onclick = () => selectTopicFilter(t.title);
        DOM.topicTabsContainer.appendChild(tabBtn);
    });
}

/**
 * Xử lý khi người dùng chọn 1 tab chủ đề -> Lọc video liên quan đến chủ đề đó
 */
async function selectTopicFilter(topicTitle) {
    state.selectedTopic = topicTitle;
    renderTopicTabs();

    // Đồng bộ chủ đề được chọn vào các modal upload
    if (topicTitle !== "all") {
        if (DOM.videoUrlTopicSelect) DOM.videoUrlTopicSelect.value = topicTitle;
        if (DOM.videoTopicSelect) DOM.videoTopicSelect.value = topicTitle;
    }

    // Lọc và tải lại danh sách video theo chủ đề này
    await loadVideos(topicTitle);
}


// ==================== VIDEO PLAYER & SEARCH LOGIC ====================

/**
 * Tải danh sách video và cập nhật dropdown theo chủ đề được chọn
 */
async function loadVideos(topic = null) {
    const filterTopic = topic || state.selectedTopic;
    try {
        state.videos = await API.fetchVideos(filterTopic);
        DOM.videoSelect.innerHTML = "";

        // Cập nhật badge hiển thị chủ đề hiện tại
        if (DOM.activeTopicBadge) {
            const topicText = filterTopic === "all" ? "Tất cả chủ đề" : filterTopic;
            DOM.activeTopicBadge.innerText = `${topicText} (${state.videos.length} video)`;
        }

        if (state.videos.length === 0) {
            const label = filterTopic === "all" ? "Chưa có video nào" : `Chưa có video nào thuộc "${filterTopic}"`;
            DOM.videoSelect.innerHTML = `<option value="">-- ${label} (Hãy thêm video) --</option>`;
            DOM.videoPlaceholder.classList.remove("hidden");
            DOM.videoTitleDisplay.innerText = "Tiêu đề: Chưa có video";
            DOM.currentTimeDisplay.innerText = "00:00.0";
            DOM.totalDurationDisplay.innerText = "00:00.0";
            DOM.mainVideo.removeAttribute("src");
            DOM.mainVideo.load();
            return;
        }

        state.videos.forEach(vid => {
            const opt = document.createElement("option");
            opt.value = vid.id;
            opt.textContent = `[${vid.topic || 'General'}] ${vid.title} (${Math.round(vid.duration)}s)`;
            DOM.videoSelect.appendChild(opt);
        });

        // Tự động chọn video đầu tiên của chủ đề
        selectVideo(state.videos[0].id);
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

    // Gán src cho HTML5 Video player (FastAPI StaticFiles phục vụ /uploads/...)
    const fullVideoUrl = vid.filepath.startsWith("http") ? vid.filepath : `${API_BASE_URL}${vid.filepath}`;
    DOM.mainVideo.src = fullVideoUrl;
    DOM.mainVideo.load();

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
    if (!DOM.mainVideo.src) return;
    
    // Đảm bảo thời gian hợp lệ
    const targetTime = Math.max(0, parseFloat(timeInSeconds));
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
        } catch (e) {
            alert("Lỗi khi cập nhật trạng thái thẻ");
        }
    });

    // Xóa thẻ Flashcard
    DOM.deleteCardBtn.addEventListener("click", async () => {
        if (state.flashcards.length === 0) return;
        const card = state.flashcards[state.currentCardIndex];
        if (!confirm(`Bạn có chắc muốn xóa thẻ "${card.word}"?`)) return;

        try {
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
        } catch (e) {
            alert("Lỗi khi xóa Flashcard");
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
            alert(`Đã thêm từ "${payload.word}" vào bộ Flashcard thành công!`);
        } catch (err) {
            alert("Không thể lưu Flashcard: " + err.message);
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

    // 1. Xử lý tải video tự động từ Link (URL / YouTube / TikTok...)
    DOM.urlVideoForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const url = DOM.videoUrlInput.value.trim();
        if (!url) {
            alert("Vui lòng dán đường link video hợp lệ!");
            return;
        }

        const payload = {
            url: url,
            title: DOM.videoUrlTitleInput.value.trim() || null,
            topic: DOM.videoUrlTopicSelect ? DOM.videoUrlTopicSelect.value : null,
            model_name: DOM.whisperUrlModelSelect.value
        };

        // Bật trạng thái đang tải & disable button
        DOM.uploadProgressBox.classList.remove("hidden");
        DOM.progressStatusText.innerText = "Đang tải video từ link & Whisper đang trích xuất từng từ...";
        DOM.submitUrlBtn.disabled = true;
        DOM.submitUrlBtn.classList.add("opacity-50");

        try {
            const uploadedVideo = await API.processVideoFromUrl(payload);
            alert(`Tải và xử lý video "${uploadedVideo.title}" thành công!`);
            DOM.uploadModal.classList.add("hidden");
            DOM.urlVideoForm.reset();
            // Nạp lại danh sách video và tự động chọn video vừa tải về
            await loadVideos();
            selectVideo(uploadedVideo.id);
        } catch (err) {
            alert("Lỗi khi xử lý video từ link: " + err.message);
        } finally {
            DOM.uploadProgressBox.classList.add("hidden");
            DOM.submitUrlBtn.disabled = false;
            DOM.submitUrlBtn.classList.remove("opacity-50");
        }
    });

    // 2. Upload Video Form từ file máy tính
    DOM.uploadVideoForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const file = DOM.videoFileInput.files[0];
        if (!file) {
            alert("Vui lòng chọn 1 file video!");
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
            alert(`Xử lý video "${uploadedVideo.title}" hoàn tất!`);
            DOM.uploadModal.classList.add("hidden");
            DOM.uploadVideoForm.reset();
            // Nạp lại danh sách video và tự động chọn video vừa upload
            await loadVideos();
            selectVideo(uploadedVideo.id);
        } catch (err) {
            alert("Lỗi khi xử lý video: " + err.message);
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

