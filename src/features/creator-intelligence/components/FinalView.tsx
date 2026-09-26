import React from "react";
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
} from "react-native";
import { GeneratedContent } from "../types/creatorIntelligence";

interface FinalViewProps {
  draft: GeneratedContent;
  onEdit: () => void;
  onRegenerate: () => void;
  onSaveToProject: () => void;
}

export const FinalView: React.FC<FinalViewProps> = ({
  draft,
  onEdit,
  onRegenerate,
  onSaveToProject,
}) => {
  return (
    <View style={styles.container}>
      <ScrollView
        style={styles.scrollArea}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* Document Header */}
        <View style={styles.header}>
          <View style={styles.docBadge}>
            <Text style={styles.docBadgeText}>STRUCTURED CONTENT BLUEPRINT</Text>
          </View>
          <Text style={styles.docTitle}>Your Content Plan</Text>
          <Text style={styles.docSubtitle}>
            Engineered for {draft.targetPlatform} • Projected {draft.estimatedRetention}
          </Text>
        </View>

        {/* 1. CONTENT IDEA */}
        <View style={styles.sectionCard}>
          <Text style={styles.sectionNum}>1. CONTENT IDEA</Text>
          <Text style={styles.ideaTitle}>{draft.title}</Text>
          <View style={styles.tagRow}>
            <View style={styles.tag}>
              <Text style={styles.tagText}>{draft.targetPlatform}</Text>
            </View>
            <View style={styles.tag}>
              <Text style={styles.tagText}>Version {draft.version}.0</Text>
            </View>
          </View>
        </View>

        {/* 2. HOOK */}
        <View style={styles.sectionCard}>
          <Text style={styles.sectionNum}>2. OPENING HOOK (0–3s)</Text>
          <View style={styles.hookBox}>
            <Text style={styles.hookQuote}>"{draft.hook}"</Text>
          </View>
        </View>

        {/* 3. CORE MESSAGE */}
        <View style={styles.sectionCard}>
          <Text style={styles.sectionNum}>3. CORE MESSAGE</Text>
          <Text style={styles.bodyText}>{draft.coreMessage}</Text>
        </View>

        {/* 4. SCRIPT */}
        <View style={styles.sectionCard}>
          <Text style={styles.sectionNum}>4. VERBATIM SCRIPT</Text>
          <View style={styles.scriptContainer}>
            <Text style={styles.scriptText}>{draft.script}</Text>
          </View>
        </View>

        {/* 5. STORYBOARD SCENES */}
        <View style={styles.sectionCard}>
          <Text style={styles.sectionNum}>5. SCENE-BY-SCENE STORYBOARD</Text>
          {draft.scenes.map((scene) => (
            <View key={scene.id} style={styles.sceneCard}>
              <View style={styles.sceneHeader}>
                <Text style={styles.sceneNumber}>SCENE {scene.sceneNumber}</Text>
                <View style={styles.sceneDurationBadge}>
                  <Text style={styles.sceneDurationText}>{scene.duration}</Text>
                </View>
              </View>

              <View style={styles.sceneRow}>
                <Text style={styles.sceneFieldLabel}>VISUAL:</Text>
                <Text style={styles.sceneFieldValue}>{scene.visual}</Text>
              </View>

              <View style={styles.sceneRow}>
                <Text style={styles.sceneFieldLabel}>DIALOGUE:</Text>
                <Text style={styles.sceneDialogueValue}>"{scene.dialogue}"</Text>
              </View>

              <View style={styles.sceneTechRow}>
                <Text style={styles.sceneTechText}>🎥 {scene.camera}</Text>
                <Text style={styles.sceneTechText}>🔄 {scene.movement}</Text>
              </View>
            </View>
          ))}
        </View>

        {/* 6. VISUAL DIRECTION */}
        <View style={styles.sectionCard}>
          <Text style={styles.sectionNum}>6. VISUAL & CAMERA DIRECTION</Text>
          <View style={styles.dirRow}>
            <Text style={styles.dirLabel}>Camera Lens:</Text>
            <Text style={styles.dirValue}>{draft.visualDirection.camera}</Text>
          </View>
          <View style={styles.dirRow}>
            <Text style={styles.dirLabel}>Movement:</Text>
            <Text style={styles.dirValue}>{draft.visualDirection.movement}</Text>
          </View>
          <View style={styles.dirRow}>
            <Text style={styles.dirLabel}>Lighting:</Text>
            <Text style={styles.dirValue}>{draft.visualDirection.lighting}</Text>
          </View>
          {draft.visualDirection.colorPalette && (
            <View style={styles.dirRow}>
              <Text style={styles.dirLabel}>Color Grading:</Text>
              <Text style={styles.dirValue}>{draft.visualDirection.colorPalette}</Text>
            </View>
          )}
        </View>

        {/* 7. B-ROLL FOOTAGE */}
        <View style={styles.sectionCard}>
          <Text style={styles.sectionNum}>7. RECOMMENDED B-ROLL</Text>
          {draft.broll.map((clip, idx) => (
            <View key={idx} style={styles.brollItem}>
              <Text style={styles.brollBullet}>•</Text>
              <Text style={styles.brollText}>{clip}</Text>
            </View>
          ))}
        </View>

        {/* 8. MUSIC & AUDIO */}
        <View style={styles.sectionCard}>
          <Text style={styles.sectionNum}>8. BACKGROUND AUDIO TRACK</Text>
          <View style={styles.musicRow}>
            <Text style={styles.musicTitle}>🎵 {draft.music.genre}</Text>
            <View style={styles.bpmBadge}>
              <Text style={styles.bpmText}>{draft.music.bpm} BPM</Text>
            </View>
          </View>
          <Text style={styles.musicMood}>Mood Profile: {draft.music.mood}</Text>
        </View>

        {/* 9. CALL TO ACTION */}
        <View style={styles.sectionCard}>
          <Text style={styles.sectionNum}>9. CLOSING CALL TO ACTION (CTA)</Text>
          <View style={styles.ctaBox}>
            <Text style={styles.ctaText}>"{draft.cta}"</Text>
          </View>
        </View>
      </ScrollView>

      {/* Fixed Bottom Action Bar */}
      <View style={styles.bottomBar}>
        <TouchableOpacity style={styles.editBtn} onPress={onEdit} activeOpacity={0.8}>
          <Text style={styles.editBtnText}>✏️ Edit in Copilot</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.regenBtn} onPress={onRegenerate} activeOpacity={0.8}>
          <Text style={styles.regenBtnText}>🔄 Regenerate</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.saveBtn} onPress={onSaveToProject} activeOpacity={0.85}>
          <Text style={styles.saveBtnText}>💾 Save to Project</Text>
        </TouchableOpacity>
      </View>
    </View>
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
    paddingBottom: 30,
  },
  header: {
    marginBottom: 16,
  },
  docBadge: {
    backgroundColor: "rgba(99, 102, 241, 0.15)",
    borderWidth: 1,
    borderColor: "#4F46E5",
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 6,
    alignSelf: "flex-start",
    marginBottom: 6,
  },
  docBadgeText: {
    fontSize: 9,
    fontWeight: "800",
    color: "#818CF8",
    letterSpacing: 0.8,
  },
  docTitle: {
    fontSize: 24,
    fontWeight: "800",
    color: "#FFFFFF",
    letterSpacing: -0.5,
  },
  docSubtitle: {
    fontSize: 12,
    color: "#94A3B8",
    marginTop: 3,
  },
  sectionCard: {
    backgroundColor: "#0F172A",
    borderRadius: 16,
    padding: 16,
    marginBottom: 14,
    borderWidth: 1,
    borderColor: "#1E293B",
  },
  sectionNum: {
    fontSize: 11,
    fontWeight: "800",
    color: "#818CF8",
    letterSpacing: 0.8,
    marginBottom: 8,
  },
  ideaTitle: {
    fontSize: 17,
    fontWeight: "700",
    color: "#FFFFFF",
    lineHeight: 23,
    marginBottom: 8,
  },
  tagRow: {
    flexDirection: "row",
    gap: 8,
  },
  tag: {
    backgroundColor: "#1E293B",
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 6,
  },
  tagText: {
    fontSize: 11,
    color: "#CBD5E1",
    fontWeight: "600",
  },
  hookBox: {
    backgroundColor: "#131C31",
    borderLeftWidth: 4,
    borderLeftColor: "#10B981",
    padding: 12,
    borderRadius: 8,
  },
  hookQuote: {
    fontSize: 15,
    fontWeight: "700",
    color: "#F8FAFC",
    fontStyle: "italic",
    lineHeight: 22,
  },
  bodyText: {
    fontSize: 13,
    color: "#CBD5E1",
    lineHeight: 20,
  },
  scriptContainer: {
    backgroundColor: "#131C31",
    borderRadius: 10,
    padding: 12,
    borderWidth: 1,
    borderColor: "#1E293B",
  },
  scriptText: {
    fontSize: 13,
    color: "#E2E8F0",
    lineHeight: 20,
    fontFamily: "Courier",
  },
  sceneCard: {
    backgroundColor: "#131C31",
    borderRadius: 12,
    padding: 12,
    marginBottom: 10,
    borderWidth: 1,
    borderColor: "#1E293B",
  },
  sceneHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 8,
  },
  sceneNumber: {
    fontSize: 11,
    fontWeight: "800",
    color: "#6366F1",
  },
  sceneDurationBadge: {
    backgroundColor: "#1E293B",
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 4,
  },
  sceneDurationText: {
    fontSize: 10,
    color: "#94A3B8",
    fontWeight: "700",
  },
  sceneRow: {
    marginBottom: 6,
  },
  sceneFieldLabel: {
    fontSize: 9,
    fontWeight: "800",
    color: "#64748B",
    marginBottom: 2,
  },
  sceneFieldValue: {
    fontSize: 12,
    color: "#CBD5E1",
    lineHeight: 17,
  },
  sceneDialogueValue: {
    fontSize: 12,
    color: "#F8FAFC",
    fontStyle: "italic",
    fontWeight: "600",
  },
  sceneTechRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    borderTopWidth: 1,
    borderTopColor: "#1E293B",
    paddingTop: 6,
    marginTop: 4,
  },
  sceneTechText: {
    fontSize: 10,
    color: "#94A3B8",
  },
  dirRow: {
    marginBottom: 8,
  },
  dirLabel: {
    fontSize: 11,
    fontWeight: "700",
    color: "#64748B",
    marginBottom: 2,
  },
  dirValue: {
    fontSize: 13,
    color: "#E2E8F0",
  },
  brollItem: {
    flexDirection: "row",
    alignItems: "flex-start",
    marginBottom: 6,
  },
  brollBullet: {
    fontSize: 14,
    color: "#6366F1",
    marginRight: 8,
    marginTop: -2,
  },
  brollText: {
    flex: 1,
    fontSize: 12,
    color: "#CBD5E1",
    lineHeight: 18,
  },
  musicRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 4,
  },
  musicTitle: {
    fontSize: 14,
    fontWeight: "700",
    color: "#FFFFFF",
  },
  bpmBadge: {
    backgroundColor: "#1E293B",
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 8,
  },
  bpmText: {
    fontSize: 11,
    fontWeight: "700",
    color: "#A5B4FC",
  },
  musicMood: {
    fontSize: 12,
    color: "#94A3B8",
  },
  ctaBox: {
    backgroundColor: "rgba(245, 158, 11, 0.1)",
    borderLeftWidth: 4,
    borderLeftColor: "#F59E0B",
    padding: 12,
    borderRadius: 8,
  },
  ctaText: {
    fontSize: 14,
    fontWeight: "700",
    color: "#FDE68A",
  },
  bottomBar: {
    flexDirection: "row",
    borderTopWidth: 1,
    borderTopColor: "#1E293B",
    padding: 12,
    backgroundColor: "#0F172A",
    gap: 8,
  },
  editBtn: {
    flex: 1,
    backgroundColor: "#1E293B",
    paddingVertical: 12,
    borderRadius: 10,
    alignItems: "center",
    borderWidth: 1,
    borderColor: "#334155",
  },
  editBtnText: {
    color: "#E2E8F0",
    fontSize: 12,
    fontWeight: "700",
  },
  regenBtn: {
    backgroundColor: "#1E293B",
    paddingVertical: 12,
    paddingHorizontal: 12,
    borderRadius: 10,
    alignItems: "center",
    borderWidth: 1,
    borderColor: "#334155",
  },
  regenBtnText: {
    color: "#94A3B8",
    fontSize: 12,
    fontWeight: "700",
  },
  saveBtn: {
    flex: 1.3,
    backgroundColor: "#10B981",
    paddingVertical: 12,
    borderRadius: 10,
    alignItems: "center",
    shadowColor: "#10B981",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
    elevation: 3,
  },
  saveBtnText: {
    color: "#FFFFFF",
    fontSize: 13,
    fontWeight: "800",
  },
});
