const API_BASE_URL = "http://127.0.0.1:8000";

// Existing system health API
export async function getSystemHealth() {
    try {
        const response = await fetch(
            `${API_BASE_URL}/api/system-health`
        );

        if (!response.ok) {
            throw new Error("Backend request failed");
        }

        return await response.json();

    } catch (error) {
        console.error("API Error:", error);
        return null;
    }
}


// SENTINEL AI Safety Assistant API
export async function sendChatMessage(question) {
    try {
        const response = await fetch(
            `${API_BASE_URL}/api/assistant/chat`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    question: question
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Assistant request failed"
            );
        }

        return data;

    } catch (error) {
        console.error("Assistant API Error:", error);
        throw error;
    }
}