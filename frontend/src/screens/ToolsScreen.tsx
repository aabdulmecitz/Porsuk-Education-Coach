import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, RefreshControl, TouchableOpacity, ActivityIndicator } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { fetchFormulas } from '../services/api';

export default function ToolsScreen() {
  const [refreshing, setRefreshing] = useState(false);
  const [formulas, setFormulas] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      const data = await fetchFormulas();
      setFormulas(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadData();
    setRefreshing(false);
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <ScrollView 
      style={styles.container}
      refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
    >
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Matematik Araçları</Text>
        <Text style={styles.headerSubtitle}>İsviçre Çakısı Modülleri</Text>
      </View>

      <View style={styles.gridContainer}>
        {/* Adım Adım Çarpanlara Ayırma */}
        <TouchableOpacity style={styles.gridItem}>
          <View style={[styles.iconWrapper, { backgroundColor: '#DBEAFE' }]}>
            <Ionicons name="git-merge" size={32} color="#2563EB" />
          </View>
          <Text style={styles.gridTitle}>Çarpanlara Ayırma</Text>
          <Text style={styles.gridSubtitle}>Adım Adım Motor</Text>
        </TouchableOpacity>

        {/* Fonksiyon Grafiği Simülatörü */}
        <TouchableOpacity style={styles.gridItem}>
          <View style={[styles.iconWrapper, { backgroundColor: '#FCE7F3' }]}>
            <Ionicons name="analytics" size={32} color="#DB2777" />
          </View>
          <Text style={styles.gridTitle}>Grafik Simülatörü</Text>
          <Text style={styles.gridSubtitle}>f(x) Görselleştir</Text>
        </TouchableOpacity>

        {/* İnteraktif Birim Çember */}
        <TouchableOpacity style={styles.gridItem}>
          <View style={[styles.iconWrapper, { backgroundColor: '#FEF3C7' }]}>
            <Ionicons name="scan-circle" size={32} color="#D97706" />
          </View>
          <Text style={styles.gridTitle}>Birim Çember</Text>
          <Text style={styles.gridSubtitle}>Trigonometri Modülü</Text>
        </TouchableOpacity>
      </View>

      <Text style={styles.sectionTitle}>Formül Sihirbazı</Text>

      {loading ? (
        <ActivityIndicator size="large" color="#4F46E5" style={{ marginTop: 20 }} />
      ) : formulas.length === 0 ? (
        <Text style={styles.emptyText}>Henüz formül kartı bulunmuyor.</Text>
      ) : (
        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.horizontalScroll}>
          {formulas.map((formula) => (
            <View key={formula.id} style={styles.formulaCard}>
              <View style={styles.formulaHeader}>
                <Text style={styles.formulaTopic}>{formula.topic_display}</Text>
              </View>
              <Text style={styles.formulaTitle}>{formula.title}</Text>
              <View style={styles.formulaBox}>
                <Text style={styles.formulaText}>{formula.formula_text}</Text>
              </View>
              {formula.explanation ? (
                <Text style={styles.formulaExplanation}>{formula.explanation}</Text>
              ) : null}
            </View>
          ))}
        </ScrollView>
      )}

      <View style={{ height: 40 }} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F9FAFB', // Gray 50
  },
  header: {
    padding: 20,
    backgroundColor: '#4F46E5', // Indigo 600
    borderBottomLeftRadius: 30,
    borderBottomRightRadius: 30,
    marginBottom: 20,
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: '900',
    color: '#fff',
  },
  headerSubtitle: {
    fontSize: 16,
    color: '#E0E7FF',
    marginTop: 4,
    marginBottom: 10,
  },
  gridContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    paddingHorizontal: 10,
    justifyContent: 'space-between',
  },
  gridItem: {
    width: '46%',
    backgroundColor: '#fff',
    borderRadius: 20,
    padding: 16,
    alignItems: 'center',
    marginBottom: 16,
    marginHorizontal: '2%',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
  },
  iconWrapper: {
    width: 64,
    height: 64,
    borderRadius: 32,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
  },
  gridTitle: {
    fontSize: 15,
    fontWeight: 'bold',
    color: '#1F2937',
    textAlign: 'center',
    marginBottom: 4,
  },
  gridSubtitle: {
    fontSize: 12,
    color: '#6B7280',
    textAlign: 'center',
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#374151',
    marginHorizontal: 16,
    marginTop: 16,
    marginBottom: 16,
  },
  horizontalScroll: {
    paddingLeft: 16,
  },
  formulaCard: {
    width: 280,
    backgroundColor: '#fff',
    borderRadius: 20,
    padding: 20,
    marginRight: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 12,
    elevation: 4,
  },
  formulaHeader: {
    alignSelf: 'flex-start',
    backgroundColor: '#EEF2FF',
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 12,
    marginBottom: 12,
  },
  formulaTopic: {
    color: '#4F46E5',
    fontSize: 12,
    fontWeight: 'bold',
  },
  formulaTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#111827',
    marginBottom: 16,
  },
  formulaBox: {
    backgroundColor: '#F3F4F6',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 16,
  },
  formulaText: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#EF4444',
    textAlign: 'center',
    fontFamily: 'serif',
  },
  formulaExplanation: {
    fontSize: 14,
    color: '#4B5563',
    lineHeight: 20,
  },
  emptyText: {
    color: '#9CA3AF',
    textAlign: 'center',
    fontStyle: 'italic',
    marginHorizontal: 16,
  },
});
