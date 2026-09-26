import React from "react";
import {
  View,
  Text,
  Image,
  StyleSheet,
  TouchableOpacity,
} from "react-native";
import { ContentItem } from "../types/creatorIntelligence";

interface ContentCardProps {
  content: ContentItem;
  isBookmarked: boolean;
  isInStoryboard: boolean;
  onPressCard: (item: ContentItem) => void;
  onToggleBookmark: (item: ContentItem) => void;
  onAddToStoryboard: (item: ContentItem) => void;
}

export const ContentCard: React.FC<ContentCardProps> = ({
  content,
  isBookmarked,
  isInStoryboard,
  onPressCard,
  onToggleBookmark,
  onAddToStoryboard,
}) => {
  const getPlatformIcon = (platform: string) => {
    switch (platform) {
      case "youtube":
        return "▶";
      case "instagram":
        return "📸";
      case "x_twitter":
        return "𝕏";
      case "linkedin":
        return "in";
      default:
        return "▶";
    }
  };

  return (
    <View style={styles.cardContainer}>
      <TouchableOpacity
        onPress={() => onPressCard(content)}
        activeOpacity={0.9}
        style={styles.clickableArea}
      >
        {/* Media Thumbnail Container */}
        <View style={styles.thumbnailWrapper}>
          <Image source={{ uri: content.thumbnail }} style={styles.thumbnail} />
          
          {/* Duration Badge */}
          {content.duration && (
            <View style={styles.durationBadge}>
              <Text style={styles.durationText}>{content.duration}</Text>
            </View>
          )}

          {/* Platform & Type Badge */}
          <View style={styles.platformBadge}>
            <Text style={styles.platformIcon}>{getPlatformIcon(content.platform)}</Text>
            <Text style={styles.platformText}>
              {content.platform.toUpperCase()} {content.type === "reel" ? "REEL" : "VIDEO"}
            </Text>
          </View>

          {/* Trend Momentum Badge */}
          <View style={styles.trendBadge}>
            <Text style={styles.trendArrow}>↑</Text>
            <Text style={styles.trendText}>+{content.trendScore}%</Text>
          </View>
        </View>

        {/* Content Metadata */}
        <View style={styles.metaContainer}>
          <Text style={styles.title} numberOfLines={2}>
            {content.title}
          </Text>

          {/* Creator Information Row */}
          <View style={styles.creatorRow}>
            <Image source={{ uri: content.creatorAvatar }} style={styles.avatar} />
            <View style={styles.creatorInfo}>
              <Text style={styles.creatorName} numberOfLines={1}>
                {content.creatorName}
              </Text>
              <Text style={styles.creatorHandle} numberOfLines={1}>
                {content.creatorHandle}
              </Text>
            </View>
          </View>

          {/* Engagement Statistics Row */}
          <View style={styles.statsRow}>
            <View style={styles.statItem}>
              <Text style={styles.statLabel}>Views</Text>
              <Text style={styles.statValue}>{content.views}</Text>
            </View>

            <View style={styles.statDivider} />

            <View style={styles.statItem}>
              <Text style={styles.statLabel}>Engagement</Text>
              <Text style={styles.statValueHighlight}>{content.engagement}</Text>
            </View>

            <View style={styles.statDivider} />

            <View style={styles.statItem}>
              <Text style={styles.statLabel}>Published</Text>
              <Text style={styles.statValue}>{content.publishedAt}</Text>
            </View>
          </View>
        </View>
      </TouchableOpacity>

      {/* Action Buttons Row */}
      <View style={styles.actionsRow}>
        <TouchableOpacity
          style={[styles.bookmarkButton, isBookmarked && styles.bookmarkButtonActive]}
          onPress={() => onToggleBookmark(content)}
          activeOpacity={0.8}
        >
          <Text style={styles.bookmarkIcon}>{isBookmarked ? "★" : "☆"}</Text>
          <Text
            style={[
              styles.bookmarkText,
              isBookmarked && styles.bookmarkTextActive,
            ]}
          >
            {isBookmarked ? "Saved" : "Bookmark"}
          </Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[
            styles.storyboardButton,
            isInStoryboard && styles.storyboardButtonActive,
          ]}
          onPress={() => onAddToStoryboard(content)}
          activeOpacity={0.8}
        >
          <Text style={styles.storyboardIcon}>
            {isInStoryboard ? "✓" : "+"}
          </Text>
          <Text
            style={[
              styles.storyboardText,
              isInStoryboard && styles.storyboardTextActive,
            ]}
          >
            {isInStoryboard ? "In Storyboard" : "Add to Storyboard"}
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  cardContainer: {
    backgroundColor: "#0F172A",
    borderRadius: 18,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: "#1E293B",
    overflow: "hidden",
  },
  clickableArea: {
    width: "100%",
  },
  thumbnailWrapper: {
    width: "100%",
    height: 190,
    position: "relative",
    backgroundColor: "#1E293B",
  },
  thumbnail: {
    width: "100%",
    height: "100%",
    resizeMode: "cover",
  },
  durationBadge: {
    position: "absolute",
    bottom: 10,
    right: 10,
    backgroundColor: "rgba(0, 0, 0, 0.8)",
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 4,
  },
  durationText: {
    color: "#FFFFFF",
    fontSize: 11,
    fontWeight: "700",
  },
  platformBadge: {
    position: "absolute",
    top: 10,
    left: 10,
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "rgba(15, 23, 42, 0.85)",
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 6,
    borderWidth: 1,
    borderColor: "rgba(255, 255, 255, 0.1)",
  },
  platformIcon: {
    color: "#FFFFFF",
    fontSize: 10,
    marginRight: 4,
  },
  platformText: {
    color: "#E2E8F0",
    fontSize: 10,
    fontWeight: "700",
    letterSpacing: 0.5,
  },
  trendBadge: {
    position: "absolute",
    top: 10,
    right: 10,
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "rgba(16, 185, 129, 0.9)",
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 12,
  },
  trendArrow: {
    color: "#FFFFFF",
    fontSize: 11,
    fontWeight: "900",
    marginRight: 2,
  },
  trendText: {
    color: "#FFFFFF",
    fontSize: 11,
    fontWeight: "800",
  },
  metaContainer: {
    padding: 16,
  },
  title: {
    fontSize: 16,
    fontWeight: "700",
    color: "#F8FAFC",
    lineHeight: 22,
    marginBottom: 12,
  },
  creatorRow: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 14,
  },
  avatar: {
    width: 32,
    height: 32,
    borderRadius: 16,
    marginRight: 10,
    borderWidth: 1,
    borderColor: "#334155",
  },
  creatorInfo: {
    flex: 1,
  },
  creatorName: {
    fontSize: 13,
    fontWeight: "600",
    color: "#F1F5F9",
  },
  creatorHandle: {
    fontSize: 11,
    color: "#64748B",
  },
  statsRow: {
    flexDirection: "row",
    backgroundColor: "#131C31",
    borderRadius: 10,
    paddingVertical: 8,
    paddingHorizontal: 12,
    justifyContent: "space-between",
    alignItems: "center",
  },
  statItem: {
    alignItems: "center",
    flex: 1,
  },
  statLabel: {
    fontSize: 10,
    color: "#64748B",
    marginBottom: 2,
    fontWeight: "500",
  },
  statValue: {
    fontSize: 12,
    fontWeight: "700",
    color: "#CBD5E1",
  },
  statValueHighlight: {
    fontSize: 12,
    fontWeight: "700",
    color: "#10B981",
  },
  statDivider: {
    width: 1,
    height: 18,
    backgroundColor: "#1E293B",
  },
  actionsRow: {
    flexDirection: "row",
    borderTopWidth: 1,
    borderTopColor: "#1E293B",
    padding: 10,
    gap: 8,
  },
  bookmarkButton: {
    flex: 1,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#1E293B",
    paddingVertical: 9,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: "#334155",
  },
  bookmarkButtonActive: {
    backgroundColor: "rgba(245, 158, 11, 0.15)",
    borderColor: "#F59E0B",
  },
  bookmarkIcon: {
    fontSize: 14,
    marginRight: 5,
    color: "#F59E0B",
  },
  bookmarkText: {
    fontSize: 12,
    fontWeight: "600",
    color: "#CBD5E1",
  },
  bookmarkTextActive: {
    color: "#F59E0B",
  },
  storyboardButton: {
    flex: 1.3,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#312E81",
    paddingVertical: 9,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: "#6366F1",
  },
  storyboardButtonActive: {
    backgroundColor: "rgba(99, 102, 241, 0.2)",
    borderColor: "#4F46E5",
  },
  storyboardIcon: {
    fontSize: 13,
    marginRight: 5,
    color: "#818CF8",
    fontWeight: "800",
  },
  storyboardText: {
    fontSize: 12,
    fontWeight: "700",
    color: "#E0E7FF",
  },
  storyboardTextActive: {
    color: "#A5B4FC",
  },
});
