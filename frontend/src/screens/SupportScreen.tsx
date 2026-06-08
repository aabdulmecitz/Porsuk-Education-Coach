import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, RefreshControl, TouchableOpacity, Image, Linking, ActivityIndicator } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { fetchAppSettings } from '../services/api';

export default function SupportScreen() {
  const [refreshing, setRefreshing] = useState(false);
  const [settings, setSettings] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      const data = await fetchAppSettings();
      setSettings(data);
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

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#4F46E5" />
      </View>
    );
  }

  if (!settings) {
    return (
      <View style={styles.loadingContainer}>
        <Text style={{ color: '#6B7280' }}>Bağlantı kurulamadı.</Text>
      </View>
    );
  }

  return (
    <ScrollView 
      style={styles.container}
      refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
    >
      {/* Teacher Profile Card */}
      <View style={styles.profileCard}>
        {settings.teacher_photo_url ? (
          <Image source={{ uri: settings.teacher_photo_url }} style={styles.avatar} />
        ) : (
          <View style={[styles.avatar, styles.avatarPlaceholder]}>
            <Ionicons name="person" size={40} color="#9CA3AF" />
          </View>
        )}
        <Text style={styles.name}>{settings.teacher_name}</Text>
        <Text style={styles.title}>{settings.teacher_title || 'Eğitim Danışmanı'}</Text>
        
        {settings.teacher_bio ? (
          <Text style={styles.bio}>{settings.teacher_bio}</Text>
        ) : null}
      </View>

      {/* Primary CTA */}
      <View style={styles.ctaCard}>
        <Text style={styles.ctaTitle}>{settings.cta_text}</Text>
        {settings.cta_subtitle ? (
          <Text style={styles.ctaSubtitle}>{settings.cta_subtitle}</Text>
        ) : null}
        
        {settings.calendly_url ? (
          <TouchableOpacity 
            style={styles.primaryButton}
            onPress={() => Linking.openURL(settings.calendly_url)}
          >
            <Ionicons name="calendar-outline" size={20} color="#fff" />
            <Text style={styles.primaryButtonText}>Ücretsiz Randevu Al</Text>
          </TouchableOpacity>
        ) : null}

        {settings.whatsapp_url ? (
          <TouchableOpacity 
            style={styles.whatsappButton}
            onPress={() => Linking.openURL(settings.whatsapp_url)}
          >
            <Ionicons name="logo-whatsapp" size={20} color="#fff" />
            <Text style={styles.primaryButtonText}>WhatsApp'tan Yaz</Text>
          </TouchableOpacity>
        ) : null}
      </View>

      {/* Social Links */}
      <View style={styles.socialRow}>
        {settings.instagram_url ? (
          <TouchableOpacity 
            style={styles.socialBtn}
            onPress={() => Linking.openURL(settings.instagram_url)}
          >
            <Ionicons name="logo-instagram" size={24} color="#E1306C" />
          </View>
        ) : null}
        {settings.youtube_url ? (
          <TouchableOpacity 
            style={styles.socialBtn}
            onPress={() => Linking.openURL(settings.youtube_url)}
          >
            <Ionicons name="logo-youtube" size={24} color="#FF0000" />
          </TouchableOpacity>
        ) : null}
        {settings.website_url ? (
          <TouchableOpacity 
            style={styles.socialBtn}
            onPress={() => Linking.openURL(settings.website_url)}
          >
            <Ionicons name="globe-outline" size={24} color="#4F46E5" />
          </TouchableOpacity>
        ) : null}
      </View>

      <View style={{ height: 40 }} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#EEF2FF',
  },
  container: {
    flex: 1,
    backgroundColor: '#EEF2FF',
    padding: 16,
  },
  profileCard: {
    backgroundColor: '#fff',
    borderRadius: 24,
    padding: 24,
    alignItems: 'center',
    shadowColor: '#4F46E5',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 12,
    elevation: 5,
    marginBottom: 20,
  },
  avatar: {
    width: 100,
    height: 100,
    borderRadius: 50,
    marginBottom: 16,
  },
  avatarPlaceholder: {
    backgroundColor: '#F3F4F6',
    justifyContent: 'center',
    alignItems: 'center',
  },
  name: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#1F2937',
    marginBottom: 4,
  },
  title: {
    fontSize: 15,
    color: '#6366F1',
    fontWeight: '600',
    marginBottom: 12,
  },
  bio: {
    fontSize: 15,
    color: '#4B5563',
    textAlign: 'center',
    lineHeight: 22,
  },
  ctaCard: {
    backgroundColor: '#fff',
    borderRadius: 24,
    padding: 24,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
    marginBottom: 20,
  },
  ctaTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1F2937',
    textAlign: 'center',
    marginBottom: 8,
  },
  ctaSubtitle: {
    fontSize: 14,
    color: '#6B7280',
    textAlign: 'center',
    marginBottom: 20,
  },
  primaryButton: {
    backgroundColor: '#4F46E5',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 14,
    borderRadius: 12,
    marginBottom: 12,
  },
  whatsappButton: {
    backgroundColor: '#25D366',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 14,
    borderRadius: 12,
  },
  primaryButtonText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
    marginLeft: 8,
  },
  socialRow: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 16,
  },
  socialBtn: {
    backgroundColor: '#fff',
    width: 50,
    height: 50,
    borderRadius: 25,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 1,
  },
});
