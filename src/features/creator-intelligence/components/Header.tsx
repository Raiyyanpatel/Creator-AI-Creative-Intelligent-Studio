import React from "react";
import { View, Text, StyleSheet, TouchableOpacity } from "react-native";

interface HeaderProps {
  storyboardCount: number;
  onOpenStoryboard: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  storyboardCount,
  onOpenStoryboard,
}) => {
  return (
    <View style={styles.container}>
      <View style={styles.titleContainer}>
        <View style={styles.badgeRow}>
          <View style={styles.pulsingDot} />
          <Text style={styles.badgeText}>LIVE SIGNALS ACTIVE</Text>
        </View>
        <Text style={styles.title}>Creator Intelligence</Text>
        <Text style={styles.subtitle}>What's happening. What's worth creating.</Text>
      </View>

      <TouchableOpacity
        style={[
          styles.storyboardButton,
          storyboardCount > 0 && styles.storyboardButtonActive,
        ]}
        onPress={onOpenStoryboard}
        activeOpacity={0.8}
      >
        <Text style={styles.storyboardIcon}>📋</Text>
        <Text
          style={[
            styles.storyboardText,
            storyboardCount > 0 && styles.storyboardTextActive,
          ]}
        >
          Storyboard
        </Text>
        <View
          style={[
            styles.countBadge,
            storyboardCount > 0 && styles.countBadgeActive,
          ]}
        >
          <Text
            style={[
              styles.countText,
              storyboardCount > 0 && styles.countTextActive,
            ]}
          >
            {storyboardCount}
          </Text>
        </View>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "flex-start",
    paddingHorizontal: 20,
    paddingTop: 16,
    paddingBottom: 12,
  },
  titleContainer: {
    flex: 1,
    paddingRight: 12,
  },
  badgeRow: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 4,
  },
  pulsingDot: {
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: "#10B981",
    marginRight: 6,
  },
  badgeText: {
    fontSize: 10,
    fontWeight: "700",
    color: "#10B981",
    letterSpacing: 0.8,
  },
  title: {
    fontSize: 26,
    fontWeight: "800",
    color: "#FFFFFF",
    letterSpacing: -0.5,
  },
  subtitle: {
    fontSize: 13,
    color: "#94A3B8",
    marginTop: 2,
    fontWeight: "400",
  },
  storyboardButton: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#1E293B",
    paddingVertical: 8,
    paddingHorizontal: 12,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: "#334155",
  },
  storyboardButtonActive: {
    backgroundColor: "#312E81",
    borderColor: "#6366F1",
  },
  storyboardIcon: {
    fontSize: 13,
    marginRight: 5,
  },
  storyboardText: {
    fontSize: 12,
    fontWeight: "600",
    color: "#94A3B8",
    marginRight: 6,
  },
  storyboardTextActive: {
    color: "#E0E7FF",
  },
  countBadge: {
    backgroundColor: "#334155",
    paddingHorizontal: 6,
    paddingVertical: 1,
    borderRadius: 10,
    minWidth: 18,
    alignItems: "center",
  },
  countBadgeActive: {
    backgroundColor: "#6366F1",
  },
  countText: {
    fontSize: 11,
    fontWeight: "700",
    color: "#CBD5E1",
  },
  countTextActive: {
    color: "#FFFFFF",
  },
});
