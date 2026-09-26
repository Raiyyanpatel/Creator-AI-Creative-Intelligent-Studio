import { MOCK_TRENDS } from "../data/mockTrends";
import { MOCK_CREATORS } from "../data/mockCreators";
import { MOCK_CONTENT } from "../data/mockContent";
import { MOCK_TOPICS } from "../data/mockTopics";
import { SearchResultsGrouped, Region } from "../types/creatorIntelligence";

export const searchService = {
  /**
   * Searches across trends, creators, videos, reels, and topics.
   * Returns grouped results ready for UI rendering.
   */
  search(query: string, regionFilter?: Region): SearchResultsGrouped {
    const cleanQ = query.trim().toLowerCase();
    if (!cleanQ) {
      return {
        trends: [],
        creators: [],
        videos: [],
        reels: [],
        topics: [],
        totalMatches: 0,
      };
    }

    const matchesTrend = MOCK_TRENDS.filter(
      (t) =>
        t.topic.toLowerCase().includes(cleanQ) ||
        t.explanation.toLowerCase().includes(cleanQ) ||
        t.category.toLowerCase().includes(cleanQ) ||
        t.relatedTopics?.some((rt) => rt.toLowerCase().includes(cleanQ))
    );

    const matchesCreator = MOCK_CREATORS.filter(
      (c) =>
        c.name.toLowerCase().includes(cleanQ) ||
        c.handle.toLowerCase().includes(cleanQ) ||
        c.niche.toLowerCase().includes(cleanQ) ||
        c.bio?.toLowerCase().includes(cleanQ)
    );

    const matchesVideo = MOCK_CONTENT.filter(
      (v) =>
        v.type === "video" &&
        (v.title.toLowerCase().includes(cleanQ) ||
          v.creatorName.toLowerCase().includes(cleanQ) ||
          v.topics.some((top) => top.toLowerCase().includes(cleanQ)) ||
          v.whyTrending?.toLowerCase().includes(cleanQ))
    );

    const matchesReel = MOCK_CONTENT.filter(
      (r) =>
        r.type === "reel" &&
        (r.title.toLowerCase().includes(cleanQ) ||
          r.creatorName.toLowerCase().includes(cleanQ) ||
          r.topics.some((top) => top.toLowerCase().includes(cleanQ)) ||
          r.whyTrending?.toLowerCase().includes(cleanQ))
    );

    const matchesTopic = MOCK_TOPICS.filter(
      (top) =>
        top.name.toLowerCase().includes(cleanQ) ||
        top.category.toLowerCase().includes(cleanQ) ||
        top.description.toLowerCase().includes(cleanQ)
    );

    const totalMatches =
      matchesTrend.length +
      matchesCreator.length +
      matchesVideo.length +
      matchesReel.length +
      matchesTopic.length;

    return {
      trends: matchesTrend,
      creators: matchesCreator,
      videos: matchesVideo,
      reels: matchesReel,
      topics: matchesTopic,
      totalMatches,
    };
  },

  /**
   * Retrieves content filtered by region for tab views.
   */
  getContentByRegion(region: Region) {
    if (region === "for_you") {
      return {
        trends: MOCK_TRENDS.filter((t) => t.region === "for_you" || t.growth >= 30),
        creators: MOCK_CREATORS.slice(0, 6),
        videos: MOCK_CONTENT.filter((c) => c.type === "video" && (c.region === "for_you" || c.trendScore >= 35)),
        reels: MOCK_CONTENT.filter((c) => c.type === "reel" && (c.region === "for_you" || c.trendScore >= 35)),
        topics: MOCK_TOPICS.filter((t) => t.region === "for_you" || t.growth >= 40),
      };
    }

    return {
      trends: MOCK_TRENDS.filter((t) => t.region === region),
      creators: MOCK_CREATORS.filter((c) => {
        if (region === "hyderabad") return c.handle.includes("hyderabad") || c.handle.includes("telugu");
        if (region === "india") return c.platform === "instagram" || c.handle.includes("dhruv") || c.handle.includes("sharan");
        if (region === "my_niche") return c.niche.toLowerCase().includes("ai") || c.niche.toLowerCase().includes("product");
        return true;
      }),
      videos: MOCK_CONTENT.filter((c) => c.type === "video" && (c.region === region || region === "global")),
      reels: MOCK_CONTENT.filter((c) => c.type === "reel" && (c.region === region || region === "global")),
      topics: MOCK_TOPICS.filter((t) => t.region === region),
    };
  },
};
