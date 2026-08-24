import { useEffect, useRef, useState } from "react";
import {
    View,
    Text,
    TextInput,
    TouchableOpacity,
    ScrollView,
    StyleSheet,
    KeyboardAvoidingView,
    Platform,
    SafeAreaView,
} from "react-native";

const API_BASE_URL = "http://SEU_IP:5000";

type Message = {
    id: string;
    text: string;
    role: "user" | "assistant";
    alert?: boolean;
};

function isAlertMessage(text: string) {
    const lowered = text.toLowerCase();
    return lowered.includes("samu") || lowered.includes("emergência") || lowered.includes("192");
}

export default function ChatScreen() {
    const [sessionId, setSessionId] = useState<string | null>(null);
    const [messages, setMessages] = useState<Message[]>([]);
    const [inputText, setInputText] = useState("");
    const [loading, setLoading] = useState(false);
    const [connected, setConnected] = useState(false);

    const scrollRef = useRef<ScrollView>(null);

    useEffect(() => {
        startSession();
    }, []);

    async function startSession() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/session`, { method: "POST" });
            const data = await response.json();
            setSessionId(data.session_id);
            setConnected(true);
            addMessage(
                "Olá! Eu sou um assistente de triagem inicial de sintomas cardíacos. Descreva o que você está sentindo para começar.",
                "assistant"
            );
        } catch (error) {
            console.error(error);
            setConnected(false);
        }
    }

    function addMessage(text: string, role: "user" | "assistant") {

        setMessages((prev) => [
            ...prev,
            {
                id: Date.now().toString() + Math.random(),
                text,
                role,
                alert: role === "assistant" && isAlertMessage(text),
            },
        ]);
    }

    async function handleSend() {
        const text = inputText.trim();
        if (!text || !sessionId) return;

        addMessage(text, "user");
        setInputText("");
        setLoading(true);

        try {
            const response = await fetch(`${API_BASE_URL}/api/message`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ session_id: sessionId, text }),
            });
            const data = await response.json();

            if (!response.ok) {
                addMessage(data.error || "Ocorreu um erro.", "assistant");
            } else {
                const replies: string[] = data.replies || [];
                if (replies.length === 0) {
                    addMessage("Não entendi. Pode reformular?", "assistant");
                } else {
                    replies.forEach((reply) => addMessage(reply, "assistant"));
                }
            }
        } catch (error) {
            console.error(error);
            addMessage("Erro de conexão com o servidor.", "assistant");
        } finally {
            setLoading(false);
        }
    }

    return (
        <SafeAreaView style={styles.safeArea}>
            <KeyboardAvoidingView
                style={styles.flex}
                behavior={Platform.OS === "ios" ? "padding" : undefined}
            >
                <View style={styles.header}>
                    <Text style={styles.headerTitle}>Assistente Cardiológico</Text>
                    <Text style={styles.headerSubtitle}>
                        Triagem inicial de sintomas — não substitui avaliação médica
                    </Text>
                </View>

                <ScrollView
                    ref={scrollRef}
                    style={styles.chatWindow}
                    contentContainerStyle={styles.chatContent}
                    onContentSizeChange={() => scrollRef.current?.scrollToEnd({ animated: true })}
                >
                    {!connected && messages.length === 0 && (
                        <Text style={styles.emptyText}>
                            Não foi possível conectar ao assistente. Confirme se o backend está rodando e se o
                            IP está certo.
                        </Text>
                    )}


                    {messages.map((message) => (
                        <View
                            key={message.id}
                            style={[
                                styles.bubble,
                                message.role === "user" ? styles.bubbleUser : styles.bubbleAssistant,
                                message.alert && styles.bubbleAlert,
                            ]}
                        >
                            <Text
                                style={[
                                    styles.bubbleText,
                                    message.role === "user" && styles.bubbleTextUser,
                                    message.alert && styles.bubbleTextAlert,
                                ]}
                            >
                                {message.text}
                            </Text>
                        </View>
                    ))}

                    {loading && <Text style={styles.pendingText}>Digitando…</Text>}
                </ScrollView>

                <View style={styles.composer}>
                    <TextInput
                        style={styles.input}
                        placeholder="Descreva o que você está sentindo…"
                        value={inputText}
                        onChangeText={setInputText}
                        editable={connected}
                    />
                    <TouchableOpacity
                        style={[styles.sendButton, !connected && styles.sendButtonDisabled]}
                        onPress={handleSend}
                        disabled={!connected}
                    >
                        <Text style={styles.sendButtonText}>➤</Text>
                    </TouchableOpacity>
                </View>

                <Text style={styles.disclaimer}>
                    Em caso de emergência, ligue imediatamente para o SAMU (192).
                </Text>
            </KeyboardAvoidingView>
        </SafeAreaView>
    );
}


const styles = StyleSheet.create({
    safeArea: { flex: 1, backgroundColor: "#FFFFFF" },
    flex: { flex: 1 },
    header: {
        backgroundColor: "#0B3D3D",
        paddingHorizontal: 20,
        paddingTop: 16,
        paddingBottom: 16,
    },
    headerTitle: { color: "#FFFFFF", fontSize: 20, fontWeight: "600" },
    headerSubtitle: { color: "rgba(255,255,255,0.7)", fontSize: 12, marginTop: 4 },
    chatWindow: { flex: 1, backgroundColor: "#F1F5F6" },
    chatContent: { padding: 16 },
    emptyText: { textAlign: "center", color: "#5B6E70", marginTop: 40 },
    bubble: {
        maxWidth: "82%",
        padding: 12,
        borderRadius: 14,
        marginBottom: 10,
    },
    bubbleAssistant: {
        alignSelf: "flex-start",
        backgroundColor: "#E1F0EF",
        borderWidth: 1,
        borderColor: "#DCE6E6",
    },
    bubbleUser: {
        alignSelf: "flex-end",
        backgroundColor: "#0E6E6E",
    },
    bubbleAlert: {
        backgroundColor: "#FBEAE6",
        borderColor: "#E4572E",
    },
    bubbleText: { fontSize: 15, color: "#1B2A2E", lineHeight: 20 },
    bubbleTextUser: { color: "#FFFFFF" },
    bubbleTextAlert: { color: "#8A3216", fontWeight: "500" },
    pendingText: { color: "#5B6E70", fontStyle: "italic", marginLeft: 4 },
    composer: {
        flexDirection: "row",
        padding: 16,
        gap: 10,
        borderTopWidth: 1,
        borderTopColor: "#DCE6E6",
    },
    input: {
        flex: 1,
        borderWidth: 1,
        borderColor: "#DCE6E6",
        borderRadius: 999,
        paddingHorizontal: 18,
        paddingVertical: 10,
        fontSize: 15,
    },
    sendButton: {
        width: 44,
        height: 44,
        borderRadius: 22,
        backgroundColor: "#0E6E6E",
        alignItems: "center",
        justifyContent: "center",
    },
    sendButtonDisabled: { backgroundColor: "#B7C6C6" },
    sendButtonText: { color: "#FFFFFF", fontSize: 18 },
    disclaimer: {
        textAlign: "center",
        fontSize: 12,
        color: "#5B6E70",
        paddingBottom: 12,
        paddingHorizontal: 20,
    },
});
