import React, { useState } from "react";
import {
  Modal,
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  SafeAreaView,
  ActivityIndicator,
  Image,
} from "react-native";
import {
  useCreatorIntelligenceStore,
} from "../state/creatorIntelligenceStore";
import {
  GenerationContentType,
  GenerationDuration,
  GenerationTone,
} from "../types/creatorIntelligence";
import { CopilotView } from "../components/CopilotView";
import { FinalView } from "../components/FinalView";

interface GenerateContentScreenProps {
  visible: boolean;
  onClose: () => void;
}

const CONTENT_TYPES: { id: GenerationContentType; label: string; icon: string }[] = [
  { id: "reel", label: "Reel", icon: "📸" },
  { id: "short_video", label: "Short Video", icon: "⚡" },
  { id: "youtube_video", label: "YouTube Video", icon: "▶" },
  { id: "linkedin_post", label: "LinkedIn Post", icon: "💼" },
  { id: "podcast", label: "Podcast", icon: "🎙️" },
  { id: "thread", label: "Thread", icon: "🧵" },
];

const DURATIONS: { id: GenerationDuration; label: string }[] = [
  { id: "30_sec", label: "30 sec" },
  { id: "60_sec", label: "60 sec" },
  { id: "90_sec", label: "90 sec" },
  { id: "custom", label: "Custom" },
];

const TONES: { id: GenerationTone; label: string; icon: string }[] = [
  { id: "creators_style", label: "Creator's Style", icon: "✨" },
  { id: "educational", label: "Educational", icon: "🎓" },
  { id: "energetic", label: "Energetic", icon: "🔥" },
  { id: "cinematic", label: "Cinematic", icon: "🎬" },
  { id: "conversational", label: "Conversational", icon: "💬" },
];

export const GenerateContentScreen: React.FC<GenerateContentScreenProps> = ({
  visible,
  onClose,
}) => {
  const {
    storyboardItems,
    generationInput,
    generationLoading,
    generatedDraft,
    activeGenerateTab,
    copilotMessages,
    setGenerationInput,
    setActiveGenerateTab,
    triggerGeneration,
    sendCopilotMessage,
    saveDraftToProject,
  } = useCreatorIntelligenceStore();

  const [loadingStepText, setLoadingStepText] = useState("Analyzing references...");

  const handleStartGeneration = () => {
    setLoadingStepText("Synthesizing references into hook angles...");
    setTimeout(() => {
      setLoadingStepText("Scripting scene breakdown and visual direction...");
    }, 600);
    triggerGeneration();
  };

  return (
    <Modal
      visible={visible}
      animationType="slide"
      presentationStyle="fullScreen"
      onRequestClose={onClose}
    >
      <SafeAreaView style={styles.safeContainer}>
        {/* Top App Header */}
        <View style={styles.topBar}>
          <TouchableOpacity onPress={onClose} style={styles.closeBtn} activeOpacity={0.7}>
            <Text style={styles.closeBtnText}>← Close</Text>
          </TouchableOpacity>

          <View style={styles.headerTitleBox}>
            <Text style={styles.headerMainTitle}>Generate Content</Text>
            <Text style={styles.headerSubtitle}>
              Turn your research into something worth creating.
            </Text>
          </View>

          <View style={styles.placeholderBox} />
        </View>

        {/* LOADING STATE */}
        {generationLoading && (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color="#6366F1" />
            <Text style={styles.loadingTitle}>Creator AI Studio</Text>
            <Text style={styles.loadingStep}>{loadingStepText}</Text>
            <Text style={styles.loadingHelper}>
              Synthesizing hook psychology, viral retention pacing, and visual B-roll specs...
            </Text>
          </View>
        )}

        {/* SETUP PHASE (When no draft has been generated yet) */}
        {!generationLoading && !generatedDraft && (
          <ScrollView
            style={styles.setupScroll}
            contentContainerStyle={styles.setupContent}
            showsVerticalScrollIndicator={false}
          >
            {/* Selected References Overview */}
            <View style={styles.section}>
              <View style={styles.sectionHeaderRow}>
                <Text style={styles.sectionTitle}>1. SELECTED STORYBOARD REFERENCES</Text>
                <Text style={styles.refCountText}>{storyboardItems.length} Captured</Text>
              </View>

              <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.refScroll}>
                {storyboardItems.map((item) => (
                  <View key={item.id} style={styles.refCard}>
                    <Image source={{ uri: item.content.thumbnail }} style={styles.refThumb} />
                    <View style={styles.refInfo}>
                      <Text style={styles.refTitle} numberOfLines={2}>
                        {item.content.title}
                      </Text>
                      <Text style={styles.refCreator}>By {item.content.creatorName}</Text>
                    </View>
                  </View>
                ))}
              </ScrollView>
            </View>

            {/* Content Type Picker */}
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>2. CHOOSE CONTENT FORMAT</Text>
              <View style={styles.gridOptions}>
                {CONTENT_TYPES.map((type) => {
                  const isSelected = generationInput.contentType === type.id;
                  return (
                    <TouchableOpacity
                      key={type.id}
                      style={[styles.gridCard, isSelected && styles.gridCardSelected]}
                      onPress={() => setGenerationInput({ contentType: type.id })}
                      activeOpacity={0.8}
                    >
                      <Text style={styles.gridCardIcon}>{type.icon}</Text>
                      <Text style={[styles.gridCardText, isSelected && styles.gridCardTextSelected]}>
                        {type.label}
                      </Text>
                    </TouchableOpacity>
                  );
                })}
              </View>
            </View>

            {/* Duration Picker */}
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>3. TARGET DURATION</Text>
              <View style={styles.rowOptions}>
                {DURATIONS.map((dur) => {
                  const isSelected = generationInput.duration === dur.id;
                  return (
                    <TouchableOpacity
                      key={dur.id}
                      style={[styles.pillCard, isSelected && styles.pillCardSelected]}
                      onPress={() => setGenerationInput({ duration: dur.id })}
                      activeOpacity={0.8}
                    >
                      <Text style={[styles.pillCardText, isSelected && styles.pillCardTextSelected]}>
                        {dur.label}
                      </Text>
                    </TouchableOpacity>
                  );
                })}
              </View>
            </View>

            {/* Tone Picker */}
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>4. VOCAL TONE & DELIVERY CADENCE</Text>
              <View style={styles.gridOptions}>
                {TONES.map((tone) => {
                  const isSelected = generationInput.tone === tone.id;
                  return (
                    <TouchableOpacity
                      key={tone.id}
                      style={[styles.gridCard, isSelected && styles.gridCardSelected]}
                      onPress={() => setGenerationInput({ tone: tone.id })}
                      activeOpacity={0.8}
                    >
                      <Text style={styles.gridCardIcon}>{tone.icon}</Text>
                      <Text style={[styles.gridCardText, isSelected && styles.gridCardTextSelected]}>
                        {tone.label}
                      </Text>
                    </TouchableOpacity>
                  );
                })}
              </View>
            </View>

            {/* Generate Action Button */}
            <TouchableOpacity
              style={styles.primaryGenerateBtn}
              onPress={handleStartGeneration}
              activeOpacity={0.85}
            >
              <Text style={styles.primaryGenerateIcon}>⚡</Text>
              <Text style={styles.primaryGenerateText}>Generate Content Plan</Text>
            </TouchableOpacity>
          </ScrollView>
        )}

        {/* WORKSPACE PHASE (Draft exists: TWO TABS [AI COPILOT] and [FINAL]) */}
        {!generationLoading && generatedDraft && (
          <View style={styles.workspaceContainer}>
            {/* Two Tabs at Top */}
            <View style={styles.twoTabsBar}>
              <TouchableOpacity
                style={[styles.tabButton, activeGenerateTab === "copilot" && styles.tabButtonActive]}
                onPress={() => setActiveGenerateTab("copilot")}
                activeOpacity={0.8}
              >
                <Text style={styles.tabIcon}>🤖</Text>
                <Text
                  style={[
                    styles.tabButtonText,
                    activeGenerateTab === "copilot" && styles.tabButtonTextActive,
                  ]}
                >
                  AI COPILOT
                </Text>
                {activeGenerateTab === "copilot" && <View style={styles.activeTabIndicator} />}
              </TouchableOpacity>

              <TouchableOpacity
                style={[styles.tabButton, activeGenerateTab === "final" && styles.tabButtonActive]}
                onPress={() => setActiveGenerateTab("final")}
                activeOpacity={0.8}
              >
                <Text style={styles.tabIcon}>📄</Text>
                <Text
                  style={[
                    styles.tabButtonText,
                    activeGenerateTab === "final" && styles.tabButtonTextActive,
                  ]}
                >
                  FINAL
                </Text>
                {activeGenerateTab === "final" && <View style={styles.activeTabIndicator} />}
              </TouchableOpacity>
            </View>

            {/* Tab 1: AI Copilot */}
            {activeGenerateTab === "copilot" && (
              <CopilotView
                draft={generatedDraft}
                messages={copilotMessages}
                onSendMessage={sendCopilotMessage}
                onSwitchToFinal={() => setActiveGenerateTab("final")}
              />
            )}

            {/* Tab 2: Final Content Plan */}
            {activeGenerateTab === "final" && (
              <FinalView
                draft={generatedDraft}
                onEdit={() => setActiveGenerateTab("copilot")}
                onRegenerate={handleStartGeneration}
                onSaveToProject={saveDraftToProject}
              />
            )}
          </View>
        )}
      </SafeAreaView>
    </Modal>
  );
};

const styles = StyleSheet.create({
  safeContainer: {
    flex: 1,
    backgroundColor: "#0B1120",
  },
  topBar: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: "#1E293B",
  },
  closeBtn: {
    paddingVertical: 6,
    paddingHorizontal: 8,
  },
  closeBtnText: {
    color: "#818CF8",
    fontSize: 14,
    fontWeight: "700",
  },
  headerTitleBox: {
    alignItems: "center",
  },
  headerMainTitle: {
    fontSize: 16,
    fontWeight: "800",
    color: "#FFFFFF",
  },
  headerSubtitle: {
    fontSize: 11,
    color: "#94A3B8",
    marginTop: 2,
  },
  placeholderBox: {
    width: 40,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    padding: 30,
  },
  loadingTitle: {
    fontSize: 20,
    fontWeight: "800",
    color: "#FFFFFF",
    marginTop: 18,
    marginBottom: 6,
  },
  loadingStep: {
    fontSize: 14,
    color: "#10B981",
    fontWeight: "700",
    marginBottom: 10,
  },
  loadingHelper: {
    fontSize: 12,
    color: "#64748B",
    textAlign: "center",
    lineHeight: 18,
  },
  setupScroll: {
    flex: 1,
  },
  setupContent: {
    padding: 20,
    paddingBottom: 40,
  },
  section: {
    marginBottom: 22,
  },
  sectionHeaderRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 10,
  },
  sectionTitle: {
    fontSize: 11,
    fontWeight: "800",
    color: "#94A3B8",
    letterSpacing: 0.8,
    marginBottom: 10,
  },
  refCountText: {
    fontSize: 11,
    color: "#818CF8",
    fontWeight: "700",
  },
  refScroll: {
    flexDirection: "row",
  },
  refCard: {
    width: 200,
    flexDirection: "row",
    backgroundColor: "#131C31",
    borderRadius: 12,
    padding: 8,
    marginRight: 10,
    borderWidth: 1,
    borderColor: "#1E293B",
    alignItems: "center",
  },
  refThumb: {
    width: 48,
    height: 48,
    borderRadius: 6,
    marginRight: 8,
    backgroundColor: "#1E293B",
  },
  refInfo: {
    flex: 1,
  },
  refTitle: {
    fontSize: 11,
    fontWeight: "700",
    color: "#FFFFFF",
    lineHeight: 15,
  },
  refCreator: {
    fontSize: 10,
    color: "#64748B",
    marginTop: 2,
  },
  gridOptions: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 10,
  },
  gridCard: {
    width: "48%",
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#0F172A",
    borderRadius: 12,
    padding: 12,
    borderWidth: 1,
    borderColor: "#1E293B",
  },
  gridCardSelected: {
    backgroundColor: "#312E81",
    borderColor: "#6366F1",
  },
  gridCardIcon: {
    fontSize: 16,
    marginRight: 8,
  },
  gridCardText: {
    fontSize: 13,
    color: "#CBD5E1",
    fontWeight: "600",
  },
  gridCardTextSelected: {
    color: "#FFFFFF",
    fontWeight: "700",
  },
  rowOptions: {
    flexDirection: "row",
    gap: 8,
  },
  pillCard: {
    flex: 1,
    backgroundColor: "#0F172A",
    borderRadius: 10,
    paddingVertical: 10,
    alignItems: "center",
    borderWidth: 1,
    borderColor: "#1E293B",
  },
  pillCardSelected: {
    backgroundColor: "#4F46E5",
    borderColor: "#6366F1",
  },
  pillCardText: {
    fontSize: 12,
    fontWeight: "600",
    color: "#94A3B8",
  },
  pillCardTextSelected: {
    color: "#FFFFFF",
    fontWeight: "700",
  },
  primaryGenerateBtn: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#4F46E5",
    paddingVertical: 16,
    borderRadius: 16,
    marginTop: 10,
    shadowColor: "#4F46E5",
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.4,
    shadowRadius: 10,
    elevation: 6,
  },
  primaryGenerateIcon: {
    fontSize: 18,
    marginRight: 8,
  },
  primaryGenerateText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "800",
  },
  workspaceContainer: {
    flex: 1,
  },
  twoTabsBar: {
    flexDirection: "row",
    backgroundColor: "#0F172A",
    borderBottomWidth: 1,
    borderBottomColor: "#1E293B",
  },
  tabButton: {
    flex: 1,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    paddingVertical: 14,
    position: "relative",
  },
  tabButtonActive: {
    backgroundColor: "#131C31",
  },
  tabIcon: {
    fontSize: 13,
    marginRight: 6,
  },
  tabButtonText: {
    fontSize: 13,
    fontWeight: "700",
    color: "#64748B",
    letterSpacing: 0.5,
  },
  tabButtonTextActive: {
    color: "#818CF8",
  },
  activeTabIndicator: {
    position: "absolute",
    bottom: 0,
    left: 20,
    right: 20,
    height: 3,
    backgroundColor: "#6366F1",
    borderRadius: 1.5,
  },
});
