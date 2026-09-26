import React from "react";
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  SafeAreaView,
  StatusBar,
  TouchableOpacity,
} from "react-native";
import {
  useCreatorIntelligenceStore,
} from "../state/creatorIntelligenceStore";
import { DiscoveryTab, Trend, ContentItem, TopicItem, Creator } from "../types/creatorIntelligence";
import { Header } from "../components/Header";
import { SearchBar } from "../components/SearchBar";
import { RegionTabs } from "../components/RegionTabs";
import { TrendCard } from "../components/TrendCard";
import { ContentCard } from "../components/ContentCard";
import { CreatorCard } from "../components/CreatorCard";
import { TopicCard } from "../components/TopicCard";
import { ContentDetailModal } from "../components/ContentDetailModal";
import { StoryboardSheet } from "../components/StoryboardSheet";
import { GenerateContentScreen } from "./GenerateContentScreen";
import { Toast } from "../components/Toast";
import { searchService } from "../services/searchService";

const DISCOVERY_TABS: { id: DiscoveryTab; label: string; countLabel?: string }[] = [
  { id: "videos", label: "Videos" },
  { id: "reels", label: "Reels" },
  { id: "creators", label: "Creators" },
  { id: "topics", label: "Topics" },
  { id: "saved", label: "Saved" },
];

export const CreatorIntelligenceScreen: React.FC = () => {
  const {
    selectedRegion,
    selectedDiscoveryTab,
    searchQuery,
    searchResults,
    isSearching,
    bookmarkedItems,
    storyboardItems,
    selectedContent,
    detailModalVisible,
    storyboardSheetVisible,
    generateModalVisible,
    toastMessage,
    setRegion,
    setDiscoveryTab,
    setSearchQuery,
    clearSearch,
    toggleBookmark,
    addToStoryboard,
    removeFromStoryboard,
    openContentDetail,
    closeContentDetail,
    setStoryboardSheetVisible,
    openGenerateModal,
    closeGenerateModal,
  } = useCreatorIntelligenceStore();

  // Retrieve regional content when not in search mode
  const regionContent = searchService.getContentByRegion(selectedRegion);

  const handleTrendClick = (trend: Trend) => {
    setSearchQuery(trend.topic);
  };

  const handleTopicClick = (topic: TopicItem) => {
    setSearchQuery(topic.name);
  };

  const handleCreatorClick = (creator: Creator) => {
    setSearchQuery(creator.name);
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar barStyle="light-content" backgroundColor="#0B1120" />
      <View style={styles.container}>
        {/* Top Header with live signal badge & storyboard button */}
        <Header
          storyboardCount={storyboardItems.length}
          onOpenStoryboard={() => setStoryboardSheetVisible(true)}
        />

        {/* Global Search Bar */}
        <SearchBar
          value={searchQuery}
          onChangeText={setSearchQuery}
          onClear={clearSearch}
        />

        <ScrollView
          style={styles.mainScroll}
          contentContainerStyle={styles.mainScrollContent}
          showsVerticalScrollIndicator={false}
        >
          {/* SEARCH MODE RESULTS */}
          {isSearching ? (
            <View style={styles.searchResultsContainer}>
              <View style={styles.searchHeaderRow}>
                <Text style={styles.searchHeaderTitle}>
                  SEARCH RESULTS ({searchResults.totalMatches} MATCHES)
                </Text>
                <TouchableOpacity onPress={clearSearch} style={styles.clearSearchTextBtn}>
                  <Text style={styles.clearSearchText}>Clear search</Text>
                </TouchableOpacity>
              </View>

              {searchResults.totalMatches === 0 ? (
                <View style={styles.emptySearchBox}>
                  <Text style={styles.emptySearchIcon}>🔍</Text>
                  <Text style={styles.emptySearchTitle}>No results found</Text>
                  <Text style={styles.emptySearchSubtitle}>
                    Try another topic, creator handle, or broader keyword like "AI", "Hyderabad", or "Video".
                  </Text>
                </View>
              ) : (
                <>
                  {/* GROUP: TRENDS */}
                  {searchResults.trends.length > 0 && (
                    <View style={styles.groupSection}>
                      <Text style={styles.groupTitle}>📈 TRENDS ({searchResults.trends.length})</Text>
                      <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.horizontalScroll}>
                        {searchResults.trends.map((trend, idx) => (
                          <TrendCard
                            key={trend.id}
                            trend={trend}
                            rank={idx + 1}
                            onPress={handleTrendClick}
                          />
                        ))}
                      </ScrollView>
                    </View>
                  )}

                  {/* GROUP: CREATORS */}
                  {searchResults.creators.length > 0 && (
                    <View style={styles.groupSection}>
                      <Text style={styles.groupTitle}>👥 CREATORS ({searchResults.creators.length})</Text>
                      {searchResults.creators.map((creator) => (
                        <CreatorCard
                          key={creator.id}
                          creator={creator}
                          onPress={handleCreatorClick}
                        />
                      ))}
                    </View>
                  )}

                  {/* GROUP: VIDEOS */}
                  {searchResults.videos.length > 0 && (
                    <View style={styles.groupSection}>
                      <Text style={styles.groupTitle}>▶ VIDEOS ({searchResults.videos.length})</Text>
                      {searchResults.videos.map((vid) => (
                        <ContentCard
                          key={vid.id}
                          content={vid}
                          isBookmarked={bookmarkedItems.some((b) => b.id === vid.id)}
                          isInStoryboard={storyboardItems.some((s) => s.contentId === vid.id)}
                          onPressCard={openContentDetail}
                          onToggleBookmark={toggleBookmark}
                          onAddToStoryboard={addToStoryboard}
                        />
                      ))}
                    </View>
                  )}

                  {/* GROUP: REELS */}
                  {searchResults.reels.length > 0 && (
                    <View style={styles.groupSection}>
                      <Text style={styles.groupTitle}>📸 REELS & SHORTS ({searchResults.reels.length})</Text>
                      {searchResults.reels.map((reel) => (
                        <ContentCard
                          key={reel.id}
                          content={reel}
                          isBookmarked={bookmarkedItems.some((b) => b.id === reel.id)}
                          isInStoryboard={storyboardItems.some((s) => s.contentId === reel.id)}
                          onPressCard={openContentDetail}
                          onToggleBookmark={toggleBookmark}
                          onAddToStoryboard={addToStoryboard}
                        />
                      ))}
                    </View>
                  )}

                  {/* GROUP: TOPICS */}
                  {searchResults.topics.length > 0 && (
                    <View style={styles.groupSection}>
                      <Text style={styles.groupTitle}>🏷️ TOPICS ({searchResults.topics.length})</Text>
                      {searchResults.topics.map((top) => (
                        <TopicCard
                          key={top.id}
                          topic={top}
                          onPress={handleTopicClick}
                        />
                      ))}
                    </View>
                  )}
                </>
              )}
            </View>
          ) : (
            /* DEFAULT EXPLORE MODE */
            <>
              {/* Horizontal Region Tabs */}
              <RegionTabs
                selectedRegion={selectedRegion}
                onSelectRegion={setRegion}
              />

              {/* SECTION 1 — TRENDING NOW */}
              <View style={styles.sectionHeader}>
                <View style={styles.sectionTitleRow}>
                  <Text style={styles.sectionTitle}>TRENDING NOW</Text>
                  <View style={styles.activeRegionBadge}>
                    <Text style={styles.activeRegionBadgeText}>
                      {selectedRegion.replace("_", " ").toUpperCase()}
                    </Text>
                  </View>
                </View>
                <Text style={styles.sectionSubtitle}>
                  High-velocity spikes across creator discussions
                </Text>
              </View>

              <ScrollView
                horizontal
                showsHorizontalScrollIndicator={false}
                contentContainerStyle={styles.trendsScrollContent}
              >
                {regionContent.trends.map((trend, idx) => (
                  <TrendCard
                    key={trend.id}
                    trend={trend}
                    rank={idx + 1}
                    onPress={handleTrendClick}
                  />
                ))}
              </ScrollView>

              {/* SECTION 2 — DISCOVER */}
              <View style={styles.discoverHeader}>
                <Text style={styles.sectionTitle}>DISCOVER</Text>
                <Text style={styles.sectionSubtitle}>
                  Curated content and creators worth analyzing
                </Text>

                {/* Sub-tabs: [Creators] [Videos] [Reels] [Topics] [Saved] */}
                <View style={styles.subTabsContainer}>
                  {DISCOVERY_TABS.map((tab) => {
                    const isSelected = selectedDiscoveryTab === tab.id;
                    const savedCount = tab.id === "saved" ? bookmarkedItems.length : undefined;
                    return (
                      <TouchableOpacity
                        key={tab.id}
                        style={[styles.subTab, isSelected && styles.subTabSelected]}
                        onPress={() => setDiscoveryTab(tab.id)}
                        activeOpacity={0.7}
                      >
                        <Text style={[styles.subTabText, isSelected && styles.subTabTextSelected]}>
                          {tab.label} {savedCount !== undefined ? `(${savedCount})` : ""}
                        </Text>
                      </TouchableOpacity>
                    );
                  })}
                </View>
              </View>

              {/* DISCOVER CONTENT LIST BASED ON ACTIVE SUB-TAB */}
              <View style={styles.cardsFeed}>
                {selectedDiscoveryTab === "videos" &&
                  regionContent.videos.map((vid) => (
                    <ContentCard
                      key={vid.id}
                      content={vid}
                      isBookmarked={bookmarkedItems.some((b) => b.id === vid.id)}
                      isInStoryboard={storyboardItems.some((s) => s.contentId === vid.id)}
                      onPressCard={openContentDetail}
                      onToggleBookmark={toggleBookmark}
                      onAddToStoryboard={addToStoryboard}
                    />
                  ))}

                {selectedDiscoveryTab === "reels" &&
                  regionContent.reels.map((reel) => (
                    <ContentCard
                      key={reel.id}
                      content={reel}
                      isBookmarked={bookmarkedItems.some((b) => b.id === reel.id)}
                      isInStoryboard={storyboardItems.some((s) => s.contentId === reel.id)}
                      onPressCard={openContentDetail}
                      onToggleBookmark={toggleBookmark}
                      onAddToStoryboard={addToStoryboard}
                    />
                  ))}

                {selectedDiscoveryTab === "creators" &&
                  regionContent.creators.map((creator) => (
                    <CreatorCard
                      key={creator.id}
                      creator={creator}
                      onPress={handleCreatorClick}
                    />
                  ))}

                {selectedDiscoveryTab === "topics" &&
                  regionContent.topics.map((topic) => (
                    <TopicCard
                      key={topic.id}
                      topic={topic}
                      onPress={handleTopicClick}
                    />
                  ))}

                {selectedDiscoveryTab === "saved" &&
                  (bookmarkedItems.length === 0 ? (
                    <View style={styles.emptySavedBox}>
                      <Text style={styles.emptySavedIcon}>☆</Text>
                      <Text style={styles.emptySavedTitle}>No Saved Items Yet</Text>
                      <Text style={styles.emptySavedSubtitle}>
                        Tap the "Bookmark" button on any video or reel to save it for later review.
                      </Text>
                    </View>
                  ) : (
                    bookmarkedItems.map((item) => (
                      <ContentCard
                        key={item.id}
                        content={item}
                        isBookmarked={true}
                        isInStoryboard={storyboardItems.some((s) => s.contentId === item.id)}
                        onPressCard={openContentDetail}
                        onToggleBookmark={toggleBookmark}
                        onAddToStoryboard={addToStoryboard}
                      />
                    ))
                  ))}
              </View>
            </>
          )}
        </ScrollView>

        {/* MODAL 1: Content Detail Sheet */}
        <ContentDetailModal
          visible={detailModalVisible}
          content={selectedContent}
          isBookmarked={
            selectedContent
              ? bookmarkedItems.some((b) => b.id === selectedContent.id)
              : false
          }
          isInStoryboard={
            selectedContent
              ? storyboardItems.some((s) => s.contentId === selectedContent.id)
              : false
          }
          onClose={closeContentDetail}
          onToggleBookmark={toggleBookmark}
          onAddToStoryboard={addToStoryboard}
        />

        {/* MODAL 2: Storyboard Reference Sheet */}
        <StoryboardSheet
          visible={storyboardSheetVisible}
          items={storyboardItems}
          onClose={() => setStoryboardSheetVisible(false)}
          onRemoveItem={removeFromStoryboard}
          onOpenGenerate={openGenerateModal}
          onSelectItem={(item) => {
            setStoryboardSheetVisible(false);
            openContentDetail(item.content);
          }}
        />

        {/* MODAL 3: Generate Content Screen (with AI Copilot & Final Tabs) */}
        <GenerateContentScreen
          visible={generateModalVisible}
          onClose={closeGenerateModal}
        />

        {/* Floating Toast Message */}
        <Toast message={toastMessage} />
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: "#0B1120",
  },
  container: {
    flex: 1,
    backgroundColor: "#0B1120",
  },
  mainScroll: {
    flex: 1,
  },
  mainScrollContent: {
    paddingBottom: 40,
  },
  sectionHeader: {
    paddingHorizontal: 20,
    marginBottom: 10,
  },
  sectionTitleRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  sectionTitle: {
    fontSize: 13,
    fontWeight: "800",
    color: "#CBD5E1",
    letterSpacing: 0.8,
  },
  activeRegionBadge: {
    backgroundColor: "#1E293B",
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 6,
  },
  activeRegionBadgeText: {
    fontSize: 10,
    color: "#818CF8",
    fontWeight: "700",
  },
  sectionSubtitle: {
    fontSize: 12,
    color: "#64748B",
    marginTop: 2,
  },
  trendsScrollContent: {
    paddingLeft: 20,
    paddingRight: 8,
    paddingBottom: 22,
  },
  discoverHeader: {
    paddingHorizontal: 20,
    marginBottom: 14,
    borderTopWidth: 1,
    borderTopColor: "#131C31",
    paddingTop: 18,
  },
  subTabsContainer: {
    flexDirection: "row",
    backgroundColor: "#0F172A",
    borderRadius: 12,
    padding: 3,
    marginTop: 12,
    borderWidth: 1,
    borderColor: "#1E293B",
  },
  subTab: {
    flex: 1,
    paddingVertical: 8,
    alignItems: "center",
    borderRadius: 9,
  },
  subTabSelected: {
    backgroundColor: "#1E293B",
  },
  subTabText: {
    fontSize: 12,
    fontWeight: "600",
    color: "#64748B",
  },
  subTabTextSelected: {
    color: "#FFFFFF",
    fontWeight: "700",
  },
  cardsFeed: {
    paddingHorizontal: 20,
  },
  searchResultsContainer: {
    paddingHorizontal: 20,
  },
  searchHeaderRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 16,
  },
  searchHeaderTitle: {
    fontSize: 11,
    fontWeight: "800",
    color: "#94A3B8",
    letterSpacing: 0.6,
  },
  clearSearchTextBtn: {
    paddingVertical: 4,
    paddingHorizontal: 6,
  },
  clearSearchText: {
    fontSize: 12,
    color: "#818CF8",
    fontWeight: "600",
  },
  groupSection: {
    marginBottom: 20,
  },
  groupTitle: {
    fontSize: 12,
    fontWeight: "800",
    color: "#E2E8F0",
    marginBottom: 10,
    letterSpacing: 0.6,
  },
  horizontalScroll: {
    flexDirection: "row",
    marginBottom: 6,
  },
  emptySearchBox: {
    alignItems: "center",
    paddingVertical: 60,
    paddingHorizontal: 20,
  },
  emptySearchIcon: {
    fontSize: 42,
    marginBottom: 12,
  },
  emptySearchTitle: {
    fontSize: 18,
    fontWeight: "700",
    color: "#FFFFFF",
    marginBottom: 6,
  },
  emptySearchSubtitle: {
    fontSize: 13,
    color: "#64748B",
    textAlign: "center",
    lineHeight: 19,
  },
  emptySavedBox: {
    alignItems: "center",
    paddingVertical: 50,
    paddingHorizontal: 20,
    backgroundColor: "#0F172A",
    borderRadius: 16,
    borderWidth: 1,
    borderColor: "#1E293B",
  },
  emptySavedIcon: {
    fontSize: 40,
    color: "#64748B",
    marginBottom: 10,
  },
  emptySavedTitle: {
    fontSize: 16,
    fontWeight: "700",
    color: "#FFFFFF",
    marginBottom: 6,
  },
  emptySavedSubtitle: {
    fontSize: 12,
    color: "#64748B",
    textAlign: "center",
    lineHeight: 18,
  },
});

export default CreatorIntelligenceScreen;
