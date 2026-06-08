import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, RefreshControl, TouchableOpacity, ActivityIndicator } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { fetchDiagnosticTests } from '../services/api';

export default function AnalysisScreen() {
  const [refreshing, setRefreshing] = useState(false);
  const [tests, setTests] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      const data = await fetchDiagnosticTests();
      setTests(data);
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
        <Text style={styles.headerTitle}>Gelişim Analizi</Text>
        <Text style={styles.headerSubtitle}>Teşhis Testleri ve Puan Hesaplama</Text>
      </View>

      {/* Puan Hesaplama Modülü (Mock) */}
      <TouchableOpacity style={[styles.card, styles.primaryCard]}>
        <View style={styles.cardIcon}>
          <Ionicons name="calculator" size={28} color="#fff" />
        </View>
        <View style={styles.cardContent}>
          <Text style={styles.cardTitleLight}>YKS / LGS Puan Hesaplama</Text>
          <Text style={styles.cardSubtitleLight}>Güncel katsayılarla netlerini gir, sıralamanı gör.</Text>
        </View>
        <Ionicons name="chevron-forward" size={24} color="#fff" />
      </TouchableOpacity>

      <Text style={styles.sectionTitle}>Teşhis Testleri</Text>
      
      {loading ? (
        <ActivityIndicator size="large" color="#4F46E5" style={{ marginTop: 20 }} />
      ) : tests.length === 0 ? (
        <Text style={styles.emptyText}>Henüz aktif test bulunmuyor.</Text>
      ) : (
        tests.map((test) => (
          <TouchableOpacity key={test.id} style={styles.card}>
            <View style={[styles.cardIcon, { backgroundColor: '#EEF2FF' }]}>
              <Ionicons name="document-text" size={24} color="#4F46E5" />
            </View>
            <View style={styles.cardContent}>
              <Text style={styles.cardTitle}>{test.title}</Text>
              <Text style={styles.cardSubtitle}>
                {test.target_exam.toUpperCase()} • {test.question_count} Soru
              </Text>
            </View>
            <Ionicons name="play-circle" size={28} color="#4F46E5" />
          </TouchableOpacity>
        ))
      )}

      {/* Hata Defteri Modülü (Mock) */}
      <TouchableOpacity style={[styles.card, { marginTop: 20 }]}>
        <View style={[styles.cardIcon, { backgroundColor: '#FEF2F2' }]}>
          <Ionicons name="book" size={24} color="#EF4444" />
        </View>
        <View style={styles.cardContent}>
          <Text style={styles.cardTitle}>Hata Defteri</Text>
          <Text style={styles.cardSubtitle}>Yanlış yaptığın konuları kaydet.</Text>
        </View>
        <Ionicons name="chevron-forward" size={24} color="#9CA3AF" />
      </TouchableOpacity>

      <View style={{ height: 40 }} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F9FAFB', // Gray 50
    padding: 16,
  },
  header: {
    marginBottom: 24,
    marginTop: 8,
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: '900',
    color: '#111827',
  },
  headerSubtitle: {
    fontSize: 16,
    color: '#6B7280',
    marginTop: 4,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#374151',
    marginBottom: 16,
    marginTop: 8,
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 16,
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
  },
  primaryCard: {
    backgroundColor: '#4F46E5',
    shadowColor: '#4F46E5',
    shadowOpacity: 0.2,
    marginBottom: 24,
  },
  cardIcon: {
    width: 48,
    height: 48,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(255,255,255,0.2)',
  },
  cardContent: {
    flex: 1,
    marginLeft: 16,
  },
  cardTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#1F2937',
    marginBottom: 4,
  },
  cardSubtitle: {
    fontSize: 13,
    color: '#6B7280',
  },
  cardTitleLight: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 4,
  },
  cardSubtitleLight: {
    fontSize: 13,
    color: '#E0E7FF',
  },
  emptyText: {
    color: '#9CA3AF',
    textAlign: 'center',
    fontStyle: 'italic',
    marginTop: 10,
  },
});
