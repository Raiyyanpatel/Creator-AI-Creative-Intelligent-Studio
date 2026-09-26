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
import { StoryboardItem } from "../types/creatorIntelligence";

interface StoryboardSheetProps {
  visible: boolean;
  items: StoryboardItem[];
  onClose: () => void;
  onRemoveItem: (id: string) => void;
  onOpenGenerate: () => void;
  onSelectItem: (item: StoryboardItem) => void;
}

export const StoryboardSheet: React.FC<StoryboardSheetProps> = ({
  visible,
  items,
  onClose,
  onRemoveItem,
  onOpenGenerate,
  onSelectItem,
}) => {
  const hasItems = items.length > 0;

  return (
    <Modal
      visible={visible}
      animationType="slide"
      transparent={true}
      onRequestClose={onClose}
    >
      <View style={styles.overlay}>
        <SafeAreaView style={styles.safeArea}>
          <View style={styles.sheetContainer}>
            {/* Header with drag pill and close button */}
            <View style={styles.topHandleBar}>
              <View style={styles.dragPill} />
              <TouchableOpacity
                onPress={onClose}
                style={styles.closeBtn}
                hitSlop={{ top: 12, bottom: 12, left: 12, right: 12 }}
              >
                <Text style={styles.closeBtnText}>✕</Text>
              </TouchableOpacity>
            </View>

            <View style={styles.headerInfo}>
              <View style={styles.titleRow}>
                <Text style={styles.title}>STORYBOARD</Text>
                <View style={styles.countBadge}>
                  <Text style={styles.countBadgeText}>{items.length} References</Text>
                </View>
              </View>
              <Text style={styles.subtitle}>References for your next piece</Text>
            </View>

            {/* References Scroll View */}
            <ScrollView
              style={styles.listContainer}
              contentContainerStyle={styles.listContent}
              showsVerticalScrollIndicator={false}
            >
              {items.length === 0 ? (
                <View style={styles.emptyContainer}>
                  <Text style={styles.emptyIcon}>📂</Text>
                  <Text style={styles.emptyTitle}>Your Storyboard is Empty</Text>
                  <Text style={styles.emptySubtitle}>
                    Explore trending videos and reels, and tap "Add to Storyboard" to capture references for generation.
                  </Text>
                </View>
              ) : (
                items.map((item, index) => (
                  <View key={item.id} style={styles.itemCard}>
                    <TouchableOpacity
                      style={styles.itemMainClickable}
                      onPress={() => onSelectItem(item)}
                      activeOpacity={0.8}
                    >
                      <Image
                        source={{ uri: item.content.thumbnail }}
                        style={styles.itemThumbnail}
                      />
                      <View style={styles.itemTextContainer}>
                        <View style={styles.itemHeader}>
                          <Text style={styles.itemIndex}>#{index + 1}</Text>
                          <Text style={styles.itemPlatform}>
                            {item.content.platform.toUpperCase()}
                          </Text>
                        </View>
                        <Text style={styles.itemTitle} numberOfLines={2}>
                          {item.content.title}
                        </Text>
                        <Text style={styles.itemCreator}>By {item.content.creatorName}</Text>
                        {item.note && (
                          <Text style={styles.itemNote} numberOfLines={1}>
                            💡 {item.note}
                          </Text>
                        )}
                      </View>
                    </TouchableOpacity>

                    <TouchableOpacity
                      style={styles.removeBtn}
                      onPress={() => onRemoveItem(item.id)}
                      hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
                    >
                      <Text style={styles.removeBtnText}>🗑️</Text>
                    </TouchableOpacity>
                  </View>
                ))
              )}
            </ScrollView>

            {/* Bottom Generate CTA */}
            <View style={styles.bottomBar}>
              {!hasItems && (
                <Text style={styles.disabledHelperText}>
                  Add references to your storyboard to generate content.
                </Text>
              )}
              <TouchableOpacity
                style={[styles.generateBtn, !hasItems && styles.generateBtnDisabled]}
                onPress={onOpenGenerate}
                disabled={!hasItems}
                activeOpacity={0.85}
              >
                <Text style={styles.generateBtnIcon}>⚡</Text>
                <Text style={styles.generateBtnText}>
                  {hasItems ? `Generate Content from ${items.length} References` : "Generate Content"}
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
  overlay: {
    flex: 1,
    backgroundColor: "rgba(0, 0, 0, 0.75)",
    justifyContent: "flex-end",
  },
  safeArea: {
    maxHeight: "85%",
  },
  sheetContainer: {
    backgroundColor: "#0F172A",
    borderTopLeftRadius: 24,
    borderTopRightRadius: 24,
    borderTopWidth: 1,
    borderTopColor: "#334155",
    height: "100%",
    display: "flex",
  },
  topHandleBar: {
    alignItems: "center",
    paddingTop: 10,
    paddingBottom: 6,
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
    top: 6,
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
  headerInfo: {
    paddingHorizontal: 20,
    paddingBottom: 14,
    borderBottomWidth: 1,
    borderBottomColor: "#1E293B",
  },
  titleRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  title: {
    fontSize: 20,
    fontWeight: "800",
    color: "#FFFFFF",
    letterSpacing: 0.5,
  },
  countBadge: {
    backgroundColor: "#312E81",
    paddingHorizontal: 10,
    paddingVertical: 3,
    borderRadius: 12,
  },
  countBadgeText: {
    color: "#A5B4FC",
    fontSize: 12,
    fontWeight: "700",
  },
  subtitle: {
    fontSize: 13,
    color: "#94A3B8",
    marginTop: 2,
  },
  listContainer: {
    flex: 1,
  },
  listContent: {
    padding: 20,
  },
  emptyContainer: {
    alignItems: "center",
    justifyContent: "center",
    paddingVertical: 50,
    paddingHorizontal: 30,
  },
  emptyIcon: {
    fontSize: 48,
    marginBottom: 12,
  },
  emptyTitle: {
    fontSize: 17,
    fontWeight: "700",
    color: "#FFFFFF",
    marginBottom: 6,
  },
  emptySubtitle: {
    fontSize: 13,
    color: "#64748B",
    textAlign: "center",
    lineHeight: 19,
  },
  itemCard: {
    flexDirection: "row",
    backgroundColor: "#131C31",
    borderRadius: 14,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: "#1E293B",
    alignItems: "center",
    overflow: "hidden",
  },
  itemMainClickable: {
    flex: 1,
    flexDirection: "row",
    padding: 10,
    alignItems: "center",
  },
  itemThumbnail: {
    width: 65,
    height: 65,
    borderRadius: 8,
    marginRight: 12,
    backgroundColor: "#1E293B",
  },
  itemTextContainer: {
    flex: 1,
  },
  itemHeader: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 2,
  },
  itemIndex: {
    fontSize: 10,
    fontWeight: "800",
    color: "#6366F1",
    marginRight: 6,
  },
  itemPlatform: {
    fontSize: 9,
    fontWeight: "700",
    color: "#94A3B8",
  },
  itemTitle: {
    fontSize: 13,
    fontWeight: "700",
    color: "#FFFFFF",
    lineHeight: 18,
    marginBottom: 2,
  },
  itemCreator: {
    fontSize: 11,
    color: "#64748B",
  },
  itemNote: {
    fontSize: 11,
    color: "#A5B4FC",
    fontStyle: "italic",
    marginTop: 2,
  },
  removeBtn: {
    padding: 14,
    justifyContent: "center",
    alignItems: "center",
  },
  removeBtnText: {
    fontSize: 16,
  },
  bottomBar: {
    borderTopWidth: 1,
    borderTopColor: "#1E293B",
    padding: 18,
    backgroundColor: "#0F172A",
  },
  disabledHelperText: {
    fontSize: 12,
    color: "#F59E0B",
    textAlign: "center",
    marginBottom: 10,
    fontWeight: "500",
  },
  generateBtn: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#4F46E5",
    paddingVertical: 14,
    borderRadius: 14,
    shadowColor: "#4F46E5",
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 4,
  },
  generateBtnDisabled: {
    backgroundColor: "#1E293B",
    shadowOpacity: 0,
    elevation: 0,
  },
  generateBtnIcon: {
    fontSize: 16,
    marginRight: 8,
  },
  generateBtnText: {
    fontSize: 15,
    fontWeight: "700",
    color: "#FFFFFF",
  },
});
