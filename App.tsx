import React from 'react';
import { StatusBar } from 'react-native';
import CreatorIntelligenceScreen from './src/features/creator-intelligence/screens/CreatorIntelligenceScreen';

export default function App() {
  return (
    <>
      <StatusBar barStyle="light-content" backgroundColor="#0B0F19" />
      <CreatorIntelligenceScreen />
    </>
  );
}
