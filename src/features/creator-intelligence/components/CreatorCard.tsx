import React from "react";
import { View, Text, Image, StyleSheet, TouchableOpacity } from "react-native";
import { Creator } from "../types/creatorIntelligence";

interface CreatorCardProps {
  creator: Creator;
  onPress: (creator: Creator) => void;
}

export const CreatorCard: React.FC<CreatorCardProps> = ({ creator, onPress }) => {
  return (
    <TouchableOpacity
      style={styles.card}
      onPress={() => onPress(creator)}
      activeOpacity={0.85}
    >
      <View style={styles.topRow}>
        <Image source={{ uri: creator.avatar }} style={styles.avatar} />
        <View style={styles.headerInfo}>
          <View style={styles.nameRow}>
            <Text style={styles.name} numberOfLines={1}>
              {creator.name}
            </Text>
            {creator.verified && <Text style={styles.verifiedBadge}>✓</Text>}
          </View>
          <Text style={styles.handle}>{creator.handle}</Text>
        </View>

        <View style={styles.platformBadge}>
          <Text style={styles.platformText}>{creator.platform.toUpperCase()}</Text>
        </View>
      </View>

      <Text style={styles.nicheBadge} numberOfLines={1}>
        🎯 {creator.niche}
      </Text>

      {creator.bio && (
        <Text style={styles.bio} numberOfLines={2}>
          {creator.bio}
        </Text>
      )}

      <View style={styles.footerRow}>
        <View style={styles.statBox}>
          <Text style={styles.statLabel}>Followers</Text>
          <Text style={styles.statValue}>{creator.followers}</Text>
        </View>

        <View style={styles.growthBadge}>
          <Text style={styles.growthText}>↑ {creator.growth}</Text>
        </View>
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
    alignItems: "center",
    marginBottom: 10,
  },
  avatar: {
    width: 44,
    height: 44,
    borderRadius: 22,
    marginRight: 12,
    borderWidth: 1.5,
    borderColor: "#4F46E5",
  },
  headerInfo: {
    flex: 1,
  },
  nameRow: {
    flexDirection: "row",
    alignItems: "center",
  },
  name: {
    fontSize: 15,
    fontWeight: "700",
    color: "#FFFFFF",
    marginRight: 4,
  },
  verifiedBadge: {
    fontSize: 11,
    color: "#38BDF8",
    fontWeight: "900",
  },
  handle: {
    fontSize: 12,
    color: "#64748B",
    marginTop: 1,
  },
  platformBadge: {
    backgroundColor: "#1E293B",
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 6,
  },
  platformText: {
    fontSize: 10,
    fontWeight: "700",
    color: "#94A3B8",
  },
  nicheBadge: {
    fontSize: 12,
    color: "#A5B4FC",
    fontWeight: "600",
    marginBottom: 6,
  },
  bio: {
    fontSize: 12,
    color: "#94A3B8",
    lineHeight: 17,
    marginBottom: 12,
  },
  footerRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    borderTopWidth: 1,
    borderTopColor: "#1E293B",
    paddingTop: 10,
  },
  statBox: {
    flexDirection: "row",
    alignItems: "center",
  },
  statLabel: {
    fontSize: 11,
    color: "#64748B",
    marginRight: 6,
  },
  statValue: {
    fontSize: 13,
    fontWeight: "700",
    color: "#F8FAFC",
  },
  growthBadge: {
    backgroundColor: "rgba(16, 185, 129, 0.15)",
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 10,
  },
  growthText: {
    fontSize: 11,
    color: "#10B981",
    fontWeight: "700",
  },
});
