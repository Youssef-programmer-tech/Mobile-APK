import React, { useState, useEffect } from 'react';
import { 
  View, 
  Text, 
  FlatList, 
  TouchableOpacity, 
  StyleSheet, 
  ActivityIndicator,
  ScrollView,
  SafeAreaView,
  StatusBar,
  TextInput,
  Modal,
  Image,
  KeyboardAvoidingView,
  Platform
} from 'react-native';
import MapView, { Marker } from 'react-native-maps';
import axios from 'axios';

const API_BASE = 'http://192.168.1.100:5000'; // Change to your IP

export default function App() {
  const [artifacts, setArtifacts] = useState([]);
  const [selectedTab, setSelectedTab] = useState('map');
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedArtifact, setSelectedArtifact] = useState(null);
  const [modalVisible, setModalVisible] = useState(false);
  const [statusFilter, setStatusFilter] = useState('all');
  const [aiAssistantVisible, setAiAssistantVisible] = useState(false);
  const [aiMessage, setAiMessage] = useState('');
  const [aiResponse, setAiResponse] = useState('');
  const [aiLoading, setAiLoading] = useState(false);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);

  useEffect(() => {
    loadArtifacts();
  }, []);

  const loadArtifacts = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE}/api/artifacts`);
      setArtifacts(response.data);
    } catch (error) {
      console.error('Error loading artifacts:', error);
      setArtifacts(getSampleArtifacts());
    } finally {
      setLoading(false);
    }
  };

  const getSampleArtifacts = () => [
    {
      id: 1,
      name: 'Rosetta Stone',
      museum: 'British Museum',
      city: 'London',
      country: 'United Kingdom',
      latitude: 51.5194,
      longitude: -0.1270,
      status: 'Contested',
      year_taken: 1801,
      description: 'Key artifact that helped decipher Egyptian hieroglyphs. Taken by French then British forces during the Napoleonic campaigns.',
      artifact_type: 'Granodiorite Stone',
      current_location: 'British Museum, London',
      image_url: 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Rosetta_Stone_BM_BNC.jpg/800px-Rosetta_Stone_BM_BNC.jpg',
      images: [
        'https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Rosetta_Stone_BM_BNC.jpg/800px-Rosetta_Stone_BM_BNC.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Rosetta_Stone%2C_British_Museum.jpg/800px-Rosetta_Stone%2C_British_Museum.jpg'
      ]
    },
    {
      id: 2,
      name: 'Bust of Nefertiti',
      museum: 'Neues Museum',
      city: 'Berlin',
      country: 'Germany',
      latitude: 52.5200,
      longitude: 13.3967,
      status: 'Contested',
      year_taken: 1912,
      description: 'Famous limestone bust of Egyptian Queen Nefertiti. Egypt claims it was smuggled out illegally by German archaeologist Ludwig Borchardt.',
      artifact_type: 'Limestone Bust',
      current_location: 'Neues Museum, Berlin',
      image_url: 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Neues_Museum_-_Nefertiti_%28profile%29.jpg/800px-Neues_Museum_-_Nefertiti_%28profile%29.jpg',
      images: [
        'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Neues_Museum_-_Nefertiti_%28profile%29.jpg/800px-Neues_Museum_-_Nefertiti_%28profile%29.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Neues_Museum_Berlin_045.jpg/800px-Neues_Museum_Berlin_045.jpg'
      ]
    },
    // Add more artifacts with images...
  ];

  const askAI = async (message = null) => {
    const question = message || aiMessage;
    if (!question.trim()) return;

    setAiLoading(true);
    try {
      const response = await axios.post(`${API_BASE}/api/ai-assistant`, {
        message: question
      });
      setAiResponse(response.data.response);
      setAiMessage('');
    } catch (error) {
      setAiResponse("I'm having trouble connecting right now. Try asking me about the map, artifacts, or navigation!");
    } finally {
      setAiLoading(false);
    }
  };

  const quickQuestions = [
    "How to use the map?",
    "What are contested artifacts?",
    "Tell me about the Rosetta Stone",
    "How do I search artifacts?"
  ];

  const openArtifactDetails = (artifact) => {
    setSelectedArtifact(artifact);
    setCurrentImageIndex(0);
    setModalVisible(true);
  };

  const nextImage = () => {
    if (selectedArtifact && selectedArtifact.images) {
      setCurrentImageIndex((prev) => 
        prev === selectedArtifact.images.length - 1 ? 0 : prev + 1
      );
    }
  };

  const prevImage = () => {
    if (selectedArtifact && selectedArtifact.images) {
      setCurrentImageIndex((prev) => 
        prev === 0 ? selectedArtifact.images.length - 1 : prev - 1
      );
    }
  };

  // ... (rest of your filtering and rendering functions remain the same)

  const renderArtifactModal = () => (
    <Modal
      animationType="slide"
      transparent={true}
      visible={modalVisible}
      onRequestClose={() => setModalVisible(false)}
    >
      <View style={styles.modalContainer}>
        <View style={styles.modalContent}>
          {selectedArtifact && (
            <>
              <View style={styles.modalHeader}>
                <Text style={styles.modalTitle}>{selectedArtifact.name}</Text>
                <TouchableOpacity 
                  style={styles.closeButton}
                  onPress={() => setModalVisible(false)}
                >
                  <Text style={styles.closeButtonText}>✕</Text>
                </TouchableOpacity>
              </View>
              
              <ScrollView style={styles.modalBody}>
                {/* Image Gallery */}
                {selectedArtifact.images && selectedArtifact.images.length > 0 && (
                  <View style={styles.imageGallery}>
                    <Image 
                      source={{ uri: selectedArtifact.images[currentImageIndex] }}
                      style={styles.artifactImage}
                      resizeMode="cover"
                    />
                    {selectedArtifact.images.length > 1 && (
                      <View style={styles.imageControls}>
                        <TouchableOpacity style={styles.imageButton} onPress={prevImage}>
                          <Text style={styles.imageButtonText}>‹</Text>
                        </TouchableOpacity>
                        <Text style={styles.imageCounter}>
                          {currentImageIndex + 1} / {selectedArtifact.images.length}
                        </Text>
                        <TouchableOpacity style={styles.imageButton} onPress={nextImage}>
                          <Text style={styles.imageButtonText}>›</Text>
                        </TouchableOpacity>
                      </View>
                    )}
                  </View>
                )}
                
                <View style={styles.modalSection}>
                  <Text style={styles.modalLabel}>🏛️ Museum</Text>
                  <Text style={styles.modalText}>{selectedArtifact.museum}</Text>
                </View>
                
                {/* ... rest of modal sections ... */}
              </ScrollView>
            </>
          )}
        </View>
      </View>
    </Modal>
  );

  const renderAIAssistant = () => (
    <Modal
      animationType="slide"
      transparent={true}
      visible={aiAssistantVisible}
      onRequestClose={() => setAiAssistantVisible(false)}
    >
      <View style={styles.aiModalContainer}>
        <View style={styles.aiModalContent}>
          <View style={styles.aiHeader}>
            <Text style={styles.aiTitle}>🏺 AI Assistant</Text>
            <TouchableOpacity 
              style={styles.closeButton}
              onPress={() => setAiAssistantVisible(false)}
            >
              <Text style={styles.closeButtonText}>✕</Text>
            </TouchableOpacity>
          </View>
          
          <ScrollView style={styles.aiChat}>
            <View style={styles.aiMessage}>
              <Text style={styles.aiResponseText}>
                {aiResponse || "Hello! I'm your Egyptian Artifacts assistant. Ask me about navigation, artifacts, or anything else!"}
              </Text>
            </View>
            
            {quickQuestions.map((question, index) => (
              <TouchableOpacity 
                key={index}
                style={styles.quickQuestion}
                onPress={() => {
                  setAiMessage(question);
                  askAI(question);
                }}
              >
                <Text style={styles.quickQuestionText}>{question}</Text>
              </TouchableOpacity>
            ))}
          </ScrollView>
          
          <View style={styles.aiInputContainer}>
            <TextInput
              style={styles.aiInput}
              placeholder="Ask me anything about artifacts..."
              value={aiMessage}
              onChangeText={setAiMessage}
              onSubmitEditing={() => askAI()}
            />
            <TouchableOpacity 
              style={styles.aiSendButton}
              onPress={() => askAI()}
              disabled={aiLoading}
            >
              <Text style={styles.aiSendButtonText}>
                {aiLoading ? "..." : "Send"}
              </Text>
            </TouchableOpacity>
          </View>
        </View>
      </View>
    </Modal>
  );

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar backgroundColor="#8B4513" barStyle="light-content" />
      
      {/* Header with AI Assistant Button */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>🏺 Egyptian Artifacts</Text>
        <TouchableOpacity 
          style={styles.aiButton}
          onPress={() => setAiAssistantVisible(true)}
        >
          <Text style={styles.aiButtonText}>🤖 AI Help</Text>
        </TouchableOpacity>
      </View>

      {/* Content */}
      <View style={styles.content}>
        {selectedTab === 'map' && renderMap()}
        {selectedTab === 'list' && renderList()}
        {selectedTab === 'stats' && renderStats()}
      </View>

      {/* Tab Bar */}
      <View style={styles.tabBar}>
        <TouchableOpacity 
          style={[styles.tabButton, selectedTab === 'map' && styles.tabButtonActive]} 
          onPress={() => setSelectedTab('map')}
        >
          <Text style={[styles.tabText, selectedTab === 'map' && styles.tabTextActive]}>
            🗺️ Map
          </Text>
        </TouchableOpacity>
        
        <TouchableOpacity 
          style={[styles.tabButton, selectedTab === 'list' && styles.tabButtonActive]} 
          onPress={() => setSelectedTab('list')}
        >
          <Text style={[styles.tabText, selectedTab === 'list' && styles.tabTextActive]}>
            📋 List
          </Text>
        </TouchableOpacity>
        
        <TouchableOpacity 
          style={[styles.tabButton, selectedTab === 'stats' && styles.tabButtonActive]} 
          onPress={() => setSelectedTab('stats')}
        >
          <Text style={[styles.tabText, selectedTab === 'stats' && styles.tabTextActive]}>
            📊 Stats
          </Text>
        </TouchableOpacity>
      </View>

      {/* Modals */}
      {renderArtifactModal()}
      {renderAIAssistant()}
    </SafeAreaView>
  );
}

// Add these new styles to your existing styles:
const styles = StyleSheet.create({
  // ... your existing styles ...
  
  // AI Assistant Styles
  aiButton: {
    backgroundColor: 'rgba(255,255,255,0.2)',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 15,
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.3)',
  },
  aiButtonText: {
    color: 'white',
    fontSize: 12,
    fontWeight: '600',
  },
  aiModalContainer: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  aiModalContent: {
    backgroundColor: 'white',
    borderRadius: 16,
    margin: 20,
    maxHeight: '80%',
    width: '90%',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 10,
  },
  aiHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
    backgroundColor: '#8B4513',
    borderTopLeftRadius: 16,
    borderTopRightRadius: 16,
  },
  aiTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: 'white',
  },
  aiChat: {
    padding: 20,
    maxHeight: 300,
  },
  aiMessage: {
    backgroundColor: '#f8f9fa',
    padding: 15,
    borderRadius: 12,
    marginBottom: 15,
  },
  aiResponseText: {
    fontSize: 16,
    lineHeight: 22,
    color: '#333',
  },
  quickQuestion: {
    backgroundColor: '#e8f4f8',
    padding: 12,
    borderRadius: 8,
    marginBottom: 8,
    borderWidth: 1,
    borderColor: '#b8e0f0',
  },
  quickQuestionText: {
    fontSize: 14,
    color: '#2c5aa0',
  },
  aiInputContainer: {
    flexDirection: 'row',
    padding: 15,
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
  },
  aiInput: {
    flex: 1,
    backgroundColor: '#f8f9fa',
    padding: 12,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#e0e0e0',
    marginRight: 10,
  },
  aiSendButton: {
    backgroundColor: '#8B4513',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 8,
    justifyContent: 'center',
  },
  aiSendButtonText: {
    color: 'white',
    fontWeight: '600',
  },
  
  // Image Gallery Styles
  imageGallery: {
    marginBottom: 20,
  },
  artifactImage: {
    width: '100%',
    height: 250,
    borderRadius: 12,
  },
  imageControls: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 10,
  },
  imageButton: {
    backgroundColor: '#8B4513',
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  imageButtonText: {
    color: 'white',
    fontSize: 20,
    fontWeight: 'bold',
  },
  imageCounter: {
    fontSize: 14,
    fontWeight: '600',
    color: '#666',
  },
});