import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QTextEdit, QMessageBox, QWidget, QTabWidget
from PyQt5.QtGui import QPixmap
import numpy as np
from motivationMessage import get_random_motivation
import tensorflow as tf
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
from PyQt5.QtWidgets import QMessageBox
from getmusic import MusicRecommendation

class DailyJournalApp(QMainWindow):
   
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Diary Analysis Application")
        self.setGeometry(100, 100, 300, 500)

        background_image = QLabel(self)
        pixmap = QPixmap("C:\\Users\\secii\\OneDrive\\Masaüstü\\LLM\\assets\\arkaplann.jpeg")
        background_image.setPixmap(pixmap)
        background_image.setGeometry(0, 0, self.width() + 800, self.height())
        background_image.setScaledContents(True)

        self.tab_widget = QTabWidget()

        self.login_tab = QWidget()
        self.setup_login_tab()

        self.journal_tab = QWidget()
        self.setup_journal_tab()

        self.tab_widget.addTab(self.login_tab, "Home")
        self.tab_widget.addTab(self.journal_tab, "Diary")

        self.setCentralWidget(self.tab_widget)

        self.model, self.tokenizer = self.load_model()
        self.music_recommendation = MusicRecommendation()
        

    def setup_login_tab(self):
        layout = QVBoxLayout()

        image_label = QLabel(self.login_tab)
        pixmap = QPixmap("C:\\Users\\secii\\OneDrive\\Masaüstü\\LLM\\assets\\home_page.png")
        image_label.setPixmap(pixmap)

        text_label = QLabel("HOME PAGE", self.login_tab)
        text_label.setStyleSheet("font-size: 20px; color: white;")

        layout.addWidget(image_label)
        layout.addWidget(text_label)
        self.login_tab.setLayout(layout)

    def setup_journal_tab(self):
        layout = QVBoxLayout()

        self.label = QLabel("Dear Diary;")
        self.label.setStyleSheet("background-color: white; color: #d686ed; font-size: 20px; font-style: italic; font-weight: bold;")

        self.text_edit = QTextEdit()
        self.text_edit.setStyleSheet("font-size: 17px;font-style: italic;")
        self.analyze_button = QPushButton("Analyze It")
        self.analyze_button.clicked.connect(self.analyze_journal)
        self.analyze_button.setStyleSheet("background-color: #d686ed; color: white; font-size: 20px")

        self.link_label = QLabel("<a href='https://www.youtube.com/' style='color:  #d686ed;font-weight: bold; '>This is exactly your mood today :)</a>")
        self.link_label.setStyleSheet("color: white; font-size: 17px")
        self.link_label.setOpenExternalLinks(True)

        layout.addWidget(self.label)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.analyze_button)
        layout.addWidget(self.link_label)

        journal_widget = QWidget(self.journal_tab)
        journal_widget.setGeometry(self.width()/2.3, 0, self.width()+400, self.height()+35)
        journal_widget.setLayout(layout)

    def load_model(self):
        # Hugging Face'de kaydettiğiniz modelin repository ID'si
        repo_id = 'sevvalkapcak/newModel2'

        # Model yükleme
        tokenizer = AutoTokenizer.from_pretrained(repo_id)
        model = TFAutoModelForSequenceClassification.from_pretrained(repo_id)
        
        return model, tokenizer

    def preprocess_text(self, text, max_length=512):
        inputs = self.tokenizer(text, truncation=True, padding=True, return_tensors="tf", max_length=max_length)
        return tuple((inputs['input_ids'], inputs['attention_mask']))

    
    def analyze_journal(self):
        
        user_text = self.text_edit.toPlainText()
        inputs_tuple = self.preprocess_text(user_text)

        logits = self.model.predict(inputs_tuple)[0]
        probabilities = tf.nn.softmax(logits)
        predicted_class = np.argmax(probabilities)
        probability_predicted_emotion = probabilities[0][predicted_class].numpy()

        emotion_labels = ['sadness', 'joy', 'love', 'anger', 'fear', 'surprise']
        predicted_emotion = emotion_labels[predicted_class]

        result_text = f"Analysis result: {predicted_emotion} (Probability: {probability_predicted_emotion})"
        print(result_text)

        song_link = self.music_recommendation.get_random_track_from_playlist(predicted_emotion)

        if song_link:
            self.link_label.setText(f"<a href='{song_link}' style='color:  #d686ed;font-weight: bold;font-style: italic; '>This is exactly your mood today :)</a>")
        else:
            self.link_label.setText("<a href='https://www.youtube.com/' style='color:  #d686ed;font-weight: bold; '>This is exactly your mood today :)</a>")
            
        
        # Motivasyon dosyasından rastgele yazı alınır
        random_motivation = get_random_motivation(predicted_emotion)
        print(f"{predicted_emotion.capitalize()} {random_motivation}")
        
        # MessageBox içinde motivasyon yazısı gösterilir
        QMessageBox.information(None, "MOTIVATION", f"{random_motivation}")


if __name__ == "__main__":
    app = QApplication([])
    window = DailyJournalApp()
    window.show()
    sys.exit(app.exec_())
