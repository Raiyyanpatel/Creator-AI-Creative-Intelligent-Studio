import React from "react";
import { View, Text, StyleSheet, TouchableOpacity } from "react-native";
import { TopicItem } from "../types/creatorIntelligence";

interface TopicCardProps {
  topic: TopicItem;
  onPress: (topic: TopicItem) => void;
}

export const TopicCard: React.FC<TopicCardProps> = ({ topic, onPress }) => {
  return (
    <TouchableOpacity
      style={styles.card}
      onPress={() => onPress(topic)}
      activeOpacity={0.85}
    >
      <View style={styles.topRow}>
        <View style={styles.categoryBadge}>
          <Text style={styles.categoryText}>{topic.category.toUpperCase()}</Text>
        </View>
        <View style={styles.growthBadge}>
          <Text style={styles.growthText}>↑ +{topic.growth}%</Text>
        </View>
      </View>

      <Text style={styles.name}>{topic.name}</Text>
      <Text style={styles.description} numberOfLines={2}>
        {topic.description}
      </Text>

      <View style={styles.footer}>
        <Text style={styles.relatedText}>
          📊 {topic.relatedCount} creators & pieces discussing this
        </Text>
        <Text style={styles.exploreArrow}>Explore →</Text>
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: "#0F172A",
    borderRadius: 16,
    padding: 16,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: "#1E293B",
  },
  topRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 8,
  },
  categoryBadge: {
    backgroundColor: "#1E293B",
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 6,
  },
  categoryText: {
    fontSize: 10,
    fontWeight: "700",
    color: "#94A3B8",
    letterSpacing: 0.5,
  },
  growthBadge: {
    backgroundColor: "rgba(16, 185, 129, 0.15)",
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 10,
  },
  growthText: {
    color: "#10B981",
    fontSize: 11,
    fontWeight: "700",
  },
  name: {
    fontSize: 16,
    fontWeight: "700",
    color: "#FFFFFF",
    marginBottom: 6,
  },
  description: {
    fontSize: 12,
    color: "#94A3B8",
    lineHeight: 17,
    marginBottom: 12,
  },
  footer: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    borderTopWidth: 1,
    borderTopColor: "#1E293B",
    paddingTop: 10,
  },
  relatedText: {
    fontSize: 11,
    color: "#64748B",
    fontWeight: "500",
  },
  exploreArrow: {
    fontSize: 12,
    color: "#818CF8",
    fontWeight: "700",
  },
});
