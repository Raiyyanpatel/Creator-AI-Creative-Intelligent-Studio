import React from "react";
import {
  ScrollView,
  TouchableOpacity,
  Text,
  StyleSheet,
  View,
} from "react-native";
import { Region } from "../types/creatorIntelligence";

interface RegionTabsProps {
  selectedRegion: Region;
  onSelectRegion: (region: Region) => void;
}

const REGION_OPTIONS: { id: Region; label: string; icon: string }[] = [
  { id: "for_you", label: "For You", icon: "✨" },
  { id: "global", label: "Global", icon: "🌍" },
  { id: "india", label: "India", icon: "🇮🇳" },
  { id: "hyderabad", label: "Hyderabad", icon: "📍" },
  { id: "my_niche", label: "My Niche", icon: "🎯" },
];

export const RegionTabs: React.FC<RegionTabsProps> = ({
  selectedRegion,
  onSelectRegion,
}) => {
  return (
    <View style={styles.container}>
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.scrollContent}
      >
        {REGION_OPTIONS.map((item) => {
          const isSelected = selectedRegion === item.id;
          return (
            <TouchableOpacity
              key={item.id}
              style={[styles.tab, isSelected && styles.tabSelected]}
              onPress={() => onSelectRegion(item.id)}
              activeOpacity={0.7}
            >
              <Text style={styles.icon}>{item.icon}</Text>
              <Text style={[styles.tabText, isSelected && styles.tabTextSelected]}>
                {item.label}
              </Text>
            </TouchableOpacity>
          );
        })}
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginBottom: 16,
  },
  scrollContent: {
    paddingHorizontal: 20,
    gap: 8,
  },
  tab: {
    flexDirection: "row",
    alignItems: "center",
    paddingVertical: 7,
    paddingHorizontal: 14,
    borderRadius: 20,
    backgroundColor: "#0F172A",
    borderWidth: 1,
    borderColor: "#1E293B",
  },
  tabSelected: {
    backgroundColor: "#4F46E5",
    borderColor: "#6366F1",
  },
  icon: {
    fontSize: 12,
    marginRight: 6,
  },
  tabText: {
    fontSize: 13,
    fontWeight: "500",
    color: "#94A3B8",
  },
  tabTextSelected: {
    color: "#FFFFFF",
    fontWeight: "700",
  },
});
