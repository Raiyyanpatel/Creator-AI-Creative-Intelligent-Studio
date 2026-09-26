import React from "react";
import { View, Text, StyleSheet } from "react-native";
import { GeneratedContent } from "../types/creatorIntelligence";

interface DraftPreviewProps {
  draft: GeneratedContent;
}

export const DraftPreview: React.FC<DraftPreviewProps> = ({ draft }) => {
  return (
    <View style={styles.container}>
      <View style={styles.topRow}>
        <View style={styles.badgeRow}>
          <View style={styles.pulseDot} />
          <Text style={styles.badgeText}>LIVE DRAFT PREVIEW (v{draft.version})</Text>
        </View>
        <Text style={styles.platformLabel}>{draft.targetPlatform}</Text>
      </View>

      <Text style={styles.title} numberOfLines={1}>
        {draft.title}
      </Text>

      <View style={styles.hookBox}>
        <Text style={styles.hookLabel}>CURRENT HOOK:</Text>
        <Text style={styles.hookText}>"{draft.hook}"</Text>
      </View>

      {draft.changesApplied && draft.changesApplied.length > 0 && (
        <View style={styles.changesRow}>
          {draft.changesApplied.map((tag, idx) => (
            <View key={idx} style={styles.changePill}>
              <Text style={styles.changePillText}>{tag}</Text>
            </View>
          ))}
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: "#131C31",
    borderRadius: 16,
    padding: 14,
    marginBottom: 14,
    borderWidth: 1,
    borderColor: "#1E293B",
  },
  topRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 6,
  },
  badgeRow: {
    flexDirection: "row",
    alignItems: "center",
  },
  pulseDot: {
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: "#10B981",
    marginRight: 6,
  },
  badgeText: {
    fontSize: 10,
    fontWeight: "800",
    color: "#10B981",
    letterSpacing: 0.5,
  },
  platformLabel: {
    fontSize: 10,
    color: "#94A3B8",
    fontWeight: "600",
  },
  title: {
    fontSize: 15,
    fontWeight: "700",
    color: "#FFFFFF",
    marginBottom: 8,
  },
  hookBox: {
    backgroundColor: "#0F172A",
    borderRadius: 10,
    padding: 10,
    borderLeftWidth: 3,
    borderLeftColor: "#6366F1",
    marginBottom: 8,
  },
  hookLabel: {
    fontSize: 9,
    fontWeight: "800",
    color: "#818CF8",
    letterSpacing: 0.6,
    marginBottom: 2,
  },
  hookText: {
    fontSize: 13,
    color: "#E2E8F0",
    fontStyle: "italic",
    lineHeight: 18,
  },
  changesRow: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 6,
  },
  changePill: {
    backgroundColor: "rgba(16, 185, 129, 0.15)",
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 8,
  },
  changePillText: {
    fontSize: 10,
    color: "#10B981",
    fontWeight: "700",
  },
});
