import React from "react";
import {
  Modal,
  View,
  Text,
  Image,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  SafeAreaView,
} from "react-native";
import { ContentItem } from "../types/creatorIntelligence";

interface ContentDetailModalProps {
  visible: boolean;
  content: ContentItem | null;
  isBookmarked: boolean;
  isInStoryboard: boolean;
  onClose: () => void;
  onToggleBookmark: (content: ContentItem) => void;
  onAddToStoryboard: (content: ContentItem) => void;
}

export const ContentDetailModal: React.FC<ContentDetailModalProps> = ({
  visible,
  content,
  isBookmarked,
  isInStoryboard,
  onClose,
  onToggleBookmark,
  onAddToStoryboard,
}) => {
  if (!content) return null;

  return (
    <Modal
      visible={visible}
      animationType="slide"
      transparent={true}
      onRequestClose={onClose}
    >
      <View style={styles.modalOverlay}>
        <SafeAreaView style={styles.safeContainer}>
          <View style={styles.modalContent}>
            {/* Top Drag Handle & Close */}
            <View style={styles.headerBar}>
              <View style={styles.dragPill} />
              <TouchableOpacity
                onPress={onClose}
                style={styles.closeBtn}
                hitSlop={{ top: 12, bottom: 12, left: 12, right: 12 }}
              >
                <Text style={styles.closeBtnText}>✕</Text>
              </TouchableOpacity>
            </View>

            <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={styles.scrollBody}>
              {/* Large Media Thumbnail */}
              <View style={styles.thumbnailContainer}>
                <Image source={{ uri: content.thumbnail }} style={styles.largeThumbnail} />
                <View style={styles.badgeOverlay}>
                  <Text style={styles.platformBadgeText}>
                    {content.platform.toUpperCase()} • {content.type.toUpperCase()}
                  </Text>
                  <Text style={styles.trendScoreText}>+{content.trendScore}% VELOCITY</Text>
                </View>
              </View>

              {/* Title & Metadata */}
              <Text style={styles.title}>{content.title}</Text>

              {/* Creator Card Row */}
              <View style={styles.creatorBanner}>
                <Image source={{ uri: content.creatorAvatar }} style={styles.creatorAvatar} />
                <View style={styles.creatorDetails}>
                  <Text style={styles.creatorName}>{content.creatorName}</Text>
                  <Text style={styles.creatorHandle}>{content.creatorHandle}</Text>
                </View>
                <View style={styles.viewsPill}>
                  <Text style={styles.viewsPillText}>{content.views} views</Text>
                </View>
              </View>

              {/* Metrics Grid */}
              <View style={styles.metricsGrid}>
                <View style={styles.metricCard}>
                  <Text style={styles.metricLabel}>ENGAGEMENT</Text>
                  <Text style={styles.metricValueGreen}>{content.engagement}</Text>
                </View>
                <View style={styles.metricCard}>
                  <Text style={styles.metricLabel}>PUBLISHED</Text>
                  <Text style={styles.metricValue}>{content.publishedAt}</Text>
                </View>
                <View style={styles.metricCard}>
                  <Text style={styles.metricLabel}>DURATION</Text>
                  <Text style={styles.metricValue}>{content.duration || "N/A"}</Text>
                </View>
              </View>

              {/* Why It's Trending Section */}
              <View style={styles.sectionBlock}>
                <Text style={styles.sectionHeader}>🔥 WHY IT'S TRENDING</Text>
                <Text style={styles.sectionText}>
                  {content.whyTrending ||
                    "Surge in algorithm distribution triggered by rapid share-to-view ratio in the first 24 hours."}
                </Text>
              </View>

              {/* Why This Matters Section */}
              <View style={styles.mattersBlock}>
                <Text style={styles.mattersHeader}>💡 WHY THIS MATTERS FOR CREATORS</Text>
                <Text style={styles.mattersText}>
                  {content.whyThisMatters ||
                    "Demonstrates massive viewer appetite for concrete, unvarnished demonstrations rather than theoretical talking points."}
                </Text>
              </View>

              {/* Related Topics Pills */}
              <View style={styles.sectionBlock}>
                <Text style={styles.sectionHeader}>🏷️ RELATED TOPIC SIGNALS</Text>
                <View style={styles.pillsContainer}>
                  {content.topics.map((t, idx) => (
                    <View key={idx} style={styles.topicPill}>
                      <Text style={styles.topicPillText}>#{t}</Text>
                    </View>
                  ))}
                </View>
              </View>
            </ScrollView>

            {/* Bottom Actions Bar */}
            <View style={styles.bottomActions}>
              <TouchableOpacity
                style={[styles.bookmarkButton, isBookmarked && styles.bookmarkButtonActive]}
                onPress={() => onToggleBookmark(content)}
                activeOpacity={0.8}
              >
                <Text style={styles.bookmarkIcon}>{isBookmarked ? "★" : "☆"}</Text>
                <Text style={[styles.bookmarkText, isBookmarked && styles.bookmarkTextActive]}>
                  {isBookmarked ? "Saved in Bookmarks" : "Bookmark"}
                </Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={[styles.storyboardButton, isInStoryboard && styles.storyboardButtonActive]}
                onPress={() => onAddToStoryboard(content)}
                activeOpacity={0.8}
              >
                <Text style={styles.storyboardIcon}>{isInStoryboard ? "✓" : "📋"}</Text>
                <Text style={[styles.storyboardText, isInStoryboard && styles.storyboardTextActive]}>
                  {isInStoryboard ? "In Storyboard" : "Add to Storyboard"}
                </Text>
              </TouchableOpacity>
            </View>
          </View>
        </SafeAreaView>
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  modalOverlay: {
    flex: 1,
    backgroundColor: "rgba(0, 0, 0, 0.75)",
    justifyContent: "flex-end",
  },
  safeContainer: {
    maxHeight: "92%",
  },
  modalContent: {
    backgroundColor: "#0F172A",
    borderTopLeftRadius: 24,
    borderTopRightRadius: 24,
    borderTopWidth: 1,
    borderTopColor: "#334155",
    height: "100%",
    display: "flex",
  },
  headerBar: {
    alignItems: "center",
    paddingTop: 10,
    paddingBottom: 8,
    position: "relative",
  },
  dragPill: {
    width: 38,
    height: 4,
    borderRadius: 2,
    backgroundColor: "#475569",
  },
  closeBtn: {
    position: "absolute",
    right: 18,
    top: 8,
    width: 28,
    height: 28,
    borderRadius: 14,
    backgroundColor: "#1E293B",
    alignItems: "center",
    justifyContent: "center",
  },
  closeBtnText: {
    color: "#94A3B8",
    fontSize: 12,
    fontWeight: "700",
  },
  scrollBody: {
    paddingHorizontal: 20,
    paddingBottom: 24,
  },
  thumbnailContainer: {
    width: "100%",
    height: 210,
    borderRadius: 16,
    overflow: "hidden",
    position: "relative",
    marginVertical: 12,
    backgroundColor: "#1E293B",
  },
  largeThumbnail: {
    width: "100%",
    height: "100%",
    resizeMode: "cover",
  },
  badgeOverlay: {
    position: "absolute",
    bottom: 10,
    left: 10,
    right: 10,
    flexDirection: "row",
    justifyContent: "space-between",
  },
  platformBadgeText: {
    backgroundColor: "rgba(15, 23, 42, 0.85)",
    color: "#F8FAFC",
    fontSize: 11,
    fontWeight: "700",
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 6,
  },
  trendScoreText: {
    backgroundColor: "rgba(16, 185, 129, 0.9)",
    color: "#FFFFFF",
    fontSize: 11,
    fontWeight: "800",
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 6,
  },
  title: {
    fontSize: 18,
    fontWeight: "800",
    color: "#FFFFFF",
    lineHeight: 25,
    marginBottom: 14,
  },
  creatorBanner: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#131C31",
    padding: 12,
    borderRadius: 12,
    marginBottom: 16,
  },
  creatorAvatar: {
    width: 40,
    height: 40,
    borderRadius: 20,
    marginRight: 10,
  },
  creatorDetails: {
    flex: 1,
  },
  creatorName: {
    fontSize: 14,
    fontWeight: "700",
    color: "#F8FAFC",
  },
  creatorHandle: {
    fontSize: 12,
    color: "#64748B",
  },
  viewsPill: {
    backgroundColor: "#1E293B",
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 8,
  },
  viewsPillText: {
    fontSize: 12,
    fontWeight: "700",
    color: "#CBD5E1",
  },
  metricsGrid: {
    flexDirection: "row",
    gap: 8,
    marginBottom: 18,
  },
  metricCard: {
    flex: 1,
    backgroundColor: "#131C31",
    borderRadius: 12,
    padding: 10,
    alignItems: "center",
  },
  metricLabel: {
    fontSize: 9,
    fontWeight: "700",
    color: "#64748B",
    marginBottom: 3,
  },
  metricValue: {
    fontSize: 13,
    fontWeight: "700",
    color: "#F8FAFC",
  },
  metricValueGreen: {
    fontSize: 13,
    fontWeight: "800",
    color: "#10B981",
  },
  sectionBlock: {
    marginBottom: 16,
  },
  sectionHeader: {
    fontSize: 11,
    fontWeight: "700",
    color: "#94A3B8",
    letterSpacing: 0.8,
    marginBottom: 6,
  },
  sectionText: {
    fontSize: 13,
    color: "#CBD5E1",
    lineHeight: 19,
  },
  mattersBlock: {
    backgroundColor: "rgba(99, 102, 241, 0.1)",
    borderWidth: 1,
    borderColor: "rgba(99, 102, 241, 0.25)",
    padding: 14,
    borderRadius: 14,
    marginBottom: 16,
  },
  mattersHeader: {
    fontSize: 11,
    fontWeight: "700",
    color: "#A5B4FC",
    letterSpacing: 0.6,
    marginBottom: 6,
  },
  mattersText: {
    fontSize: 13,
    color: "#E0E7FF",
    lineHeight: 19,
  },
  pillsContainer: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 6,
  },
  topicPill: {
    backgroundColor: "#1E293B",
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 20,
  },
  topicPillText: {
    fontSize: 12,
    color: "#94A3B8",
    fontWeight: "500",
  },
  bottomActions: {
    flexDirection: "row",
    borderTopWidth: 1,
    borderTopColor: "#1E293B",
    padding: 16,
    gap: 10,
    backgroundColor: "#0F172A",
  },
  bookmarkButton: {
    flex: 1,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#1E293B",
    paddingVertical: 12,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: "#334155",
  },
  bookmarkButtonActive: {
    backgroundColor: "rgba(245, 158, 11, 0.15)",
    borderColor: "#F59E0B",
  },
  bookmarkIcon: {
    fontSize: 15,
    marginRight: 6,
    color: "#F59E0B",
  },
  bookmarkText: {
    fontSize: 13,
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
    backgroundColor: "#4F46E5",
    paddingVertical: 12,
    borderRadius: 12,
  },
  storyboardButtonActive: {
    backgroundColor: "#312E81",
    borderWidth: 1,
    borderColor: "#6366F1",
  },
  storyboardIcon: {
    fontSize: 14,
    marginRight: 6,
    color: "#FFFFFF",
  },
  storyboardText: {
    fontSize: 13,
    fontWeight: "700",
    color: "#FFFFFF",
  },
  storyboardTextActive: {
    color: "#C7D2FE",
  },
});
