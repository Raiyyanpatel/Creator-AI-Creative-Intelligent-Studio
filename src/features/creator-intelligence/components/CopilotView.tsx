import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ScrollView,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
} from "react-native";
import {
  GeneratedContent,
  CopilotMessage,
} from "../types/creatorIntelligence";
import { DraftPreview } from "./DraftPreview";

interface CopilotViewProps {
  draft: GeneratedContent;
  messages: CopilotMessage[];
  onSendMessage: (text: string) => void;
  onSwitchToFinal: () => void;
}

const QUICK_PROMPTS = [
  "Make it more controversial.",
  "Make the hook shorter.",
  "Use my usual style.",
  "Make it more cinematic.",
  "Add a stronger CTA.",
  "Turn this into a 30 second Reel.",
  "Make the second scene more visual.",
];

export const CopilotView: React.FC<CopilotViewProps> = ({
  draft,
  messages,
  onSendMessage,
  onSwitchToFinal,
}) => {
  const [inputText, setInputText] = useState("");

  const handleSend = () => {
    if (!inputText.trim()) return;
    onSendMessage(inputText);
    setInputText("");
  };

  const handlePromptChip = (chip: string) => {
    onSendMessage(chip);
  };

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === "ios" ? "padding" : "height"}
      style={styles.container}
    >
      <ScrollView
        style={styles.scrollArea}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* Workspace Subheader */}
        <View style={styles.workspaceHeader}>
          <Text style={styles.workspaceTitle}>AI Copilot Workspace</Text>
          <Text style={styles.workspaceSubtitle}>Let's build this together.</Text>
        </View>

        {/* Live Draft Preview Card */}
        <DraftPreview draft={draft} />

        {/* Quick Suggestion Chips */}
        <View style={styles.chipsSection}>
          <Text style={styles.chipsSectionTitle}>QUICK CREATIVE REVISIONS:</Text>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.chipsScroll}>
            {QUICK_PROMPTS.map((prompt, idx) => (
              <TouchableOpacity
                key={idx}
                style={styles.chipButton}
                onPress={() => handlePromptChip(prompt)}
                activeOpacity={0.75}
              >
                <Text style={styles.chipText}>{prompt}</Text>
              </TouchableOpacity>
            ))}
          </ScrollView>
        </View>

        {/* Chat Feed */}
        <View style={styles.messagesContainer}>
          {messages.map((msg) => {
            const isUser = msg.sender === "user";
            return (
              <View
                key={msg.id}
                style={[styles.messageWrapper, isUser ? styles.userWrapper : styles.aiWrapper]}
              >
                {!isUser && (
                  <View style={styles.aiSenderBadge}>
                    <Text style={styles.aiSenderIcon}>✨</Text>
                    <Text style={styles.aiSenderName}>Copilot Director</Text>
                  </View>
                )}

                <View style={[styles.bubble, isUser ? styles.userBubble : styles.aiBubble]}>
                  <Text style={[styles.messageText, isUser ? styles.userText : styles.aiText]}>
                    {msg.text}
                  </Text>
                </View>

                {/* Real-time Diff Box when changes were made */}
                {msg.changesMade && msg.changesMade.length > 0 && (
                  <View style={styles.changeCard}>
                    <View style={styles.changeCardHeader}>
                      <Text style={styles.changeCardIcon}>⚡</Text>
                      <Text style={styles.changeCardTitle}>CHANGE MADE TO DRAFT</Text>
                    </View>

                    {msg.changesMade.map((c, cIdx) => (
                      <View key={cIdx} style={styles.diffGroup}>
                        <Text style={styles.diffFieldLabel}>{c.field}:</Text>
                        <View style={styles.diffBefore}>
                          <Text style={styles.diffBeforeTag}>BEFORE</Text>
                          <Text style={styles.diffBeforeText}>"{c.before}"</Text>
                        </View>
                        <View style={styles.diffAfter}>
                          <Text style={styles.diffAfterTag}>AFTER</Text>
                          <Text style={styles.diffAfterText}>"{c.after}"</Text>
                        </View>
                      </View>
                    ))}

                    <View style={styles.appliedIndicator}>
                      <Text style={styles.appliedText}>
                        {msg.appliedSummary || "3 changes applied to draft"}
                      </Text>
                    </View>
                  </View>
                )}

                <Text style={styles.timestamp}>{msg.timestamp}</Text>
              </View>
            );
          })}
        </View>
      </ScrollView>

      {/* Switch to Final Plan Prompt */}
      <View style={styles.finalPromptBar}>
        <Text style={styles.finalPromptText}>Satisfied with the draft?</Text>
        <TouchableOpacity style={styles.viewFinalBtn} onPress={onSwitchToFinal} activeOpacity={0.8}>
          <Text style={styles.viewFinalBtnText}>View Final Plan →</Text>
        </TouchableOpacity>
      </View>

      {/* Input Bar */}
      <View style={styles.inputBar}>
        <TextInput
          style={styles.chatInput}
          placeholder="Ask Copilot (e.g. 'Make it more controversial')..."
          placeholderTextColor="#64748B"
          value={inputText}
          onChangeText={setInputText}
          multiline
        />
        <TouchableOpacity
          style={[styles.sendButton, !inputText.trim() && styles.sendButtonDisabled]}
          onPress={handleSend}
          disabled={!inputText.trim()}
          activeOpacity={0.8}
        >
          <Text style={styles.sendButtonText}>↑</Text>
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#0B1120",
  },
  scrollArea: {
    flex: 1,
  },
  scrollContent: {
    padding: 16,
    paddingBottom: 24,
  },
  workspaceHeader: {
    marginBottom: 12,
  },
  workspaceTitle: {
    fontSize: 20,
    fontWeight: "800",
    color: "#FFFFFF",
  },
  workspaceSubtitle: {
    fontSize: 13,
    color: "#94A3B8",
    marginTop: 2,
  },
  chipsSection: {
    marginBottom: 16,
  },
  chipsSectionTitle: {
    fontSize: 10,
    fontWeight: "700",
    color: "#64748B",
    letterSpacing: 0.5,
    marginBottom: 6,
  },
  chipsScroll: {
    flexDirection: "row",
  },
  chipButton: {
    backgroundColor: "#1E293B",
    borderWidth: 1,
    borderColor: "#334155",
    paddingHorizontal: 12,
    paddingVertical: 7,
    borderRadius: 20,
    marginRight: 8,
  },
  chipText: {
    color: "#CBD5E1",
    fontSize: 12,
    fontWeight: "500",
  },
  messagesContainer: {
    gap: 14,
  },
  messageWrapper: {
    marginBottom: 12,
    maxWidth: "88%",
  },
  userWrapper: {
    alignSelf: "flex-end",
  },
  aiWrapper: {
    alignSelf: "flex-start",
  },
  aiSenderBadge: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 4,
  },
  aiSenderIcon: {
    fontSize: 12,
    marginRight: 4,
  },
  aiSenderName: {
    fontSize: 11,
    fontWeight: "700",
    color: "#818CF8",
  },
  bubble: {
    paddingHorizontal: 14,
    paddingVertical: 10,
    borderRadius: 16,
  },
  userBubble: {
    backgroundColor: "#4F46E5",
    borderBottomRightRadius: 4,
  },
  aiBubble: {
    backgroundColor: "#1E293B",
    borderTopLeftRadius: 4,
    borderWidth: 1,
    borderColor: "#334155",
  },
  messageText: {
    fontSize: 14,
    lineHeight: 20,
  },
  userText: {
    color: "#FFFFFF",
  },
  aiText: {
    color: "#F1F5F9",
  },
  timestamp: {
    fontSize: 10,
    color: "#64748B",
    marginTop: 4,
    alignSelf: "flex-start",
  },
  changeCard: {
    backgroundColor: "#0F172A",
    borderRadius: 12,
    padding: 12,
    marginTop: 8,
    borderWidth: 1,
    borderColor: "#312E81",
  },
  changeCardHeader: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 8,
  },
  changeCardIcon: {
    fontSize: 12,
    marginRight: 5,
  },
  changeCardTitle: {
    fontSize: 10,
    fontWeight: "800",
    color: "#818CF8",
    letterSpacing: 0.6,
  },
  diffGroup: {
    marginBottom: 8,
  },
  diffFieldLabel: {
    fontSize: 11,
    fontWeight: "700",
    color: "#F8FAFC",
    marginBottom: 4,
  },
  diffBefore: {
    backgroundColor: "rgba(239, 68, 68, 0.1)",
    borderLeftWidth: 2,
    borderLeftColor: "#EF4444",
    padding: 6,
    borderRadius: 4,
    marginBottom: 4,
  },
  diffBeforeTag: {
    fontSize: 9,
    fontWeight: "800",
    color: "#F87171",
  },
  diffBeforeText: {
    fontSize: 12,
    color: "#FCA5A5",
    fontStyle: "italic",
  },
  diffAfter: {
    backgroundColor: "rgba(16, 185, 129, 0.1)",
    borderLeftWidth: 2,
    borderLeftColor: "#10B981",
    padding: 6,
    borderRadius: 4,
  },
  diffAfterTag: {
    fontSize: 9,
    fontWeight: "800",
    color: "#34D399",
  },
  diffAfterText: {
    fontSize: 12,
    color: "#A7F3D0",
    fontWeight: "600",
  },
  appliedIndicator: {
    flexDirection: "row",
    alignItems: "center",
    paddingTop: 6,
    borderTopWidth: 1,
    borderTopColor: "#1E293B",
  },
  appliedText: {
    fontSize: 11,
    color: "#10B981",
    fontWeight: "700",
  },
  finalPromptBar: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    backgroundColor: "#131C31",
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderTopWidth: 1,
    borderTopColor: "#1E293B",
  },
  finalPromptText: {
    color: "#94A3B8",
    fontSize: 12,
  },
  viewFinalBtn: {
    backgroundColor: "#312E81",
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: "#4F46E5",
  },
  viewFinalBtnText: {
    color: "#E0E7FF",
    fontSize: 12,
    fontWeight: "700",
  },
  inputBar: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 16,
    paddingVertical: 10,
    backgroundColor: "#0F172A",
    borderTopWidth: 1,
    borderTopColor: "#1E293B",
  },
  chatInput: {
    flex: 1,
    backgroundColor: "#1E293B",
    borderRadius: 20,
    paddingHorizontal: 14,
    paddingVertical: 8,
    color: "#FFFFFF",
    fontSize: 13,
    maxHeight: 80,
  },
  sendButton: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: "#4F46E5",
    alignItems: "center",
    justifyContent: "center",
    marginLeft: 10,
  },
  sendButtonDisabled: {
    backgroundColor: "#334155",
  },
  sendButtonText: {
    color: "#FFFFFF",
    fontSize: 18,
    fontWeight: "700",
  },
});
