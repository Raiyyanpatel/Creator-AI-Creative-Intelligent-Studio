import React from "react";
import {
  View,
  TextInput,
  StyleSheet,
  TouchableOpacity,
  Text,
} from "react-native";

interface SearchBarProps {
  value: string;
  onChangeText: (text: string) => void;
  onClear: () => void;
}

export const SearchBar: React.FC<SearchBarProps> = ({
  value,
  onChangeText,
  onClear,
}) => {
  return (
    <View style={styles.wrapper}>
      <View style={[styles.container, value.length > 0 && styles.containerActive]}>
        <Text style={styles.searchIcon}>🔍</Text>
        <TextInput
          style={styles.input}
          placeholder="Search trends, creators, videos, topics..."
          placeholderTextColor="#64748B"
          value={value}
          onChangeText={onChangeText}
          autoCorrect={false}
          autoCapitalize="none"
          returnKeyType="search"
        />
        {value.length > 0 && (
          <TouchableOpacity
            onPress={onClear}
            style={styles.clearButton}
            hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
          >
            <View style={styles.clearBadge}>
              <Text style={styles.clearText}>✕</Text>
            </View>
          </TouchableOpacity>
        )}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  wrapper: {
    paddingHorizontal: 20,
    marginBottom: 12,
  },
  container: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#0F172A",
    borderRadius: 14,
    paddingHorizontal: 14,
    paddingVertical: 10,
    borderWidth: 1,
    borderColor: "#1E293B",
  },
  containerActive: {
    borderColor: "#4F46E5",
    backgroundColor: "#131C31",
  },
  searchIcon: {
    fontSize: 14,
    marginRight: 10,
  },
  input: {
    flex: 1,
    color: "#F8FAFC",
    fontSize: 14,
    padding: 0,
    fontWeight: "400",
  },
  clearButton: {
    marginLeft: 8,
  },
  clearBadge: {
    width: 20,
    height: 20,
    borderRadius: 10,
    backgroundColor: "#334155",
    alignItems: "center",
    justifyContent: "center",
  },
  clearText: {
    color: "#94A3B8",
    fontSize: 10,
    fontWeight: "700",
  },
});
