import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, RefreshControl, TouchableOpacity, Image, Linking } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { fetchExamDates, fetchLatestDailyQuestion, fetchRandomQuote } from '../services/api';

export default function HomeScreen() {
  const [refreshing, setRefreshing] = useState(false);
  const [examDates, setExamDates] = useState<any[]>([]);
  const [dailyQuestion, setDailyQuestion] = useState<any>(null);
  const [quote, setQuote] = useState<any>(null);
  const [pomodoroTime, setPomodoroTime] = useState(25 * 60); // 25 mins
  const [isPomodoroRunning, setIsPomodoroRunning] = useState(false);

  const loadData = async () => {
    try {
      const [exams, question, randomQuote] = await Promise.all([
        fetchExamDates(),
        fetchLatestDailyQuestion().catch(() => null),
        fetchRandomQuote().catch(() => null)
      ]);
      setExamDates(exams);
      setDailyQuestion(question);
      setQuote(randomQuote);
    } catch (error) {
      console.error(error);
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

  // Pomodoro Timer Logic
  useEffect(() => {
    let interval: any = null;
    if (isPomodoroRunning && pomodoroTime > 0) {
      interval = setInterval(() => {
        setPomodoroTime((time) => time - 1);
      }, 1000);
    } else if (pomodoroTime === 0) {
      setIsPomodoroRunning(false);
    }
    return () => clearInterval(interval);
  }, [isPomodoroRunning, pomodoroTime]);

  const togglePomodoro = () => setIsPomodoroRunning(!isPomodoroRunning);
  const resetPomodoro = () => {
    setIsPomodoroRunning(false);
    setPomodoroTime(25 * 60);
  };

  const formatTime = (time: number) => {
    const mins = Math.floor(time / 60);
    const secs = time % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <ScrollView 
      style={styles.container}
      refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
    >
      {/* Motivational Quote */}
      {quote && (
        <View style={styles.quoteCard}>
          <Text style={styles.quoteText}>"{quote.quote}"</Text>
          <Text style={styles.quoteAuthor}>— {quote.author}</Text>
        </View>
      )}

      {/* Exam Countdown */}
      {examDates.length > 0 && (
        <LinearGradient colors={['#4F46E5', '#6366F1']} style={styles.card}>
          <View style={styles.cardHeader}>
            <Ionicons name="timer-outline" size={24} color="#fff" />
            <Text style={styles.cardTitle}>Sınavlara Kalan Zaman</Text>
          </View>
          {examDates.map((exam, index) => (
            <View key={exam.id} style={[styles.examRow, index !== examDates.length - 1 && styles.borderBottom]}>
              <Text style={styles.examName}>{exam.name}</Text>
              <View style={styles.badge}>
                <Text style={styles.badgeText}>{exam.days_remaining} Gün</Text>
              </View>
            </View>
          ))}
        </LinearGradient>
      )}

      {/* Daily Question */}
      {dailyQuestion && (
        <View style={[styles.card, styles.glassCard]}>
          <View style={styles.cardHeader}>
            <Ionicons name="bulb-outline" size={24} color="#312E81" />
            <Text style={[styles.cardTitle, { color: '#312E81' }]}>Günün Sorusu</Text>
          </View>
          <Text style={styles.questionTitle}>{dailyQuestion.title}</Text>
          {dailyQuestion.question_text ? (
            <Text style={styles.questionText}>{dailyQuestion.question_text}</Text>
          ) : null}
          {dailyQuestion.question_image_url && (
            <Image 
              source={{ uri: dailyQuestion.question_image_url }} 
              style={styles.questionImage} 
              resizeMode="contain" 
            />
          )}
          {dailyQuestion.solution_url && (
            <TouchableOpacity 
              style={styles.solutionButton} 
              onPress={() => Linking.openURL(dailyQuestion.solution_url)}
            >
              <Ionicons name="play-circle-outline" size={20} color="#fff" />
              <Text style={styles.solutionButtonText}>Çözümü İzle</Text>
            </TouchableOpacity>
          )}
        </View>
      )}

      {/* Pomodoro Timer */}
      <View style={[styles.card, styles.pomodoroCard]}>
        <Text style={styles.pomodoroTitle}>🍅 Pomodoro Sayacı</Text>
        <Text style={styles.pomodoroTimer}>{formatTime(pomodoroTime)}</Text>
        <View style={styles.pomodoroControls}>
          <TouchableOpacity style={[styles.pomodoroButton, isPomodoroRunning ? styles.pauseBtn : styles.startBtn]} onPress={togglePomodoro}>
            <Text style={styles.pomodoroButtonText}>{isPomodoroRunning ? 'Durdur' : 'Başlat'}</Text>
          </TouchableOpacity>
          <TouchableOpacity style={[styles.pomodoroButton, styles.resetBtn]} onPress={resetPomodoro}>
            <Text style={styles.pomodoroButtonText}>Sıfırla</Text>
          </TouchableOpacity>
        </View>
      </View>

      <View style={{ height: 40 }} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#EEF2FF', // Indigo 50
    padding: 16,
  },
  quoteCard: {
    backgroundColor: '#fff',
    padding: 16,
    borderRadius: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
    borderLeftWidth: 4,
    borderLeftColor: '#F59E0B',
  },
  quoteText: {
    fontSize: 15,
    fontStyle: 'italic',
    color: '#4B5563',
    lineHeight: 22,
  },
  quoteAuthor: {
    fontSize: 13,
    fontWeight: 'bold',
    color: '#9CA3AF',
    marginTop: 8,
    textAlign: 'right',
  },
  card: {
    borderRadius: 20,
    padding: 20,
    marginBottom: 20,
    shadowColor: '#4F46E5',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 12,
    elevation: 5,
  },
  glassCard: {
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    shadowColor: '#000',
    shadowOpacity: 0.1,
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
    marginLeft: 8,
  },
  examRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 12,
  },
  borderBottom: {
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(255,255,255,0.2)',
  },
  examName: {
    fontSize: 16,
    color: '#fff',
    fontWeight: '600',
  },
  badge: {
    backgroundColor: 'rgba(255,255,255,0.2)',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
  },
  badgeText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 14,
  },
  questionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1F2937',
    marginBottom: 8,
  },
  questionText: {
    fontSize: 15,
    color: '#4B5563',
    lineHeight: 24,
    marginBottom: 16,
  },
  questionImage: {
    width: '100%',
    height: 200,
    borderRadius: 12,
    marginBottom: 16,
  },
  solutionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#EC4899', // Pink 500 for instagram feel
    padding: 12,
    borderRadius: 12,
  },
  solutionButtonText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
    marginLeft: 8,
  },
  pomodoroCard: {
    backgroundColor: '#fff',
    alignItems: 'center',
  },
  pomodoroTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#374151',
    marginBottom: 16,
  },
  pomodoroTimer: {
    fontSize: 56,
    fontWeight: '900',
    color: '#EF4444', // Red 500
    fontVariant: ['tabular-nums'],
    marginBottom: 20,
  },
  pomodoroControls: {
    flexDirection: 'row',
    gap: 16,
  },
  pomodoroButton: {
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 24,
    minWidth: 100,
    alignItems: 'center',
  },
  startBtn: {
    backgroundColor: '#10B981', // Emerald 500
  },
  pauseBtn: {
    backgroundColor: '#F59E0B', // Amber 500
  },
  resetBtn: {
    backgroundColor: '#6B7280', // Gray 500
  },
  pomodoroButtonText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  },
});
