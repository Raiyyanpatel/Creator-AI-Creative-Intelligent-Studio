import React from "react";
import { View, Text, StyleSheet, TouchableOpacity } from "react-native";
import { Trend } from "../types/creatorIntelligence";

interface TrendCardProps {
  trend: Trend;
  rank: number;
  onPress: (trend: Trend) => void;
}

export const TrendCard: React.FC<TrendCardProps> = ({ trend, rank, onPress }) => {
  return (
    <TouchableOpacity
      style={styles.card}
      onPress={() => onPress(trend)}
      activeOpacity={0.85}
    >
      <View style={styles.topRow}>
        <View style={styles.rankBadge}>
          <Text style={styles.rankText}>#{rank}</Text>
        </View>
        <View style={styles.growthBadge}>
          <Text style={styles.growthArrow}>↑</Text>
          <Text style={styles.growthText}>+{trend.growth}%</Text>
        </View>
      </View>

      <Text style={styles.topic} numberOfLines={2}>
        {trend.topic}
      </Text>

      <Text style={styles.explanation} numberOfLines={2}>
        "{trend.explanation}"
      </Text>

      <View style={styles.footer}>
        <View style={styles.volumeContainer}>
          <View style={styles.volumeIndicator} />
          <Text style={styles.volumeText}>{trend.volume || "120K posts"}</Text>
        </View>
        <View style={styles.categoryBadge}>
          <Text style={styles.categoryText}>{trend.category}</Text>
        </View>
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  card: {
    width: 250,
    backgroundColor: "#0F172A",
    borderRadius: 16,
    padding: 16,
    marginRight: 12,
    borderWidth: 1,
    borderColor: "#1E293B",
    justifyContent: "space-between",
  },
  topRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 10,
  },
  rankBadge: {
    backgroundColor: "#1E293B",
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 6,
  },
  rankText: {
    fontSize: 11,
    fontWeight: "700",
    color: "#94A3B8",
  },
  growthBadge: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "rgba(16, 185, 129, 0.15)",
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: "rgba(16, 185, 129, 0.3)",
  },
  growthArrow: {
    color: "#10B981",
    fontSize: 10,
    fontWeight: "800",
    marginRight: 3,
  },
  growthText: {
    color: "#10B981",
    fontSize: 12,
    fontWeight: "700",
  },
  topic: {
    fontSize: 16,
    fontWeight: "700",
    color: "#FFFFFF",
    lineHeight: 22,
    marginBottom: 6,
  },
  explanation: {
    fontSize: 12,
    color: "#94A3B8",
    lineHeight: 17,
    fontStyle: "italic",
    marginBottom: 14,
  },
  footer: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    borderTopWidth: 1,
    borderTopColor: "#1E293B",
    paddingTop: 10,
  },
  volumeContainer: {
    flexDirection: "row",
    alignItems: "center",
  },
  volumeIndicator: {
    width: 5,
    height: 5,
    borderRadius: 2.5,
    backgroundColor: "#6366F1",
    marginRight: 6,
  },
  volumeText: {
    fontSize: 11,
    color: "#64748B",
    fontWeight: "500",
  },
  categoryBadge: {
    backgroundColor: "#1E293B",
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 4,
  },
  categoryText: {
    fontSize: 10,
    color: "#CBD5E1",
    fontWeight: "600",
  },
});
