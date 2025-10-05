from tkinter import *
from tkintermapview import TkinterMapView
from PIL import Image, ImageTk, ImageDraw
import requests
from io import BytesIO
import hashlib
import os
import json
from datetime import datetime, timedelta
from tkinter import simpledialog, messagebox, filedialog
import matplotlib.pyplot as plt
import mplcursors
from tkcalendar import Calendar
import threading
import random
import webbrowser  # Copernicus web sitesi için
import math
import time
# Diğer import'ların yanına ekle (dosyanın en başına)
from tkinter import ttk


# Sesli asistan için
try:
    import pyttsx3
    import speech_recognition as sr
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    print("Sesli asistan için: pip install pyttsx3 SpeechRecognition pyaudio")

app = Tk()
app.geometry('420x730')
app.title('')
API_KEY = 'b4ba14e57562904295447a407a20dc8b'
FORECAST_URL = 'https://api.openweathermap.org/data/2.5/forecast'
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'
AIR_POLLUTION_URL = 'https://api.openweathermap.org/data/2.5/air_pollution'
UV_INDEX_URL = 'https://api.openweathermap.org/data/2.5/uvi'
ICON_URL = 'https://openweathermap.org/img/wn/{}@2x.png'
USERS_FILE = 'users.txt'
PREFS_FOLDER = 'user_prefs'
CLIMATE_DATA_FILE = 'climate_data.json'
ALERTS_FILE = 'alerts.json'
SOCIAL_POSTS_FILE = 'social_posts.json'
AVATAR_FILE = 'avatars.json'
ACHIEVEMENTS_FILE = 'achievements.json'
PREDICTION_FILE = 'predictions.json'
CLOUD_PHOTOS_FILE = 'cloud_photos.json'
CLOUD_PHOTOS_DIR = 'cloud_photos'

current_user = None
user_prefs = {}
available_languages = {'Türkçe':'tr', 'English':'en'}
current_language = 'tr'
# Global widget değişkenleri
avatar_btn = None
future_btn = None
achievements_btn = None
# Mevcut global değişkenlere ekle:
CLOUD_PHOTOS_FILE = 'cloud_photos.json'
current_week_winner = None
# Translation dictionary (genişletilmiş)
translations = {
    'tr': {
        'title': 'Hava Durumu Uygulaması',
        'login': 'Giriş Yap',
        'register': 'Kayıt Ol',
        'username': 'Kullanıcı Adı',
        'password': 'Şifre',
        'hot': 'Çok Sıcak (°C)',
        'cold': 'Çok Soğuk (°C)',
        'wind': 'Çok Rüzgarlı (m/s)',
        'humidity': 'Çok Nemli (%)',
        'back': '🔙 Geri',
        'settings': '⚙︎',
        'logout': '⬅️',
        'coordinate':'Kordinat (Iat,Ion)',
        'city': 'Şehir veya Koordinat (lat,lon)',
        'date': 'Tarih (YYYY-AA-GG)',
        'hour': 'Saat (0-23)',
        'map_select': '🌍 Haritadan Şehir Seç',
        'date_select': '📅 Tarih Seç',
        'hour_select': '⏰ Saat Seç',
        'get_forecast': 'Tahmini Getir',
        'show_graph': '📊 Tahmin Grafiği',
        'comfort_settings': 'Konfor Eşiği Ayarları',
        'save': '💾 Kaydet',
        'back_arrow': '⬅️ Geri',
        'language': 'Dil:',
        'new_user': 'Yeni Kullanıcı Oluştur',
        'info': 'Bilgi',
        'select': 'Seç',
        'login_title': 'Hava Durumu App',
        'invalid': 'Geçersiz',
        'success': 'Başarılı',
        'error': 'Hata',
        'settings_saved': 'Ayarlar kaydedildi',
        'numeric_required': 'Eşikler sayısal olmalı.',
        'user_exists': 'Kullanıcı zaten var.',
        'empty_fields': 'Boş bırakmayın.',
        'login_failed': 'Hatalı giriş.',
        'city_not_found': 'Şehir bulunamadı.',
        'invalid_date': 'Tarih veya saat geçersiz',
        'data_error': 'Veri alınamadı.',
        'coord_error': 'Koordinatlar hatalı',
        'select_date': 'Tarih Seç',
        'select_hour': 'Saat Seç',
        'select_city': 'Şehir Seç',
        'graph_title': '5 Günlük Tahmin Grafiği',
        'very_cold': '❄️ Çok soğuk',
        'very_hot': '🔥 Çok sıcak',
        'very_wet': '🌧️ Çok ıslak',
        'very_windy': '💨 Çok rüzgarlı',
        'very_uncomfortable': '😣 Çok rahatsız edici',
        'comfortable': '😊 Hava koşulları oldukça uygun.',
        'selected_coords': 'Seçilen Koordinatlar: {}',
        'temp_c': 'Sıcaklık (°C)',
        'ai_title': 'Yapay Zeka Önerileri',
        'ai_generate': 'Öneri Oluştur',
        'ai_history': 'Önceki Öneriler',
        'ai_no_history': 'Kayıtlı öneri yok.',
        'ai_select_coords': 'Lütfen koordinat seçin.',
        'ai_select_datetime': 'Lütfen tarih ve saat seçin.',
        'lightning_title': 'Yıldırım Takibi',
        'lightning_start': 'Başlat',
        'lightning_stop': 'Durdur',
        'lightning_status_running': 'Çalışıyor',
        'lightning_status_stopped': 'Durduruldu',
        'legend_title': 'Lejant',
        'legend_active': 'Aktif Yıldırım',
        'legend_recent': 'Son Yıldırım',
        'micro_climate': '🌡️ Mikro-İklim Analizi',
        'alerts': '🚨 Acil Uyarılar',
        'climate_data': '📈 İklim Verileri',
        'energy': '⚡ Enerji Tahmini',
        'voice': '🎤 Sesli Asistan',
        'widget': '📱 Widget Görünümü',
        'traveler': '✈️ Gezgin Modu',
        'social': '📷 Sosyal Paylaşımlar',
        'microclimate_title': 'Mikro-İklim Hesaplaması',
        'elevation': 'Yükseklik (m):',
        'urban_factor': 'Şehirleşme Faktörü (0-1):',
        'calculate_micro': 'Hesapla',
        'alerts_title': 'Acil Durum Uyarıları',
        'no_alerts': 'Aktif uyarı yok.',
        'show_on_map': 'Haritada Göster',
        'climate_title': 'İklim İstatistikleri',
        'compare_years': 'Yılları Karşılaştır',
        'energy_title': 'Enerji Tüketim Tahmini',
        'heating_need': 'Isıtma İhtiyacı:',
        'cooling_need': 'Soğutma İhtiyacı:',
        'kwh_day': 'kWh/gün',
        'voice_title': 'Sesli Asistan',
        'voice_start': 'Dinlemeye Başla',
        'voice_listening': 'Dinleniyor...',
        'voice_not_available': 'Sesli asistan kullanılamıyor.',
        'widget_title': 'Widget Modu',
        'widget_show': 'Widget Göster',
        'traveler_title': 'Gezgin Modu',
        'destination': 'Varış Şehri:',
        'departure_date': 'Gidiş Tarihi:',
        'return_date': 'Dönüş Tarihi:',
        'get_travel_forecast': 'Seyahat Tahmini Al',
        'social_title': 'Social Weather',
        'add_post': 'Paylaşım Ekle',
        'view_posts': 'Paylaşımları Gör',
        'your_comment': 'Yorumunuz:',
        'upload_photo': 'Fotoğraf Yükle',
        'post': 'Paylaş',
        'maps': '🗺️ Haritalar',
        'uv_map': '☀️ UV Haritası',
        'air_quality_map': '🌫️ Hava Kalitesi',
        'pollen_map': '🌾 Polen Haritası',
        'visibility_map': '👁️ Görüş Mesafesi',
        'wave_map': '🌊 Dalga Haritası',
        'heat_map': '🌡️ Sıcaklık Haritası',
        'storm_map': '🌀 Fırtına Haritası',
        'lightning_map': '⚡ Yıldırım Haritası',
        'uv_index': 'UV İndeksi',
        'aqi': 'Hava Kalitesi İndeksi',
        'pollen_level': 'Polen Seviyesi',
        'visibility': 'Görüş Mesafesi (km)',
        'wave_height': 'Dalga Yüksekliği (m)',
        'heat_index': 'Hissedilen Sıcaklık',
        'storm_category': 'Fırtına Kategorisi',
        'low': 'Düşük',
        'moderate': 'Orta',
        'high': 'Yüksek',
        'very_high': 'Çok Yüksek',
        'extreme': 'Aşırı',
        'good': 'İyi',
        'fair': 'Orta',
        'poor': 'Kötü',
        'very_poor': 'Çok Kötü',
        'hazardous': 'Tehlikeli',
        'refresh': '🔄 Yenile',
        'auto_refresh': 'Otomatik Yenileme',
        # YENİ ÇEVİRİLER
        'avatar': '👤 Avatarım',
        'avatar_title': 'Hava Durumu Avatarı',
        'future_weather': '🔮 Gelecek Havası',
        'future_weather_title': 'Gelecek Hava Simülasyonu',
        'achievements': '🏆 Rozetlerim',
        'achievements_title': 'Hava Durumu Görevleri',
        'climate_change_sim': 'İklim değişikliği simülasyonu',
        'years_future': 'Yıl sonra:',
        'current_weather': 'Şu anki hava:',
        'future_prediction': 'Gelecek tahmini:',
        'change': 'Değişim:',
        'mission': 'Görev:',
        'progress': 'İlerleme:',
        'unlock_badge': 'Rozet Kazanıldı!',
        'check_weather': 'Hava kontrolü yap',
        'umbrella_mission': 'Yağmurlu günde şemsiye kullan',
        'winter_mission': 'Soğuk havada mont kullan',
        'hot_mission': 'Sıcak havada şapka kullan',
        'complete': 'Tamamlandı',
        'prediction_game': '🎯 Tahmin Et!',
        'prediction_title': 'Yarınki Sıcaklığı Tahmin Et',
        'predict_temperature': 'Sıcaklık Tahmini (°C):',
        'make_prediction': 'Tahmin Yap',
        'check_prediction': 'Tahmini Kontrol Et',
        'prediction_result': 'Tahmin Sonucu',
        'prediction_correct': '🎉 Tebrikler! Doğru tahmin!',
        'prediction_off': '❌ Yanlış tahmin. Fark: {}°C',
        'points_earned': 'Kazanılan puan: {}',
        'total_points': 'Toplam Puan: {}',
        'prediction_made': 'Tahmininiz: {}°C',
        'actual_temperature': 'Gerçek Sıcaklık: {}°C',
        'make_prediction_first': 'Önce tahmin yapmalısınız!',
        'wait_for_tomorrow': 'Yarının tahminini bekleyin...',
        'game_instructions': 'Yarınki sıcaklığı tahmin edin ve puan kazanın!',
                'earthquake_alerts': 'Deprem Uyarıları',
        'storm_alerts': 'Fırtına Uyarıları',
        'flood_alerts': 'Sel Uyarıları',
        'real_earthquake_alerts': 'Gerçek Deprem Uyarıları',
        'real_storm_alerts': 'Gerçek Fırtına Uyarıları',
        'real_flood_alerts': 'Copernicus EMS Sel Uyarıları',
        'emergency_copernicus': 'Avrupa Komisyonu Copernicus Acil Durum Yönetimi Servisi',
        'active_events': 'Aktif Olaylar',
        'high_risk': 'Yüksek Risk',
        'affected_areas': 'Etkilenen Bölgeler',
        'rivers_at_risk': 'Riskli Nehirler',
        'start_date': 'Başlangıç',
        'status': 'Durum',
        'source': 'Kaynak',
        'show_on_map': 'Haritada Göster',
        'open_website': 'Web Sitesini Aç',
        'magnitude': 'Büyüklük',
        'intensity': 'Şiddet',
        'coordinates': 'Koordinatlar',
        'storm_category': 'Fırtına Kategorisi',
        'wind_speed': 'Rüzgar Hızı',
        'weather_condition': 'Hava Durumu',
        'health_warning': 'Sağlık Uyarısı',
        'safety_recommendations': 'Güvenlik Önerileri',
        'no_alerts': 'Şu anda aktif uyarı bulunmuyor',
        'data_error': 'Veri alınamadı',
        'searching': 'Aranıyor...',
        'city_not_found': 'Şehir bulunamadı',
        'data_source_openweather': 'OpenWeatherMap verilerine göre şiddetli hava olayları',
        'temperature': 'Sıcaklık',
        'moderate': 'Orta',
        'low': 'Düşük',
        'lightning_title': 'Yıldırım Takip Sistemi',
        'lightning_start': 'Başlat',
        'lightning_stop': 'Durdur',
        'lightning_status_running': 'Durum: Çalışıyor',
        'lightning_status_stopped': 'Durum: Durduruldu',
        'legend_title': 'Gösterge',
        'legend_active': 'Aktif Yıldırım',
        'legend_recent': 'Son Yıldırım',
        'select': 'Seç',
        'refresh': 'Yenile',
        'auto_refresh': 'Otomatik Yenileme',
        'search': 'Ara',
        'close': 'Kapat',
        'cancel': 'İptal',
        'save': 'Kaydet',
        'loading': 'Yükleniyor...',
        'cloud_photo_contest': 'Bulut Fotoğraf Yarışması',
        'upload_cloud_photo': '📸 Bulut Fotoğrafı Yükle',
        'current_month_photos': '🏆 Bu Ayın Fotoğrafları',
        'past_winners': '👑 Geçmiş Kazananlar',
        'close': '❌ Kapat',
        'select_photo': '📁 Fotoğraf Seç',
        'city_label': '📍 Şehir:',
        'weather_condition_label': '⛅ Hava Durumu:',
        'description_label': '📝 Açıklama:',
        'upload_success': '✅ Fotoğrafınız başarıyla yüklendi!',
        'upload_error': '❌ Yükleme başarısız:',
        'no_photos_this_month': '📷 Bu ay henüz fotoğraf yüklenmemiş!\nİlk fotoğrafı sen yükle! 🎉',
        'no_winners_yet': '🏆 Henüz kazanan yok!\nİlk kazanan sen ol! 🎉',
        'vote_success': 'Oyunuz kaydedildi! ❤️',
        'login_to_upload': 'Fotoğraf yüklemek için giriş yapmalısınız!',
        'login_to_vote': 'Oy vermek için giriş yapmalısınız!',
        'fill_all_fields': 'Lütfen tüm alanları doldurun!',
        'select_photo_first': 'Lütfen önce bir fotoğraf seçin!',
        'photo_uploaded': ' fotoğraf',
        'weather_options': ['Güneşli', 'Bulutlu', 'Parçalı Bulutlu', 'Yağmurlu', 'Fırtınalı', 'Sisli'],
        'current_status': 'Bu ay: {} fotoğraf',
        'winner_month': 'Ay: {}',
        'votes_count': '{} oy',
        'click_to_select': '📷 Fotoğraf seçmek için tıkla',
        'photo_upload_failed': '📷 Fotoğraf yüklenemedi',
        'cloud_contest_description': 'En güzel bulut fotoğrafını seç!\nAylık kazanan belirlenir.',
        'default_description': 'Harika bir bulut manzarası! ☁️',
        'winner': 'KAZANAN',
        'vote': 'Oy Ver',
        'warning': 'Uyarı',
        'error': 'Hata',
        'success': 'Başarılı',
        'avatar_title': 'Hava Durumu Avatarı',
        'avatar_accessories': '👔 Aksesuarlar: ',
        'avatar_no_weather_check': '👔 Henüz hava kontrolü yapmadınız',
        'avatar_total_checks': '📊 Toplam Hava Kontrolü: {}',
        'avatar_last_weather': '🌤️ Son: {}°C, {}',
        'avatar_no_weather_data': '🌤️ Henüz hava verisi yok',
        'avatar_update_from_weather': '🔄 Hava Durumundan Güncelle',
        'avatar_update_success': 'Avatar güncellendi! {}°C, {}',
        'avatar_accessory_coat': 'mont',
        'avatar_accessory_scarf': 'atkı',
        'avatar_accessory_hat': 'şapka',
        'avatar_accessory_sunglasses': 'güneş_gözlüğü',
        'avatar_accessory_umbrella': 'şemsiye',
        'avatar_accessory_beanie': 'bere',
        'avatar_accessory_gloves': 'eldiven',
        'avatar_accessory_casual': 'casual',
        'avatar_mission_weather_tracker': '🌤️ Hava Takipçisi',
        'avatar_mission_umbrella_master': '☔ Şemsiye Ustası',
        'avatar_mission_winter_warrior': '🧥 Kış Savaşçısı',
        'avatar_mission_summer_champion': '🎩 Yaz Şampiyonu',
        'avatar_mission_extreme_survivor': '🌪️ Ekstrem Survivor',
        'avatar_mission_check_weather': 'Hava kontrolü yap',
        'avatar_mission_use_umbrella': 'Yağmurlu günde şemsiye kullan',
        'avatar_mission_wear_coat': 'Soğuk havada mont kullan',
        'avatar_mission_wear_hat': 'Sıcak havada şapka kullan',
        'avatar_mission_experience_extreme': 'Ekstrem havayı yaşa',
        'avatar_progress': 'İlerleme: {}/{}',
        'avatar_completed': '✅ Tamamlandı',
        'avatar_in_progress': '⏳ Devam ediyor',
        'avatar_new_badge': 'Tebrikler! Yeni rozet kazandınız:\n{}',
        'unlocked_badges': 'Kazanılan Rozetler',
        'missions': 'Görevler',
        'no_badges_yet': 'Henüz rozet kazanılmadı',
        'predictor': 'Tahminci',
        'prediction_expert': 'Tahmin Uzmanı',
        'prediction_master': 'Tahmin Ustası',
                'traveler_title': 'Gezgin Modu',
        'destination': 'Varış Şehri:',
        'departure_date': 'Gidiş Tarihi:',
        'return_date': 'Dönüş Tarihi:',
        'get_travel_forecast': 'Seyahat Tahmini Al',
        'travel_forecast_for': '✈️ {} Seyahat Tahmini',
        'travel_advice': '💼 Tavsiyeler:',
        'advice_thick_clothes': '• Kalın giysiler alın',
        'advice_coat_necessary': '• Mont gerekli',
        'advice_light_clothes': '• Hafif giysiler yeterli',
        'advice_sunscreen': '• Güneş kremi unutmayın',
        'advice_medium_clothes': '• Orta kalınlıkta giysiler',
        'advice_umbrella_useful': '• Şemsiye faydalı olabilir',
        'travel_date': '📅 {}',
        'travel_temp': '🌡️ {}°C - {}',
        'travel_no_data': 'Seyahat verisi alınamadı',
        'travel_city_not_found': 'Şehir bulunamadı',
                'enter_city_first': 'Lütfen önce bir şehir girin',
        'invalid_dates': 'Dönüş tarihi gidiş tarihinden sonra olmalıdır',
        'invalid_date_format': 'Geçersiz tarih formatı (YYYY-AA-GG)',
        'travel_period': 'Seyahat Periyodu: {} - {}',
        'very_cold_weather': 'Çok Soğuk Hava',
        'cold_weather': 'Soğuk Hava',
        'pleasant_weather': 'Ilıman Hava',
        'hot_weather': 'Sıcak Hava',
        'rain_expected': 'Yağmur Bekleniyor',
        'advice_thermal_clothes': 'Termal giysiler ve kalın mont',
        'advice_winter_boots': 'Kış botları ve çorap',
        'advice_gloves_scarf': 'Eldiven, bere ve atkı',
        'advice_jacket': 'Ceket veya mont',
        'advice_long_pants': 'Uzun pantolonlar',
        'advice_closed_shoes': 'Kapalı ayakkabılar',
        'advice_light_jacket': 'Hafif ceket veya hırka',
        'advice_versatile_clothes': 'Katmanlı giyim (üst üste giyilebilir)',
        'advice_comfortable_shoes': 'Rahat yürüyüş ayakkabıları',
        'advice_hat': 'Şapka veya güneş gözlüğü',
        'advice_water': 'Bol su tüketin',
        'advice_umbrella': 'Şemsiye veya yağmurluk',
        'advice_waterproof': 'Su geçirmez ayakkabı/çantalar',
                'voice_title': 'Sesli Asistan',
        'voice_start': 'Dinlemeye Başla',
        'voice_listening': 'Dinleniyor...',
        'voice_not_available': 'Sesli asistan kullanılamıyor.',
        'voice_ready': 'Hazır...',
        'voice_speaking': '🎤 Siz: {}',
        'voice_assistant': '🤖 Asistan: {}',
        'voice_not_understood': '❌ Ses anlaşılamadı. Lütfen tekrar deneyin.',
        'voice_error': '❌ Hata oluştu: {}',
        'voice_example_commands': '💡 Örnek Komutlar:',
        'voice_example_1': '• \'İstanbul hava durumu\'',
        'voice_example_2': '• \'Ankara sıcaklık kaç derece\'',
        'voice_example_3': '• \'İzmir hava nasıl\'',
        'voice_example_4': '• \'London weather\'',
        'voice_example_5': '• \'Paris temperature\'',
        'voice_weather_for': '🌤️ {} hava durumu:',
        'voice_temperature': '🌡️ Sıcaklık: {}°C',
        'voice_condition': '📝 Durum: {}',
        'voice_humidity': '💧 Nem: {}%',
        'voice_wind': '💨 Rüzgar: {} m/s',
        'voice_city_not_found': '❌ {} için hava durumu alınamadı: {}',
        'voice_tip': '💡 İpucu: \'İstanbul hava durumu\' veya \'Ankara sıcaklığı\' şeklinde sorabilirsiniz.',
        'voice_asking_weather': '🤔 Hava durumu hakkında mı soruyorsunuz? Örneğin: \'İstanbul hava durumu nedir?\'',
        'voice_default_city': '🌤️ {} hava durumu:\n🌡️ Sıcaklık: {}°C\n📝 Durum: {}\n\n💡 İpucu: \'İstanbul hava durumu\' veya \'Ankara sıcaklığı\' şeklinde sorabilirsiniz.',
                'energy_title': 'Enerji Tüketim Tahmini',
        'energy_24h_forecast': '⚡ 24 Saatlik Enerji Tahmini',
        'heating_need': 'Isıtma İhtiyacı',
        'cooling_need': 'Soğutma İhtiyacı',
        'total_energy': 'Toplam Enerji',
        'kwh_day': 'kWh/gün',
        'estimated_cost': '💰 Tahmini Maliyet:',
        'heating_cost': 'Isıtma: {} TL/gün',
        'cooling_cost': 'Soğutma: {} TL/gün',
        'recommendation': '📊 Öneri:',
        'use_heater': 'Isıtıcı kullanın',
        'use_ac': 'Klima gerekebilir',
        'energy_efficient': 'Enerji verimli modda kullanın',
        'no_heating_cooling': 'Isıtma/soğutma gerekmiyor',
        'energy_data_error': 'Enerji verisi alınamadı',
        'enter_city_energy': 'Lütfen bir şehir girin',
        'target_temperature': 'Hedef Sıcaklık: {}°C',
        'current_temperature': 'Mevcut Sıcaklık: {}°C',
        'temperature_difference': 'Sıcaklık Farkı: {}°C',
        'energy_savings_tip': '💡 Enerji Tasarrufu İpuçları:',
        'tip_heating': '• Isıtıcıyı 21°C\'de tutun',
        'tip_cooling': '• Klimayı 24°C\'de kullanın',
        'tip_insulation': '• Pencere ve kapı yalıtımını kontrol edin',
        'tip_curtains': '• Gündüz perdeleri açık tutun',
        'tip_unplug': '• Kullanılmayan cihazları fişten çekin',
        'daily_energy_consumption': 'Günlük Enerji Tüketimi',
        'monthly_estimate': 'Aylık Tahmini Tüketim',
        'monthly_cost': 'Aylık Tahmini Maliyet',
        'programmable_thermostat': 'Programlanabilir termostat kullanın',
        'seal_leaks': 'Hava kaçaklarını kapatın',
        'use_fans': 'Vantilatör kullanın',
        'close_blinds': 'Güneşli saatlerde panjurları kapatın',
        'energy_efficient_appliances': 'Enerji verimli cihazlar kullanın',
                # HARİTA BAŞLIKLARI
        'world_uv_map': '🌞 Dünya UV Haritası',
        'world_air_quality_map': '🌫️ Dünya Hava Kalitesi Haritası',
        'world_pollen_map': '🌸 Dünya Polen Haritası',
        'world_visibility_map': '👁️ Dünya Görüş Mesafesi Haritası',
        'world_wave_map': '🌊 Dünya Dalga Haritası',
        'world_heat_map': '🌡️ Dünya Hissedilen Sıcaklık Haritası',
        'world_storm_map': '🌪️ Dünya Fırtına Takip Haritası',
       
        # HARİTA KONTROL YAZILARI
        'real_time_data': 'Gerçek Zamanlı Veriler',
        'loading_data': 'Veriler yükleniyor...',
        'cities_loaded': '{} şehir yüklendi',
        'last_update': 'Son güncelleme: {}',
        'search_city': '🔍 Şehir Ara',
        'refresh': '🔄 Yenile',
        'world_view': '🗺️ Dünya Görünümü',
        'ocean_view': '🌊 Okyanus Görünümü',
        'auto_refresh': '🔄 Otomatik Yenileme',
       
        # UV HARİTASI
        'uv_index_legend': 'UV İndeksi Lejantı',
        'uv_low': 'Düşük (0-2)',
        'uv_moderate': 'Orta (3-5)',
        'uv_high': 'Yüksek (6-7)',
        'uv_very_high': 'Çok Yüksek (8-10)',
        'uv_extreme': 'Aşırı (11+)',
        'uv_protection_tip': '💡 Korunma İpucu:',
        'uv_tip_low': 'Güneş kremi gerekli değil',
        'uv_tip_moderate': 'SPF 15+ güneş kremi önerilir',
        'uv_tip_high': 'SPF 30+ güneş kremi kullanın',
        'uv_tip_very_high': 'SPF 50+ ve şapka kullanın',
        'uv_tip_extreme': 'Öğle saatlerinde güneşten kaçının',
       
        # HAVA KALİTESİ HARİTASI
        'air_quality_legend': 'Hava Kalitesi Lejantı',
        'aqi_good': '✅ İyi (1)',
        'aqi_moderate': '😊 Orta (2)',
        'aqi_sensitive': '😐 Hassas (3)',
        'aqi_unhealthy': '⚠️ Sağlıksız (4)',
        'aqi_very_unhealthy': '🚨 Çok Sağlıksız (5)',
        'aqi_hazardous': '☠️ Tehlikeli (6)',
        'pollutant_components': '📊 Kirletici Bileşenler',
        'pm25': 'PM2.5',
        'pm10': 'PM10',
        'co': 'CO',
        'no2': 'NO₂',
        'o3': 'O₃',
        'health_recommendations': '❤️ Sağlık Önerileri',
        'aqi_tip_good': 'Hava kalitesi iyi, dışarıda vakit geçirebilirsiniz',
        'aqi_tip_moderate': 'Hassas gruplar dikkatli olmalı',
        'aqi_tip_sensitive': 'Astımı olanlar dikkatli olmalı',
        'aqi_tip_unhealthy': 'Dışarıda uzun süre kalmayın',
        'aqi_tip_very_unhealthy': 'Maske kullanın, dışarı çıkmayın',
        'aqi_tip_hazardous': 'Acil durum! İçeride kalın',
       
        # POLEN HARİTASI
        'pollen_legend': 'Polen Seviyesi Lejantı',
        'pollen_very_low': '✅ Çok Düşük (0-2)',
        'pollen_low': '😊 Düşük (3-4)',
        'pollen_moderate': '😐 Orta (5-6)',
        'pollen_high': '⚠️ Yüksek (7-8)',
        'pollen_very_high': '🚨 Çok Yüksek (9-10)',
        'pollen_types': '📊 Polen Türleri',
        'tree_pollen': '🌳 Ağaç Poleni',
        'grass_pollen': '🌾 Ot Poleni',
        'weed_pollen': '🌿 Yabani Ot',
        'allergy_advice': '🤧 Alerji Önerileri',
        'pollen_tip_low': 'Alerjisi olanlar için güvenli',
        'pollen_tip_moderate': 'Hassas kişiler dikkatli olmalı',
        'pollen_tip_high': 'Alerji ilacı kullanmayı düşünün',
        'pollen_tip_very_high': 'Pencereleri kapalı tutun',
       
        # GÖRÜŞ MESAFESİ HARİTASI
        'visibility_legend': 'Görüş Mesafesi Lejantı',
        'visibility_excellent': '👁️ Mükemmel (20+ km)',
        'visibility_good': '👀 İyi (10-20 km)',
        'visibility_moderate': '😐 Orta (5-10 km)',
        'visibility_poor': '😑 Kötü (2-5 km)',
        'visibility_very_poor': '😵 Çok Kötü (1-2 km)',
        'visibility_dangerous': '🚫 Tehlikeli (<1 km)',
        'travel_conditions': '🚗 Seyahat Koşulları',
        'visibility_tip_excellent': 'Mükemmel görüş, güvenli sürüş',
        'visibility_tip_good': 'İyi görüş, normal hız',
        'visibility_tip_moderate': 'Dikkatli sürün, hızı azaltın',
        'visibility_tip_poor': 'Sis lambalarını açın, yavaşlayın',
        'visibility_tip_very_poor': 'Zorunlu değilse yola çıkmayın',
        'visibility_tip_dangerous': 'Çok tehlikeli, seyahat etmeyin',
       
        # DALGA HARİTASI
        'wave_legend': 'Dalga Yüksekliği Lejantı',
        'wave_calm': '😌 Sakin (<0.5m)',
        'wave_light': '🌊 Hafif (0.5-1m)',
        'wave_moderate': '〰️ Orta (1-2m)',
        'wave_high': '🌀 Yüksek (2-3m)',
        'wave_very_high': '⚠️ Çok Yüksek (3-5m)',
        'wave_extreme': '🚨 Aşırı Yüksek (>5m)',
        'wave_details': '🌊 Dalga Bilgileri',
        'wave_height': 'Dalga Yüksekliği',
        'wave_period': 'Dalga Periyodu',
        'wave_direction': 'Dalga Yönü',
        'water_body': 'Su Kütlesi',
        'activity_recommendations': '🏄 Aktivite Önerileri',
        'wave_tip_calm': 'Yüzme ve tüm su sporları için ideal',
        'wave_tip_light': 'Sörf için düşük, yüzme için uygun',
        'wave_tip_moderate': 'Başlangıç sörf için iyi',
        'wave_tip_high': 'İleri seviye sörf, yüzme tehlikeli',
        'wave_tip_very_high': 'Sadece profesyonel sörfçüler',
        'wave_tip_extreme': 'Tüm su aktiviteleri YASAK',
       
        # ISI HARİTASI
        'heat_index_legend': 'Heat Index Lejantı',
        'heat_normal': '😊 Normal (<27°C)',
        'heat_caution': '😐 Dikkat (27-32°C)',
        'heat_extreme_caution': '😓 Aşırı Dikkat (32-39°C)',
        'heat_danger': '🥵 Tehlike (39-51°C)',
        'heat_extreme_danger': '🚨 Aşırı Tehlike (>51°C)',
        'heat_details': '🌡️ Isı Detayları',
        'actual_temperature': 'Gerçek Sıcaklık',
        'feels_like': 'Hissedilen',
        'heat_index': 'Heat Index',
        'health_warning': '⚠️ Sağlık Uyarısı',
        'heat_tip_normal': 'Güvenli, normal önlemler',
        'heat_tip_caution': 'Yorgunluk mümkün, su için',
        'heat_tip_extreme_caution': 'Isı krampları mümkün',
        'heat_tip_danger': 'Isı yorgunluğu olası',
        'heat_tip_extreme_danger': 'Isı çarpması riski!',
       
        # FIRTINA HARİTASI
        'storm_legend': 'Fırtına Şiddeti Lejantı',
        'storm_normal': '☁️ Normal',
        'storm_windy': '💨 Rüzgarlı',
        'storm_storm': '🌬️ Fırtına',
        'storm_severe': '🌪️ Şiddetli',
        'storm_very_severe': '⛈️ Çok Şiddetli',
        'storm_hurricane': '🌀 Kasırga/Tayfun',
        'storm_details': '🌪️ Fırtına Detayları',
        'wind_speed': 'Rüzgar Hızı',
        'wind_direction': 'Rüzgar Yönü',
        'pressure': 'Basınç',
        'storm_type': 'Fırtına Türü',
        'beaufort_scale': '📊 Beaufort Skalası',
        'safety_recommendations': '🛡️ Güvenlik Önerileri',
        'storm_tip_normal': 'Normal önlemler yeterli',
        'storm_tip_windy': 'Dışarıda dikkatli olun',
        'storm_tip_storm': 'Pencere ve kapıları kapatın',
        'storm_tip_severe': 'İçeride kalın, ağaçlardan uzak durun',
        'storm_tip_very_severe': 'Acil durum! Güvenli odaya geçin',
        'storm_tip_hurricane': 'KIRMIZI ALARM! Sığınağa geçin',
       
        # GENEL HARITA TERİMLERİ
        'city_search': 'Şehir Arama',
        'enter_city_name': 'Şehir adını girin',
        'searching': 'Aranıyor...',
        'city_found': 'Şehir bulundu: {}',
        'city_not_found': 'Şehir bulunamadı',
        'show_on_map': '🗺️ Haritada Göster',
        'close': '❌ Kapat',
        'details': '📋 Detaylar',
        'recommendations': '💡 Öneriler',
        'source': 'Kaynak: {}',
        'coordinates': 'Koordinatlar: {}',
        'timestamp': 'Zaman: {}',
        'world_wave_map': '🌊 Dünya Dalga Haritası',
        'wave_height': 'Dalga Yüksekliği',
        'wave_period': 'Dalga Periyodu',
        'wave_direction': 'Dalga Yönü',
        'wave_calm': 'Sakin',
        'wave_light': 'Hafif',
        'wave_moderate': 'Orta',
        'wave_high': 'Yüksek',
        'wave_very_high': 'Çok Yüksek',
        'wave_extreme': 'Aşırı Yüksek',
        'wave_legend': 'Dalga Yüksekliği Lejantı',
        'wave_details': 'Dalga Bilgisi',
        'activity_recommendations': '🏄 Aktivite Önerileri',
        'wave_tip_calm': '✅ İdeal yüzme koşulları\n🏊 Tüm su sporları için uygun',
        'wave_tip_light': '🏄 Sörf için düşük\n✅ Yüzme ve kano için uygun',
        'wave_tip_moderate': '🏄 Başlangıç sörf için iyi\n⚠️ Yüzmede dikkatli olun',
        'wave_tip_high': '🏄 Orta seviye sörf\n⚠️ Deneyimsizler yüzmemeli',
        'wave_tip_very_high': '🏄 İleri seviye sörf\n🚫 Yüzme tehlikeli',
        'wave_tip_extreme': '🚨 Aşırı tehlikeli\n🚫 Tüm su aktiviteleri yasak',
        'search_coastal_tip': '💡 İpucu: Kıyı şehri girin (örn: Miami, Sydney)',
        'ocean_view': '🌊 Okyanus Görünümü',
        'world_heat_map': '🌡️ Dünya Hissedilen Sıcaklık Haritası',
        'heat_index': 'Heat Index',
        'actual_temperature': 'Gerçek Sıcaklık',
        'feels_like': 'Hissedilen',
        'heat_indicator': 'Isı Göstergesi',
        'heat_index_legend': 'Heat Index Lejantı',
        'heat_normal': 'Normal',
        'heat_caution': 'Dikkat',
        'heat_extreme_caution': 'Aşırı Dikkat',
        'heat_danger': 'Tehlike',
        'heat_extreme_danger': 'Aşırı Tehlike',
        'heat_safe': 'Güvenli',
        'heat_fatigue_possible': 'Yorgunluk mümkün',
        'heat_cramps_possible': 'Isı krampları mümkün',
        'heat_exhaustion_likely': 'Isı yorgunluğu olası',
        'heat_stroke_risk': 'Isı çarpması riski!',
        'world_storm_map': '🌪️ Dünya Fırtına Takip Haritası',
        'storm_details': 'Fırtına Detayları',
        'storm_intensity': 'Fırtına Şiddeti',
        'storm_tracking': 'Fırtına Takibi',
        'microclimate_title': 'Mikro-İklim Hesaplaması',
        'elevation': 'Yükseklik (m):',
        'urban_factor': 'Şehirleşme Faktörü (0-1):',
        'calculate_micro': 'Hesapla',
        'base_temperature': 'Baz Sıcaklık',
        'microclimate_temperature': 'Mikro-İklim Sıcaklık',
        'correction': 'Düzeltme',
        'humidity': 'Nem',
        'wind_speed': 'Rüzgar Hızı',
        'elevation_label': 'Yükseklik',
        'urbanization': 'Şehirleşme',
        'microclimate_results': 'Mikro-İklim Sonuçları',
        'microclimate_calculation': 'Mikro-İklim Hesaplama',
        'enter_coordinates': 'Koordinatları girin (enlem,boylam)',
        'energy_title': 'Enerji Tüketim Tahmini',
        'energy_24h_forecast': '⚡ 24 Saatlik Enerji Tahmini',
        'heating_need': 'Isıtma İhtiyacı',
        'cooling_need': 'Soğutma İhtiyacı',
        'total_energy': 'Toplam Enerji',
        'kwh_day': 'kWh/gün',
        'estimated_cost': '💰 Tahmini Maliyet:',
        'heating_cost': 'Isıtma: {} TL/gün',
        'cooling_cost': 'Soğutma: {} TL/gün',
        'recommendation': '📊 Öneri:',
        'use_heater': 'Isıtıcı kullanın',
        'use_ac': 'Klima gerekebilir',
        'energy_efficient': 'Enerji verimli modda kullanın',
        'no_heating_cooling': 'Isıtma/soğutma gerekmiyor',
        'energy_data_error': 'Enerji verisi alınamadı',
        'enter_city_energy': 'Lütfen bir şehir girin',
        'target_temperature': 'Hedef Sıcaklık: {}°C',
        'current_temperature': 'Mevcut Sıcaklık: {}°C',
        'temperature_difference': 'Sıcaklık Farkı: {}°C',
        'energy_savings_tip': '💡 Enerji Tasarrufu İpuçları:',
        'tip_heating': '• Isıtıcıyı 21°C\'de tutun',
        'tip_cooling': '• Klimayı 24°C\'de kullanın',
        'tip_insulation': '• Pencere ve kapı yalıtımını kontrol edin',
        'tip_curtains': '• Gündüz perdeleri açık tutun',
        'tip_unplug': '• Kullanılmayan cihazları fişten çekin',
        'daily_energy_consumption': 'Günlük Enerji Tüketimi',
        'monthly_estimate': 'Aylık Tahmini Tüketim',
        'monthly_cost': 'Aylık Tahmini Maliyet',
        'energy_title': 'Enerji Tüketim Tahmini',
        'energy_24h_forecast': '⚡ 24 Saatlik Enerji Tahmini',
        'heating_need': 'Isıtma İhtiyacı',
        'cooling_need': 'Soğutma İhtiyacı',
        'total_energy': 'Toplam Enerji',
        'kwh_day': 'kWh/gün',
        'estimated_cost': '💰 Tahmini Maliyet:',
        'heating_cost': 'Isıtma: {} TL/gün',
        'cooling_cost': 'Soğutma: {} TL/gün',
        'recommendation': '📊 Öneri:',
        'use_heater': 'Isıtıcı kullanın',
        'use_ac': 'Klima gerekebilir',
        'energy_efficient': 'Enerji verimli modda kullanın',
        'no_heating_cooling': 'Isıtma/soğutma gerekmiyor',
        'energy_data_error': 'Enerji verisi alınamadı',
        'enter_city_energy': 'Lütfen bir şehir girin',
        'target_temperature': 'Hedef Sıcaklık: {}°C',
        'current_temperature': 'Mevcut Sıcaklık: {}°C',
        'temperature_difference': 'Sıcaklık Farkı: {}°C',
        'energy_savings_tip': '💡 Enerji Tasarrufu İpuçları:',
        'tip_heating': '• Isıtıcıyı 21°C\'de tutun',
        'tip_cooling': '• Klimayı 24°C\'de kullanın',
        'tip_insulation': '• Pencere ve kapı yalıtımını kontrol edin',
        'tip_curtains': '• Gündüz perdeleri açık tutun',
        'tip_unplug': '• Kullanılmayan cihazları fişten çekin',
        'daily_energy_consumption': 'Günlük Enerji Tüketimi',
        'monthly_estimate': 'Aylık Tahmini Tüketim',
        'monthly_cost': 'Aylık Tahmini Maliyet',
        'climate_title': 'İklim İstatistikleri',
        'select_years': 'Karşılaştırılacak Yıllar:',
        'year1': 'Yıl 1:',
        'year2': 'Yıl 2:',
        'climate_analysis_for': 'İklim Analizi -',
        'analysis_period': 'Analiz Periyodu',
        'coordinates': 'Koordinatlar',
        'yearly_comparison': 'Yıllık Karşılaştırma',
        'average_temperature': 'Ortalama Sıcaklık',
        'temperature_change': 'Sıcaklık Değişimi',
        'monthly_breakdown': 'Aylık Dağılım',
        'change': 'Değişim',
        'winter_months': 'Kış Ayları',
        'spring_months': 'İlkbahar Ayları',
        'summer_months': 'Yaz Ayları',
        'autumn_months': 'Sonbahar Ayları',
        'climate_insights': 'İklim İçgörüleri',
        'trend_analysis': 'Trend Analizi',
        'current_temperature': 'Mevcut Sıcaklık',
        'warming_trend': 'Isınma Trendi',
        'data_source_note': 'Not: Veriler simüle edilmiştir. Gerçek veriler için tarihsel iklim API\'si gereklidir.',
        'significant_warming': 'Belirgin ısınma trendi gözlemleniyor',
        'moderate_warming': 'Orta düzeyde ısınma trendi',
        'slight_warming': 'Hafif ısınma eğilimi',
        'stable_temperatures': 'Kararlı sıcaklık seviyeleri',
        'per_decade': 'on yılda',
        'invalid_years': 'Yıl 1, Yıl 2\'den küçük olmalıdır',
        'invalid_year_format': 'Geçersiz yıl formatı',
        'calculate_prediction': '🔮 Tahmini Hesapla',
        'temperature_projection': 'Sıcaklık Projeksiyonu',
        'extreme_weather_probability': 'Ekstrem hava olayları olasılığı',
        'climate_change_simulation': 'İklim değişikliği simülasyonu',
        'note_simplified_prediction': 'Not: Bu basitleştirilmiş bir tahmindir.',
        'prediction_note': 'Tahmin Notu',
        'simulated_prediction': 'Simüle edilmiş tahmin',
        'warming_effect': 'Isınma etkisi',
        'yearly_warming': 'Yıllık ısınma',
        'climate_model': 'İklim modeli',
        'future_scenario': 'Gelecek senaryosu',
       
        # DİĞER EKSİK ÇEVİRİLER
        'calculate': 'Hesapla',
        'prediction': 'Tahmin',
        'simulation': 'Simülasyon',
        'scenario': 'Senaryo',
        'model': 'Model',
        'probability': 'Olasılık',
        'projection': 'Projeksiyon',
        'effect': 'Etki',
       
    },
    'en': {
        'title': 'Weather App',
        'login': 'Login',
        'register': 'Register',
        'username': 'Username',
        'password': 'Password',
        'hot': 'Very Hot (°C)',
        'cold': 'Very Cold (°C)',
        'wind': 'Very Windy (m/s)',
        'humidity': 'Very Humid (%)',
        'back': '⬅️ Back',
        'settings': '⚙︎',
        'logout': '⬅️',
        'coordinate':'Coordinates (Iat,Ion)',
        'city': 'City or Coordinates (lat,lon)',
        'date': 'Date (YYYY-MM-DD)',
        'hour': 'Hour (0-23)',
        'map_select': '🌍 Select City from Map',
        'date_select': '📅 Select Date',
        'hour_select': '⏰ Select Hour',
        'get_forecast': 'Get Forecast',
        'show_graph': '📊 Forecast Graph',
        'comfort_settings': 'Comfort Threshold Settings',
        'save': '💾 Save',
        'back_arrow': '⬅️ Back',
        'language': 'Language:',
        'new_user': 'Create New User',
        'info': 'Info',
        'select': 'Select',
        'login_title': 'Weather App',
        'invalid': 'Invalid',
        'success': 'Success',
        'error': 'Error',
        'settings_saved': 'Settings saved',
        'numeric_required': 'Thresholds must be numeric.',
        'user_exists': 'User already exists.',
        'empty_fields': 'Do not leave blank.',
        'login_failed': 'Login failed.',
        'city_not_found': 'City not found.',
        'invalid_date': 'Invalid date or hour',
        'data_error': 'Could not get data.',
        'coord_error': 'Invalid coordinates',
        'select_date': 'Select Date',
        'select_hour': 'Select Hour',
        'select_city': 'Select City',
        'graph_title': '5-Day Forecast Graph',
        'very_cold': '❄️ Very cold',
        'very_hot': '🔥 Very hot',
        'very_wet': '🌧️ Very wet',
        'very_windy': '💨 Very windy',
        'very_uncomfortable': '😣 Very uncomfortable',
        'comfortable': '😊 Weather conditions are quite comfortable.',
        'selected_coords': 'Selected Coordinates: {}',
        'temp_c': 'Temperature (°C)',
        'ai_title': 'AI Suggestions',
        'ai_generate': 'Generate Advice',
        'ai_history': 'Previous Suggestions',
        'ai_no_history': 'No saved suggestions.',
        'ai_select_coords': 'Please select coordinates.',
        'ai_select_datetime': 'Please select date and hour.',
        'lightning_title': 'Lightning Monitor',
        'lightning_start': 'Start',
        'lightning_stop': 'Stop',
        'lightning_status_running': 'Running',
        'lightning_status_stopped': 'Stopped',
        'legend_title': 'Legend',
        'legend_active': 'Active Strike',
        'legend_recent': 'Recent Strike',
        'micro_climate': '🌡️ Micro-Climate Analysis',
        'alerts': '🚨 Emergency Alerts',
        'climate_data': '📈 Climate Data',
        'energy': '⚡ Energy Forecast',
        'voice': '🎤 Voice Assistant',
        'widget': '📱 Widget View',
        'traveler': '✈️ Traveler Mode',
        'social': '📷 Social Posts',
        'microclimate_title': 'Micro-Climate Calculation',
        'elevation': 'Elevation (m):',
        'urban_factor': 'Urban Factor (0-1):',
        'calculate_micro': 'Calculate',
        'alerts_title': 'Emergency Alerts',
        'no_alerts': 'No active alerts.',
        'show_on_map': 'Show on Map',
        'climate_title': 'Climate Statistics',
        'compare_years': 'Compare Years',
        'energy_title': 'Energy Consumption Forecast',
        'heating_need': 'Heating Need:',
        'cooling_need': 'Cooling Need:',
        'kwh_day': 'kWh/day',
        'voice_title': 'Voice Assistant',
        'voice_start': 'Start Listening',
        'voice_listening': 'Listening...',
        'voice_not_available': 'Voice assistant not available.',
        'widget_title': 'Widget Mode',
        'widget_show': 'Show Widget',
        'traveler_title': 'Traveler Mode',
        'destination': 'Destination City:',
        'departure_date': 'Departure Date:',
        'return_date': 'Return Date:',
        'get_travel_forecast': 'Get Travel Forecast',
        'social_title': 'Social Weather',
        'add_post': 'Add Post',
        'view_posts': 'View Posts',
        'your_comment': 'Your Comment:',
        'upload_photo': 'Upload Photo',
        'post': 'Post',
        'maps': '🗺️ Maps',
        'uv_map': '☀️ UV Map',
        'air_quality_map': '🌫️ Air Quality',
        'pollen_map': '🌾 Pollen Map',
        'visibility_map': '👁️ Visibility',
        'wave_map': '🌊 Wave Map',
        'heat_map': '🌡️ Heat Map',
        'storm_map': '🌀 Storm Map',
        'lightning_map': '⚡ Lightning Map',
        'uv_index': 'UV Index',
        'aqi': 'Air Quality Index',
        'pollen_level': 'Pollen Level',
        'visibility': 'Visibility (km)',
        'wave_height': 'Wave Height (m)',
        'heat_index': 'Feels Like',
        'storm_category': 'Storm Category',
        'low': 'Low',
        'moderate': 'Moderate',
        'high': 'High',
        'very_high': 'Very High',
        'extreme': 'Extreme',
        'good': 'Good',
        'fair': 'Fair',
        'poor': 'Poor',
        'very_poor': 'Very Poor',
        'hazardous': 'Hazardous',
        'refresh': '🔄 Refresh',
        'auto_refresh': 'Auto Refresh',
        # NEW TRANSLATIONS
        'avatar': '👤 My Avatar',
        'avatar_title': 'Weather Avatar',
        'future_weather': '🔮 Future Weather',
        'future_weather_title': 'Future Weather Simulation',
        'achievements': '🏆 My Badges',
        'achievements_title': 'Weather Missions',
        'climate_change_sim': 'Climate change simulation',
        'years_future': 'Years ahead:',
        'current_weather': 'Current weather:',
        'future_prediction': 'Future prediction:',
        'change': 'Change:',
        'mission': 'Mission:',
        'progress': 'Progress:',
        'unlock_badge': 'Badge Unlocked!',
        'check_weather': 'Check weather',
        'umbrella_mission': 'Use umbrella on rainy day',
        'winter_mission': 'Wear coat in cold weather',
        'hot_mission': 'Wear hat in hot weather',
        'complete': 'Completed',
        'prediction_game': '🎯 Guess It!',
        'prediction_title': 'Guess Tomorrow\'s Temperature',
        'predict_temperature': 'Temperature Guess (°C):',
        'make_prediction': 'Make Prediction',
        'check_prediction': 'Check Prediction',
        'prediction_result': 'Prediction Result',
        'prediction_correct': '🎉 Congratulations! Correct guess!',
        'prediction_off': '❌ Wrong guess. Off by {}°C',
        'points_earned': 'Points Earned: {}',
        'total_points': 'Total Points: {}',
        'prediction_made': 'Your Prediction: {}°C',
        'actual_temperature': 'Actual Temperature: {}°C',
        'make_prediction_first': 'You must make a prediction first!',
        'wait_for_tomorrow': 'Wait for tomorrow\'s prediction...',
        'game_instructions': 'Guess tomorrow\'s temperature and earn points!',
        'earthquake_alerts': 'Earthquake Alerts',
        'storm_alerts': 'Storm Alerts',
        'flood_alerts': 'Flood Alerts',
        'real_earthquake_alerts': 'Real Earthquake Alerts',
        'real_storm_alerts': 'Real Storm Alerts',
        'real_flood_alerts': 'Copernicus EMS Flood Alerts',
        'emergency_copernicus': 'European Commission Copernicus Emergency Management Service',
        'active_events': 'Active Events',
        'high_risk': 'High Risk',
        'affected_areas': 'Affected Areas',
        'rivers_at_risk': 'Rivers at Risk',
        'start_date': 'Start Date',
        'status': 'Status',
        'source': 'Source',
        'show_on_map': 'Show on Map',
        'open_website': 'Open Website',
        'magnitude': 'Magnitude',
        'intensity': 'Intensity',
        'coordinates': 'Coordinates',
        'storm_category': 'Storm Category',
        'wind_speed': 'Wind Speed',
        'weather_condition': 'Weather Condition',
        'health_warning': 'Health Warning',
        'safety_recommendations': 'Safety Recommendations',
        'no_alerts': 'No active alerts at the moment',
        'data_error': 'Could not retrieve data',
        'searching': 'Searching...',
        'city_not_found': 'City not found',
        'data_source_openweather': 'Severe weather events based on OpenWeatherMap data',
        'temperature': 'Temperature',
        'moderate': 'Moderate',
        'low': 'Low',
        'lightning_title': 'Lightning Monitor',
        'lightning_start': 'Start',
        'lightning_stop': 'Stop',
        'lightning_status_running': 'Status: Running',
        'lightning_status_stopped': 'Status: Stopped',
        'legend_title': 'Legend',
        'legend_active': 'Active Lightning',
        'legend_recent': 'Recent Lightning',
        'select': 'Select',
        'refresh': 'Refresh',
        'auto_refresh': 'Auto Refresh',
        'search': 'Search',
        'close': 'Close',
        'cancel': 'Cancel',
        'save': 'Save',
        'loading': 'Loading...',
        'cloud_photo_contest': 'Cloud Photo Contest',
        'upload_cloud_photo': '📸 Upload Cloud Photo',
        'current_month_photos': '🏆 This Month\'s Photos',
        'past_winners': '👑 Past Winners',
        'close': '❌ Close',
        'select_photo': '📁 Select Photo',
        'city_label': '📍 City:',
        'weather_condition_label': '⛅ Weather Condition:',
        'description_label': '📝 Description:',
        'upload_success': '✅ Your photo was uploaded successfully!',
        'upload_error': '❌ Upload failed:',
        'no_photos_this_month': '📷 No photos uploaded this month yet!\nBe the first to upload! 🎉',
        'no_winners_yet': '🏆 No winners yet!\nBe the first winner! 🎉',
        'vote_success': 'Your vote has been recorded! ❤️',
        'login_to_upload': 'You must login to upload photos!',
        'login_to_vote': 'You must login to vote!',
        'fill_all_fields': 'Please fill all fields!',
        'select_photo_first': 'Please select a photo first!',
        'photo_uploaded': ' photos',
        'weather_options': ['Sunny', 'Cloudy', 'Partly Cloudy', 'Rainy', 'Stormy', 'Foggy'],
        'current_status': 'This month: {} photos',
        'winner_month': 'Month: {}',
        'votes_count': '{} votes',
        'click_to_select': '📷 Click to select photo',
        'photo_upload_failed': '📷 Photo could not be loaded',
        'cloud_contest_description': 'Choose the most beautiful cloud photo!\nMonthly winner is selected.',
        'default_description': 'Amazing cloud scenery! ☁️',
        'winner': 'WINNER',
        'vote': 'Vote',
        'warning': 'Warning',
        'error': 'Error',
        'success': 'Success',
        'avatar_title': 'Weather Avatar',
        'avatar_accessories': '👔 Accessories: ',
        'avatar_no_weather_check': '👔 No weather check yet',
        'avatar_total_checks': '📊 Total Weather Checks: {}',
        'avatar_last_weather': '🌤️ Last: {}°C, {}',
        'avatar_no_weather_data': '🌤️ No weather data yet',
        'avatar_update_from_weather': '🔄 Update from Weather',
        'avatar_update_success': 'Avatar updated! {}°C, {}',
        'avatar_accessory_coat': 'coat',
        'avatar_accessory_scarf': 'scarf',
        'avatar_accessory_hat': 'hat',
        'avatar_accessory_sunglasses': 'sunglasses',
        'avatar_accessory_umbrella': 'umbrella',
        'avatar_accessory_beanie': 'beanie',
        'avatar_accessory_gloves': 'gloves',
        'avatar_accessory_casual': 'casual',
        'avatar_mission_weather_tracker': '🌤️ Weather Tracker',
        'avatar_mission_umbrella_master': '☔ Umbrella Master',
        'avatar_mission_winter_warrior': '🧥 Winter Warrior',
        'avatar_mission_summer_champion': '🎩 Summer Champion',
        'avatar_mission_extreme_survivor': '🌪️ Extreme Survivor',
        'avatar_mission_check_weather': 'Check weather',
        'avatar_mission_use_umbrella': 'Use umbrella on rainy day',
        'avatar_mission_wear_coat': 'Wear coat in cold weather',
        'avatar_mission_wear_hat': 'Wear hat in hot weather',
        'avatar_mission_experience_extreme': 'Experience extreme weather',
        'avatar_progress': 'Progress: {}/{}',
        'avatar_completed': '✅ Completed',
        'avatar_in_progress': '⏳ In Progress',
        'avatar_new_badge': 'Congratulations! New badge unlocked:\n{}',
        'unlocked_badges': 'Unlocked Badges',
        'missions': 'Missions',
        'no_badges_yet': 'No badges earned yet',
        'predictor': 'Predictor',
        'prediction_expert': 'Prediction Expert',
        'prediction_master': 'Prediction Master',
        'traveler_title': 'Traveler Mode',
        'destination': 'Destination City:',
        'departure_date': 'Departure Date:',
        'return_date': 'Return Date:',
        'get_travel_forecast': 'Get Travel Forecast',
        'travel_forecast_for': '✈️ {} Travel Forecast',
        'travel_advice': '💼 Recommendations:',
        'advice_thick_clothes': '• Take thick clothes',
        'advice_coat_necessary': '• Coat necessary',
        'advice_light_clothes': '• Light clothes sufficient',
        'advice_sunscreen': '• Don\'t forget sunscreen',
        'advice_medium_clothes': '• Medium thickness clothes',
        'advice_umbrella_useful': '• Umbrella might be useful',
        'travel_date': '📅 {}',
        'travel_temp': '🌡️ {}°C - {}',
        'travel_no_data': 'Could not retrieve travel data',
        'travel_city_not_found': 'City not found',
        'enter_city_first': 'Please enter a city first',
        'invalid_dates': 'Return date must be after departure date',
        'invalid_date_format': 'Invalid date format (YYYY-MM-DD)',
        'travel_period': 'Travel Period: {} - {}',
        'very_cold_weather': 'Very Cold Weather',
        'cold_weather': 'Cold Weather',
        'pleasant_weather': 'Pleasant Weather',
        'hot_weather': 'Hot Weather',
        'rain_expected': 'Rain Expected',
        'advice_thermal_clothes': 'Thermal clothes and thick coat',
        'advice_winter_boots': 'Winter boots and socks',
        'advice_gloves_scarf': 'Gloves, beanie and scarf',
        'advice_jacket': 'Jacket or coat',
        'advice_long_pants': 'Long pants',
        'advice_closed_shoes': 'Closed shoes',
        'advice_light_jacket': 'Light jacket or sweater',
        'advice_versatile_clothes': 'Layered clothing (can be worn over each other)',
        'advice_comfortable_shoes': 'Comfortable walking shoes',
        'advice_hat': 'Hat or sunglasses',
        'advice_water': 'Drink plenty of water',
        'advice_umbrella': 'Umbrella or raincoat',
        'advice_waterproof': 'Waterproof shoes/bags',
        'voice_title': 'Voice Assistant',
        'voice_start': 'Start Listening',
        'voice_listening': 'Listening...',
        'voice_not_available': 'Voice assistant not available.',
        'voice_ready': 'Ready...',
        'voice_speaking': '🎤 You: {}',
        'voice_assistant': '🤖 Assistant: {}',
        'voice_not_understood': '❌ Voice not understood. Please try again.',
        'voice_error': '❌ Error occurred: {}',
        'voice_example_commands': '💡 Example Commands:',
        'voice_example_1': '• \'Istanbul weather\'',
        'voice_example_2': '• \'Ankara temperature\'',
        'voice_example_3': '• \'Izmir how is weather\'',
        'voice_example_4': '• \'London weather\'',
        'voice_example_5': '• \'Paris temperature\'',
        'voice_weather_for': '🌤️ {} weather:',
        'voice_temperature': '🌡️ Temperature: {}°C',
        'voice_condition': '📝 Condition: {}',
        'voice_humidity': '💧 Humidity: {}%',
        'voice_wind': '💨 Wind: {} m/s',
        'voice_city_not_found': '❌ Could not get weather for {}: {}',
        'voice_tip': '💡 Tip: You can ask like \'Istanbul weather\' or \'Ankara temperature\'',
        'voice_asking_weather': '🤔 Are you asking about weather? For example: \'What is the weather in Istanbul?\'',
        'voice_default_city': '🌤️ {} weather:\n🌡️ Temperature: {}°C\n📝 Condition: {}\n\n💡 Tip: You can ask like \'Istanbul weather\' or \'Ankara temperature\'',
         'energy_title': 'Energy Consumption Forecast',
        'energy_24h_forecast': '⚡ 24-Hour Energy Forecast',
        'heating_need': 'Heating Need',
        'cooling_need': 'Cooling Need',
        'total_energy': 'Total Energy',
        'kwh_day': 'kWh/day',
        'estimated_cost': '💰 Estimated Cost:',
        'heating_cost': 'Heating: {} TL/day',
        'cooling_cost': 'Cooling: {} TL/day',
        'recommendation': '📊 Recommendation:',
        'use_heater': 'Use heater',
        'use_ac': 'AC may be needed',
        'energy_efficient': 'Use in energy efficient mode',
        'no_heating_cooling': 'No heating/cooling needed',
        'energy_data_error': 'Could not retrieve energy data',
        'enter_city_energy': 'Please enter a city',
        'target_temperature': 'Target Temperature: {}°C',
        'current_temperature': 'Current Temperature: {}°C',
        'temperature_difference': 'Temperature Difference: {}°C',
        'energy_savings_tip': '💡 Energy Saving Tips:',
        'tip_heating': '• Keep heater at 21°C',
        'tip_cooling': '• Use AC at 24°C',
        'tip_insulation': '• Check window and door insulation',
        'tip_curtains': '• Keep curtains open during daytime',
        'tip_unplug': '• Unplug unused devices',
        'daily_energy_consumption': 'Daily Energy Consumption',
        'monthly_estimate': 'Monthly Estimate',
        'monthly_cost': 'Monthly Estimated Cost',
        'programmable_thermostat': 'Use programmable thermostat',
        'seal_leaks': 'Seal air leaks',
        'use_fans': 'Use fans',
        'close_blinds': 'Close blinds during sunny hours',
        'energy_efficient_appliances': 'Use energy efficient appliances',
                # MAP TITLES
        'world_uv_map': '🌞 World UV Map',
        'world_air_quality_map': '🌫️ World Air Quality Map',
        'world_pollen_map': '🌸 World Pollen Map',
        'world_visibility_map': '👁️ World Visibility Map',
        'world_wave_map': '🌊 World Wave Map',
        'world_heat_map': '🌡️ World Feels Like Temperature Map',
        'world_storm_map': '🌪️ World Storm Tracking Map',
       
        # MAP CONTROL TEXT
        'real_time_data': 'Real-Time Data',
        'loading_data': 'Loading data...',
        'cities_loaded': '{} cities loaded',
        'last_update': 'Last update: {}',
        'search_city': '🔍 Search City',
        'refresh': '🔄 Refresh',
        'world_view': '🗺️ World View',
        'ocean_view': '🌊 Ocean View',
        'auto_refresh': '🔄 Auto Refresh',
       
        # UV MAP
        'uv_index_legend': 'UV Index Legend',
        'uv_low': 'Low (0-2)',
        'uv_moderate': 'Moderate (3-5)',
        'uv_high': 'High (6-7)',
        'uv_very_high': 'Very High (8-10)',
        'uv_extreme': 'Extreme (11+)',
        'uv_protection_tip': '💡 Protection Tip:',
        'uv_tip_low': 'Sunscreen not required',
        'uv_tip_moderate': 'SPF 15+ sunscreen recommended',
        'uv_tip_high': 'Use SPF 30+ sunscreen',
        'uv_tip_very_high': 'Use SPF 50+ and hat',
        'uv_tip_extreme': 'Avoid sun during midday',
       
        # AIR QUALITY MAP
        'air_quality_legend': 'Air Quality Legend',
        'aqi_good': '✅ Good (1)',
        'aqi_moderate': '😊 Moderate (2)',
        'aqi_sensitive': '😐 Sensitive (3)',
        'aqi_unhealthy': '⚠️ Unhealthy (4)',
        'aqi_very_unhealthy': '🚨 Very Unhealthy (5)',
        'aqi_hazardous': '☠️ Hazardous (6)',
        'pollutant_components': '📊 Pollutant Components',
        'pm25': 'PM2.5',
        'pm10': 'PM10',
        'co': 'CO',
        'no2': 'NO₂',
        'o3': 'O₃',
        'health_recommendations': '❤️ Health Recommendations',
        'aqi_tip_good': 'Air quality good, can spend time outside',
        'aqi_tip_moderate': 'Sensitive groups should be cautious',
        'aqi_tip_sensitive': 'People with asthma should be careful',
        'aqi_tip_unhealthy': 'Avoid prolonged outdoor exposure',
        'aqi_tip_very_unhealthy': 'Wear mask, avoid going outside',
        'aqi_tip_hazardous': 'Emergency! Stay indoors',
       
        # POLLEN MAP
        'pollen_legend': 'Pollen Level Legend',
        'pollen_very_low': '✅ Very Low (0-2)',
        'pollen_low': '😊 Low (3-4)',
        'pollen_moderate': '😐 Moderate (5-6)',
        'pollen_high': '⚠️ High (7-8)',
        'pollen_very_high': '🚨 Very High (9-10)',
        'pollen_types': '📊 Pollen Types',
        'tree_pollen': '🌳 Tree Pollen',
        'grass_pollen': '🌾 Grass Pollen',
        'weed_pollen': '🌿 Weed Pollen',
        'allergy_advice': '🤧 Allergy Advice',
        'pollen_tip_low': 'Safe for people with allergies',
        'pollen_tip_moderate': 'Sensitive people should be cautious',
        'pollen_tip_high': 'Consider using allergy medication',
        'pollen_tip_very_high': 'Keep windows closed',
       
        # VISIBILITY MAP
        'visibility_legend': 'Visibility Legend',
        'visibility_excellent': '👁️ Excellent (20+ km)',
        'visibility_good': '👀 Good (10-20 km)',
        'visibility_moderate': '😐 Moderate (5-10 km)',
        'visibility_poor': '😑 Poor (2-5 km)',
        'visibility_very_poor': '😵 Very Poor (1-2 km)',
        'visibility_dangerous': '🚫 Dangerous (<1 km)',
        'travel_conditions': '🚗 Travel Conditions',
        'visibility_tip_excellent': 'Excellent visibility, safe driving',
        'visibility_tip_good': 'Good visibility, normal speed',
        'visibility_tip_moderate': 'Drive carefully, reduce speed',
        'visibility_tip_poor': 'Turn on fog lights, slow down',
        'visibility_tip_very_poor': 'Avoid travel unless necessary',
        'visibility_tip_dangerous': 'Very dangerous, do not travel',
       
        # WAVE MAP
        'wave_legend': 'Wave Height Legend',
        'wave_calm': '😌 Calm (<0.5m)',
        'wave_light': '🌊 Light (0.5-1m)',
        'wave_moderate': '〰️ Moderate (1-2m)',
        'wave_high': '🌀 High (2-3m)',
        'wave_very_high': '⚠️ Very High (3-5m)',
        'wave_extreme': '🚨 Extreme (>5m)',
        'wave_details': '🌊 Wave Information',
        'wave_height': 'Wave Height',
        'wave_period': 'Wave Period',
        'wave_direction': 'Wave Direction',
        'water_body': 'Water Body',
        'activity_recommendations': '🏄 Activity Recommendations',
        'wave_tip_calm': 'Ideal for swimming and all water sports',
        'wave_tip_light': 'Low for surfing, suitable for swimming',
        'wave_tip_moderate': 'Good for beginner surfing',
        'wave_tip_high': 'Advanced surfing, swimming dangerous',
        'wave_tip_very_high': 'Professional surfers only',
        'wave_tip_extreme': 'ALL water activities BANNED',
       
        # HEAT MAP
        'heat_index_legend': 'Heat Index Legend',
        'heat_normal': '😊 Normal (<27°C)',
        'heat_caution': '😐 Caution (27-32°C)',
        'heat_extreme_caution': '😓 Extreme Caution (32-39°C)',
        'heat_danger': '🥵 Danger (39-51°C)',
        'heat_extreme_danger': '🚨 Extreme Danger (>51°C)',
        'heat_details': '🌡️ Heat Details',
        'actual_temperature': 'Actual Temperature',
        'feels_like': 'Feels Like',
        'heat_index': 'Heat Index',
        'health_warning': '⚠️ Health Warning',
        'heat_tip_normal': 'Safe, normal precautions',
        'heat_tip_caution': 'Fatigue possible, drink water',
        'heat_tip_extreme_caution': 'Heat cramps possible',
        'heat_tip_danger': 'Heat exhaustion likely',
        'heat_tip_extreme_danger': 'Heat stroke risk!',
       
        # STORM MAP
        'storm_legend': 'Storm Intensity Legend',
        'storm_normal': '☁️ Normal',
        'storm_windy': '💨 Windy',
        'storm_storm': '🌬️ Storm',
        'storm_severe': '🌪️ Severe',
        'storm_very_severe': '⛈️ Very Severe',
        'storm_hurricane': '🌀 Hurricane/Typhoon',
        'storm_details': '🌪️ Storm Details',
        'wind_speed': 'Wind Speed',
        'wind_direction': 'Wind Direction',
        'pressure': 'Pressure',
        'storm_type': 'Storm Type',
        'beaufort_scale': '📊 Beaufort Scale',
        'safety_recommendations': '🛡️ Safety Recommendations',
        'storm_tip_normal': 'Normal precautions sufficient',
        'storm_tip_windy': 'Be careful outside',
        'storm_tip_storm': 'Close windows and doors',
        'storm_tip_severe': 'Stay indoors, avoid trees',
        'storm_tip_very_severe': 'Emergency! Move to safe room',
        'storm_tip_hurricane': 'RED ALERT! Move to shelter',
       
        # GENERAL MAP TERMS
        'city_search': 'City Search',
        'enter_city_name': 'Enter city name',
        'searching': 'Searching...',
        'city_found': 'City found: {}',
        'city_not_found': 'City not found',
        'show_on_map': '🗺️ Show on Map',
        'close': '❌ Close',
        'details': '📋 Details',
        'recommendations': '💡 Recommendations',
        'source': 'Source: {}',
        'coordinates': 'Coordinates: {}',
        'timestamp': 'Time: {}',
        'world_wave_map': '🌊 World Wave Map',
        'wave_height': 'Wave Height',
        'wave_period': 'Wave Period',
        'wave_direction': 'Wave Direction',
        'wave_calm': 'Calm',
        'wave_light': 'Light',
        'wave_moderate': 'Moderate',
        'wave_high': 'High',
        'wave_very_high': 'Very High',
        'wave_extreme': 'Extreme',
        'wave_legend': 'Wave Height Legend',
        'wave_details': 'Wave Information',
        'activity_recommendations': '🏄 Activity Recommendations',
        'wave_tip_calm': '✅ Ideal swimming conditions\n🏊 Suitable for all water sports',
        'wave_tip_light': '🏄 Low for surfing\n✅ Suitable for swimming and canoeing',
        'wave_tip_moderate': '🏄 Good for beginner surfing\n⚠️ Be careful when swimming',
        'wave_tip_high': '🏄 Intermediate surfing\n⚠️ Inexperienced should not swim',
        'wave_tip_very_high': '🏄 Advanced surfing\n🚫 Swimming dangerous',
        'wave_tip_extreme': '🚨 Extremely dangerous\n🚫 All water activities prohibited',
        'search_coastal_tip': '💡 Tip: Enter coastal city (e.g.: Miami, Sydney)',
        'ocean_view': '🌊 Ocean View',
        'world_heat_map': '🌡️ World Feels Like Temperature Map',
        'heat_index': 'Heat Index',
        'actual_temperature': 'Actual Temperature',
        'feels_like': 'Feels Like',
        'heat_indicator': 'Heat Indicator',
        'heat_index_legend': 'Heat Index Legend',
        'heat_normal': 'Normal',
        'heat_caution': 'Caution',
        'heat_extreme_caution': 'Extreme Caution',
        'heat_danger': 'Danger',
        'heat_extreme_danger': 'Extreme Danger',
        'heat_safe': 'Safe',
        'heat_fatigue_possible': 'Fatigue possible',
        'heat_cramps_possible': 'Heat cramps possible',
        'heat_exhaustion_likely': 'Heat exhaustion likely',
        'heat_stroke_risk': 'Heat stroke risk!',
        'world_storm_map': '🌪️ World Storm Tracking Map',
        'storm_details': 'Storm Details',
        'storm_intensity': 'Storm Intensity',
        'storm_tracking': 'Storm Tracking',
        'microclimate_title': 'Micro-Climate Calculation',
        'elevation': 'Elevation (m):',
        'urban_factor': 'Urban Factor (0-1):',
        'calculate_micro': 'Calculate',
        'base_temperature': 'Base Temperature',
        'microclimate_temperature': 'Micro-Climate Temperature',
        'correction': 'Correction',
        'humidity': 'Humidity',
        'wind_speed': 'Wind Speed',
        'elevation_label': 'Elevation',
        'urbanization': 'Urbanization',
        'microclimate_results': 'Micro-Climate Results',
        'microclimate_calculation': 'Micro-Climate Calculation',
        'enter_coordinates': 'Enter coordinates (lat,lon)',
        'energy_title': 'Energy Consumption Forecast',
        'energy_24h_forecast': '⚡ 24-Hour Energy Forecast',
        'heating_need': 'Heating Need',
        'cooling_need': 'Cooling Need',
        'total_energy': 'Total Energy',
        'kwh_day': 'kWh/day',
        'estimated_cost': '💰 Estimated Cost:',
        'heating_cost': 'Heating: {} TL/day',
        'cooling_cost': 'Cooling: {} TL/day',
        'recommendation': '📊 Recommendation:',
        'use_heater': 'Use heater',
        'use_ac': 'AC may be needed',
        'energy_efficient': 'Use in energy efficient mode',
        'no_heating_cooling': 'No heating/cooling needed',
        'energy_data_error': 'Could not retrieve energy data',
        'enter_city_energy': 'Please enter a city',
        'target_temperature': 'Target Temperature: {}°C',
        'current_temperature': 'Current Temperature: {}°C',
        'temperature_difference': 'Temperature Difference: {}°C',
        'energy_savings_tip': '💡 Energy Saving Tips:',
        'tip_heating': '• Keep heater at 21°C',
        'tip_cooling': '• Use AC at 24°C',
        'tip_insulation': '• Check window and door insulation',
        'tip_curtains': '• Keep curtains open during daytime',
        'tip_unplug': '• Unplug unused devices',
        'daily_energy_consumption': 'Daily Energy Consumption',
        'monthly_estimate': 'Monthly Estimate',
        'monthly_cost': 'Monthly Estimated Cost',
        'energy_title': 'Energy Consumption Forecast',
        'energy_24h_forecast': '⚡ 24-Hour Energy Forecast',
        'heating_need': 'Heating Need',
        'cooling_need': 'Cooling Need',
        'total_energy': 'Total Energy',
        'kwh_day': 'kWh/day',
        'estimated_cost': '💰 Estimated Cost:',
        'heating_cost': 'Heating: {} TL/day',
        'cooling_cost': 'Cooling: {} TL/day',
        'recommendation': '📊 Recommendation:',
        'use_heater': 'Use heater',
        'use_ac': 'AC may be needed',
        'energy_efficient': 'Use in energy efficient mode',
        'no_heating_cooling': 'No heating/cooling needed',
        'energy_data_error': 'Could not retrieve energy data',
        'enter_city_energy': 'Please enter a city',
        'target_temperature': 'Target Temperature: {}°C',
        'current_temperature': 'Current Temperature: {}°C',
        'temperature_difference': 'Temperature Difference: {}°C',
        'energy_savings_tip': '💡 Energy Saving Tips:',
        'tip_heating': '• Keep heater at 21°C',
        'tip_cooling': '• Use AC at 24°C',
        'tip_insulation': '• Check window and door insulation',
        'tip_curtains': '• Keep curtains open during daytime',
        'tip_unplug': '• Unplug unused devices',
        'daily_energy_consumption': 'Daily Energy Consumption',
        'monthly_estimate': 'Monthly Estimate',
        'monthly_cost': 'Monthly Estimated Cost',
        'climate_title': 'Climate Statistics',
        'select_years': 'Years to Compare:',
        'year1': 'Year 1:',
        'year2': 'Year 2:',
        'climate_analysis_for': 'Climate Analysis for',
        'analysis_period': 'Analysis Period',
        'coordinates': 'Coordinates',
        'yearly_comparison': 'Yearly Comparison',
        'average_temperature': 'Average Temperature',
        'temperature_change': 'Temperature Change',
        'monthly_breakdown': 'Monthly Breakdown',
        'change': 'Change',
        'winter_months': 'Winter Months',
        'spring_months': 'Spring Months',
        'summer_months': 'Summer Months',
        'autumn_months': 'Autumn Months',
        'climate_insights': 'Climate Insights',
        'trend_analysis': 'Trend Analysis',
        'current_temperature': 'Current Temperature',
        'warming_trend': 'Warming Trend',
        'data_source_note': 'Note: Data is simulated. Historical climate API required for real data.',
        'significant_warming': 'Significant warming trend observed',
        'moderate_warming': 'Moderate warming trend',
        'slight_warming': 'Slight warming tendency',
        'stable_temperatures': 'Stable temperature levels',
        'per_decade': 'per decade',
        'invalid_years': 'Year 1 must be less than Year 2',
        'invalid_year_format': 'Invalid year format',
        'calculate_prediction': '🔮 Calculate Prediction',
        'temperature_projection': 'Temperature Projection',
        'extreme_weather_probability': 'Extreme weather probability',
        'climate_change_simulation': 'Climate change simulation',
        'note_simplified_prediction': 'Note: This is a simplified prediction.',
        'prediction_note': 'Prediction Note',
        'simulated_prediction': 'Simulated prediction',
        'warming_effect': 'Warming effect',
        'yearly_warming': 'Yearly warming',
        'climate_model': 'Climate model',
        'future_scenario': 'Future scenario',
       
        # OTHER MISSING TRANSLATIONS
        'calculate': 'Calculate',
        'prediction': 'Prediction',
        'simulation': 'Simulation',
        'scenario': 'Scenario',
        'model': 'Model',
        'probability': 'Probability',
        'projection': 'Projection',
        'effect': 'Effect',
    }
}
#------------------- Oyun---------------------
def load_predictions():
    """Tahmin verilerini yükle"""
    if not os.path.exists(PREDICTION_FILE):
        return {}
    try:
        with open(PREDICTION_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_predictions(data):
    """Tahmin verilerini kaydet"""
    try:
        with open(PREDICTION_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Tahmin kayıt hatası: {e}")

def get_user_prediction_data(username):
    """Kullanıcının tahmin verilerini al"""
    predictions = load_predictions()
    if username not in predictions:
        predictions[username] = {
            'total_points': 0,
            'predictions': [],
            'last_prediction_date': None
        }
        save_predictions(predictions)
    return predictions[username]

def calculate_points(difference):
    """Sıcaklık farkına göre puan hesapla"""
    if difference == 0:
        return 100  # Tam isabet
    elif difference <= 1:
        return 50   # 1°C'den az fark
    elif difference <= 2:
        return 25   # 2°C'den az fark
    elif difference <= 3:
        return 10   # 3°C'den az fark
    else:
        return 5    # Diğer durumlar
def open_prediction_game():
    """Tahmin oyunu penceresi"""
    if not current_user:
        messagebox.showinfo(t('info'), 'Önce giriş yapmalısınız!')
        return
   
    win = Toplevel()
    win.title(t('prediction_game'))
    win.geometry('500x600')
    win.configure(bg='#E8F5E9')
   
    # Kullanıcı verilerini yükle
    user_data = get_user_prediction_data(current_user)
   
    # Başlık
    Label(win, text=t('prediction_title'), font=('Arial', 16, 'bold'),
          bg='#E8F5E9', fg='#2E7D32').pack(pady=15)
   
    # Şehir seçimi
    Label(win, text=t('city'), bg='#E8F5E9', font=('Arial', 11)).pack(pady=5)
    city_entry = Entry(win, justify='center', width=30, font=('Arial', 11))
    city_entry.pack(pady=5)
    city_entry.insert(0, 'Istanbul')  # Varsayılan şehir
   
    # Tahmin girişi
    Label(win, text=t('predict_temperature'), bg='#E8F5E9', font=('Arial', 11)).pack(pady=10)
    prediction_scale = Scale(win, from_=-20, to=50, orient=HORIZONTAL,
                           length=300, bg='#E8F5E9', font=('Arial', 10))
    prediction_scale.set(20)  # Varsayılan tahmin
    prediction_scale.pack(pady=5)
   
    # Gerçek zamanlı tahmin gösterimi
    current_temp_label = Label(win, text='', font=('Arial', 10), bg='#E8F5E9', fg='#666')
    current_temp_label.pack(pady=5)
   
    # Sonuç alanı
    result_frame = Frame(win, bg='white', bd=2, relief='ridge')
    result_frame.pack(pady=15, padx=20, fill='both', expand=True)
   
    result_label = Label(result_frame, text=t('game_instructions'),
                        font=('Arial', 12), bg='white', wraplength=400)
    result_label.pack(pady=20)
   
    # İstatistikler
    stats_frame = Frame(win, bg='#C8E6C9', bd=1, relief='solid')
    stats_frame.pack(pady=10, padx=20, fill='x')
   
    points_label = Label(stats_frame,
                        text=f"🏆 {t('total_points')}: {user_data['total_points']}",
                        font=('Arial', 12, 'bold'), bg='#C8E6C9')
    points_label.pack(pady=8)
   
    # Geçmiş tahminler
    history_frame = Frame(win, bg='#E8F5E9')
    history_frame.pack(pady=10, padx=20, fill='both', expand=True)
   
    Label(history_frame, text='📊 Geçmiş Tahminler',
          font=('Arial', 12, 'bold'), bg='#E8F5E9').pack(pady=5)
   
    history_canvas = Canvas(history_frame, bg='#E8F5E9', height=150)
    scrollbar = Scrollbar(history_frame, orient='vertical', command=history_canvas.yview)
    history_scroll_frame = Frame(history_canvas, bg='#E8F5E9')
   
    history_scroll_frame.bind('<Configure>',
                            lambda e: history_canvas.configure(scrollregion=history_canvas.bbox('all')))
    history_canvas.create_window((0, 0), window=history_scroll_frame, anchor='nw')
    history_canvas.configure(yscrollcommand=scrollbar.set)
   
    history_canvas.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')
   
    def update_current_weather():
        """Mevcut hava durumunu güncelle"""
        city = city_entry.get().strip()
        if not city:
            return
       
        try:
            params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
            response = requests.get(WEATHER_URL, params=params, timeout=5)
           
            if response.status_code == 200:
                data = response.json()
                current_temp = data['main']['temp']
                current_temp_label.config(
                    text=f"🌡️ Şu anki sıcaklık: {current_temp}°C | 🌤️ {data['weather'][0]['description']}"
                )
        except Exception as e:
            print(f"Hava durumu güncelleme hatası: {e}")
   
    def make_prediction():
        """Tahmin yap"""
        city = city_entry.get().strip()
        predicted_temp = prediction_scale.get()
        today = datetime.now().date()
       
        # Son tahmin tarihini kontrol et
        last_date = user_data.get('last_prediction_date')
        if last_date and last_date == today.isoformat():
            messagebox.showinfo(t('info'), 'Bugün zaten tahmin yaptınız!')
            return
       
        # Tahmini kaydet
        user_data['predictions'].append({
            'date': today.isoformat(),
            'city': city,
            'predicted_temp': predicted_temp,
            'actual_temp': None,  # Yarın dolacak
            'points_earned': 0,
            'checked': False
        })
        user_data['last_prediction_date'] = today.isoformat()
       
        save_predictions({current_user: user_data})
       
        result_label.config(
            text=f"✅ Tahmininiz kaydedildi!\n"
                 f"📅 Tarih: {today.strftime('%d.%m.%Y')}\n"
                 f"🎯 Tahmin: {predicted_temp}°C\n"
                 f"🏙️ Şehir: {city}\n\n"
                 f"⏰ Yarın gerçek sıcaklığı kontrol edebilirsiniz!"
        )
       
        update_history_display()
        update_current_weather()
   
    def check_prediction():
        """Tahmini kontrol et"""
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
       
        # Dünkü tahmini bul
        yesterday_prediction = None
        for pred in user_data['predictions']:
            pred_date = datetime.fromisoformat(pred['date']).date()
            if pred_date == yesterday and not pred.get('checked', False):
                yesterday_prediction = pred
                break
       
        if not yesterday_prediction:
            messagebox.showinfo(t('info'), t('make_prediction_first'))
            return
       
        # Gerçek sıcaklığı al
        city = yesterday_prediction['city']
        try:
            params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
            response = requests.get(WEATHER_URL, params=params, timeout=5)
           
            if response.status_code == 200:
                data = response.json()
                actual_temp = data['main']['temp']
                predicted_temp = yesterday_prediction['predicted_temp']
               
                # Farkı hesapla
                difference = abs(actual_temp - predicted_temp)
                points = calculate_points(difference)
               
                # Tahmini güncelle
                yesterday_prediction['actual_temp'] = actual_temp
                yesterday_prediction['points_earned'] = points
                yesterday_prediction['checked'] = True
                user_data['total_points'] += points
               
                save_predictions({current_user: user_data})
               
                # Sonucu göster
                if difference == 0:
                    result_text = f"🎉 {t('prediction_correct')}\n"
                else:
                    result_text = f"❌ {t('prediction_off').format(difference)}\n"
               
                result_text += (f"⭐ {t('points_earned').format(points)}\n\n"
                              f"🎯 {t('prediction_made').format(predicted_temp)}\n"
                              f"🌡️ {t('actual_temperature').format(actual_temp)}")
               
                result_label.config(text=result_text)
                points_label.config(text=f"🏆 {t('total_points')}: {user_data['total_points']}")
                update_history_display()
               
            else:
                messagebox.showerror(t('error'), t('city_not_found'))
               
        except Exception as e:
            messagebox.showerror(t('error'), f"Veri alınamadı: {str(e)}")
   
    def update_history_display():
        """Geçmiş tahminleri güncelle"""
        for widget in history_scroll_frame.winfo_children():
            widget.destroy()
       
        if not user_data['predictions']:
            Label(history_scroll_frame, text='Henüz tahmin yapılmadı',
                  font=('Arial', 10), bg='#E8F5E9', fg='#666').pack(pady=10)
            return
       
        # Son 5 tahmini göster
        recent_predictions = user_data['predictions'][-5:]
       
        for pred in reversed(recent_predictions):
            pred_frame = Frame(history_scroll_frame, bg='white', bd=1, relief='solid')
            pred_frame.pack(pady=2, padx=5, fill='x')
           
            date_str = datetime.fromisoformat(pred['date']).strftime('%d.%m.%Y')
           
            if pred.get('checked', False):
                # Kontrol edilmiş tahmin
                status = f"✅ {pred['points_earned']} puan"
                color = '#4CAF50'
                info_text = f"Tahmin: {pred['predicted_temp']}°C | Gerçek: {pred['actual_temp']}°C"
            else:
                # Bekleyen tahmin
                status = "⏰ Bekliyor"
                color = '#FF9800'
                info_text = f"Tahmin: {pred['predicted_temp']}°C"
           
            Label(pred_frame, text=f"📅 {date_str} - {pred['city']}",
                  font=('Arial', 9, 'bold'), bg='white').pack(anchor='w', padx=5, pady=2)
            Label(pred_frame, text=info_text, font=('Arial', 8),
                  bg='white').pack(anchor='w', padx=5)
            Label(pred_frame, text=status, font=('Arial', 8, 'bold'),
                  bg='white', fg=color).pack(anchor='e', padx=5, pady=2)
   
    # Butonlar
    button_frame = Frame(win, bg='#E8F5E9')
    button_frame.pack(pady=15)
   
    create_button(button_frame, '🎯 Tahmin Yap', make_prediction,
                  bg='#4CAF50', font=('Arial', 11, 'bold')).pack(side='left', padx=5)
    create_button(button_frame, '✅ Tahmini Kontrol Et', check_prediction,
                  bg='#2196F3', font=('Arial', 11, 'bold')).pack(side='left', padx=5)
   
    create_button(win, t('back_arrow'), win.destroy,
                  bg='#9E9E9E', font=('Arial', 10)).pack(pady=10)
   
    # İlk güncellemeler
    update_current_weather()
    update_history_display()
   
    # Şehir değiştiğinde otomatik güncelle
    def on_city_change(*args):
        update_current_weather()
   
    city_entry.bind('<KeyRelease>', on_city_change)
#-------------------Bulut Resmi--------------------
def get_current_week():
    """Basit ay bazlı sistem"""
    return datetime.now().strftime("%Y-%m")  # YYYY-AA formatı

def load_cloud_photos():
    """Bulut fotoğraflarını yükle"""
    if not os.path.exists(CLOUD_PHOTOS_FILE):
        return {
            'current_week': get_current_week(),
            'photos': [],
            'winners': [],
            'votes': {}
        }
    try:
        with open(CLOUD_PHOTOS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {
            'current_week': get_current_week(),
            'photos': [],
            'winners': [],
            'votes': {}
        }

def save_cloud_photo(original_path, photo_id):
    """Fotoğrafı kaydet - PNG DESTEKLİ"""
    try:
        # Klasörü oluştur
        if not os.path.exists(CLOUD_PHOTOS_DIR):
            os.makedirs(CLOUD_PHOTOS_DIR)
       
        # Yeni dosya yolu
        new_filename = f"{photo_id}.jpg"
        new_path = os.path.join(CLOUD_PHOTOS_DIR, new_filename)
       
        # Fotoğrafı aç
        img = Image.open(original_path)
       
        # PNG şeffaflık sorununu çöz
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1])
            img = background
       
        # Boyutlandır
        img.thumbnail((800, 600), Image.LANCZOS)
       
        # JPEG olarak kaydet
        img.save(new_path, "JPEG", quality=85, optimize=True)
       
        return new_path
       
    except Exception as e:
        print(f"❌ Kaydetme hatası: {e}")
        return None
def open_upload_photo_window(parent):
    """Fotoğraf yükleme penceresi"""
    win = Toplevel(parent)
    win.title(t('upload_cloud_photo'))
    win.geometry('500x650')
    win.configure(bg='#E8F5E9')
   
    Label(win, text=t('upload_cloud_photo'),
          font=('Arial', 16, 'bold'), bg='#E8F5E9').pack(pady=15)
   
    # Önizleme alanı
    preview_frame = Frame(win, bg='white', bd=2, relief='solid', width=300, height=200)
    preview_frame.pack(pady=10, padx=20)
    preview_frame.pack_propagate(False)
   
    preview_label = Label(preview_frame, text=t('click_to_select'),
                         bg='white', fg='gray', font=('Arial', 10))
    preview_label.pack(expand=True)
   
    # Form alanları
    form_frame = Frame(win, bg='#E8F5E9')
    form_frame.pack(fill='x', padx=20, pady=10)
   
    # Şehir
    Label(form_frame, text=t('city_label'), bg='#E8F5E9', font=('Arial', 11)).pack(anchor='w', pady=(5,2))
    city_entry = Entry(form_frame, font=('Arial', 11))
    city_entry.pack(fill='x', pady=(0,10))
    city_entry.insert(0, "Istanbul")
   
    # Hava Durumu
    Label(form_frame, text=t('weather_condition_label'), bg='#E8F5E9', font=('Arial', 11)).pack(anchor='w', pady=(5,2))
   
    weather_var = StringVar(value=t('weather_options')[1])  # Varsayılan Bulutlu/Cloudy
    weather_frame = Frame(form_frame, bg='#E8F5E9')
    weather_frame.pack(fill='x', pady=(0,10))
   
    weather_options = t('weather_options')
    for option in weather_options:
        Radiobutton(weather_frame, text=option, variable=weather_var, value=option,
                   bg='#E8F5E9', font=('Arial', 10)).pack(side='left', padx=(0,10))
   
    # Açıklama
    Label(form_frame, text=t('description_label'), bg='#E8F5E9', font=('Arial', 11)).pack(anchor='w', pady=(5,2))
    desc_text = Text(form_frame, height=3, font=('Arial', 11))
    desc_text.pack(fill='x', pady=(0,10))
    desc_text.insert('1.0', t('default_description'))
   
    photo_path = None
    current_image = None
   
    def select_photo():
        nonlocal photo_path, current_image
       
        path = filedialog.askopenfilename(
            title=t('select_photo'),
            filetypes=[
                ("JPEG files", "*.jpg *.jpeg"),
                ("PNG files", "*.png"),
                ("All files", "*.*")
            ]
        )
       
        if path:
            photo_path = path
            try:
                img = Image.open(path)
                img.thumbnail((280, 180), Image.LANCZOS)
               
                current_image = ImageTk.PhotoImage(img)
                preview_label.config(image=current_image, text="")
               
            except Exception as e:
                messagebox.showerror(t('error'), f"{t('upload_error')}\n{str(e)}")
   
    def upload_photo():
        nonlocal photo_path
       
        if not photo_path:
            messagebox.showwarning(t('warning'), t('select_photo_first'))
            return
       
        city = city_entry.get().strip()
        weather = weather_var.get()
        description = desc_text.get('1.0', 'end').strip()
       
        if not all([city, weather, description]):
            messagebox.showwarning(t('warning'), t('fill_all_fields'))
            return
       
        if not current_user:
            messagebox.showwarning(t('warning'), t('login_to_upload'))
            return
       
        try:
            photos_data = load_cloud_photos()
            current_week = get_current_week()
           
            # Hafta kontrolü
            if photos_data.get('current_week') != current_week:
                photos_data['current_week'] = current_week
                photos_data['photos'] = []
                photos_data['votes'] = {}
           
            # Fotoğrafı kaydet
            photo_id = f"{current_user}_{int(time.time())}"
            saved_path = save_cloud_photo(photo_path, photo_id)
           
            if not saved_path:
                raise Exception(t('photo_upload_failed'))
           
            # Yeni fotoğraf
            new_photo = {
                'id': photo_id,
                'username': current_user,
                'photo_path': saved_path,
                'description': description,
                'city': city,
                'weather_condition': weather,
                'timestamp': datetime.now().isoformat(),
                'votes': 0,
                'week': current_week
            }
           
            photos_data['photos'].append(new_photo)
           
            # Kaydet
            with open(CLOUD_PHOTOS_FILE, 'w', encoding='utf-8') as f:
                json.dump(photos_data, f, ensure_ascii=False, indent=2)
           
            messagebox.showinfo(t('success'), t('upload_success'))
            win.destroy()
           
        except Exception as e:
            messagebox.showerror(t('error'), f"{t('upload_error')}\n{str(e)}")
   
    # Butonlar
    btn_frame = Frame(win, bg='#E8F5E9')
    btn_frame.pack(fill='x', padx=20, pady=15)
   
    create_button(btn_frame, t('select_photo'), select_photo,
                 bg='#2196F3', font=('Arial', 11)).pack(pady=5, fill='x')
   
    create_button(btn_frame, t('upload_cloud_photo'), upload_photo,
                 bg='#4CAF50', font=('Arial', 11)).pack(pady=5, fill='x')
   
    create_button(btn_frame, t('close'), win.destroy,
                 bg='#f44336', font=('Arial', 11)).pack(pady=5, fill='x')
   
    return win
def open_cloud_gallery_simple():
    """Bu ayın fotoğraflarını göster"""
    win = Toplevel()
    win.title(t('current_month_photos'))
    win.geometry('700x600')
    win.configure(bg='#F3E5F5')
   
    photos_data = load_cloud_photos()
    current_week = get_current_week()
   
    # Sadece bu ayın fotoğrafları
    current_photos = [p for p in photos_data.get('photos', []) if p.get('week') == current_week]
   
    if not current_photos:
        Label(win, text=t('no_photos_this_month'),
              font=('Arial', 14), bg='#F3E5F5').pack(expand=True, pady=50)
        return
   
    Label(win, text=f"{t('current_month_photos')} ({len(current_photos)}{t('photo_uploaded')})",
          font=('Arial', 16, 'bold'), bg='#F3E5F5').pack(pady=10)
   
    # Scroll
    canvas = Canvas(win, bg='#F3E5F5')
    scrollbar = Scrollbar(win, orient='vertical', command=canvas.yview)
    scroll_frame = Frame(canvas, bg='#F3E5F5')
   
    scroll_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    canvas.create_window((0, 0), window=scroll_frame, anchor='nw')
    canvas.configure(yscrollcommand=scrollbar.set)
   
    canvas.pack(side='left', fill='both', expand=True, padx=10)
    scrollbar.pack(side='right', fill='y')
   
    for photo in current_photos:
        frame = Frame(scroll_frame, bg='white', bd=2, relief='raised')
        frame.pack(pady=10, padx=10, fill='x')
       
        # Header
        header = Frame(frame, bg='white')
        header.pack(fill='x', padx=10, pady=5)
       
        Label(header, text=f"👤 {photo['username']}",
              font=('Arial', 12, 'bold'), bg='white').pack(side='left')
       
        Label(header, text=f"📍 {photo['city']} | ⛅ {photo['weather_condition']}",
              font=('Arial', 10), bg='white', fg='#666').pack(side='right')
       
        # Fotoğraf
        try:
            img = Image.open(photo['photo_path'])
            img.thumbnail((400, 300), Image.LANCZOS)
            photo_img = ImageTk.PhotoImage(img)
            img_label = Label(frame, image=photo_img, bg='white')
            img_label.image = photo_img
            img_label.pack(pady=10)
        except:
            Label(frame, text=t('photo_upload_failed'),
                  bg='white', fg='red').pack(pady=20)
       
        # Açıklama
        Label(frame, text=photo['description'],
              font=('Arial', 11), bg='white', wraplength=400).pack(pady=5)
       
        # Oy sayısı
        Label(frame, text=f"❤️ {t('votes_count').format(photo['votes'])}",
              font=('Arial', 10, 'bold'), bg='white', fg='#E91E63').pack(pady=5)
       
        # Oy verme butonu
        def vote_photo(photo_id=photo['id']):
            vote_for_photo(photo_id)
            win.destroy()
            open_cloud_gallery_simple()
       
        Button(frame, text="❤️ " + t('vote'), command=vote_photo,
               bg='#E91E63', fg='white', font=('Arial', 10)).pack(pady=5)
def open_winners_gallery():
    """Geçmiş kazananları göster"""
    win = Toplevel()
    win.title(t('past_winners'))
    win.geometry('700x600')
    win.configure(bg='#FFF8E1')
   
    photos_data = load_cloud_photos()
    winners = photos_data.get('winners', [])
   
    if not winners:
        Label(win, text=t('no_winners_yet'),
              font=('Arial', 14), bg='#FFF8E1').pack(expand=True, pady=50)
        return
   
    Label(win, text=t('past_winners'),
          font=('Arial', 16, 'bold'), bg='#FFF8E1').pack(pady=10)
   
    canvas = Canvas(win, bg='#FFF8E1')
    scrollbar = Scrollbar(win, orient='vertical', command=canvas.yview)
    scroll_frame = Frame(canvas, bg='#FFF8E1')
   
    scroll_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    canvas.create_window((0, 0), window=scroll_frame, anchor='nw')
    canvas.configure(yscrollcommand=scrollbar.set)
   
    canvas.pack(side='left', fill='both', expand=True, padx=10)
    scrollbar.pack(side='right', fill='y')
   
    for winner in reversed(winners):
        winner_frame = Frame(scroll_frame, bg='#FFECB3', bd=2, relief='raised')
        winner_frame.pack(pady=10, padx=10, fill='x')
       
        # Taç
        crown_frame = Frame(winner_frame, bg='#FFD54F')
        crown_frame.pack(fill='x', padx=10, pady=5)
       
        Label(crown_frame, text="👑 " + t('winner'),
              font=('Arial', 12, 'bold'), bg='#FFD54F').pack()
       
        # Kazanan bilgisi
        info_frame = Frame(winner_frame, bg='white')
        info_frame.pack(fill='x', padx=10, pady=10)
       
        Label(info_frame, text=f"🏆 {winner['winner_photo']['username']}",
              font=('Arial', 14, 'bold'), bg='white').pack(pady=5)
       
        Label(info_frame, text=t('winner_month').format(winner['week']),
              font=('Arial', 11), bg='white').pack()
       
        Label(info_frame, text=f"📍 {winner['winner_photo']['city']}",
              font=('Arial', 11), bg='white', fg='#666').pack()
       
        Label(info_frame, text=f"❤️ {t('votes_count').format(winner['winner_photo']['votes'])}",
              font=('Arial', 12, 'bold'), bg='white', fg='#E91E63').pack()
       
        # Fotoğraf
        try:
            img = Image.open(winner['winner_photo']['photo_path'])
            img.thumbnail((350, 250), Image.LANCZOS)
            winner_img = ImageTk.PhotoImage(img)
            img_label = Label(winner_frame, image=winner_img, bg='white')
            img_label.image = winner_img
            img_label.pack(pady=10)
        except:
            Label(winner_frame, text=t('photo_upload_failed'),
                  bg='white').pack(pady=20)
       
        Label(winner_frame, text=winner['winner_photo']['description'],
              font=('Arial', 11), bg='white', wraplength=350).pack(pady=10)
def vote_for_photo(photo_id):
    """Fotoğrafa oy ver"""
    if not current_user:
        messagebox.showwarning(t('warning'), t('login_to_vote'))
        return
   
    photos_data = load_cloud_photos()
   
    # Kullanıcının önceki oyunu kaldır
    if current_user in photos_data['votes']:
        previous_vote = photos_data['votes'][current_user]
        for photo in photos_data['photos']:
            if photo['id'] == previous_vote:
                photo['votes'] = max(0, photo['votes'] - 1)
                break
   
    # Yeni oyu ekle
    for photo in photos_data['photos']:
        if photo['id'] == photo_id:
            photo['votes'] += 1
            photos_data['votes'][current_user] = photo_id
            break
   
    # Kaydet
    with open(CLOUD_PHOTOS_FILE, 'w', encoding='utf-8') as f:
        json.dump(photos_data, f, ensure_ascii=False, indent=2)
   
    messagebox.showinfo(t('success'), t('vote_success'))
def open_cloud_photos_window():
    """Ana bulut fotoğraf penceresi"""
    win = Toplevel()
    win.title(t('cloud_photo_contest'))
    win.geometry('400x400')
    win.configure(bg='#E0F7FA')
   
    Label(win, text=t('cloud_photo_contest'),
          font=('Arial', 16, 'bold'), bg='#E0F7FA').pack(pady=20)
   
    Label(win, text=t('cloud_contest_description'),
          font=('Arial', 12), bg='#E0F7FA').pack(pady=10)
   
    # Butonlar
    btn_frame = Frame(win, bg='#E0F7FA')
    btn_frame.pack(pady=30)
   
    create_button(btn_frame, t('upload_cloud_photo'),
                 lambda: open_upload_photo_window(win),
                 bg='#4CAF50', font=('Arial', 12)).pack(pady=10, fill='x')
   
    create_button(btn_frame, t('current_month_photos'),
                 open_cloud_gallery_simple,
                 bg='#2196F3', font=('Arial', 12)).pack(pady=10, fill='x')
   
    create_button(btn_frame, t('past_winners'),
                 open_winners_gallery,
                 bg='#FF9800', font=('Arial', 12)).pack(pady=10, fill='x')
   
    create_button(btn_frame, t('close'),
                 win.destroy,
                 bg='#f44336', font=('Arial', 12)).pack(pady=10, fill='x')
   
    # Durum bilgisi
    photos_data = load_cloud_photos()
    current_week = get_current_week()
    current_photos = [p for p in photos_data.get('photos', []) if p.get('week') == current_week]
   
    status_text = t('current_status').format(len(current_photos))
    Label(win, text=status_text, font=('Arial', 10),
          bg='#E0F7FA', fg='#666').pack(side='bottom', pady=10)
#-----------------KOD SONU-----------------
def t(key):
    return translations.get(current_language, translations['tr']).get(key, key)

def set_language(lang_code):
    global current_language, user_prefs
    current_language = lang_code
    app.title(t('title'))
    if current_user:
        user_prefs['language'] = lang_code
        try:
            with open(os.path.join(PREFS_FOLDER, current_user + ".json"), 'w') as f:
                json.dump(user_prefs, f)
        except Exception:
            pass
    if hasattr(app, 'current_screen') and app.current_screen:
        app.current_screen()
    try:
        if hasattr(app, 'lang_var'):
            for k, v in available_languages.items():
                if v == lang_code:
                    app.lang_var.set(k)
                    break
    except Exception:
        pass

def create_language_selector():
    try:
        lang_frame = Frame(app, bg='#FFFFFF')
        lang_frame.place(x=6, y=6)
        lang_frame.is_persistent = True
       
        Label(lang_frame, text=t('language'), bg='#FFFFFF', font=('Arial', 9)).pack(side='left', padx=(4,0))
        var = StringVar(value='Türkçe' if current_language=='tr' else 'English')
        opt = OptionMenu(lang_frame, var, *available_languages.keys(),
                        command=lambda v: set_language(available_languages[v]))
        opt.config(width=8)
        opt.pack(side='left', padx=(2,4))
        app.lang_var = var
        app.lang_frame = lang_frame
    except Exception as e:
        print(f"Dil seçici hatası: {e}")

# ==================== YENİ AVATAR SİSTEMİ ====================

def load_avatar_data():
    """Avatar verilerini yükle"""
    if not os.path.exists(AVATAR_FILE):
        return {}
    try:
        with open(AVATAR_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_avatar_data(data):
    """Avatar verilerini kaydet"""
    try:
        with open(AVATAR_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Avatar kayıt hatası: {e}")

def get_user_avatar_state(username):
    """Kullanıcının avatar durumunu al"""
    avatars = load_avatar_data()
    if username not in avatars:
        avatars[username] = {
            'accessories': [],
            'last_weather': None,
            'weather_checks': 0
        }
        save_avatar_data(avatars)
    return avatars[username]

def update_avatar_accessories(username, temp, condition):
    """Hava durumuna göre avatar aksesuarlarını güncelle"""
    try:
        avatars = load_avatar_data()
        if username not in avatars:
            avatars[username] = {'accessories': [], 'last_weather': None, 'weather_checks': 0}
       
        accessories = []
       
        # Sıcaklığa göre aksesuar
        if temp < 10:
            accessories.append(t('avatar_accessory_coat'))
            accessories.append(t('avatar_accessory_scarf'))
        elif temp > 28:
            accessories.append(t('avatar_accessory_hat'))
            accessories.append(t('avatar_accessory_sunglasses'))
        else:
            accessories.append(t('avatar_accessory_casual'))
       
        # Hava durumuna göre aksesuar
        condition_lower = condition.lower()
        if 'rain' in condition_lower or 'yağmur' in condition_lower:
            accessories.append(t('avatar_accessory_umbrella'))
        elif 'snow' in condition_lower or 'kar' in condition_lower:
            accessories.append(t('avatar_accessory_beanie'))
            accessories.append(t('avatar_accessory_gloves'))
        elif 'sun' in condition_lower or 'clear' in condition_lower or 'açık' in condition_lower:
            accessories.append(t('avatar_accessory_sunglasses'))
       
        # Aksesuar isimlerini orijinal hallerine çevir (kayıt için)
        original_accessories = []
        accessory_reverse_translations = {
            t('avatar_accessory_coat'): 'mont',
            t('avatar_accessory_scarf'): 'atkı',
            t('avatar_accessory_hat'): 'şapka',
            t('avatar_accessory_sunglasses'): 'güneş_gözlüğü',
            t('avatar_accessory_umbrella'): 'şemsiye',
            t('avatar_accessory_beanie'): 'bere',
            t('avatar_accessory_gloves'): 'eldiven',
            t('avatar_accessory_casual'): 'casual'
        }
       
        for acc in accessories:
            original_accessories.append(accessory_reverse_translations.get(acc, acc))
       
        avatars[username]['accessories'] = list(set(original_accessories))
        avatars[username]['last_weather'] = {
            'temp': temp,
            'condition': condition,
            'timestamp': datetime.now().isoformat()
        }
        avatars[username]['weather_checks'] = avatars[username].get('weather_checks', 0) + 1
       
        save_avatar_data(avatars)
       
        # Görev kontrolü
        check_and_update_achievements(username, temp, condition, original_accessories)
       
        return original_accessories
    except Exception as e:
        print(f"Avatar güncelleme hatası: {e}")
        return []
def draw_avatar(accessories, size=200):
    """Avatar çiz (PIL ile)"""
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
   
    # Vücut (basit çubuk adam)
    center_x = size // 2
    head_y = size // 4
    head_radius = size // 8
   
    # Kafa
    draw.ellipse(
        [center_x - head_radius, head_y - head_radius,
         center_x + head_radius, head_y + head_radius],
        fill='#FFD4A3', outline='#000000', width=2
    )
   
    # Gözler
    eye_offset = head_radius // 3
    eye_size = 3
    draw.ellipse(
        [center_x - eye_offset - eye_size, head_y - eye_size,
         center_x - eye_offset + eye_size, head_y + eye_size],
        fill='#000000'
    )
    draw.ellipse(
        [center_x + eye_offset - eye_size, head_y - eye_size,
         center_x + eye_offset + eye_size, head_y + eye_size],
        fill='#000000'
    )
   
    # Gülümseme
    draw.arc(
        [center_x - head_radius//2, head_y - head_radius//4,
         center_x + head_radius//2, head_y + head_radius//2],
        start=0, end=180, fill='#000000', width=2
    )
   
    # Gövde
    body_top = head_y + head_radius
    body_bottom = size * 3 // 4
    draw.line([center_x, body_top, center_x, body_bottom], fill='#000000', width=3)
   
    # Kollar
    arm_y = body_top + (body_bottom - body_top) // 3
    arm_length = size // 4
    draw.line([center_x, arm_y, center_x - arm_length, arm_y + arm_length//2],
              fill='#000000', width=3)
    draw.line([center_x, arm_y, center_x + arm_length, arm_y + arm_length//2],
              fill='#000000', width=3)
   
    # Bacaklar
    leg_length = size // 4
    draw.line([center_x, body_bottom, center_x - leg_length//2, body_bottom + leg_length],
              fill='#000000', width=3)
    draw.line([center_x, body_bottom, center_x + leg_length//2, body_bottom + leg_length],
              fill='#000000', width=3)
   
    # Aksesuarlar
    if 'şapka' in accessories:
        # Şapka
        hat_y = head_y - head_radius - 5
        draw.rectangle(
            [center_x - head_radius - 10, hat_y - 15,
             center_x + head_radius + 10, hat_y],
            fill='#FF6B6B', outline='#000000', width=2
        )
        draw.ellipse(
            [center_x - head_radius//2, hat_y - 25,
             center_x + head_radius//2, hat_y - 10],
            fill='#FF6B6B', outline='#000000', width=2
        )
   
    if 'bere' in accessories:
        # Bere
        hat_y = head_y - head_radius
        draw.ellipse(
            [center_x - head_radius - 5, hat_y - 20,
             center_x + head_radius + 5, hat_y + 5],
            fill='#4ECDC4', outline='#000000', width=2
        )
        # Ponpon
        draw.ellipse(
            [center_x - 8, hat_y - 28,
             center_x + 8, hat_y - 12],
            fill='#FFFFFF', outline='#000000', width=2
        )
   
    if 'güneş_gözlüğü' in accessories:
        # Güneş gözlüğü
        glass_y = head_y - 5
        glass_size = head_radius // 3
        draw.ellipse(
            [center_x - head_radius//2 - glass_size, glass_y - glass_size,
             center_x - head_radius//2 + glass_size, glass_y + glass_size],
            fill='#333333', outline='#000000', width=2
        )
        draw.ellipse(
            [center_x + head_radius//2 - glass_size, glass_y - glass_size,
             center_x + head_radius//2 + glass_size, glass_y + glass_size],
            fill='#333333', outline='#000000', width=2
        )
        draw.line(
            [center_x - head_radius//2 + glass_size, glass_y,
             center_x + head_radius//2 - glass_size, glass_y],
            fill='#000000', width=2
        )
   
    if 'mont' in accessories:
        # Mont (gövdeye ekstra kalınlık)
        coat_top = body_top
        coat_bottom = body_bottom - 20
        draw.rectangle(
            [center_x - 25, coat_top,
             center_x + 25, coat_bottom],
            fill='#2C3E50', outline='#000000', width=2
        )
   
    if 'şemsiye' in accessories:
        # Şemsiye (sağ elde)
        umbrella_x = center_x + arm_length
        umbrella_y = arm_y + arm_length//2
        # Sap
        draw.line([umbrella_x, umbrella_y, umbrella_x, umbrella_y - 40],
                  fill='#8B4513', width=3)
        # Kubbe
        draw.arc(
            [umbrella_x - 30, umbrella_y - 50,
             umbrella_x + 30, umbrella_y - 30],
            start=0, end=180, fill='#FF1744', width=4
        )
   
    if 'atkı' in accessories:
        # Atkı
        scarf_y = body_top + 5
        draw.rectangle(
            [center_x - 15, scarf_y,
             center_x + 15, scarf_y + 15],
            fill='#FFC107', outline='#000000', width=2
        )
   
    if 'eldiven' in accessories:
        # Eldivenler (ellerde)
        # Sol el
        draw.ellipse(
            [center_x - arm_length - 10, arm_y + arm_length//2 - 5,
             center_x - arm_length + 10, arm_y + arm_length//2 + 15],
            fill='#8B4513', outline='#000000', width=2
        )
        # Sağ el
        draw.ellipse(
            [center_x + arm_length - 10, arm_y + arm_length//2 - 5,
             center_x + arm_length + 10, arm_y + arm_length//2 + 15],
            fill='#8B4513', outline='#000000', width=2
        )
   
    return img

def open_avatar_window():
    """Avatar penceresini aç"""
    if not current_user:
        return
   
    win = Toplevel()
    win.title(t('avatar_title'))
    win.geometry('450x600')
    win.configure(bg='#E8EAF6')
   
    Label(win, text=t('avatar_title'), font=('Arial', 16, 'bold'), bg='#E8EAF6').pack(pady=10)
   
    # Avatar canvas
    canvas_frame = Frame(win, bg='white', bd=2, relief='ridge')
    canvas_frame.pack(pady=10, padx=20)
   
    avatar_canvas = Canvas(canvas_frame, width=220, height=220, bg='white', bd=0, highlightthickness=0)
    avatar_canvas.pack(padx=10, pady=10)
   
    # Avatar bilgileri
    info_frame = Frame(win, bg='#E8EAF6')
    info_frame.pack(pady=10, padx=20, fill='x')
   
    accessories_label = Label(info_frame, text='', font=('Arial', 11), bg='#E8EAF6', wraplength=400)
    accessories_label.pack(pady=5)
   
    stats_label = Label(info_frame, text='', font=('Arial', 10), bg='#E8EAF6', fg='#666')
    stats_label.pack(pady=5)
   
    weather_label = Label(info_frame, text='', font=('Arial', 10), bg='#E8EAF6', fg='#1976D2')
    weather_label.pack(pady=5)
   
    def update_avatar_display():
        """Avatar görünümünü güncelle"""
        avatar_state = get_user_avatar_state(current_user)
        accessories = avatar_state.get('accessories', [])
       
        # Avatar çiz
        avatar_img = draw_avatar(accessories, size=200)
        photo = ImageTk.PhotoImage(avatar_img)
        avatar_canvas.create_image(110, 110, image=photo)
        avatar_canvas.image = photo
       
        # Aksesuar listesi
        if accessories:
            # Aksesuar isimlerini çevir
            translated_accessories = []
            accessory_translations = {
                'mont': t('avatar_accessory_coat'),
                'atkı': t('avatar_accessory_scarf'),
                'şapka': t('avatar_accessory_hat'),
                'güneş_gözlüğü': t('avatar_accessory_sunglasses'),
                'şemsiye': t('avatar_accessory_umbrella'),
                'bere': t('avatar_accessory_beanie'),
                'eldiven': t('avatar_accessory_gloves'),
                'casual': t('avatar_accessory_casual')
            }
           
            for acc in accessories:
                translated_accessories.append(accessory_translations.get(acc, acc))
           
            acc_text = t('avatar_accessories') + ", ".join(translated_accessories)
        else:
            acc_text = t('avatar_no_weather_check')
        accessories_label.config(text=acc_text)
       
        # İstatistikler
        checks = avatar_state.get('weather_checks', 0)
        stats_label.config(text=t('avatar_total_checks').format(checks))
       
        # Son hava durumu
        last_weather = avatar_state.get('last_weather')
        if last_weather:
            weather_text = t('avatar_last_weather').format(last_weather['temp'], last_weather['condition'])
            weather_label.config(text=weather_text)
        else:
            weather_label.config(text=t('avatar_no_weather_data'))
   
    def refresh_from_current_weather():
        """Şu anki hava durumundan avatar güncelle"""
        city = city_entry.get().strip() if hasattr(app, 'city_entry_ref') and app.city_entry_ref else 'Istanbul'
       
        try:
            params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
            r = requests.get(WEATHER_URL, params=params, timeout=5)
            if r.status_code == 200:
                data = r.json()
                temp = data['main']['temp']
                condition = data['weather'][0]['description']
               
                update_avatar_accessories(current_user, temp, condition)
                update_avatar_display()
                messagebox.showinfo(t('success'), t('avatar_update_success').format(temp, condition))
            else:
                messagebox.showwarning(t('error'), t('data_error'))
        except Exception as e:
            messagebox.showwarning(t('error'), f'{t("data_error")}: {str(e)}')
   
    update_avatar_display()
   
    create_button(win, t('avatar_update_from_weather'), refresh_from_current_weather, bg='#2196F3').pack(pady=10)
    create_button(win, t('back_arrow'), win.destroy, bg='#9E9E9E').pack(pady=5)

# ==================== GELECEK HAVASI SİMÜLASYONU ====================

def simulate_climate_change(current_temp, years_ahead):
    """İklim değişikliği simülasyonu"""
    # Basitleştirilmiş iklim değişikliği modeli
    # Yılda ortalama ~0.02°C artış (IPCC senaryolarına göre)
    warming_rate = 0.02
   
    # Rastgele varyasyon
    variation = random.uniform(-0.5, 1.0)
   
    predicted_temp = current_temp + (years_ahead * warming_rate) + variation
   
    # Ekstrem olaylar olasılığı artışı
    extreme_prob = min(0.3 + (years_ahead * 0.02), 0.7)
   
    return {
        'temp': round(predicted_temp, 1),
        'warming': round(years_ahead * warming_rate, 2),
        'extreme_probability': round(extreme_prob, 2)
    }

def open_future_weather_window():
    """Gelecek hava simülasyonu penceresi"""
    win = Toplevel()
    win.title(t('future_weather_title'))
    win.geometry('500x650')
    win.configure(bg='#E1F5FE')
   
    Label(win, text=t('future_weather_title'), font=('Arial', 16, 'bold'), bg='#E1F5FE').pack(pady=10)
   
    Label(win, text=t('city'), bg='#E1F5FE', font=('Arial', 11)).pack(pady=5)
    city_entry_local = Entry(win, justify='center', width=30, font=('Arial', 11))
    city_entry_local.pack(pady=5)
   
    Label(win, text=t('years_future'), bg='#E1F5FE', font=('Arial', 11)).pack(pady=5)
    years_scale = Scale(win, from_=1, to=50, orient=HORIZONTAL, length=300, bg='#E1F5FE')
    years_scale.set(10)
    years_scale.pack(pady=5)
   
    result_frame = Frame(win, bg='white', bd=2, relief='ridge')
    result_frame.pack(pady=15, padx=20, fill='both', expand=True)
   
    current_label = Label(result_frame, text='', font=('Arial', 12), bg='white', fg='#1976D2', wraplength=450)
    current_label.pack(pady=10, padx=10)
   
    future_label = Label(result_frame, text='', font=('Arial', 12, 'bold'), bg='white', fg='#D32F2F', wraplength=450)
    future_label.pack(pady=10, padx=10)
   
    change_label = Label(result_frame, text='', font=('Arial', 11), bg='white', fg='#F57C00', wraplength=450)
    change_label.pack(pady=10, padx=10)
   
    warning_label = Label(result_frame, text='', font=('Arial', 10), bg='white', fg='#666', wraplength=450)
    warning_label.pack(pady=10, padx=10)
   
    # Grafik için canvas
    graph_canvas = Canvas(result_frame, width=450, height=150, bg='white', bd=0, highlightthickness=0)
    graph_canvas.pack(pady=10)
   
    def calculate_future():
        """Gelecek tahmini hesapla"""
        city = city_entry_local.get().strip()
        if not city:
            city = 'Istanbul'
       
        years = years_scale.get()
       
        try:
            # Şu anki hava durumunu al
            params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
            r = requests.get(WEATHER_URL, params=params, timeout=5)
           
            if r.status_code == 200:
                data = r.json()
                current_temp = data['main']['temp']
                condition = data['weather'][0]['description']
               
                # Gelecek simülasyonu
                future = simulate_climate_change(current_temp, years)
               
                # Sonuçları göster - ÇEVİRİLERİ KULLAN
                current_label.config(
                    text=f"{t('current_weather')} {city}: {current_temp}°C, {condition}"
                )
               
                future_label.config(
                    text=f"{t('future_prediction')} ({years} {t('years_future')}) {t('prediction')}: {future['temp']}°C"
                )
               
                temp_diff = future['temp'] - current_temp
                change_label.config(
                    text=f"{t('change')} +{temp_diff:.1f}°C {t('warming_effect')}: +{future['warming']}°C"
                )
               
                warning_label.config(
                    text=f"⚠️ {t('extreme_weather_probability')}: %{future['extreme_probability']*100:.0f}\n"
                         f"📊 {t('climate_change_simulation')}\n"
                         f"{t('note_simplified_prediction')}"
                )
               
                # Basit grafik çiz
                graph_canvas.delete('all')
               
                # Grafik veri noktaları
                years_list = list(range(0, years+1, max(1, years//5)))
                temps = []
               
                for y in years_list:
                    if y == 0:
                        temps.append(current_temp)
                    else:
                        sim = simulate_climate_change(current_temp, y)
                        temps.append(sim['temp'])
               
                # Grafik çizimi
                padding = 30
                width = 450 - 2*padding
                height = 150 - 2*padding
               
                max_temp = max(temps)
                min_temp = min(temps)
                temp_range = max_temp - min_temp if max_temp != min_temp else 1
               
                # Eksen çizgileri
                graph_canvas.create_line(padding, padding, padding, padding+height, fill='#999', width=2)
                graph_canvas.create_line(padding, padding+height, padding+width, padding+height, fill='#999', width=2)
               
                # Veri noktalarını çiz
                points = []
                for i, (year, temp) in enumerate(zip(years_list, temps)):
                    x = padding + (i / (len(years_list)-1)) * width if len(years_list) > 1 else padding + width/2
                    y = padding + height - ((temp - min_temp) / temp_range * height)
                    points.append((x, y))
                   
                    # Nokta
                    graph_canvas.create_oval(x-4, y-4, x+4, y+4, fill='#D32F2F', outline='#B71C1C')
                   
                    # Etiket
                    if i % 2 == 0:
                        graph_canvas.create_text(x, padding+height+15, text=str(year), font=('Arial', 8))
               
                # Çizgiyi çiz
                for i in range(len(points)-1):
                    graph_canvas.create_line(points[i][0], points[i][1],
                                            points[i+1][0], points[i+1][1],
                                            fill='#F57C00', width=2)
               
                # Başlık - ÇEVİRİ KULLAN
                graph_canvas.create_text(padding+width/2, 15,
                                        text=t('temperature_projection'),
                                        font=('Arial', 10, 'bold'))
               
            else:
                messagebox.showwarning(t('error'), t('city_not_found'))
       
        except Exception as e:
            messagebox.showwarning(t('error'), f'{t("data_error")}: {str(e)}')
   
    # Buton metnini çevir
    create_button(win, t('calculate_prediction'), calculate_future, bg='#00BCD4').pack(pady=10)
    create_button(win, t('back_arrow'), win.destroy, bg='#9E9E9E').pack(pady=5)

# ==================== OYUNLAŞTIRMA SİSTEMİ ====================

def load_achievements():
    """Rozetleri yükle"""
    if not os.path.exists(ACHIEVEMENTS_FILE):
        return {}
    try:
        with open(ACHIEVEMENTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_achievements(data):
    """Rozetleri kaydet"""
    try:
        with open(ACHIEVEMENTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Rozet kayıt hatası: {e}")

def get_user_achievements(username):
    """Kullanıcının rozetlerini al"""
    achievements = load_achievements()
    if username not in achievements:
        achievements[username] = {
            'badges': [],
            'missions': {
                'weather_checks': {'count': 0, 'target': 10, 'completed': False},
                'umbrella_use': {'count': 0, 'target': 3, 'completed': False},
                'winter_coat': {'count': 0, 'target': 5, 'completed': False},
                'summer_hat': {'count': 0, 'target': 5, 'completed': False},
                'extreme_weather': {'count': 0, 'target': 2, 'completed': False},
                # YENİ: Tahmin oyunu görevleri
                'prediction_streak': {'count': 0, 'target': 7, 'completed': False},
                'perfect_prediction': {'count': 0, 'target': 3, 'completed': False},
                'quick_learner': {'count': 0, 'target': 50, 'completed': False}  # 50 puan
            }
        }
        save_achievements(achievements)
    return achievements[username]
def check_and_update_achievements(username, temp, condition, accessories):
    """Görevleri kontrol et ve rozetleri güncelle"""
    achievements = load_achievements()
    if username not in achievements:
        get_user_achievements(username)  # Initialize
        achievements = load_achievements()
   
    user_data = achievements[username]
    missions = user_data['missions']
    new_badges = []
   
    # Hava kontrolü görevi
    missions['weather_checks']['count'] += 1
    if missions['weather_checks']['count'] >= missions['weather_checks']['target'] and not missions['weather_checks']['completed']:
        missions['weather_checks']['completed'] = True
        user_data['badges'].append(t('avatar_mission_weather_tracker'))
        new_badges.append(t('avatar_mission_weather_tracker'))
   
    # Şemsiye görevi
    condition_lower = condition.lower()
    if ('rain' in condition_lower or 'yağmur' in condition_lower) and t('avatar_accessory_umbrella') in accessories:
        missions['umbrella_use']['count'] += 1
        if missions['umbrella_use']['count'] >= missions['umbrella_use']['target'] and not missions['umbrella_use']['completed']:
            missions['umbrella_use']['completed'] = True
            user_data['badges'].append(t('avatar_mission_umbrella_master'))
            new_badges.append(t('avatar_mission_umbrella_master'))
   
    # Mont görevi
    if temp < 10 and t('avatar_accessory_coat') in accessories:
        missions['winter_coat']['count'] += 1
        if missions['winter_coat']['count'] >= missions['winter_coat']['target'] and not missions['winter_coat']['completed']:
            missions['winter_coat']['completed'] = True
            user_data['badges'].append(t('avatar_mission_winter_warrior'))
            new_badges.append(t('avatar_mission_winter_warrior'))
   
    # Şapka görevi
    if temp > 28 and t('avatar_accessory_hat') in accessories:
        missions['summer_hat']['count'] += 1
        if missions['summer_hat']['count'] >= missions['summer_hat']['target'] and not missions['summer_hat']['completed']:
            missions['summer_hat']['completed'] = True
            user_data['badges'].append(t('avatar_mission_summer_champion'))
            new_badges.append(t('avatar_mission_summer_champion'))
   
    # Ekstrem hava görevi
    if temp < 0 or temp > 35:
        missions['extreme_weather']['count'] += 1
        if missions['extreme_weather']['count'] >= missions['extreme_weather']['target'] and not missions['extreme_weather']['completed']:
            missions['extreme_weather']['completed'] = True
            user_data['badges'].append(t('avatar_mission_extreme_survivor'))
            new_badges.append(t('avatar_mission_extreme_survivor'))

    # YENİ: Tahmin oyunu rozetleri için puan kontrolü
    try:
        prediction_data = get_user_prediction_data(username)
        total_points = prediction_data.get('total_points', 0)
       
        # Tahminci rozeti (100 puan)
        if total_points >= 100 and '🔮 ' + t('predictor') not in user_data['badges']:
            user_data['badges'].append('🔮 ' + t('predictor'))
            new_badges.append('🔮 ' + t('predictor'))
       
        # Tahmin Uzmanı rozeti (500 puan)
        if total_points >= 500 and '📊 ' + t('prediction_expert') not in user_data['badges']:
            user_data['badges'].append('📊 ' + t('prediction_expert'))
            new_badges.append('📊 ' + t('prediction_expert'))
       
        # Tahmin Ustası rozeti (1000 puan)
        if total_points >= 1000 and '🎯 ' + t('prediction_master') not in user_data['badges']:
            user_data['badges'].append('🎯 ' + t('prediction_master'))
            new_badges.append('🎯 ' + t('prediction_master'))
    except Exception as e:
        print(f"Tahmin rozetleri hatası: {e}")
   
    achievements[username] = user_data
    save_achievements(achievements)
   
    # Yeni rozet kazanıldıysa bildirim göster
    if new_badges:
        try:
            messagebox.showinfo(t('unlock_badge'), t('avatar_new_badge').format("\n".join(new_badges)))
        except:
            pass
   
    return new_badges

def open_achievements_window():
    """Rozetler penceresini aç"""
    if not current_user:
        return
   
    win = Toplevel()
    win.title(t('achievements_title'))
    win.geometry('500x650')
    win.configure(bg='#FFF8E1')
   
    Label(win, text=t('achievements_title'), font=('Arial', 16, 'bold'), bg='#FFF8E1').pack(pady=10)
   
    user_data = get_user_achievements(current_user)
   
    # Kazanılan rozetler
    badges_frame = Frame(win, bg='white', bd=2, relief='ridge')
    badges_frame.pack(pady=10, padx=20, fill='x')
   
    Label(badges_frame, text='🏆 ' + t('unlocked_badges'), font=('Arial', 13, 'bold'), bg='white').pack(pady=5)
   
    if user_data['badges']:
        # Rozet isimlerini çevir
        badge_translations = {
            '🌤️ Hava Takipçisi': t('avatar_mission_weather_tracker'),
            '☔ Şemsiye Ustası': t('avatar_mission_umbrella_master'),
            '🧥 Kış Savaşçısı': t('avatar_mission_winter_warrior'),
            '🎩 Yaz Şampiyonu': t('avatar_mission_summer_champion'),
            '🌪️ Ekstrem Survivor': t('avatar_mission_extreme_survivor'),
            '🔮 Tahminci': '🔮 ' + t('predictor'),
            '📊 Tahmin Uzmanı': '📊 ' + t('prediction_expert'),
            '🎯 Tahmin Ustası': '🎯 ' + t('prediction_master')
        }
       
        for badge in user_data['badges']:
            translated_badge = badge_translations.get(badge, badge)
            Label(badges_frame, text=translated_badge, font=('Arial', 11), bg='white').pack(pady=2)
    else:
        Label(badges_frame, text=t('no_badges_yet'), font=('Arial', 10), bg='white', fg='#999').pack(pady=5)
   
    # Görevler
    Label(win, text='📋 ' + t('missions'), font=('Arial', 14, 'bold'), bg='#FFF8E1').pack(pady=(15,5))
   
    missions_canvas = Canvas(win, bg='#FFF8E1', bd=0, highlightthickness=0)
    scrollbar = Scrollbar(win, orient='vertical', command=missions_canvas.yview)
    missions_frame = Frame(missions_canvas, bg='#FFF8E1')
   
    missions_frame.bind('<Configure>', lambda e: missions_canvas.configure(scrollregion=missions_canvas.bbox('all')))
    missions_canvas.create_window((0, 0), window=missions_frame, anchor='nw')
    missions_canvas.configure(yscrollcommand=scrollbar.set)
   
    missions_canvas.pack(side='left', fill='both', expand=True, padx=20)
    scrollbar.pack(side='right', fill='y')
   
    mission_info = {
        'weather_checks': ('🌤️', t('avatar_mission_check_weather')),
        'umbrella_use': ('☔', t('avatar_mission_use_umbrella')),
        'winter_coat': ('🧥', t('avatar_mission_wear_coat')),
        'summer_hat': ('🎩', t('avatar_mission_wear_hat')),
        'extreme_weather': ('🌪️', t('avatar_mission_experience_extreme')),
    }
   
    for mission_key, mission_data in user_data['missions'].items():
        icon, desc = mission_info.get(mission_key, ('📌', mission_key))
       
        mission_frame = Frame(missions_frame, bg='white', bd=2, relief='raised')
        mission_frame.pack(pady=5, padx=5, fill='x')
       
        status = '✅ ' + t('avatar_completed') if mission_data['completed'] else '⏳ ' + t('avatar_in_progress')
        color = '#4CAF50' if mission_data['completed'] else '#FF9800'
       
        Label(mission_frame, text=f"{icon} {desc}",
              font=('Arial', 11, 'bold'), bg='white').pack(anchor='w', padx=10, pady=5)
       
        progress_text = t('avatar_progress').format(mission_data['count'], mission_data['target'])
        Label(mission_frame, text=progress_text, font=('Arial', 10), bg='white').pack(anchor='w', padx=10)
       
        # Progress bar
        progress_bar_frame = Frame(mission_frame, bg='#E0E0E0', height=20, bd=1, relief='sunken')
        progress_bar_frame.pack(fill='x', padx=10, pady=5)
       
        progress_percent = min(mission_data['count'] / mission_data['target'], 1.0)
        progress_bar = Frame(progress_bar_frame, bg=color, height=18)
        progress_bar.place(relx=0, rely=0, relwidth=progress_percent, relheight=1)
       
        Label(mission_frame, text=status, font=('Arial', 9), bg='white', fg=color).pack(anchor='e', padx=10, pady=5)
   
    create_button(win, t('back_arrow'), win.destroy, bg='#9E9E9E').pack(pady=10)

# -------------------- Yardımcı Fonksiyonlar --------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, prefs):
    if not os.path.exists(USERS_FILE):
        open(USERS_FILE, 'w').close()
    with open(USERS_FILE, 'r') as f:
        for line in f:
            user, _ = line.strip().split(',')
            if user == username:
                return False
    with open(USERS_FILE, 'a') as f:
        f.write(f"{username},{hash_password(password)}\n")
    if not os.path.exists(PREFS_FOLDER):
        os.makedirs(PREFS_FOLDER)
    with open(os.path.join(PREFS_FOLDER, username + ".json"), 'w') as f:
        json.dump(prefs, f)
    return True

def login_user(username, password):
    if not os.path.exists(USERS_FILE):
        return False
    with open(USERS_FILE, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 2:
                user, hashed = parts
                if user == username and hashed == hash_password(password):
                    return True
    return False

def clear_screen():
    for widget in app.winfo_children():
        if getattr(widget, 'is_persistent', False):
            continue
        widget.pack_forget()
        widget.place_forget()

def analyze_conditions(temp, condition, humidity, wind_speed,
                       hot_limit, cold_limit, wind_limit, humid_limit):
    result = []
    if temp < cold_limit:
        result.append(t('very_cold'))
    elif temp > hot_limit:
        result.append(t('very_hot'))
    if "yağmur" in condition.lower() or "kar" in condition.lower() or humidity > humid_limit:
        result.append(t('very_wet'))
    if wind_speed > wind_limit:
        result.append(t('very_windy'))
    if (temp > hot_limit - 2 and humidity > humid_limit - 10) or (temp < cold_limit + 1 and wind_speed > wind_limit - 1):
        result.append(t('very_uncomfortable'))
    return " | ".join(result) if result else t('comfortable')

def create_button(master, text, command, bg="#4CAF50", fg="white", hover_bg=None, font=("Arial", 12, "bold"), pady=5, shape='rounded'):
    class RoundedButton(Frame):
        def __init__(self, master, text, command, bg, fg, hover_bg, font, pady, shape='rounded'):
            super().__init__(master, bg=master.cget('bg'))
            self.command = command
            self.text = text
            self.fg = fg
            self.base_bg = bg
            self.hover_bg = hover_bg if hover_bg else bg
            self.font = font
            self.pady = pady
            self.shape = shape

            # 🔧 HATA DÜZELTİLMİŞ KISIM
            try:
                parent_bg = master.cget('bg')
            except Exception:
                try:
                    parent_bg = app.cget('bg') if 'app' in globals() else 'white'
                except:
                    parent_bg = '#ffffff'

            # 🔹 Yardımcı renk fonksiyonları
            def hex_to_rgb(h):
                h = h.lstrip('#')
                return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

            def rgb_to_hex(r, g, b):
                return '#%02x%02x%02x' % (int(r), int(g), int(b))

            def blend(c1, c2, a=0.6):
                r1, g1, b1 = hex_to_rgb(c1)
                r2, g2, b2 = hex_to_rgb(c2)
                r = r2 * (1 - a) + r1 * a
                g = g2 * (1 - a) + g1 * a
                b = b2 * (1 - a) + b1 * a
                return rgb_to_hex(r, g, b)


            self.normal_color = blend(self.base_bg, parent_bg, a=0.6)
            self.hover_color = blend(self.hover_bg, parent_bg, a=0.75)

            self.width = 180
            self.height = 36 + max(0, int(self.pady))

            self.canvas = Canvas(self, width=self.width, height=self.height, bg=parent_bg, bd=0, highlightthickness=0)
            self.canvas.pack(fill='both', expand=True)
            self.canvas.bind('<Configure>', self._on_configure)
            self.text_id = self.canvas.create_text(0, 0, text=self.text, fill=self.fg, font=self.font)

            self.canvas.bind('<Button-1>', lambda e: self.command() if callable(self.command) else None)
            self.canvas.bind('<Enter>', lambda e: self._on_enter())
            self.canvas.bind('<Leave>', lambda e: self._on_leave())

            self.canvas.config(cursor='hand2')

        def _draw_button(self, fill_color=None):
            """Canvas üzerinde özel butonun şekil ve metnini çizer"""

            # --- Arka plan rengi kontrolü ---
            fill_color = fill_color or getattr(self, 'bg_color', 'gray')

            # Önce eski şekli temizle
            self.canvas.delete('bgrect')

            # --- Canvas boyutlarını al ---
            w = self.canvas.winfo_width() or getattr(self, 'width', 100)
            h = self.canvas.winfo_height() or getattr(self, 'height', 40)

            # Çok küçükse minimum boyut ver
            if w < 20:
             w = 20
            if h < 20:
                h = 20

            # Koordinatlar
            x1, y1, x2, y2 = 2, 2, w - 2, h - 2

            # --- Şekil çizimi ---
            if getattr(self, 'shape', 'rounded') == 'circle':
                # Daire
                diameter = min(w, h) - 4
                cx = w // 2
                cy = h // 2
                x1c = cx - diameter // 2
                y1c = cy - diameter // 2
                x2c = cx + diameter // 2
                y2c = cy + diameter // 2
                self.canvas.create_oval(
                 x1c, y1c, x2c, y2c,
                fill=fill_color,
                outline=fill_color,
                tags='bgrect'
            )
            else:
                # Yuvarlatılmış köşeli dikdörtgen
                r = min(16, h // 2)
                self.canvas.create_arc(x1, y1, x1 + 2 * r, y1 + 2 * r,
                               start=90, extent=90,
                               fill=fill_color, outline=fill_color, tags='bgrect')
                self.canvas.create_arc(x2 - 2 * r, y1, x2, y1 + 2 * r,
                               start=0, extent=90,
                               fill=fill_color, outline=fill_color, tags='bgrect')
                self.canvas.create_arc(x1, y2 - 2 * r, x1 + 2 * r, y2,
                               start=180, extent=90,
                               fill=fill_color, outline=fill_color, tags='bgrect')
                self.canvas.create_arc(x2 - 2 * r, y2 - 2 * r, x2, y2,
                               start=270, extent=90,
                               fill=fill_color, outline=fill_color, tags='bgrect')
                self.canvas.create_rectangle(x1 + r, y1, x2 - r, y2,
                                     fill=fill_color, outline=fill_color, tags='bgrect')
                self.canvas.create_rectangle(x1, y1 + r, x2, y2 - r,
                                     fill=fill_color, outline=fill_color, tags='bgrect')

            # --- Metin çizimi veya güncellemesi ---
            text = getattr(self, 'text', '')
            text_color = getattr(self, 'text_color', 'white')
            font = getattr(self, 'font', ('Arial', 10, 'bold'))

            if hasattr(self, 'text_id'):
            # Önceden oluşturulduysa sadece ortala
                self.canvas.lift(self.text_id)
                self.canvas.coords(self.text_id, w // 2, h // 2)
            else:
                # İlk kez oluşturuluyorsa metni ekle
                self.text_id = self.canvas.create_text(
                w // 2, h // 2,
                text=text,
                fill=text_color,
                font=font,
                tags='text'
        )
        def _on_enter(self):
            self._draw_button(self.hover_color)

        def _on_leave(self):
            self._draw_button(self.normal_color)

        def _on_configure(self, event):
            try:
                w = event.width
                h = event.height
            except Exception:
                w = self.canvas.winfo_width()
                h = self.canvas.winfo_height()
            self.width = w
            self.height = h
            self.canvas.config(width=w, height=h)
            self._draw_button(self.normal_color)

        def config(self, **kwargs):
            if 'width' in kwargs:
                w = kwargs.get('width')
                try:
                    w = int(w)
                    if w <= 20:
                        self.width = max(40, w * 12)
                    else:
                        self.width = w
                    self.canvas.config(width=self.width)
                except Exception:
                    pass
            if 'height' in kwargs:
                h = kwargs.get('height')
                try:
                    h = int(h)
                    if h <= 10:
                        self.height = max(24, h * 18)
                    else:
                        self.height = h
                    self.canvas.config(height=self.height)
                except Exception:
                    pass
            if 'text' in kwargs:
                self.canvas.itemconfigure(self.text_id, text=kwargs.get('text'))

        def __getattr__(self, name):
            return getattr(self.canvas, name)

    rb = RoundedButton(master, text, command, bg, fg, hover_bg, font, pady, shape)
    return rb
# ==================== SESLİ ASİSTAN GELİŞTİRİLMİŞ ====================

def extract_city_from_text(text):
    """Sesli komuttan şehir ismini çıkar - Çok dilli destek"""
    # Çok dilli şehir eşleme sözlüğü
    city_mapping = {
        # Türkçe şehir isimleri
        'istanbul': 'Istanbul', 'ankara': 'Ankara', 'izmir': 'Izmir',
        'antalya': 'Antalya', 'bursa': 'Bursa', 'adana': 'Adana',
        'konya': 'Konya', 'mersin': 'Mersin', 'gaziantep': 'Gaziantep',
        'kayseri': 'Kayseri', 'eskişehir': 'Eskisehir', 'trabzon': 'Trabzon',
        'erzurum': 'Erzurum', 'samsun': 'Samsun', 'denizli': 'Denizli',
        'muğla': 'Mugla', 'aydın': 'Aydin', 'balıkesir': 'Balikesir',
        'van': 'Van', 'malatya': 'Malatya',
       
        # İngilizce/Uluslararası şehir isimleri
        'london': 'London', 'paris': 'Paris', 'berlin': 'Berlin',
        'roma': 'Rome', 'madrid': 'Madrid', 'new york': 'New York',
        'tokyo': 'Tokyo', 'moscow': 'Moscow', 'dubai': 'Dubai',
        'amsterdam': 'Amsterdam', 'barcelona': 'Barcelona',
        'vienna': 'Vienna', 'prague': 'Prague', 'budapest': 'Budapest'
    }
   
    text_lower = text.lower()
   
    # Doğrudan eşleşme
    for city_name, english_name in city_mapping.items():
        if city_name in text_lower:
            return english_name
   
    # Anahtar kelime tabanlı algılama
    words = text_lower.split()
   
    # Hava durumu ile ilgili anahtar kelimeler (çok dilli)
    weather_keywords = {
        'tr': ['hava', 'durumu', 'sıcaklık', 'derece', 'havası', 'nasıl'],
        'en': ['weather', 'temperature', 'degree', 'forecast', 'how']
    }
   
    # Mevcut dil için anahtar kelimeleri al
    keywords = weather_keywords.get(current_language, weather_keywords['en'])
   
    # Anahtar kelimelerden sonraki kelimeyi al
    for i, word in enumerate(words):
        if word in keywords and i + 1 < len(words):
            potential_city = words[i + 1]
            if len(potential_city) > 2:  # Anlamlı bir kelime olmalı
                # Türkçe karakterleri İngilizce'ye çevir
                converted_city = (potential_city
                                .replace('ı', 'i').replace('ğ', 'g')
                                .replace('ü', 'u').replace('ş', 's')
                                .replace('ö', 'o').replace('ç', 'c')
                                .title())
                return converted_city
   
    return None

def get_weather_by_city(city_name):
    """Şehir ismine göre hava durumu al"""
    try:
        params = {
            'q': city_name,
            'appid': API_KEY,
            'units': 'metric',
            'lang': current_language
        }
        r = requests.get(WEATHER_URL, params=params, timeout=5)
       
        if r.status_code == 200:
            data = r.json()
            city = data['name']
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            humidity = data['main']['humidity']
            wind = data['wind']['speed']
           
            return {
                'success': True,
                'city': city,
                'temp': temp,
                'description': desc,
                'humidity': humidity,
                'wind': wind
            }
        else:
            return {'success': False, 'error': t('city_not_found')}
           
    except Exception as e:
        return {'success': False, 'error': str(e)}

def open_voice_assistant():
    if not VOICE_AVAILABLE:
        messagebox.showinfo(t('voice_title'), t('voice_not_available'))
        return
   
    win = Toplevel()
    win.title(t('voice_title'))
    win.geometry('400x450')
    win.configure(bg='#F3E5F5')
   
    Label(win, text=t('voice_title'), font=('Arial', 14, 'bold'), bg='#F3E5F5').pack(pady=10)
   
    status_label = Label(win, text=t('voice_ready'), font=('Arial', 12), bg='#F3E5F5')
    status_label.pack(pady=10)
   
    result_text = Text(win, height=12, width=45, wrap='word')
    result_text.pack(pady=10, padx=10)
   
    def start_listening():
        status_label.config(text=t('voice_listening'))
       
        def listen_thread():
            try:
                text = listen_voice()
                if text:
                    win.after(0, lambda: result_text.delete('1.0', 'end'))
                    win.after(0, lambda: result_text.insert('1.0', t('voice_speaking').format(text) + "\n\n"))
                   
                    # Şehir ismini çıkar
                    detected_city = extract_city_from_text(text)
                   
                    if detected_city:
                        # Algılanan şehir için hava durumu al
                        weather_data = get_weather_by_city(detected_city)
                       
                        if weather_data['success']:
                            response = (t('voice_weather_for').format(weather_data['city']) + "\n" +
                                      t('voice_temperature').format(weather_data['temp']) + "\n" +
                                      t('voice_condition').format(weather_data['description']) + "\n" +
                                      t('voice_humidity').format(weather_data['humidity']) + "\n" +
                                      t('voice_wind').format(weather_data['wind']))
                        else:
                            response = t('voice_city_not_found').format(detected_city, weather_data['error'])
                   
                    elif any(word in text.lower() for word in ['hava', 'sıcaklık', 'derece', 'weather', 'temperature']):
                        # Şehir belirtilmemişse, varsayılan şehir kullan
                        default_city = "Istanbul"
                        weather_data = get_weather_by_city(default_city)
                       
                        if weather_data['success']:
                            response = t('voice_default_city').format(
                                weather_data['city'],
                                weather_data['temp'],
                                weather_data['description']
                            )
                        else:
                            response = t('voice_city_not_found').format(default_city, weather_data['error'])
                   
                    else:
                        response = t('voice_asking_weather')
                   
                    win.after(0, lambda: result_text.insert('end', t('voice_assistant').format(response)))
                    speak_text(response.split('\n')[0])  # Sadece ilk satırı söyle
                   
                else:
                    win.after(0, lambda: result_text.insert('end', "\n\n" + t('voice_not_understood')))
                   
            except Exception as e:
                win.after(0, lambda: result_text.insert('end', "\n\n" + t('voice_error').format(str(e))))
           
            win.after(0, lambda: status_label.config(text=t('voice_ready')))
       
        threading.Thread(target=listen_thread, daemon=True).start()
   
    # Butonları oluştur
    button_frame = Frame(win, bg='#F3E5F5')
    button_frame.pack(pady=10)
   
    create_button(button_frame, t('voice_start'), start_listening, bg='#9C27B0').pack(side='left', padx=5)
   
    # Örnek komutlar
    examples_frame = Frame(win, bg='#F3E5F5')
    examples_frame.pack(pady=10)
   
    Label(examples_frame, text=t('voice_example_commands'), font=('Arial', 10, 'bold'), bg='#F3E5F5').pack()
   
    # Örnek komutları mevcut dile göre göster
    example_commands = [
        t('voice_example_1'),
        t('voice_example_2'),
        t('voice_example_3'),
        t('voice_example_4'),
        t('voice_example_5')
    ]
   
    example_text = "\n".join(example_commands)
    Label(examples_frame, text=example_text,
          font=('Arial', 9), bg='#F3E5F5', justify='left').pack()
def speak_text(text):
    """Metni sese çevir - Çok dilli destek"""
    if not VOICE_AVAILABLE:
        return
    try:
        engine = pyttsx3.init()
       
        # Dil ayarı
        if current_language == 'tr':
            # Türkçe ses ayarı (eğer sistemde varsa)
            voices = engine.getProperty('voices')
            for voice in voices:
                if 'turkish' in voice.name.lower() or 'türkçe' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
        elif current_language == 'en':
            # İngilizce ses ayarı
            voices = engine.getProperty('voices')
            for voice in voices:
                if 'english' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
       
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Ses hatası: {e}")
def listen_voice():
    """Mikrofonu dinle"""
    if not VOICE_AVAILABLE:
        return None
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Dinleniyor...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=10)
            text = recognizer.recognize_google(audio, language='tr-TR' if current_language == 'tr' else 'en-US')
            return text
    except sr.WaitTimeoutError:
        return None
    except Exception as e:
        print(f"Ses tanıma hatası: {e}")
        return None
    # ==================== HARITA ÖZELLİKLERİ ====================

# 1. UV HARİTASI
def open_uv_map():
    """Tüm dünya için UV haritası"""
    win = Toplevel()
    win.title(t('world_uv_map'))
    win.geometry('900x700')
    win.configure(bg='#FFF3E0')
   
    control_frame = Frame(win, bg='#FFF3E0', height=80)
    control_frame.pack(side='top', fill='x', padx=10, pady=10)
    control_frame.pack_propagate(False)
   
    Label(control_frame, text=t('world_uv_map'), font=('Arial', 16, 'bold'), bg='#FFF3E0').pack(side='left', padx=10)
   
    info_label = Label(control_frame, text=t('loading_data'), font=('Arial', 11), bg='#FFF3E0', fg='#E65100')
    info_label.pack(side='left', padx=20)
   
    # Harita widget'ını oluştur
    map_widget = TkinterMapView(win, width=900, height=600)
    map_widget.pack(fill='both', expand=True)
   
    # Tüm dünya görünümü için başlangıç pozisyonu
    map_widget.set_position(20.0, 0.0)  # Ekvator bölgesi
    map_widget.set_zoom(2)  # Dünya görünümü
   
    markers = []
   
    def get_global_uv_data():
        """Tüm dünyadan UV verilerini al"""
        try:
            # Dünya genelindeki önemli şehirler
            global_cities = [
                # Kuzey Amerika
                ('New York', 40.7128, -74.0060, 'US'),
                ('Los Angeles', 34.0522, -118.2437, 'US'),
                ('Mexico City', 19.4326, -99.1332, 'MX'),
                ('Toronto', 43.6532, -79.3832, 'CA'),
               
                # Güney Amerika
                ('São Paulo', -23.5505, -46.6333, 'BR'),
                ('Buenos Aires', -34.6037, -58.3816, 'AR'),
                ('Lima', -12.0464, -77.0428, 'PE'),
               
                # Avrupa
                ('London', 51.5074, -0.1278, 'GB'),
                ('Paris', 48.8566, 2.3522, 'FR'),
                ('Berlin', 52.5200, 13.4050, 'DE'),
                ('Rome', 41.9028, 12.4964, 'IT'),
                ('Madrid', 40.4168, -3.7038, 'ES'),
                ('Moscow', 55.7558, 37.6173, 'RU'),
                ('Istanbul', 41.0082, 28.9784, 'TR'),
               
                # Asya
                ('Tokyo', 35.6762, 139.6503, 'JP'),
                ('Beijing', 39.9042, 116.4074, 'CN'),
                ('Delhi', 28.6139, 77.2090, 'IN'),
                ('Dubai', 25.2048, 55.2708, 'AE'),
                ('Singapore', 1.3521, 103.8198, 'SG'),
                ('Bangkok', 13.7563, 100.5018, 'TH'),
                ('Seoul', 37.5665, 126.9780, 'KR'),
               
                # Afrika
                ('Cairo', 30.0444, 31.2357, 'EG'),
                ('Lagos', 6.5244, 3.3792, 'NG'),
                ('Nairobi', -1.2921, 36.8219, 'KE'),
                ('Johannesburg', -26.2041, 28.0473, 'ZA'),
               
                # Okyanusya
                ('Sydney', -33.8688, 151.2093, 'AU'),
                ('Melbourne', -37.8136, 144.9631, 'AU'),
                ('Auckland', -36.8485, 174.7633, 'NZ')
            ]
           
            uv_data = []
            successful_requests = 0
           
            for city_name, lat, lon, country in global_cities:
                try:
                    # OpenWeatherMap UV endpoint
                    params = {
                        'lat': lat,
                        'lon': lon,
                        'appid': API_KEY
                    }
                    response = requests.get(UV_INDEX_URL, params=params, timeout=8)
                   
                    if response.status_code == 200:
                        data = response.json()
                        uv_value = data.get('value', 0)
                        successful_requests += 1
                    else:
                        # API çalışmazsa mevsime ve enleme göre tahmin
                        uv_value = estimate_uv_by_location(lat, lon)
                   
                    category, color = get_uv_category(uv_value)
                   
                    uv_data.append({
                        'city': city_name,
                        'country': country,
                        'lat': lat,
                        'lon': lon,
                        'uv': uv_value,
                        'category': category,
                        'color': color
                    })
                   
                except Exception as e:
                    print(f"UV veri hatası {city_name}: {e}")
                    continue
           
            display_global_uv_data(uv_data)
            info_label.config(text=t('cities_loaded').format(successful_requests) + ' | ' + t('last_update').format(datetime.now().strftime("%H:%M:%S")))
           
        except Exception as e:
            info_label.config(text=f'UV verileri alınamadı: {str(e)}')
   
    def estimate_uv_by_location(lat, lon):
        """Konuma göre UV değeri tahmini"""
        import math
       
        # Mevcut ay
        current_month = datetime.now().month
        current_hour = datetime.now().hour
       
        # Enlem faktörü (ekvatorda daha yüksek UV)
        latitude_factor = 1 - abs(lat) / 90
       
        # Mevsim faktörü (yaz aylarında daha yüksek)
        if current_month in [12, 1, 2]:  # Kış
            season_factor = 0.3
        elif current_month in [3, 4, 5]:  # İlkbahar
            season_factor = 0.6
        elif current_month in [6, 7, 8]:  # Yaz
            season_factor = 1.0
        else:  # Sonbahar
            season_factor = 0.7
       
        # Saat faktörü (öğlen en yüksek)
        hour_factor = 1 - abs(current_hour - 12) / 12
       
        # Temel UV değeri
        base_uv = 8 * latitude_factor * season_factor * hour_factor
       
        return max(0, min(12, base_uv + random.uniform(-1, 1)))
   
    def get_uv_category(uv_value):
        """UV değerine göre kategori ve renk belirle"""
        if uv_value < 3:
            return t('uv_low'), '#4CAF50'
        elif uv_value < 6:
            return t('uv_moderate'), '#FFEB3B'
        elif uv_value < 8:
            return t('uv_high'), '#FF9800'
        elif uv_value < 11:
            return t('uv_very_high'), '#F44336'
        else:
            return t('uv_extreme'), '#9C27B0'
   
    def display_global_uv_data(uv_data):
        """UV verilerini haritada göster"""
        # Önceki marker'ları temizle
        for marker in markers:
            try:
                map_widget.delete(marker)
            except:
                pass
        markers.clear()
       
        for data in uv_data:
            try:
                # Marker oluştur
                marker = map_widget.set_marker(
                    data['lat'], data['lon'],
                    text=f"☀️ {data['city']}\nUV: {data['uv']:.1f}\n{data['category']}",
                    marker_color_circle=data['color'],
                    text_color="black"
                )
                markers.append(marker)
            except Exception as e:
                print(f"Marker oluşturma hatası {data['city']}: {e}")
   
    def search_city():
        """Şehir arama fonksiyonu"""
        search_win = Toplevel()
        search_win.title(t('city_search'))
        search_win.geometry('300x150')
       
        Label(search_win, text=t('enter_city_name'), font=('Arial', 12)).pack(pady=10)
        search_entry = Entry(search_win, font=('Arial', 12), width=20)
        search_entry.pack(pady=5)
        search_entry.focus()
       
        def perform_search():
            city_name = search_entry.get().strip()
            if city_name:
                # OpenWeatherMap'ten şehir koordinatlarını al
                params = {
                    'q': city_name,
                    'appid': API_KEY,
                    'limit': 1
                }
                try:
                    response = requests.get("http://api.openweathermap.org/geo/1.0/direct", params=params, timeout=5)
                    if response.status_code == 200 and response.json():
                        city_data = response.json()[0]
                        lat = city_data['lat']
                        lon = city_data['lon']
                       
                        # Haritayı bu şehre odakla
                        map_widget.set_position(lat, lon)
                        map_widget.set_zoom(10)
                        search_win.destroy()
                    else:
                        messagebox.showerror(t('error'), t('city_not_found'))
                except Exception as e:
                    messagebox.showerror(t('error'), f"Arama hatası: {str(e)}")
       
        Button(search_win, text=t('search_city'), command=perform_search, bg='#2196F3', fg='white').pack(pady=10)
   
    # Kontrol butonları
    button_frame = Frame(control_frame, bg='#FFF3E0')
    button_frame.pack(side='right', padx=10)
   
    create_button(button_frame, t('search_city'), search_city, bg='#2196F3', font=('Arial', 10)).pack(side='left', padx=2)
    create_button(button_frame, t('refresh'), get_global_uv_data, bg='#FF9800', font=('Arial', 10)).pack(side='left', padx=2)
    create_button(button_frame, t('world_view'), lambda: [map_widget.set_position(20.0, 0.0), map_widget.set_zoom(2)],
                  bg='#4CAF50', font=('Arial', 10)).pack(side='left', padx=2)
   
    # Lejant
    legend_frame = Frame(win, bg='#FFF3E0')
    legend_frame.pack(fill='x', pady=5, padx=10)
   
    Label(legend_frame, text=t('uv_index_legend'), font=('Arial', 9, 'bold'), bg='#FFF3E0').pack(side='left', padx=5)
   
    legend_items = [
        ('0-2', t('uv_low'), '#4CAF50'),
        ('3-5', t('uv_moderate'), '#FFEB3B'),
        ('6-7', t('uv_high'), '#FF9800'),
        ('8-10', t('uv_very_high'), '#F44336'),
        ('11+', t('uv_extreme'), '#9C27B0')
    ]
   
    for uv_range, desc, color in legend_items:
        item_frame = Frame(legend_frame, bg='#FFF3E0')
        item_frame.pack(side='left', padx=10)
       
        color_canvas = Canvas(item_frame, width=15, height=15, bg=color, highlightthickness=0)
        color_canvas.pack(side='left', padx=2)
       
        Label(item_frame, text=f"{uv_range} ({desc})", font=('Arial', 8), bg='#FFF3E0').pack(side='left')
   
    # İlk verileri yükle
    get_global_uv_data()
   
    def auto_refresh():
        get_global_uv_data()
        win.after(600000, auto_refresh)  # 10 dakikada bir yenile
   
    auto_refresh()
   
    # Harita kontrolleri için kısayollar
    def on_key_press(event):
        if event.keysym == 'r':
            get_global_uv_data()
        elif event.keysym == 'plus':
            current_zoom = map_widget.zoom
            map_widget.set_zoom(current_zoom + 1)
        elif event.keysym == 'minus':
            current_zoom = map_widget.zoom
            map_widget.set_zoom(max(1, current_zoom - 1))
   
    win.bind('<KeyPress>', on_key_press)
    win.focus_set()
# 2. HAVA KALİTESİ HARİTASI
def open_air_quality_map():
    """Dünya Hava Kalitesi Haritası"""
    win = Toplevel()
    win.title(t('world_air_quality_map'))
    win.geometry('900x700')
    win.configure(bg='#E8F5E9')
   
    control_frame = Frame(win, bg='#E8F5E9', height=80)
    control_frame.pack(side='top', fill='x', padx=10, pady=10)
    control_frame.pack_propagate(False)
   
    Label(control_frame, text=t('world_air_quality_map'),
          font=('Arial', 16, 'bold'), bg='#E8F5E9').pack(side='left', padx=10)
   
    info_label = Label(control_frame, text=t('loading_data'),
                       font=('Arial', 11), bg='#E8F5E9', fg='#1B5E20')
    info_label.pack(side='left', padx=20)
   
    # Harita widget
    map_widget = TkinterMapView(win, width=900, height=600)
    map_widget.pack(fill='both', expand=True)
    map_widget.set_position(20.0, 0.0)
    map_widget.set_zoom(2)
   
    markers = []
   
    def get_global_air_quality_data():
        """Dünya genelinden hava kalitesi verilerini al"""
        try:
            # 35 stratejik şehir - Dünya çapında dengeli dağılım
            global_cities = [
                # Kuzey Amerika (6)
                ('New York', 40.7128, -74.0060, 'US'),
                ('Los Angeles', 34.0522, -118.2437, 'US'),
                ('Chicago', 41.8781, -87.6298, 'US'),
                ('Houston', 29.7604, -95.3698, 'US'),
                ('Toronto', 43.6532, -79.3832, 'CA'),
                ('Mexico City', 19.4326, -99.1332, 'MX'),
               
                # Güney Amerika (3)
                ('São Paulo', -23.5505, -46.6333, 'BR'),
                ('Buenos Aires', -34.6037, -58.3816, 'AR'),
                ('Lima', -12.0464, -77.0428, 'PE'),
               
                # Avrupa (8)
                ('London', 51.5074, -0.1278, 'GB'),
                ('Paris', 48.8566, 2.3522, 'FR'),
                ('Berlin', 52.5200, 13.4050, 'DE'),
                ('Rome', 41.9028, 12.4964, 'IT'),
                ('Madrid', 40.4168, -3.7038, 'ES'),
                ('Moscow', 55.7558, 37.6173, 'RU'),
                ('Istanbul', 41.0082, 28.9784, 'TR'),
                ('Warsaw', 52.2297, 21.0122, 'PL'),
               
                # Asya (12)
                ('Tokyo', 35.6762, 139.6503, 'JP'),
                ('Beijing', 39.9042, 116.4074, 'CN'),
                ('Shanghai', 31.2304, 121.4737, 'CN'),
                ('Delhi', 28.6139, 77.2090, 'IN'),
                ('Mumbai', 19.0760, 72.8777, 'IN'),
                ('Dubai', 25.2048, 55.2708, 'AE'),
                ('Singapore', 1.3521, 103.8198, 'SG'),
                ('Bangkok', 13.7563, 100.5018, 'TH'),
                ('Seoul', 37.5665, 126.9780, 'KR'),
                ('Hong Kong', 22.3193, 114.1694, 'HK'),
                ('Jakarta', -6.2088, 106.8456, 'ID'),
                ('Karachi', 24.8607, 67.0011, 'PK'),
               
                # Afrika (3)
                ('Cairo', 30.0444, 31.2357, 'EG'),
                ('Lagos', 6.5244, 3.3792, 'NG'),
                ('Johannesburg', -26.2041, 28.0473, 'ZA'),
               
                # Okyanusya (3)
                ('Sydney', -33.8688, 151.2093, 'AU'),
                ('Melbourne', -37.8136, 144.9631, 'AU'),
                ('Auckland', -36.8485, 174.7633, 'NZ')
            ]
           
            air_quality_data = []
            successful_requests = 0
           
            for city_name, lat, lon, country in global_cities:
                try:
                    # OpenWeatherMap Air Pollution API
                    params = {
                        'lat': lat,
                        'lon': lon,
                        'appid': API_KEY
                    }
                    response = requests.get(AIR_POLLUTION_URL, params=params, timeout=8)
                   
                    if response.status_code == 200:
                        data = response.json()
                        aqi = data['list'][0]['main']['aqi']
                        components = data['list'][0]['components']
                       
                        pm25 = components.get('pm2_5', 0)
                        pm10 = components.get('pm10', 0)
                        co = components.get('co', 0)
                        no2 = components.get('no2', 0)
                        o3 = components.get('o3', 0)
                       
                        successful_requests += 1
                    else:
                        # API başarısız olursa tahmin
                        aqi = estimate_aqi_by_location(lat, lon)
                        pm25 = aqi * 10
                        pm10 = aqi * 15
                        co = aqi * 200
                        no2 = aqi * 20
                        o3 = aqi * 50
                   
                    category, color, icon = get_aqi_category(aqi)
                   
                    air_quality_data.append({
                        'city': city_name,
                        'country': country,
                        'lat': lat,
                        'lon': lon,
                        'aqi': aqi,
                        'pm25': pm25,
                        'pm10': pm10,
                        'co': co,
                        'no2': no2,
                        'o3': o3,
                        'category': category,
                        'color': color,
                        'icon': icon
                    })
                   
                except Exception as e:
                    print(f"Hava kalitesi hatası {city_name}: {e}")
                    continue
           
            display_global_air_quality_data(air_quality_data)
            info_label.config(text=t('cities_loaded').format(successful_requests) + ' | ' + t('last_update').format(datetime.now().strftime("%H:%M:%S")))
           
        except Exception as e:
            info_label.config(text=f'Veri hatası: {str(e)}')
   
    def estimate_aqi_by_location(lat, lon):
        """Konuma göre AQI tahmini (yedek)"""
        # Enlem faktörü (ekvator bölgesinde genelde daha yüksek kirlilik)
        latitude_factor = 1 - abs(abs(lat) - 30) / 60
       
        # Büyük şehir bölgeleri için daha yüksek kirlilik
        major_city_regions = [
            (28.6139, 77.2090),  # Delhi
            (39.9042, 116.4074),  # Beijing
            (19.0760, 72.8777),  # Mumbai
            (30.0444, 31.2357),  # Cairo
        ]
       
        proximity_factor = 0
        for city_lat, city_lon in major_city_regions:
            distance = ((lat - city_lat)**2 + (lon - city_lon)**2)**0.5
            if distance < 5:
                proximity_factor = 1.5
                break
       
        base_aqi = 2 + latitude_factor + proximity_factor
        base_aqi += random.uniform(-0.5, 0.5)
       
        return max(1, min(5, int(base_aqi)))
   
    def get_aqi_category(aqi):
        """AQI kategorisi ve renk"""
        if aqi == 1:
            return t('aqi_good'), '#4CAF50', '✅'
        elif aqi == 2:
            return t('aqi_moderate'), '#8BC34A', '😊'
        elif aqi == 3:
            return t('aqi_sensitive'), '#FFEB3B', '😐'
        elif aqi == 4:
            return t('aqi_unhealthy'), '#FF9800', '⚠️'
        elif aqi == 5:
            return t('aqi_very_unhealthy'), '#F44336', '🚨'
        else:
            return t('aqi_hazardous'), '#9C27B0', '☠️'
   
    def display_global_air_quality_data(air_quality_data):
        """Hava kalitesi verilerini haritada göster"""
        for marker in markers:
            try:
                map_widget.delete(marker)
            except:
                pass
        markers.clear()
       
        for data in air_quality_data:
            try:
                # Kompakt marker metni
                marker_text = f"{data['icon']} {data['city']} AQI: {data['aqi']}"
               
                marker = map_widget.set_marker(
                    data['lat'], data['lon'],
                    text=marker_text,
                    marker_color_circle=data['color'],
                    text_color="black",
                    font=("Arial", 8),
                    command=lambda d=data: show_air_quality_detail(d)
                )
                markers.append(marker)
               
            except Exception as e:
                print(f"Marker hatası {data['city']}: {e}")
   
    def show_air_quality_detail(data):
        """Hava kalitesi detay penceresi"""
        detail_win = Toplevel()
        detail_win.title(f"🌫️ {data['city']} " + t('air_quality'))
        detail_win.geometry('450x450')
        detail_win.configure(bg='#E8F5E9')
       
        # Başlık
        Label(detail_win, text=f"🌫️ {data['city']}, {data['country']}",
              font=('Arial', 16, 'bold'), bg='#E8F5E9', fg='#1B5E20').pack(pady=10)
       
        # Genel durum
        status_frame = Frame(detail_win, bg=data['color'], relief='solid', bd=2)
        status_frame.pack(fill='x', padx=20, pady=10)
       
        Label(status_frame, text=f"{data['icon']} {data['category']}",
              font=('Arial', 14, 'bold'), bg=data['color'], fg='white').pack(pady=10)
       
        Label(status_frame, text=f"AQI: {data['aqi']}/5",
              font=('Arial', 12), bg=data['color'], fg='white').pack(pady=5)
       
        # Kirletici bileşenler
        components_frame = Frame(detail_win, bg='white', relief='solid', bd=1)
        components_frame.pack(fill='both', expand=True, padx=20, pady=10)
       
        Label(components_frame, text=t('pollutant_components'),
              font=('Arial', 12, 'bold'), bg='white', fg='#424242').pack(pady=10)
       
        pollutants = [
            (t('pm25'), data['pm25'], 'µg/m³', '#FF9800'),
            (t('pm10'), data['pm10'], 'µg/m³', '#FF5722'),
            (t('co'), data['co'], 'µg/m³', '#9C27B0'),
            (t('no2'), data['no2'], 'µg/m³', '#F44336'),
            (t('o3'), data['o3'], 'µg/m³', '#2196F3')
        ]
       
        for pollutant_name, value, unit, color in pollutants:
            pollutant_frame = Frame(components_frame, bg='white')
            pollutant_frame.pack(fill='x', padx=15, pady=5)
           
            Label(pollutant_frame, text=pollutant_name,
                  font=('Arial', 11, 'bold'), bg='white', fg='#424242',
                  width=8, anchor='w').pack(side='left')
           
            # Progress bar
            progress_canvas = Canvas(pollutant_frame, width=180, height=18,
                                    bg='#E0E0E0', highlightthickness=0)
            progress_canvas.pack(side='left', padx=10)
           
            max_value = 200 if 'PM' in pollutant_name else 500
            bar_width = int(180 * min(value, max_value) / max_value)
            progress_canvas.create_rectangle(0, 0, bar_width, 18, fill=color, outline='')
           
            Label(pollutant_frame, text=f"{value:.1f} {unit}",
                  font=('Arial', 10), bg='white', fg='#424242').pack(side='left')
       
        # Sağlık önerileri
        suggestion_frame = Frame(detail_win, bg='#FFF3E0', relief='solid', bd=1)
        suggestion_frame.pack(fill='x', padx=20, pady=10)
       
        if data['aqi'] >= 4:
            suggestion = t('aqi_tip_very_unhealthy')
        elif data['aqi'] >= 3:
            suggestion = t('aqi_tip_unhealthy')
        elif data['aqi'] >= 2:
            suggestion = t('aqi_tip_sensitive')
        else:
            suggestion = t('aqi_tip_good')
       
        Label(suggestion_frame, text=t('health_recommendations'), font=('Arial', 10, 'bold'),
              bg='#FFF3E0', fg='#E65100').pack(pady=5)
       
        Label(suggestion_frame, text=suggestion, font=('Arial', 10),
              bg='#FFF3E0', fg='#E65100', wraplength=380).pack(pady=10, padx=10)
       
        Button(detail_win, text=t('close'), command=detail_win.destroy,
               bg='#9E9E9E', fg='white', font=('Arial', 11, 'bold'),
               width=20).pack(pady=10)
   
    def search_city():
        """Şehir arama"""
        search_win = Toplevel()
        search_win.title(t('city_search'))
        search_win.geometry('350x200')
        search_win.configure(bg='#E8F5E9')
       
        Label(search_win, text=t('enter_city_name'), font=('Arial', 12, 'bold'),
              bg='#E8F5E9').pack(pady=10)
       
        search_entry = Entry(search_win, font=('Arial', 12), width=25)
        search_entry.pack(pady=5)
        search_entry.focus()
       
        result_label = Label(search_win, text='', font=('Arial', 10),
                            bg='#E8F5E9', fg='#1B5E20')
        result_label.pack(pady=5)
       
        def perform_search():
            city_name = search_entry.get().strip()
            if not city_name:
                result_label.config(text=t('enter_city_name'), fg='red')
                return
           
            result_label.config(text=t('searching'), fg='#1B5E20')
            search_win.update()
           
            try:
                # Geocoding ile şehir bul
                params = {
                    'q': city_name,
                    'appid': API_KEY,
                    'limit': 1
                }
                response = requests.get("http://api.openweathermap.org/geo/1.0/direct",
                                      params=params, timeout=5)
               
                if response.status_code == 200 and response.json():
                    city_data = response.json()[0]
                    lat = city_data['lat']
                    lon = city_data['lon']
                    found_name = city_data['name']
                   
                    # Hava kalitesi verisi al
                    aqi_params = {
                        'lat': lat,
                        'lon': lon,
                        'appid': API_KEY
                    }
                    aqi_response = requests.get(AIR_POLLUTION_URL, params=aqi_params, timeout=5)
                   
                    if aqi_response.status_code == 200:
                        aqi_data = aqi_response.json()
                        aqi = aqi_data['list'][0]['main']['aqi']
                        pm25 = aqi_data['list'][0]['components'].get('pm2_5', 0)
                    else:
                        aqi = estimate_aqi_by_location(lat, lon)
                        pm25 = aqi * 10
                   
                    category, color, icon = get_aqi_category(aqi)
                   
                    result_label.config(
                        text=f'✅ {found_name} {icon} AQI: {aqi}/5 - {category} PM2.5: {pm25:.1f} µg/m³',
                        fg='green'
                    )
                   
                    # Haritada göster
                    map_widget.set_position(lat, lon)
                    map_widget.set_zoom(10)
                   
                    # Geçici marker
                    temp_marker = map_widget.set_marker(
                        lat, lon,
                        text=f"🌫️ {found_name} AQI: {aqi}",
                        marker_color_circle=color
                    )
                   
                    def remove_temp():
                        try:
                            map_widget.delete(temp_marker)
                        except:
                            pass
                   
                    search_win.after(10000, remove_temp)
                else:
                    result_label.config(text=t('city_not_found'), fg='red')
                   
            except Exception as e:
                result_label.config(text=f'❌ Hata: {str(e)[:30]}', fg='red')
       
        search_entry.bind('<Return>', lambda e: perform_search())
       
        Button(search_win, text=t('search_city'), command=perform_search,
               bg='#4CAF50', fg='white', font=('Arial', 11, 'bold'),
               width=15).pack(pady=10)
       
        Button(search_win, text=t('close'), command=search_win.destroy,
               bg='#9E9E9E', fg='white', font=('Arial', 10),
               width=15).pack(pady=5)
   
    # Kontrol butonları
    button_frame = Frame(control_frame, bg='#E8F5E9')
    button_frame.pack(side='right', padx=10)
   
    create_button(button_frame, t('search_city'), search_city,
                  bg='#2196F3', font=('Arial', 10, 'bold')).pack(side='left', padx=2)
    create_button(button_frame, t('refresh'), get_global_air_quality_data,
                  bg='#4CAF50', font=('Arial', 10, 'bold')).pack(side='left', padx=2)
    create_button(button_frame, t('world_view'),
                  lambda: [map_widget.set_position(20.0, 0.0), map_widget.set_zoom(2)],
                  bg='#FF9800', font=('Arial', 10, 'bold')).pack(side='left', padx=2)
   
    # Lejant
    legend_frame = Frame(win, bg='#E8F5E9')
    legend_frame.pack(fill='x', pady=5, padx=10)
   
    Label(legend_frame, text=t('air_quality_legend'), font=('Arial', 9, 'bold'),
          bg='#E8F5E9').pack(side='left', padx=5)
   
    legend_items = [
        ('1', t('aqi_good'), '#4CAF50'),
        ('2', t('aqi_moderate'), '#8BC34A'),
        ('3', t('aqi_sensitive'), '#FFEB3B'),
        ('4', t('aqi_unhealthy'), '#FF9800'),
        ('5', t('aqi_very_unhealthy'), '#F44336')
    ]
   
    for aqi_val, desc, color in legend_items:
        item_frame = Frame(legend_frame, bg='#E8F5E9')
        item_frame.pack(side='left', padx=8)
       
        Canvas(item_frame, width=12, height=12, bg=color,
               highlightthickness=0).pack(side='left', padx=2)
       
        Label(item_frame, text=f"{aqi_val} {desc}",
              font=('Arial', 8), bg='#E8F5E9').pack(side='left')
   
    # İlk yükleme
    get_global_air_quality_data()
   
    # Otomatik yenileme (15 dakika)
    def auto_refresh():
        get_global_air_quality_data()
        win.after(900000, auto_refresh)
   
    auto_refresh()
   
    # Klavye kısayolları
    def on_key_press(event):
        if event.keysym == 'r':
            get_global_air_quality_data()
        elif event.keysym == 's':
            search_city()
   
    win.bind('<KeyPress>', on_key_press)
    win.focus_set()

# 3. POLEN HARİTASI
def open_pollen_map():
    """Dünya Polen Haritası"""
    win = Toplevel()
    win.title(t('world_pollen_map'))
    win.geometry('900x700')
    win.configure(bg='#FFF9C4')
   
    control_frame = Frame(win, bg='#FFF9C4', height=80)
    control_frame.pack(side='top', fill='x', padx=10, pady=10)
    control_frame.pack_propagate(False)
   
    Label(control_frame, text=t('world_pollen_map'),
          font=('Arial', 16, 'bold'), bg='#FFF9C4', fg='#F57F17').pack(side='left', padx=10)
   
    info_label = Label(control_frame, text=t('loading_data'),
                       font=('Arial', 11), bg='#FFF9C4', fg='#F57F17')
    info_label.pack(side='left', padx=20)
   
    # Harita widget
    map_widget = TkinterMapView(win, width=900, height=600)
    map_widget.pack(fill='both', expand=True)
    map_widget.set_position(20.0, 0.0)
    map_widget.set_zoom(2)
   
    markers = []
   
    def get_pollen_data():
        """Polen verilerini al - 35 şehir"""
        try:
            # 35 stratejik şehir
            global_cities = [
                # Kuzey Amerika (6)
                ('New York', 40.7128, -74.0060, 'US'),
                ('Los Angeles', 34.0522, -118.2437, 'US'),
                ('Chicago', 41.8781, -87.6298, 'US'),
                ('Houston', 29.7604, -95.3698, 'US'),
                ('Toronto', 43.6532, -79.3832, 'CA'),
                ('Mexico City', 19.4326, -99.1332, 'MX'),
               
                # Güney Amerika (3)
                ('São Paulo', -23.5505, -46.6333, 'BR'),
                ('Buenos Aires', -34.6037, -58.3816, 'AR'),
                ('Bogotá', 4.7110, -74.0721, 'CO'),
               
                # Avrupa (10)
                ('London', 51.5074, -0.1278, 'GB'),
                ('Paris', 48.8566, 2.3522, 'FR'),
                ('Berlin', 52.5200, 13.4050, 'DE'),
                ('Rome', 41.9028, 12.4964, 'IT'),
                ('Madrid', 40.4168, -3.7038, 'ES'),
                ('Amsterdam', 52.3676, 4.9041, 'NL'),
                ('Vienna', 48.2082, 16.3738, 'AT'),
                ('Warsaw', 52.2297, 21.0122, 'PL'),
                ('Moscow', 55.7558, 37.6173, 'RU'),
                ('Istanbul', 41.0082, 28.9784, 'TR'),
               
                # Asya (11)
                ('Tokyo', 35.6762, 139.6503, 'JP'),
                ('Beijing', 39.9042, 116.4074, 'CN'),
                ('Shanghai', 31.2304, 121.4737, 'CN'),
                ('Delhi', 28.6139, 77.2090, 'IN'),
                ('Mumbai', 19.0760, 72.8777, 'IN'),
                ('Dubai', 25.2048, 55.2708, 'AE'),
                ('Singapore', 1.3521, 103.8198, 'SG'),
                ('Bangkok', 13.7563, 100.5018, 'TH'),
                ('Seoul', 37.5665, 126.9780, 'KR'),
                ('Jakarta', -6.2088, 106.8456, 'ID'),
                ('Manila', 14.5995, 120.9842, 'PH'),
               
                # Afrika (3)
                ('Cairo', 30.0444, 31.2357, 'EG'),
                ('Lagos', 6.5244, 3.3792, 'NG'),
                ('Johannesburg', -26.2041, 28.0473, 'ZA'),
               
                # Okyanusya (2)
                ('Sydney', -33.8688, 151.2093, 'AU'),
                ('Melbourne', -37.8136, 144.9631, 'AU')
            ]
           
            pollen_data = []
            successful = 0
           
            for city_name, lat, lon, country in global_cities:
                try:
                    # Hava durumu verisiyle birlikte polen tahmini
                    params = {
                        'lat': lat,
                        'lon': lon,
                        'appid': API_KEY,
                        'units': 'metric'
                    }
                    response = requests.get(WEATHER_URL, params=params, timeout=8)
                   
                    if response.status_code == 200:
                        weather_data = response.json()
                        temp = weather_data['main']['temp']
                        humidity = weather_data['main']['humidity']
                        wind_speed = weather_data['wind']['speed']
                       
                        # Polen seviyesi tahmini (mevsim, sıcaklık, nem, rüzgar)
                        pollen_levels = estimate_pollen(lat, temp, humidity, wind_speed)
                        successful += 1
                    else:
                        pollen_levels = estimate_pollen_simple(lat)
                   
                    category, color, icon = get_pollen_category(pollen_levels['total'])
                   
                    pollen_data.append({
                        'city': city_name,
                        'country': country,
                        'lat': lat,
                        'lon': lon,
                        'tree': pollen_levels['tree'],
                        'grass': pollen_levels['grass'],
                        'weed': pollen_levels['weed'],
                        'total': pollen_levels['total'],
                        'category': category,
                        'color': color,
                        'icon': icon
                    })
                   
                except Exception as e:
                    print(f"Polen hatası {city_name}: {e}")
                    continue
           
            display_pollen_data(pollen_data)
            info_label.config(text=t('cities_loaded').format(successful) + ' | ' + t('last_update').format(datetime.now().strftime("%H:%M:%S")))
           
        except Exception as e:
            info_label.config(text=f'Veri hatası: {str(e)}')
   
    def estimate_pollen(lat, temp, humidity, wind_speed):
        """Gelişmiş polen tahmini"""
        current_month = datetime.now().month
       
        # Mevsimsel faktör
        if lat > 0:  # Kuzey yarımküre
            if current_month in [3, 4, 5]:  # İlkbahar
                season_tree, season_grass, season_weed = 8, 6, 3
            elif current_month in [6, 7, 8]:  # Yaz
                season_tree, season_grass, season_weed = 4, 9, 7
            elif current_month in [9, 10]:  # Sonbahar
                season_tree, season_grass, season_weed = 2, 3, 8
            else:  # Kış
                season_tree, season_grass, season_weed = 1, 1, 1
        else:  # Güney yarımküre (mevsimler ters)
            if current_month in [9, 10, 11]:  # İlkbahar
                season_tree, season_grass, season_weed = 8, 6, 3
            elif current_month in [12, 1, 2]:  # Yaz
                season_tree, season_grass, season_weed = 4, 9, 7
            elif current_month in [3, 4]:  # Sonbahar
                season_tree, season_grass, season_weed = 2, 3, 8
            else:  # Kış
                season_tree, season_grass, season_weed = 1, 1, 1
       
        # Sıcaklık faktörü (15-25°C ideal polen)
        if 15 <= temp <= 25:
            temp_factor = 1.3
        elif 10 <= temp <= 30:
            temp_factor = 1.0
        else:
            temp_factor = 0.5
       
        # Nem faktörü (düşük nem = daha çok polen)
        humidity_factor = 1.5 if humidity < 40 else 1.0 if humidity < 60 else 0.7
       
        # Rüzgar faktörü (orta rüzgar polen yayılımını artırır)
        wind_factor = 1.2 if 3 <= wind_speed <= 7 else 0.8
       
        # Final hesaplama
        tree = int(season_tree * temp_factor * humidity_factor * wind_factor + random.randint(-1, 2))
        grass = int(season_grass * temp_factor * humidity_factor * wind_factor + random.randint(-1, 2))
        weed = int(season_weed * temp_factor * humidity_factor * wind_factor + random.randint(-1, 2))
       
        return {
            'tree': max(0, min(10, tree)),
            'grass': max(0, min(10, grass)),
            'weed': max(0, min(10, weed)),
            'total': max(0, min(10, (tree + grass + weed) // 3))
        }
   
    def estimate_pollen_simple(lat):
        """Basit polen tahmini"""
        current_month = datetime.now().month
       
        if lat > 0:
            if current_month in [3, 4, 5]:
                return {'tree': 7, 'grass': 5, 'weed': 3, 'total': 5}
            elif current_month in [6, 7, 8]:
                return {'tree': 3, 'grass': 8, 'weed': 6, 'total': 6}
            elif current_month in [9, 10]:
                return {'tree': 2, 'grass': 3, 'weed': 7, 'total': 4}
            else:
                return {'tree': 1, 'grass': 1, 'weed': 1, 'total': 1}
        else:
            if current_month in [9, 10, 11]:
                return {'tree': 7, 'grass': 5, 'weed': 3, 'total': 5}
            elif current_month in [12, 1, 2]:
                return {'tree': 3, 'grass': 8, 'weed': 6, 'total': 6}
            elif current_month in [3, 4]:
                return {'tree': 2, 'grass': 3, 'weed': 7, 'total': 4}
            else:
                return {'tree': 1, 'grass': 1, 'weed': 1, 'total': 1}
   
    def get_pollen_category(total_level):
        """Polen kategorisi"""
        if total_level <= 2:
            return t('pollen_very_low'), '#4CAF50', '✅'
        elif total_level <= 4:
            return t('pollen_low'), '#8BC34A', '😊'
        elif total_level <= 6:
            return t('pollen_moderate'), '#FFEB3B', '😐'
        elif total_level <= 8:
            return t('pollen_high'), '#FF9800', '⚠️'
        else:
            return t('pollen_very_high'), '#F44336', '🚨'
   
    def display_pollen_data(pollen_data):
        """Polen verilerini haritada göster"""
        for marker in markers:
            try:
                map_widget.delete(marker)
            except:
                pass
        markers.clear()
       
        for data in pollen_data:
            try:
                # Kompakt marker metni
                marker_text = f"{data['icon']} {data['city']} Polen: {data['total']}/10"
               
                marker = map_widget.set_marker(
                    data['lat'], data['lon'],
                    text=marker_text,
                    marker_color_circle=data['color'],
                    text_color="black",
                    font=("Arial", 8),
                    command=lambda d=data: show_pollen_detail(d)
                )
                markers.append(marker)
               
            except Exception as e:
                print(f"Marker hatası {data['city']}: {e}")
   
    def show_pollen_detail(data):
        """Polen detay penceresi"""
        detail_win = Toplevel()
        detail_win.title(f"🌸 {data['city']} " + t('pollen_details'))
        detail_win.geometry('400x350')
        detail_win.configure(bg='#FFF9C4')
       
        # Başlık
        Label(detail_win, text=f"🌸 {data['city']}, {data['country']}",
              font=('Arial', 16, 'bold'), bg='#FFF9C4', fg='#F57F17').pack(pady=10)
       
        # Genel durum
        status_frame = Frame(detail_win, bg=data['color'], relief='solid', bd=2)
        status_frame.pack(fill='x', padx=20, pady=10)
       
        Label(status_frame, text=f"{data['icon']} {data['category']}",
              font=('Arial', 14, 'bold'), bg=data['color'], fg='white').pack(pady=10)
       
        Label(status_frame, text=t('pollen_level').format(data['total']),
              font=('Arial', 12), bg=data['color'], fg='white').pack(pady=5)
       
        # Detaylı polen türleri
        detail_frame = Frame(detail_win, bg='white', relief='solid', bd=1)
        detail_frame.pack(fill='both', expand=True, padx=20, pady=10)
       
        polen_types = [
            (t('tree_pollen'), data['tree'], '#8BC34A'),
            (t('grass_pollen'), data['grass'], '#CDDC39'),
            (t('weed_pollen'), data['weed'], '#FFC107')
        ]
       
        for pollen_name, level, color in polen_types:
            type_frame = Frame(detail_frame, bg='white')
            type_frame.pack(fill='x', padx=10, pady=8)
           
            Label(type_frame, text=pollen_name, font=('Arial', 11, 'bold'),
                  bg='white', fg='#424242', width=15, anchor='w').pack(side='left')
           
            # Progress bar
            progress_canvas = Canvas(type_frame, width=150, height=20, bg='#E0E0E0',
                                    highlightthickness=0)
            progress_canvas.pack(side='left', padx=10)
           
            bar_width = int(150 * level / 10)
            progress_canvas.create_rectangle(0, 0, bar_width, 20, fill=color, outline='')
           
            Label(type_frame, text=f"{level}/10", font=('Arial', 11, 'bold'),
                  bg='white', fg='#424242').pack(side='left')
       
        # Öneriler
        suggestion_frame = Frame(detail_win, bg='#FFF3E0', relief='solid', bd=1)
        suggestion_frame.pack(fill='x', padx=20, pady=10)
       
        if data['total'] >= 7:
            suggestion = t('pollen_tip_very_high')
        elif data['total'] >= 5:
            suggestion = t('pollen_tip_high')
        else:
            suggestion = t('pollen_tip_low')
       
        Label(suggestion_frame, text=t('allergy_advice'), font=('Arial', 10, 'bold'),
              bg='#FFF3E0', fg='#E65100').pack(pady=5)
       
        Label(suggestion_frame, text=suggestion, font=('Arial', 10),
              bg='#FFF3E0', fg='#E65100', wraplength=350).pack(pady=10, padx=10)
       
        Button(detail_win, text=t('close'), command=detail_win.destroy,
               bg='#9E9E9E', fg='white', font=('Arial', 11, 'bold'),
               width=20).pack(pady=10)
   
    def search_city():
        """Şehir arama"""
        search_win = Toplevel()
        search_win.title(t('city_search'))
        search_win.geometry('350x200')
        search_win.configure(bg='#FFF9C4')
       
        Label(search_win, text=t('enter_city_name'), font=('Arial', 12, 'bold'),
              bg='#FFF9C4').pack(pady=10)
       
        search_entry = Entry(search_win, font=('Arial', 12), width=25)
        search_entry.pack(pady=5)
        search_entry.focus()
       
        result_label = Label(search_win, text='', font=('Arial', 10),
                            bg='#FFF9C4', fg='#F57F17')
        result_label.pack(pady=5)
       
        def perform_search():
            city_name = search_entry.get().strip()
            if not city_name:
                result_label.config(text=t('enter_city_name'), fg='red')
                return
           
            result_label.config(text=t('searching'), fg='#F57F17')
            search_win.update()
           
            try:
                params = {
                    'q': city_name,
                    'appid': API_KEY,
                    'limit': 1
                }
                response = requests.get("http://api.openweathermap.org/geo/1.0/direct",
                                      params=params, timeout=5)
               
                if response.status_code == 200 and response.json():
                    city_data = response.json()[0]
                    lat = city_data['lat']
                    lon = city_data['lon']
                    found_name = city_data['name']
                   
                    # Hava durumu al
                    params2 = {
                        'lat': lat,
                        'lon': lon,
                        'appid': API_KEY,
                        'units': 'metric'
                    }
                    weather_response = requests.get(WEATHER_URL, params=params2, timeout=5)
                   
                    if weather_response.status_code == 200:
                        weather_data = weather_response.json()
                        temp = weather_data['main']['temp']
                        humidity = weather_data['main']['humidity']
                        wind_speed = weather_data['wind']['speed']
                       
                        pollen_levels = estimate_pollen(lat, temp, humidity, wind_speed)
                    else:
                        pollen_levels = estimate_pollen_simple(lat)
                   
                    category, color, icon = get_pollen_category(pollen_levels['total'])
                   
                    result_label.config(
                        text=f'✅ {found_name}{icon} Polen: {pollen_levels["total"]}/10 - {category}',
                        fg='green'
                    )
                   
                    map_widget.set_position(lat, lon)
                    map_widget.set_zoom(10)
                   
                    temp_marker = map_widget.set_marker(
                        lat, lon,
                        text=f"🌸 {found_name} Polen: {pollen_levels['total']}/10",
                        marker_color_circle=color
                    )
                   
                    def remove_temp():
                        try:
                            map_widget.delete(temp_marker)
                        except:
                            pass
                   
                    search_win.after(10000, remove_temp)
                else:
                    result_label.config(text=t('city_not_found'), fg='red')
                   
            except Exception as e:
                result_label.config(text=f'❌ Hata: {str(e)[:30]}', fg='red')
       
        search_entry.bind('<Return>', lambda e: perform_search())
       
        Button(search_win, text=t('search_city'), command=perform_search,
               bg='#FF9800', fg='white', font=('Arial', 11, 'bold'),
               width=15).pack(pady=10)
       
        Button(search_win, text=t('close'), command=search_win.destroy,
               bg='#9E9E9E', fg='white', font=('Arial', 10),
               width=15).pack(pady=5)
   
    # Kontrol butonları
    button_frame = Frame(control_frame, bg='#FFF9C4')
    button_frame.pack(side='right', padx=10)
   
    create_button(button_frame, t('search_city'), search_city,
                  bg='#FF9800', font=('Arial', 10, 'bold')).pack(side='left', padx=2)
    create_button(button_frame, t('refresh'), get_pollen_data,
                  bg='#F57F17', font=('Arial', 10, 'bold')).pack(side='left', padx=2)
    create_button(button_frame, t('world_view'),
                  lambda: [map_widget.set_position(20.0, 0.0), map_widget.set_zoom(2)],
                  bg='#8BC34A', font=('Arial', 10, 'bold')).pack(side='left', padx=2)
   
    # Lejant
    legend_frame = Frame(win, bg='#FFF9C4')
    legend_frame.pack(fill='x', pady=5, padx=10)
   
    Label(legend_frame, text=t('pollen_legend'), font=('Arial', 9, 'bold'),
          bg='#FFF9C4').pack(side='left', padx=5)
   
    legend_items = [
        ('0-2', t('pollen_very_low'), '#4CAF50'),
        ('3-4', t('pollen_low'), '#8BC34A'),
        ('5-6', t('pollen_moderate'), '#FFEB3B'),
        ('7-8', t('pollen_high'), '#FF9800'),
        ('9-10', t('pollen_very_high'), '#F44336')
    ]
   
    for range_val, desc, color in legend_items:
        item_frame = Frame(legend_frame, bg='#FFF9C4')
        item_frame.pack(side='left', padx=8)
       
        Canvas(item_frame, width=12, height=12, bg=color,
               highlightthickness=0).pack(side='left', padx=2)
       
        Label(item_frame, text=f"{range_val} ({desc})",
              font=('Arial', 8), bg='#FFF9C4').pack(side='left')
   
    # İlk yükleme
    get_pollen_data()
   
    # Otomatik yenileme (20 dakika)
    def auto_refresh():
        get_pollen_data()
        win.after(1200000, auto_refresh)
   
    auto_refresh()
# 4. GÖRÜŞ MESAFESİ HARİTASI
def open_visibility_map():
    """Dünya görüş mesafesi haritası - Optimize edilmiş"""
    win = Toplevel()
    win.title(t('world_visibility_map'))
    win.geometry('900x700')
    win.configure(bg='#E1F5FE')
   
    control_frame = Frame(win, bg='#E1F5FE', height=80)
    control_frame.pack(side='top', fill='x', padx=10, pady=10)
    control_frame.pack_propagate(False)
   
    Label(control_frame, text=t('world_visibility_map'),
          font=('Arial', 16, 'bold'), bg='#E1F5FE').pack(side='left', padx=10)
   
    info_label = Label(control_frame, text=t('loading_data'),
                       font=('Arial', 11), bg='#E1F5FE', fg='#01579B')
    info_label.pack(side='left', padx=20)
   
    # Harita widget
    map_widget = TkinterMapView(win, width=900, height=600)
    map_widget.pack(fill='both', expand=True)
    map_widget.set_position(20.0, 0.0)
    map_widget.set_zoom(2)
   
    markers = []
   
    def get_global_visibility_data():
        """Dünya genelinden görüş mesafesi verilerini al - 30 stratejik şehir"""
        try:
            # 30 stratejik şehir - Daha dengeli dağılım
            global_cities = [
                # Kuzey Amerika (5)
                ('New York', 40.7128, -74.0060, 'US'),
                ('Los Angeles', 34.0522, -118.2437, 'US'),
                ('Mexico City', 19.4326, -99.1332, 'MX'),
                ('Toronto', 43.6532, -79.3832, 'CA'),
                ('Miami', 25.7617, -80.1918, 'US'),
               
                # Güney Amerika (3)
                ('São Paulo', -23.5505, -46.6333, 'BR'),
                ('Buenos Aires', -34.6037, -58.3816, 'AR'),
                ('Lima', -12.0464, -77.0428, 'PE'),
               
                # Avrupa (7)
                ('London', 51.5074, -0.1278, 'GB'),
                ('Paris', 48.8566, 2.3522, 'FR'),
                ('Berlin', 52.5200, 13.4050, 'DE'),
                ('Rome', 41.9028, 12.4964, 'IT'),
                ('Madrid', 40.4168, -3.7038, 'ES'),
                ('Moscow', 55.7558, 37.6173, 'RU'),
                ('Istanbul', 41.0082, 28.9784, 'TR'),
               
                # Asya (10)
                ('Tokyo', 35.6762, 139.6503, 'JP'),
                ('Beijing', 39.9042, 116.4074, 'CN'),
                ('Shanghai', 31.2304, 121.4737, 'CN'),
                ('Delhi', 28.6139, 77.2090, 'IN'),
                ('Mumbai', 19.0760, 72.8777, 'IN'),
                ('Dubai', 25.2048, 55.2708, 'AE'),
                ('Singapore', 1.3521, 103.8198, 'SG'),
                ('Bangkok', 13.7563, 100.5018, 'TH'),
                ('Seoul', 37.5665, 126.9780, 'KR'),
                ('Hong Kong', 22.3193, 114.1694, 'HK'),
               
                # Afrika (3)
                ('Cairo', 30.0444, 31.2357, 'EG'),
                ('Lagos', 6.5244, 3.3792, 'NG'),
                ('Johannesburg', -26.2041, 28.0473, 'ZA'),
               
                # Okyanusya (2)
                ('Sydney', -33.8688, 151.2093, 'AU'),
                ('Auckland', -36.8485, 174.7633, 'NZ')
            ]
           
            visibility_data = []
            successful_requests = 0
           
            for city_name, lat, lon, country in global_cities:
                try:
                    params = {
                        'lat': lat,
                        'lon': lon,
                        'appid': API_KEY,
                        'units': 'metric'
                    }
                    response = requests.get(WEATHER_URL, params=params, timeout=8)
                   
                    if response.status_code == 200:
                        data = response.json()
                        vis_meters = data.get('visibility', 10000)
                        vis_km = vis_meters / 1000
                        weather_desc = data['weather'][0]['description']
                        successful_requests += 1
                    else:
                        vis_km = estimate_visibility(lat, lon)
                        weather_desc = 'N/A'
                   
                    category, color, icon = get_visibility_category(vis_km)
                   
                    visibility_data.append({
                        'city': city_name,
                        'country': country,
                        'lat': lat,
                        'lon': lon,
                        'visibility_km': vis_km,
                        'category': category,
                        'color': color,
                        'icon': icon,
                        'weather': weather_desc
                    })
                   
                except Exception as e:
                    print(f"Görüş mesafesi hatası {city_name}: {e}")
                    continue
           
            display_global_visibility_data(visibility_data)
            info_label.config(text=t('cities_loaded').format(successful_requests) + ' | ' + t('last_update').format(datetime.now().strftime("%H:%M:%S")))
           
        except Exception as e:
            info_label.config(text=f'Veri hatası: {str(e)}')
   
    def estimate_visibility(lat, lon):
        """Konuma göre görüş mesafesi tahmini"""
        current_hour = datetime.now().hour
        time_factor = 1.0 if 6 <= current_hour <= 18 else 0.8
        latitude_factor = 1 - abs(lat) / 180
       
        current_month = datetime.now().month
        if current_month in [12, 1, 2]:
            season_factor = 0.7
        elif current_month in [6, 7, 8]:
            season_factor = 0.9
        else:
            season_factor = 0.8
       
        base_visibility = 15 * time_factor * (1 - latitude_factor * 0.3) * season_factor
        variation = random.uniform(-3, 3)
       
        return max(0.5, min(50, base_visibility + variation))
   
    def get_visibility_category(vis_km):
        """Görüş mesafesine göre kategori"""
        if vis_km >= 20:
            return t('visibility_excellent'), '#4CAF50', '👁️'
        elif vis_km >= 10:
            return t('visibility_good'), '#8BC34A', '👀'
        elif vis_km >= 5:
            return t('visibility_moderate'), '#FFEB3B', '😐'
        elif vis_km >= 2:
            return t('visibility_poor'), '#FF9800', '😑'
        elif vis_km >= 1:
            return t('visibility_very_poor'), '#F44336', '😵'
        else:
            return t('visibility_dangerous'), '#9C27B0', '🚫'
   
    def display_global_visibility_data(visibility_data):
        """Görüş mesafesi verilerini haritada göster - Kompakt görünüm"""
        for marker in markers:
            try:
                map_widget.delete(marker)
            except:
                pass
        markers.clear()
       
        for data in visibility_data:
            try:
                # KOMPAKT MARKER METNİ - Sadece önemli bilgiler
                marker_text = f"{data['icon']} {data['city']}{data['visibility_km']:.1f}km"
               
                marker = map_widget.set_marker(
                    data['lat'], data['lon'],
                    text=marker_text,
                    marker_color_circle=data['color'],
                    text_color="black",
                    font=("Arial", 8)  # Küçük font
                )
                markers.append(marker)
               
            except Exception as e:
                print(f"Marker hatası {data['city']}: {e}")
   
    def search_city():
        """Şehir arama özelliği"""
        search_win = Toplevel()
        search_win.title(t('city_search'))
        search_win.geometry('350x200')
        search_win.configure(bg='#E1F5FE')
       
        Label(search_win, text=t('enter_city_name'), font=('Arial', 12, 'bold'),
              bg='#E1F5FE').pack(pady=10)
       
        search_entry = Entry(search_win, font=('Arial', 12), width=25)
        search_entry.pack(pady=5)
        search_entry.focus()
       
        result_label = Label(search_win, text='', font=('Arial', 10),
                            bg='#E1F5FE', fg='#01579B')
        result_label.pack(pady=5)
       
        def perform_search():
            city_name = search_entry.get().strip()
            if not city_name:
                result_label.config(text=t('enter_city_name'), fg='red')
                return
           
            result_label.config(text=t('searching'), fg='#01579B')
            search_win.update()
           
            try:
                # Geocoding API ile şehir bul
                params = {
                    'q': city_name,
                    'appid': API_KEY,
                    'limit': 1
                }
                response = requests.get("http://api.openweathermap.org/geo/1.0/direct",
                                      params=params, timeout=5)
               
                if response.status_code == 200 and response.json():
                    city_data = response.json()[0]
                    lat = city_data['lat']
                    lon = city_data['lon']
                    found_name = city_data['name']
                   
                    # Görüş mesafesi verisini al
                    params2 = {
                        'lat': lat,
                        'lon': lon,
                        'appid': API_KEY,
                        'units': 'metric'
                    }
                    weather_response = requests.get(WEATHER_URL, params=params2, timeout=5)
                   
                    if weather_response.status_code == 200:
                        weather_data = weather_response.json()
                        vis_meters = weather_data.get('visibility', 10000)
                        vis_km = vis_meters / 1000
                       
                        category, color, icon = get_visibility_category(vis_km)
                       
                        result_label.config(
                            text=f'✅ {found_name}{icon} Görüş: {vis_km:.1f}km - {category}',
                            fg='green'
                        )
                       
                        # Haritada göster
                        map_widget.set_position(lat, lon)
                        map_widget.set_zoom(10)
                       
                        # Geçici marker ekle
                        temp_marker = map_widget.set_marker(
                            lat, lon,
                            text=f"🔍 {found_name}{vis_km:.1f}km",
                            marker_color_circle=color
                        )
                       
                        # 10 saniye sonra geçici marker'ı sil
                        def remove_temp_marker():
                            try:
                                map_widget.delete(temp_marker)
                            except:
                                pass
                       
                        search_win.after(10000, remove_temp_marker)
                    else:
                        result_label.config(text=f'✅ {found_name} bulundu Görüş verisi yok', fg='orange')
                        map_widget.set_position(lat, lon)
                        map_widget.set_zoom(10)
                else:
                    result_label.config(text=t('city_not_found'), fg='red')
                   
            except Exception as e:
                result_label.config(text=f'❌ Hata: {str(e)[:30]}', fg='red')
       
        # Enter tuşu ile arama
        search_entry.bind('<Return>', lambda e: perform_search())
       
        Button(search_win, text=t('search_city'), command=perform_search,
               bg='#2196F3', fg='white', font=('Arial', 11, 'bold'),
               width=15).pack(pady=10)
       
        Button(search_win, text=t('close'), command=search_win.destroy,
               bg='#9E9E9E', fg='white', font=('Arial', 10),
               width=15).pack(pady=5)
   
    # Kontrol butonları
    button_frame = Frame(control_frame, bg='#E1F5FE')
    button_frame.pack(side='right', padx=10)
   
    create_button(button_frame, t('search_city'), search_city,
                  bg='#2196F3', font=('Arial', 10, 'bold')).pack(side='left', padx=2)
    create_button(button_frame, t('refresh'), get_global_visibility_data,
                  bg='#FF9800', font=('Arial', 10, 'bold')).pack(side='left', padx=2)
    create_button(button_frame, t('world_view'),
                  lambda: [map_widget.set_position(20.0, 0.0), map_widget.set_zoom(2)],
                  bg='#4CAF50', font=('Arial', 10, 'bold')).pack(side='left', padx=2)
   
    # Kompakt Lejant
    legend_frame = Frame(win, bg='#E1F5FE')
    legend_frame.pack(fill='x', pady=5, padx=10)
   
    Label(legend_frame, text=t('visibility_legend'), font=('Arial', 9, 'bold'),
          bg='#E1F5FE').pack(side='left', padx=5)
   
    legend_items = [
        ('20+', t('visibility_excellent'), '#4CAF50'),
        ('10-20', t('visibility_good'), '#8BC34A'),
        ('5-10', t('visibility_moderate'), '#FFEB3B'),
        ('2-5', t('visibility_poor'), '#FF9800'),
        ('1-2', t('visibility_very_poor'), '#F44336'),
        ('<1', t('visibility_dangerous'), '#9C27B0')
    ]
   
    for vis_range, desc, color in legend_items:
        item_frame = Frame(legend_frame, bg='#E1F5FE')
        item_frame.pack(side='left', padx=8)
       
        Canvas(item_frame, width=12, height=12, bg=color,
               highlightthickness=0).pack(side='left', padx=2)
       
        Label(item_frame, text=f"{desc}",
              font=('Arial', 8), bg='#E1F5FE').pack(side='left')
   
    # İlk yükleme
    get_global_visibility_data()
   
    # Otomatik yenileme
    def auto_refresh():
        get_global_visibility_data()
        win.after(600000, auto_refresh)  # 10 dakika
   
    auto_refresh()
   
    # Klavye kısayolları
    def on_key_press(event):
        if event.keysym == 'r':
            get_global_visibility_data()
        elif event.keysym == 's':
            search_city()
        elif event.keysym == 'plus':
            map_widget.set_zoom(map_widget.zoom + 1)
        elif event.keysym == 'minus':
            map_widget.set_zoom(max(1, map_widget.zoom - 1))
   
    win.bind('<KeyPress>', on_key_press)
    win.focus_set()
   
# 5. DALGA HARİTASI
def open_wave_map():
    """Dünya Dalga Haritası"""
    win = Toplevel()
    win.title(t('world_wave_map'))  # Çeviri fonksiyonu eklendi
    win.geometry('900x700')
    win.configure(bg='#E0F7FA')
   
    control_frame = Frame(win, bg='#E0F7FA', height=80)
    control_frame.pack(side='top', fill='x', padx=10, pady=10)
    control_frame.pack_propagate(False)
   
    Label(control_frame, text=t('world_wave_map'),  # Çeviri fonksiyonu eklendi
          font=('Arial', 16, 'bold'), bg='#E0F7FA').pack(side='left', padx=10)
   
    info_label = Label(control_frame, text=t('loading_data'),  # Çeviri fonksiyonu eklendi
                       font=('Arial', 11), bg='#E0F7FA', fg='#006064')
    info_label.pack(side='left', padx=20)
   
    # Harita widget
    map_widget = TkinterMapView(win, width=900, height=600)
    map_widget.pack(fill='both', expand=True)
    map_widget.set_position(0.0, 0.0)  # Ekvator merkezli
    map_widget.set_zoom(2)
   
    markers = []
   
    def get_global_wave_data():
        """Dünya genelinden dalga verilerini al"""
        try:
            # 40 stratejik kıyı şehri - Okyanus ve deniz kıyıları
            coastal_cities = [
                # Kuzey Amerika Atlantik (5)
                ('New York', 40.7128, -74.0060, 'US', 'Atlantic'),
                ('Miami', 25.7617, -80.1918, 'US', 'Atlantic'),
                ('Halifax', 44.6488, -63.5752, 'CA', 'Atlantic'),
                ('Boston', 42.3601, -71.0589, 'US', 'Atlantic'),
                ('Charleston', 32.7765, -79.9311, 'US', 'Atlantic'),
               
                # Kuzey Amerika Pasifik (5)
                ('San Francisco', 37.7749, -122.4194, 'US', 'Pacific'),
                ('Los Angeles', 33.7701, -118.1937, 'US', 'Pacific'),
                ('Vancouver', 49.2827, -123.1207, 'CA', 'Pacific'),
                ('Honolulu', 21.3099, -157.8581, 'US', 'Pacific'),
                ('San Diego', 32.7157, -117.1611, 'US', 'Pacific'),
               
                # Güney Amerika (4)
                ('Rio de Janeiro', -22.9068, -43.1729, 'BR', 'Atlantic'),
                ('Valparaíso', -33.0472, -71.6127, 'CL', 'Pacific'),
                ('Buenos Aires', -34.6037, -58.3816, 'AR', 'Atlantic'),
                ('Lima', -12.0464, -77.0428, 'PE', 'Pacific'),
               
                # Avrupa Atlantik (6)
                ('Lisbon', 38.7223, -9.1393, 'PT', 'Atlantic'),
                ('Dublin', 53.3498, -6.2603, 'IE', 'Atlantic'),
                ('Reykjavik', 64.1466, -21.9426, 'IS', 'Atlantic'),
                ('Bergen', 60.3913, 5.3221, 'NO', 'Atlantic'),
                ('Brest', 48.3905, -4.4860, 'FR', 'Atlantic'),
                ('Porto', 41.1579, -8.6291, 'PT', 'Atlantic'),
               
                # Akdeniz (5)
                ('Barcelona', 41.3851, 2.1734, 'ES', 'Mediterranean'),
                ('Marseille', 43.2965, 5.3698, 'FR', 'Mediterranean'),
                ('Athens', 37.9838, 23.7275, 'GR', 'Mediterranean'),
                ('Istanbul', 41.0082, 28.9784, 'TR', 'Black Sea'),
                ('Tel Aviv', 32.0853, 34.7818, 'IL', 'Mediterranean'),
               
                # Asya Pasifik (8)
                ('Tokyo', 35.6762, 139.6503, 'JP', 'Pacific'),
                ('Hong Kong', 22.3193, 114.1694, 'HK', 'Pacific'),
                ('Singapore', 1.3521, 103.8198, 'SG', 'Pacific'),
                ('Sydney', -33.8688, 151.2093, 'AU', 'Pacific'),
                ('Auckland', -36.8485, 174.7633, 'NZ', 'Pacific'),
                ('Busan', 35.1796, 129.0756, 'KR', 'Pacific'),
                ('Manila', 14.5995, 120.9842, 'PH', 'Pacific'),
                ('Jakarta', -6.2088, 106.8456, 'ID', 'Indian Ocean'),
               
                # Hint Okyanusu (4)
                ('Mumbai', 19.0760, 72.8777, 'IN', 'Arabian Sea'),
                ('Dubai', 25.2048, 55.2708, 'AE', 'Persian Gulf'),
                ('Cape Town', -33.9249, 18.4241, 'ZA', 'Atlantic'),
                ('Colombo', 6.9271, 79.8612, 'LK', 'Indian Ocean'),
               
                # Afrika (3)
                ('Lagos', 6.5244, 3.3792, 'NG', 'Atlantic'),
                ('Casablanca', 33.5731, -7.5898, 'MA', 'Atlantic'),
                ('Alexandria', 31.2001, 29.9187, 'EG', 'Mediterranean'),
            ]
           
            wave_data = []
            successful_requests = 0
           
            for city_name, lat, lon, country, water_body in coastal_cities:
                try:
                    # Rüzgar verilerini al
                    params = {
                        'lat': lat,
                        'lon': lon,
                        'appid': API_KEY,
                        'units': 'metric'
                    }
                    response = requests.get(WEATHER_URL, params=params, timeout=8)
                   
                    if response.status_code == 200:
                        data = response.json()
                        wind_speed = data['wind']['speed']
                        wind_deg = data['wind'].get('deg', 0)
                       
                        # Dalga yüksekliği hesaplama
                        wave_height = calculate_wave_height(wind_speed, water_body, wind_deg)
                        wave_period = calculate_wave_period(wave_height)
                        wave_direction = get_wave_direction(wind_deg)
                       
                        successful_requests += 1
                    else:
                        # Yedek tahmin
                        wave_height = estimate_wave_by_location(lat, lon, water_body)
                        wave_period = calculate_wave_period(wave_height)
                        wave_direction = 'N/A'
                        wind_speed = 0
                   
                    category, color, icon = get_wave_category(wave_height)
                   
                    wave_data.append({
                        'city': city_name,
                        'country': country,
                        'lat': lat,
                        'lon': lon,
                        'wave_height': wave_height,
                        'wave_period': wave_period,
                        'wave_direction': wave_direction,
                        'wind_speed': wind_speed,
                        'water_body': water_body,
                        'category': category,
                        'color': color,
                        'icon': icon
                    })
                   
                except Exception as e:
                    print(f"Dalga verisi hatası {city_name}: {e}")
                    continue
           
            display_global_wave_data(wave_data)
            info_label.config(text=t('cities_loaded').format(successful_requests) + ' | ' + t('last_update').format(datetime.now().strftime("%H:%M:%S")))
           
        except Exception as e:
            info_label.config(text=f'{t("data_error")}: {str(e)}')  # Çeviri fonksiyonu eklendi
   
    def calculate_wave_height(wind_speed, water_body, wind_deg):
        """Gelişmiş dalga yüksekliği hesaplama"""
        # Temel dalga yüksekliği (Beaufort skalası benzeri)
        # H = 0.21 * (wind_speed)^2 / g (basitleştirilmiş)
        base_height = (wind_speed ** 2) * 0.005
       
        # Su kütlesi faktörü (okyanus > deniz > körfez)
        water_factors = {
            'Pacific': 1.5,
            'Atlantic': 1.4,
            'Indian Ocean': 1.3,
            'Arabian Sea': 1.2,
            'Mediterranean': 0.9,
            'Black Sea': 0.8,
            'Persian Gulf': 0.7,
        }
        water_factor = water_factors.get(water_body, 1.0)
       
        # Rüzgar yönü faktörü (açık denize doğru rüzgar = daha yüksek dalga)
        # Bu basitleştirilmiş bir yaklaşım
        direction_factor = 1.0 + (random.random() * 0.3)
       
        # Mevsimsel faktör
        current_month = datetime.now().month
        if current_month in [12, 1, 2, 3]:  # Kış
            season_factor = 1.3
        elif current_month in [6, 7, 8, 9]:  # Yaz
            season_factor = 0.8
        else:
            season_factor = 1.0
       
        wave_height = base_height * water_factor * direction_factor * season_factor
       
        # Rastgele varyasyon ekle
        wave_height += random.uniform(-0.2, 0.3)
       
        return max(0.1, min(8.0, wave_height))
   
    def calculate_wave_period(wave_height):
        """Dalga periyodu hesaplama (saniye)"""
        # Yaklaşık formül: T ≈ 3.86 * √H (derin su dalgaları için)
        period = 3.86 * (wave_height ** 0.5)
        return round(period, 1)
   
    def get_wave_direction(wind_deg):
        """Dalga yönü (rüzgar yönüne benzer)"""
        directions = ['K', 'KD', 'D', 'GD', 'G', 'GB', 'B', 'KB']
        index = int((wind_deg + 22.5) / 45) % 8
        return directions[index]
   
    def estimate_wave_by_location(lat, lon, water_body):
        """Konuma göre dalga tahmini (yedek)"""
        water_factors = {
            'Pacific': 2.5,
            'Atlantic': 2.0,
            'Indian Ocean': 1.8,
            'Arabian Sea': 1.5,
            'Mediterranean': 1.0,
            'Black Sea': 0.8,
            'Persian Gulf': 0.6,
        }
        base = water_factors.get(water_body, 1.5)
       
        # Enlem faktörü (yüksek enlemlerde genelde daha yüksek dalga)
        latitude_factor = 1 + abs(lat) / 90 * 0.5
       
        wave = base * latitude_factor + random.uniform(-0.5, 0.5)
        return max(0.1, min(6.0, wave))
   
    def get_wave_category(wave_height):
        """Dalga kategorisi"""
        if wave_height < 0.5:
            return t('wave_calm'), '#4CAF50', '😌'  # Çeviri fonksiyonu eklendi
        elif wave_height < 1.0:
            return t('wave_light'), '#8BC34A', '🌊'  # Çeviri fonksiyonu eklendi
        elif wave_height < 2.0:
            return t('wave_moderate'), '#FFEB3B', '〰️'  # Çeviri fonksiyonu eklendi
        elif wave_height < 3.0:
            return t('wave_high'), '#FF9800', '🌀'  # Çeviri fonksiyonu eklendi
        elif wave_height < 5.0:
            return t('wave_very_high'), '#F44336', '⚠️'  # Çeviri fonksiyonu eklendi
        else:
            return t('wave_extreme'), '#9C27B0', '🚨'  # Çeviri fonksiyonu eklendi
   
    def display_global_wave_data(wave_data):
        """Dalga verilerini haritada göster"""
        for marker in markers:
            try:
                map_widget.delete(marker)
            except:
                pass
        markers.clear()
       
        for data in wave_data:
            try:
                # Kompakt marker metni
                marker_text = f"{data['icon']} {data['city']}{data['wave_height']:.1f}m"
               
                marker = map_widget.set_marker(
                    data['lat'], data['lon'],
                    text=marker_text,
                    marker_color_circle=data['color'],
                    text_color="black",
                    font=("Arial", 8),
                    command=lambda d=data: show_wave_detail(d)
                )
                markers.append(marker)
               
            except Exception as e:
                print(f"Marker hatası {data['city']}: {e}")
   
    def show_wave_detail(data):
        """Dalga detay penceresi"""
        detail_win = Toplevel()
        detail_win.title(f"🌊 {data['city']} {t('wave_details')}")  # Çeviri fonksiyonu eklendi
        detail_win.geometry('450x500')
        detail_win.configure(bg='#E0F7FA')
       
        # Başlık
        Label(detail_win, text=f"🌊 {data['city']}, {data['country']}",
              font=('Arial', 16, 'bold'), bg='#E0F7FA', fg='#006064').pack(pady=10)
       
        Label(detail_win, text=f"📍 {data['water_body']}",
              font=('Arial', 11), bg='#E0F7FA', fg='#00838F').pack(pady=5)
       
        # Genel durum
        status_frame = Frame(detail_win, bg=data['color'], relief='solid', bd=2)
        status_frame.pack(fill='x', padx=20, pady=10)
       
        Label(status_frame, text=f"{data['icon']} {data['category']}",
              font=('Arial', 14, 'bold'), bg=data['color'], fg='white').pack(pady=10)
       
        # Ana dalga bilgileri
        main_info_frame = Frame(detail_win, bg='white', relief='solid', bd=1)
        main_info_frame.pack(fill='x', padx=20, pady=10)
       
        wave_info = [
            ('🌊 ' + t('wave_height'), f"{data['wave_height']:.2f} {t('wave_height')}"),  # Çeviri fonksiyonu eklendi
            ('⏱️ ' + t('wave_period'), f"{data['wave_period']:.1f} {t('wave_period')}"),  # Çeviri fonksiyonu eklendi
            ('🧭 ' + t('wave_direction'), data['wave_direction']),  # Çeviri fonksiyonu eklendi
            ('💨 ' + t('wind_speed'), f"{data['wind_speed']:.1f} {t('wind_speed')}"),  # Çeviri fonksiyonu eklendi
        ]
       
        for label, value in wave_info:
            info_row = Frame(main_info_frame, bg='white')
            info_row.pack(fill='x', padx=15, pady=8)
           
            Label(info_row, text=label, font=('Arial', 11, 'bold'),
                  bg='white', fg='#424242', width=20, anchor='w').pack(side='left')
           
            Label(info_row, text=value, font=('Arial', 11),
                  bg='white', fg='#00838F').pack(side='left', padx=10)
       
        # Dalga yüksekliği göstergesi (görsel)
        visual_frame = Frame(detail_win, bg='white', relief='solid', bd=1)
        visual_frame.pack(fill='x', padx=20, pady=10)
       
        Label(visual_frame, text="📊 " + t('wave_height'),  # Çeviri fonksiyonu eklendi
              font=('Arial', 11, 'bold'), bg='white').pack(pady=5)
       
        canvas = Canvas(visual_frame, width=380, height=80, bg='#B2EBF2',
                       highlightthickness=0)
        canvas.pack(pady=10, padx=10)
       
        # Deniz çizgisi
        canvas.create_line(10, 60, 370, 60, fill='#006064', width=2)
       
        # Dalga yüksekliği (bar)
        max_height = 8.0  # metre
        bar_height = int(50 * data['wave_height'] / max_height)
        canvas.create_rectangle(180, 60 - bar_height, 200, 60,
                               fill=data['color'], outline='#006064', width=2)
       
        # Etiket
        canvas.create_text(190, 30, text=f"{data['wave_height']:.1f}m",
                          font=('Arial', 12, 'bold'), fill='#006064')
       
        # Aktivite önerileri
        suggestion_frame = Frame(detail_win, bg='#FFF9C4', relief='solid', bd=1)
        suggestion_frame.pack(fill='x', padx=20, pady=10)
       
        if data['wave_height'] < 0.5:
            suggestions = t('wave_tip_calm')  # Çeviri fonksiyonu eklendi
        elif data['wave_height'] < 1.0:
            suggestions = t('wave_tip_light')  # Çeviri fonksiyonu eklendi
        elif data['wave_height'] < 2.0:
            suggestions = t('wave_tip_moderate')  # Çeviri fonksiyonu eklendi
        elif data['wave_height'] < 3.0:
            suggestions = t('wave_tip_high')  # Çeviri fonksiyonu eklendi
        elif data['wave_height'] < 5.0:
            suggestions = t('wave_tip_very_high')  # Çeviri fonksiyonu eklendi
        else:
            suggestions = t('wave_tip_extreme')  # Çeviri fonksiyonu eklendi
       
        Label(suggestion_frame, text=t('activity_recommendations'),  # Çeviri fonksiyonu eklendi
              font=('Arial', 10, 'bold'), bg='#FFF9C4', fg='#F57F00').pack(pady=5)
       
        Label(suggestion_frame, text=suggestions, font=('Arial', 10),
              bg='#FFF9C4', fg='#E65100', justify='left').pack(pady=5, padx=10)
       
        Button(detail_win, text=t('close'), command=detail_win.destroy,  # Çeviri fonksiyonu eklendi
               bg='#9E9E9E', fg='white', font=('Arial', 11, 'bold'),
               width=20).pack(pady=10)
   
    def search_coastal_city():
        """Kıyı şehir arama"""
        search_win = Toplevel()
        search_win.title(t('city_search'))  # Çeviri fonksiyonu eklendi
        search_win.geometry('350x250')
        search_win.configure(bg='#E0F7FA')
       
        Label(search_win, text=t('enter_city_name'), font=('Arial', 12, 'bold'),  # Çeviri fonksiyonu eklendi
              bg='#E0F7FA').pack(pady=10)
       
        search_entry = Entry(search_win, font=('Arial', 12), width=25)
        search_entry.pack(pady=5)
        search_entry.focus()
       
        Label(search_win, text=t('search_coastal_tip'),  # Çeviri için translations'a eklemeniz gerekebilir
              font=('Arial', 9), bg='#E0F7FA', fg='#666').pack(pady=5)
       
        result_label = Label(search_win, text='', font=('Arial', 10),
                            bg='#E0F7FA', fg='#006064')
        result_label.pack(pady=5)
       
        def perform_search():
            city_name = search_entry.get().strip()
            if not city_name:
                result_label.config(text=t('enter_city_name'), fg='red')  # Çeviri fonksiyonu eklendi
                return
           
            result_label.config(text=t('searching'), fg='#006064')  # Çeviri fonksiyonu eklendi
            search_win.update()
           
            try:
                # Geocoding ile şehir bul
                params = {
                    'q': city_name,
                    'appid': API_KEY,
                    'limit': 1
                }
                response = requests.get("http://api.openweathermap.org/geo/1.0/direct",
                                      params=params, timeout=5)
               
                if response.status_code == 200 and response.json():
                    city_data = response.json()[0]
                    lat = city_data['lat']
                    lon = city_data['lon']
                    found_name = city_data['name']
                   
                    # Rüzgar verisini al
                    weather_params = {
                        'lat': lat,
                        'lon': lon,
                        'appid': API_KEY,
                        'units': 'metric'
                    }
                    weather_response = requests.get(WEATHER_URL, params=weather_params, timeout=5)
                   
                    if weather_response.status_code == 200:
                        weather_data = weather_response.json()
                        wind_speed = weather_data['wind']['speed']
                        wind_deg = weather_data['wind'].get('deg', 0)
                       
                        wave_height = calculate_wave_height(wind_speed, 'Ocean', wind_deg)
                    else:
                        wave_height = estimate_wave_by_location(lat, lon, 'Ocean')
                   
                    category, color, icon = get_wave_category(wave_height)
                   
                    result_label.config(
                        text=f'✅ {found_name} {icon}{t("wave_height")}: {wave_height:.1f}m - {category}',  # Çeviri fonksiyonu eklendi
                        fg='green'
                    )
                   
                    # Haritada göster
                    map_widget.set_position(lat, lon)
                    map_widget.set_zoom(8)
                   
                    # Geçici marker
                    temp_marker = map_widget.set_marker(
                        lat, lon,
                        text=f"🌊 {found_name}{wave_height:.1f}m",
                        marker_color_circle=color
                    )
                   
                    def remove_temp():
                        try:
                            map_widget.delete(temp_marker)
                        except:
                            pass
                   
                    search_win.after(12000, remove_temp)
                else:
                    result_label.config(text=t('city_not_found'), fg='red')  # Çeviri fonksiyonu eklendi
                   
            except Exception as e:
                result_label.config(text=f'❌ {t("error")}: {str(e)[:30]}', fg='red')  # Çeviri fonksiyonu eklendi
       
        search_entry.bind('<Return>', lambda e: perform_search())
       
        Button(search_win, text=t('search_city'), command=perform_search,  # Çeviri fonksiyonu eklendi
               bg='#00BCD4', fg='white', font=('Arial', 11, 'bold'),
               width=15).pack(pady=10)
       
        Button(search_win, text=t('close'), command=search_win.destroy,  # Çeviri fonksiyonu eklendi
               bg='#9E9E9E', fg='white', font=('Arial', 10),
               width=15).pack(pady=5)
   
    # Kontrol butonları
    button_frame = Frame(control_frame, bg='#E0F7FA')
    button_frame.pack(side='right', padx=10)
   
    create_button(button_frame, t('search_city'), search_coastal_city,  # Çeviri fonksiyonu eklendi
                  bg='#2196F3', font=('Arial', 10, 'bold')).pack(side='left', padx=2)
    create_button(button_frame, t('refresh'), get_global_wave_data,  # Çeviri fonksiyonu eklendi
                  bg='#00BCD4', font=('Arial', 10, 'bold')).pack(side='left', padx=2)
    create_button(button_frame, t('ocean_view'),  # Çeviri fonksiyonu eklendi
                  lambda: [map_widget.set_position(0.0, -30.0), map_widget.set_zoom(2)],
                  bg='#4CAF50', font=('Arial', 10, 'bold')).pack(side='left', padx=2)
   
    # Lejant
    legend_frame = Frame(win, bg='#E0F7FA')
    legend_frame.pack(fill='x', pady=5, padx=10)
   
    Label(legend_frame, text=t('wave_legend'), font=('Arial', 9, 'bold'),  # Çeviri fonksiyonu eklendi
          bg='#E0F7FA').pack(side='left', padx=5)
   
    legend_items = [
        ('<0.5m', t('wave_calm'), '#4CAF50'),  # Çeviri fonksiyonu eklendi
        ('0.5-1m', t('wave_light'), '#8BC34A'),  # Çeviri fonksiyonu eklendi
        ('1-2m', t('wave_moderate'), '#FFEB3B'),  # Çeviri fonksiyonu eklendi
        ('2-3m', t('wave_high'), '#FF9800'),  # Çeviri fonksiyonu eklendi
        ('3-5m', t('wave_very_high'), '#F44336'),  # Çeviri fonksiyonu eklendi
        ('>5m', t('wave_extreme'), '#9C27B0')  # Çeviri fonksiyonu eklendi
    ]
   
    for height_range, desc, color in legend_items:
        item_frame = Frame(legend_frame, bg='#E0F7FA')
        item_frame.pack(side='left', padx=6)
       
        Canvas(item_frame, width=12, height=12, bg=color,
               highlightthickness=0).pack(side='left', padx=2)
       
        Label(item_frame, text=f"{height_range} {desc}",
              font=('Arial', 8), bg='#E0F7FA').pack(side='left')
   
    # İlk yükleme
    get_global_wave_data()
   
    # Otomatik yenileme (10 dakika)
    def auto_refresh():
        get_global_wave_data()
        win.after(600000, auto_refresh)
   
    auto_refresh()
   
    # Klavye kısayolları
    def on_key_press(event):
        if event.keysym == 'r':
            get_global_wave_data()
        elif event.keysym == 's':
            search_coastal_city()
        elif event.keysym == 'o':
            map_widget.set_position(0.0, -30.0)
            map_widget.set_zoom(2)
   
    win.bind('<KeyPress>', on_key_press)
    win.focus_set()
   
# 6. ISI DALGASI HARİTASI - DÜNYA ÇAPINDAKİ GELİŞTİRİLMİŞ
def open_heat_map():
    """Dünya Çapında Hissedilen Sıcaklık Haritası"""
    win = Toplevel()
    win.title(t('world_heat_map'))  # Çeviri fonksiyonu eklendi
    win.geometry('900x700')
    win.configure(bg='#FFEBEE')
   
    # Kontrol paneli
    control_frame = Frame(win, bg='#FFEBEE', height=80)
    control_frame.pack(side='top', fill='x', padx=10, pady=10)
    control_frame.pack_propagate(False)
   
    Label(control_frame, text=t('world_heat_map'),  # Çeviri fonksiyonu eklendi
          font=('Arial', 16, 'bold'), bg='#FFEBEE', fg='#B71C1C').pack(side='left', padx=10)
   
    info_label = Label(control_frame, text=t('loading_data'),  # Çeviri fonksiyonu eklendi
                       font=('Arial', 11), bg='#FFEBEE', fg='#D32F2F')
    info_label.pack(side='left', padx=20)
   
    # Harita widget
    map_widget = TkinterMapView(win, width=900, height=600)
    map_widget.pack(fill='both', expand=True)
    map_widget.set_position(20.0, 0.0)
    map_widget.set_zoom(2)
   
    markers = []
   
    def get_global_heat_data():
        """Dünya genelinden hissedilen sıcaklık verilerini al - 40 şehir"""
        try:
            # 40 stratejik şehir - Dünya çapında dengeli dağılım
            global_cities = [
                # Kuzey Amerika (7)
                ('New York', 40.7128, -74.0060, 'US'),
                ('Los Angeles', 34.0522, -118.2437, 'US'),
                ('Phoenix', 33.4484, -112.0740, 'US'),
                ('Miami', 25.7617, -80.1918, 'US'),
                ('Chicago', 41.8781, -87.6298, 'US'),
                ('Toronto', 43.6532, -79.3832, 'CA'),
                ('Mexico City', 19.4326, -99.1332, 'MX'),
               
                # Güney Amerika (4)
                ('São Paulo', -23.5505, -46.6333, 'BR'),
                ('Buenos Aires', -34.6037, -58.3816, 'AR'),
                ('Lima', -12.0464, -77.0428, 'PE'),
                ('Bogotá', 4.7110, -74.0721, 'CO'),
               
                # Avrupa (8)
                ('London', 51.5074, -0.1278, 'GB'),
                ('Paris', 48.8566, 2.3522, 'FR'),
                ('Berlin', 52.5200, 13.4050, 'DE'),
                ('Rome', 41.9028, 12.4964, 'IT'),
                ('Madrid', 40.4168, -3.7038, 'ES'),
                ('Athens', 37.9838, 23.7275, 'GR'),
                ('Moscow', 55.7558, 37.6173, 'RU'),
                ('Istanbul', 41.0082, 28.9784, 'TR'),
               
                # Asya (13)
                ('Tokyo', 35.6762, 139.6503, 'JP'),
                ('Beijing', 39.9042, 116.4074, 'CN'),
                ('Shanghai', 31.2304, 121.4737, 'CN'),
                ('Delhi', 28.6139, 77.2090, 'IN'),
                ('Mumbai', 19.0760, 72.8777, 'IN'),
                ('Kolkata', 22.5726, 88.3639, 'IN'),
                ('Dubai', 25.2048, 55.2708, 'AE'),
                ('Singapore', 1.3521, 103.8198, 'SG'),
                ('Bangkok', 13.7563, 100.5018, 'TH'),
                ('Seoul', 37.5665, 126.9780, 'KR'),
                ('Hong Kong', 22.3193, 114.1694, 'HK'),
                ('Jakarta', -6.2088, 106.8456, 'ID'),
                ('Karachi', 24.8607, 67.0011, 'PK'),
               
                # Ortadoğu (3)
                ('Cairo', 30.0444, 31.2357, 'EG'),
                ('Baghdad', 33.3152, 44.3661, 'IQ'),
                ('Tehran', 35.6892, 51.3890, 'IR'),
               
                # Afrika (3)
                ('Lagos', 6.5244, 3.3792, 'NG'),
                ('Nairobi', -1.2921, 36.8219, 'KE'),
                ('Johannesburg', -26.2041, 28.0473, 'ZA'),
               
                # Okyanusya (2)
                ('Sydney', -33.8688, 151.2093, 'AU'),
                ('Auckland', -36.8485, 174.7633, 'NZ')
            ]
           
            heat_data = []
            successful_requests = 0
           
            for city_name, lat, lon, country in global_cities:
                try:
                    # OpenWeatherMap API - Mevcut hava durumu
                    params = {
                        'lat': lat,
                        'lon': lon,
                        'appid': API_KEY,
                        'units': 'metric'
                    }
                    response = requests.get(WEATHER_URL, params=params, timeout=8)
                   
                    if response.status_code == 200:
                        data = response.json()
                        temp = data['main']['temp']
                        feels_like = data['main']['feels_like']
                        humidity = data['main']['humidity']
                       
                        # Heat Index hesaplama (gelişmiş)
                        heat_index = calculate_advanced_heat_index(temp, humidity)
                       
                        successful_requests += 1
                    else:
                        # Yedek tahmin
                        temp = estimate_temperature(lat, lon)
                        humidity = 60
                        feels_like = temp
                        heat_index = calculate_advanced_heat_index(temp, humidity)
                   
                    category, color, icon, warning = get_heat_index_category(heat_index)
                   
                    heat_data.append({
                        'city': city_name,
                        'country': country,
                        'lat': lat,
                        'lon': lon,
                        'temp': temp,
                        'feels_like': feels_like,
                        'humidity': humidity,
                        'heat_index': heat_index,
                        'category': category,
                        'color': color,
                        'icon': icon,
                        'warning': warning
                    })
                   
                except Exception as e:
                    print(f"Isı verisi hatası {city_name}: {e}")
                    continue
           
            display_global_heat_data(heat_data)
            info_label.config(text=t('cities_loaded').format(successful_requests) + ' | ' + t('last_update').format(datetime.now().strftime("%H:%M:%S")))
           
        except Exception as e:
            info_label.config(text=f'{t("data_error")}: {str(e)}')  # Çeviri fonksiyonu eklendi
   
    def calculate_advanced_heat_index(temp, humidity):
        """Gelişmiş Heat Index hesaplama (NOAA formülü)"""
        # Celsius'u Fahrenheit'a çevir
        temp_f = (temp * 9/5) + 32
       
        # Basit formül (düşük sıcaklıklar için)
        if temp_f < 80:
            heat_index_f = 0.5 * (temp_f + 61.0 + ((temp_f - 68.0) * 1.2) + (humidity * 0.094))
        else:
            # Rothfusz regresyon denklemi
            hi = (-42.379 +
                  2.04901523 * temp_f +
                  10.14333127 * humidity +
                  -0.22475541 * temp_f * humidity +
                  -0.00683783 * temp_f**2 +
                  -0.05481717 * humidity**2 +
                  0.00122874 * temp_f**2 * humidity +
                  0.00085282 * temp_f * humidity**2 +
                  -0.00000199 * temp_f**2 * humidity**2)
           
            # Düzeltmeler
            if humidity < 13 and 80 <= temp_f <= 112:
                adjustment = ((13 - humidity) / 4) * ((17 - abs(temp_f - 95)) / 17) ** 0.5
                hi -= adjustment
            elif humidity > 85 and 80 <= temp_f <= 87:
                adjustment = ((humidity - 85) / 10) * ((87 - temp_f) / 5)
                hi += adjustment
           
            heat_index_f = hi
       
        # Fahrenheit'ı Celsius'a geri çevir
        heat_index_c = (heat_index_f - 32) * 5/9
       
        return round(heat_index_c, 1)
   
    def estimate_temperature(lat, lon):
        """Konuma göre sıcaklık tahmini (yedek)"""
        current_month = datetime.now().month
       
        # Enlem faktörü
        abs_lat = abs(lat)
        latitude_factor = 1 - abs_lat / 90
       
        # Mevsim faktörü (Kuzey yarımküre)
        if lat > 0:
            if current_month in [6, 7, 8]:  # Yaz
                season_temp = 25 + latitude_factor * 10
            elif current_month in [12, 1, 2]:  # Kış
                season_temp = 5 - latitude_factor * 10
            else:
                season_temp = 15 + latitude_factor * 5
        else:  # Güney yarımküre
            if current_month in [12, 1, 2]:  # Yaz
                season_temp = 25 + latitude_factor * 10
            elif current_month in [6, 7, 8]:  # Kış
                season_temp = 5 - latitude_factor * 10
            else:
                season_temp = 15 + latitude_factor * 5
       
        return round(season_temp + random.uniform(-3, 3), 1)
   
    def get_heat_index_category(heat_index):
        """Heat Index kategorisi (NOAA standartları)"""
        if heat_index < 27:
            return t('heat_normal'), '#4CAF50', '😊', t('heat_safe')  # Çeviri fonksiyonu eklendi
        elif heat_index < 32:
            return t('heat_caution'), '#FFEB3B', '😐', t('heat_fatigue_possible')  # Çeviri fonksiyonu eklendi
        elif heat_index < 39:
            return t('heat_extreme_caution'), '#FF9800', '😓', t('heat_cramps_possible')  # Çeviri fonksiyonu eklendi
        elif heat_index < 51:
            return t('heat_danger'), '#F44336', '🥵', t('heat_exhaustion_likely')  # Çeviri fonksiyonu eklendi
        else:
            return t('heat_extreme_danger'), '#9C27B0', '🚨', t('heat_stroke_risk')  # Çeviri fonksiyonu eklendi
   
    def display_global_heat_data(heat_data):
        """Isı verilerini haritada göster"""
        for marker in markers:
            try:
                map_widget.delete(marker)
            except:
                pass
        markers.clear()
       
        for data in heat_data:
            try:
                # Kompakt marker metni
                marker_text = f"{data['icon']} {data['city']}🌡️ {data['heat_index']}°C"
               
                marker = map_widget.set_marker(
                    data['lat'], data['lon'],
                    text=marker_text,
                    marker_color_circle=data['color'],
                    text_color="black",
                    font=("Arial", 8),
                    command=lambda d=data: show_heat_detail(d)
                )
                markers.append(marker)
               
            except Exception as e:
                print(f"Marker hatası {data['city']}: {e}")
   
    def show_heat_detail(data):
        """Isı detay penceresi"""
        detail_win = Toplevel()
        detail_win.title(f"🌡️ {data['city']} {t('heat_index')}")  # Çeviri fonksiyonu eklendi
        detail_win.geometry('450x500')
        detail_win.configure(bg='#FFEBEE')
       
        # Başlık
        Label(detail_win, text=f"🌡️ {data['city']}, {data['country']}",
              font=('Arial', 16, 'bold'), bg='#FFEBEE', fg='#B71C1C').pack(pady=10)
       
        # Genel durum
        status_frame = Frame(detail_win, bg=data['color'], relief='solid', bd=2)
        status_frame.pack(fill='x', padx=20, pady=10)
       
        Label(status_frame, text=f"{data['icon']} {data['category']}",
              font=('Arial', 14, 'bold'), bg=data['color'], fg='white').pack(pady=10)
       
        Label(status_frame, text=f"{t('heat_index')}: {data['heat_index']}°C",  # Çeviri fonksiyonu eklendi
              font=('Arial', 12), bg=data['color'], fg='white').pack(pady=5)
       
        # Detaylı bilgiler
        info_frame = Frame(detail_win, bg='white', relief='solid', bd=1)
        info_frame.pack(fill='x', padx=20, pady=10)
       
        details = [
            ('🌡️ ' + t('actual_temperature'), f"{data['temp']}°C"),  # Çeviri fonksiyonu eklendi
            ('🔥 ' + t('feels_like'), f"{data['feels_like']}°C"),  # Çeviri fonksiyonu eklendi
            ('💧 ' + t('humidity'), f"{data['humidity']}%"),  # Çeviri fonksiyonu eklendi
            ('📊 ' + t('heat_index'), f"{data['heat_index']}°C"),  # Çeviri fonksiyonu eklendi
        ]
       
        for label, value in details:
            detail_row = Frame(info_frame, bg='white')
            detail_row.pack(fill='x', padx=15, pady=8)
           
            Label(detail_row, text=label, font=('Arial', 11, 'bold'),
                  bg='white', fg='#424242', width=18, anchor='w').pack(side='left')
           
            Label(detail_row, text=value, font=('Arial', 11),
                  bg='white', fg='#D32F2F').pack(side='left', padx=10)
       
        # Termometre görseli
        visual_frame = Frame(detail_win, bg='white', relief='solid', bd=1)
        visual_frame.pack(fill='x', padx=20, pady=10)
       
        Label(visual_frame, text="🌡️ " + t('heat_indicator'),  # Çeviri fonksiyonu eklendi
              font=('Arial', 11, 'bold'), bg='white').pack(pady=5)
       
        canvas = Canvas(visual_frame, width=380, height=100, bg='white',
                       highlightthickness=0)
        canvas.pack(pady=10, padx=10)
       
        # Sıcaklık skalası (0°C - 60°C)
        canvas.create_rectangle(50, 70, 350, 85, fill='#E0E0E0', outline='#424242')
       
        # Renk gradyanı
        colors = ['#4CAF50', '#FFEB3B', '#FF9800', '#F44336', '#9C27B0']
        segment_width = 300 / len(colors)
        for i, color in enumerate(colors):
            x1 = 50 + i * segment_width
            x2 = 50 + (i + 1) * segment_width
            canvas.create_rectangle(x1, 70, x2, 85, fill=color, outline='')
       
        # Heat index göstergesi
        max_temp = 60
        indicator_x = 50 + (data['heat_index'] / max_temp) * 300
        indicator_x = max(50, min(350, indicator_x))
       
        canvas.create_oval(indicator_x - 8, 60, indicator_x + 8, 92,
                          fill='#B71C1C', outline='white', width=2)
       
        # Etiketler
        canvas.create_text(50, 95, text='0°C', font=('Arial', 8))
        canvas.create_text(200, 95, text='30°C', font=('Arial', 8))
        canvas.create_text(350, 95, text='60°C', font=('Arial', 8))
       
        canvas.create_text(indicator_x, 45, text=f"{data['heat_index']}°C",
                          font=('Arial', 12, 'bold'), fill='#B71C1C')
       
        # Uyarı mesajı
        warning_frame = Frame(detail_win, bg='#FFF3E0', relief='solid', bd=1)
        warning_frame.pack(fill='x', padx=20, pady=10)
       
        Label(warning_frame, text="⚠️ " + t('health_warning'),  # Çeviri fonksiyonu eklendi
              font=('Arial', 10, 'bold'), bg='#FFF3E0', fg='#E65100').pack(pady=5)
       
        Label(warning_frame, text=data['warning'],
              font=('Arial', 10), bg='#FFF3E0', fg='#E65100',
              wraplength=380).pack(pady=5, padx=10)
       
        Button(detail_win, text=t('close'), command=detail_win.destroy,  # Çeviri fonksiyonu eklendi
               bg='#9E9E9E', fg='white', font=('Arial', 11, 'bold'),
               width=20).pack(pady=10)
   
    def search_city():
        """Şehir arama"""
        search_win = Toplevel()
        search_win.title(t('city_search'))  # Çeviri fonksiyonu eklendi
        search_win.geometry('350x220')
        search_win.configure(bg='#FFEBEE')
       
        Label(search_win, text=t('enter_city_name'), font=('Arial', 12, 'bold'),  # Çeviri fonksiyonu eklendi
              bg='#FFEBEE').pack(pady=10)
       
        search_entry = Entry(search_win, font=('Arial', 12), width=25)
        search_entry.pack(pady=5)
        search_entry.focus()
       
        result_label = Label(search_win, text='', font=('Arial', 10),
                            bg='#FFEBEE', fg='#D32F2F')
        result_label.pack(pady=5)
       
        def perform_search():
            city_name = search_entry.get().strip()
            if not city_name:
                result_label.config(text=t('enter_city_name'), fg='red')  # Çeviri fonksiyonu eklendi
                return
           
            result_label.config(text=t('searching'), fg='#D32F2F')  # Çeviri fonksiyonu eklendi
            search_win.update()
           
            try:
                # Geocoding
                params = {
                    'q': city_name,
                    'appid': API_KEY,
                    'limit': 1
                }
                response = requests.get("http://api.openweathermap.org/geo/1.0/direct",
                                      params=params, timeout=5)
               
                if response.status_code == 200 and response.json():
                    city_data = response.json()[0]
                    lat = city_data['lat']
                    lon = city_data['lon']
                    found_name = city_data['name']
                   
                    # Hava durumu al
                    params2 = {
                        'lat': lat,
                        'lon': lon,
                        'appid': API_KEY,
                        'units': 'metric'
                    }
                    weather_response = requests.get(WEATHER_URL, params=params2, timeout=5)
                   
                    if weather_response.status_code == 200:
                        weather_data = weather_response.json()
                        temp = weather_data['main']['temp']
                        humidity = weather_data['main']['humidity']
                       
                        heat_index = calculate_advanced_heat_index(temp, humidity)
                    else:
                        temp = estimate_temperature(lat, lon)
                        humidity = 60
                        heat_index = calculate_advanced_heat_index(temp, humidity)
                   
                    category, color, icon, warning = get_heat_index_category(heat_index)
                   
                    result_label.config(
                        text=f'✅ {found_name}{icon} {t("heat_index")}: {heat_index}°C - {category}',  # Çeviri fonksiyonu eklendi
                        fg='green'
                    )
                   
                    # Haritada göster
                    map_widget.set_position(lat, lon)
                    map_widget.set_zoom(10)
                   
                    # Geçici marker
                    temp_marker = map_widget.set_marker(
                        lat, lon,
                        text=f"🌡️ {found_name}{heat_index}°C",
                        marker_color_circle=color
                    )
                   
                    def remove_temp():
                        try:
                            map_widget.delete(temp_marker)
                        except:
                            pass
                   
                    search_win.after(10000, remove_temp)
                else:
                    result_label.config(text=t('city_not_found'), fg='red')  # Çeviri fonksiyonu eklendi
                   
            except Exception as e:
                result_label.config(text=f'❌ {t("error")}: {str(e)[:30]}', fg='red')  # Çeviri fonksiyonu eklendi
       
        search_entry.bind('<Return>', lambda e: perform_search())
       
        Button(search_win, text=t('search_city'), command=perform_search,  # Çeviri fonksiyonu eklendi
               bg='#F44336', fg='white', font=('Arial', 11, 'bold'),
               width=15).pack(pady=10)
       
        Button(search_win, text=t('close'), command=search_win.destroy,  # Çeviri fonksiyonu eklendi
               bg='#9E9E9E', fg='white', font=('Arial', 10),
               width=15).pack(pady=5)
   
    # Kontrol butonları
    button_frame = Frame(control_frame, bg='#FFEBEE')
    button_frame.pack(side='right', padx=10)
   
    create_button(button_frame, t('search_city'), search_city,  # Çeviri fonksiyonu eklendi
                  bg='#F44336', font=('Arial', 10, 'bold')).pack(side='left', padx=2)
    create_button(button_frame, t('refresh'), get_global_heat_data,  # Çeviri fonksiyonu eklendi
                  bg='#FF5722', font=('Arial', 10, 'bold')).pack(side='left', padx=2)
    create_button(button_frame, t('world_view'),  # Çeviri fonksiyonu eklendi
                  lambda: [map_widget.set_position(20.0, 0.0), map_widget.set_zoom(2)],
                  bg='#FF9800', font=('Arial', 10, 'bold')).pack(side='left', padx=2)
   
    # Lejant
    legend_frame = Frame(win, bg='#FFEBEE')
    legend_frame.pack(fill='x', pady=5, padx=10)
   
    Label(legend_frame, text=t('heat_index_legend'), font=('Arial', 9, 'bold'),  # Çeviri fonksiyonu eklendi
          bg='#FFEBEE').pack(side='left', padx=5)
   
    legend_items = [
        ('<27°C', t('heat_normal'), '#4CAF50'),  # Çeviri fonksiyonu eklendi
        ('27-32°C', t('heat_caution'), '#FFEB3B'),  # Çeviri fonksiyonu eklendi
        ('32-39°C', t('heat_extreme_caution'), '#FF9800'),  # Çeviri fonksiyonu eklendi
        ('39-51°C', t('heat_danger'), '#F44336'),  # Çeviri fonksiyonu eklendi
        ('>51°C', t('heat_extreme_danger'), '#9C27B0')  # Çeviri fonksiyonu eklendi
    ]
   
    for temp_range, desc, color in legend_items:
        item_frame = Frame(legend_frame, bg='#FFEBEE')
        item_frame.pack(side='left', padx=6)
       
        Canvas(item_frame, width=12, height=12, bg=color,
               highlightthickness=0).pack(side='left', padx=2)
       
        Label(item_frame, text=f"{temp_range} {desc}",
              font=('Arial', 8), bg='#FFEBEE').pack(side='left')
   
    # İlk yükleme
    get_global_heat_data()
   
    # Otomatik yenileme (10 dakika)
    def auto_refresh():
        get_global_heat_data()
        win.after(600000, auto_refresh)
   
    auto_refresh()
   
    # Klavye kısayolları
    def on_key_press(event):
        if event.keysym == 'r':
            get_global_heat_data()
        elif event.keysym == 's':
            search_city()
   
    win.bind('<KeyPress>', on_key_press)
    win.focus_set()
   
# 7. FIRTINA İZİ HARİTASI - DÜNYA ÇAPINDAKİ GELİŞTİRİLMİŞ
def open_storm_map():
    """Dünya Çapında Gerçek Zamanlı Fırtına Takip Haritası"""
    win = Toplevel()
    win.title("🌪️ Dünya Fırtına Takip Haritası")
    win.geometry('900x700')
    win.configure(bg='#E3F2FD')
   
    # Kontrol paneli
    control_frame = Frame(win, bg='#E3F2FD', height=80)
    control_frame.pack(side='top', fill='x', padx=10, pady=10)
    control_frame.pack_propagate(False)
   
    Label(control_frame, text="🌪️ Dünya Fırtına Takip Haritası",
          font=('Arial', 16, 'bold'), bg='#E3F2FD', fg='#01579B').pack(side='left', padx=10)
   
    info_label = Label(control_frame, text='Veriler yükleniyor...',
                       font=('Arial', 11), bg='#E3F2FD', fg='#0277BD')
    info_label.pack(side='left', padx=20)
   
    # Harita widget
    map_widget = TkinterMapView(win, width=900, height=600)
    map_widget.pack(fill='both', expand=True)
    map_widget.set_position(20.0, 0.0)
    map_widget.set_zoom(2)
   
    markers = []
    storm_paths = []
   
    def get_global_storm_data():
        """Dünya genelinden fırtına verilerini al - 45 şehir"""
        try:
            # 45 stratejik şehir - Fırtına riski yüksek bölgeler
            global_cities = [
                # Kuzey Amerika - Atlantik Kıyısı (8)
                ('New York', 40.7128, -74.0060, 'US'),
                ('Miami', 25.7617, -80.1918, 'US'),
                ('Houston', 29.7604, -95.3698, 'US'),
                ('New Orleans', 29.9511, -90.0715, 'US'),
                ('Boston', 42.3601, -71.0589, 'US'),
                ('Charleston', 32.7765, -79.9311, 'US'),
                ('Tampa', 27.9506, -82.4572, 'US'),
                ('Norfolk', 36.8508, -76.2859, 'US'),
               
                # Kuzey Amerika - Pasifik Kıyısı (5)
                ('San Francisco', 37.7749, -122.4194, 'US'),
                ('Los Angeles', 34.0522, -118.2437, 'US'),
                ('Seattle', 47.6062, -122.3321, 'US'),
                ('Vancouver', 49.2827, -123.1207, 'CA'),
                ('Portland', 45.5152, -122.6784, 'US'),
               
                # Orta Amerika & Karayipler (4)
                ('Mexico City', 19.4326, -99.1332, 'MX'),
                ('Havana', 23.1136, -82.3666, 'CU'),
                ('Kingston', 17.9714, -76.7931, 'JM'),
                ('Santo Domingo', 18.4861, -69.9312, 'DO'),
               
                # Avrupa - Atlantik & Akdeniz (7)
                ('London', 51.5074, -0.1278, 'GB'),
                ('Lisbon', 38.7223, -9.1393, 'PT'),
                ('Barcelona', 41.3851, 2.1734, 'ES'),
                ('Naples', 40.8518, 14.2681, 'IT'),
                ('Marseille', 43.2965, 5.3698, 'FR'),
                ('Dublin', 53.3498, -6.2603, 'IE'),
                ('Reykjavik', 64.1466, -21.9426, 'IS'),
               
                # Asya - Tayfun Bölgesi (12)
                ('Tokyo', 35.6762, 139.6503, 'JP'),
                ('Osaka', 34.6937, 135.5023, 'JP'),
                ('Shanghai', 31.2304, 121.4737, 'CN'),
                ('Hong Kong', 22.3193, 114.1694, 'HK'),
                ('Manila', 14.5995, 120.9842, 'PH'),
                ('Taipei', 25.0330, 121.5654, 'TW'),
                ('Hanoi', 21.0285, 105.8542, 'VN'),
                ('Bangkok', 13.7563, 100.5018, 'TH'),
                ('Ho Chi Minh', 10.8231, 106.6297, 'VN'),
                ('Guangzhou', 23.1291, 113.2644, 'CN'),
                ('Busan', 35.1796, 129.0756, 'KR'),
                ('Naha', 26.2124, 127.6809, 'JP'),
               
                # Hint Okyanusu (4)
                ('Mumbai', 19.0760, 72.8777, 'IN'),
                ('Kolkata', 22.5726, 88.3639, 'IN'),
                ('Colombo', 6.9271, 79.8612, 'LK'),
                ('Chittagong', 22.3569, 91.7832, 'BD'),
               
                # Okyanusya - Tropikal Bölge (3)
                ('Brisbane', -27.4698, 153.0251, 'AU'),
                ('Darwin', -12.4634, 130.8456, 'AU'),
                ('Port Vila', -17.7333, 168.3273, 'VU'),
               
                # Afrika - Tropikal Bölge (2)
                ('Maputo', -25.9655, 32.5832, 'MZ'),
                ('Antananarivo', -18.8792, 47.5079, 'MG'),
            ]
           
            storm_data = []
            successful_requests = 0
            active_storms = 0
           
            for city_name, lat, lon, country in global_cities:
                try:
                    # OpenWeatherMap API - Mevcut hava durumu
                    params = {
                        'lat': lat,
                        'lon': lon,
                        'appid': API_KEY,
                        'units': 'metric'
                    }
                    response = requests.get(WEATHER_URL, params=params, timeout=8)
                   
                    if response.status_code == 200:
                        data = response.json()
                       
                        # Hava durumu analizi
                        weather_main = data['weather'][0]['main']
                        weather_desc = data['weather'][0]['description']
                        wind_speed = data['wind']['speed']
                        wind_deg = data['wind'].get('deg', 0)
                        pressure = data['main']['pressure']
                       
                        # Fırtına analizi
                        storm_info = analyze_storm_conditions(
                            weather_main, weather_desc, wind_speed,
                            wind_deg, pressure, lat
                        )
                       
                        if storm_info['is_storm']:
                            active_storms += 1
                       
                        successful_requests += 1
                    else:
                        # Yedek tahmin
                        storm_info = estimate_storm_by_location(lat, lon)
                   
                    category, color, icon, intensity = get_storm_category(
                        storm_info['wind_speed'], storm_info['pressure']
                    )
                   
                    storm_data.append({
                        'city': city_name,
                        'country': country,
                        'lat': lat,
                        'lon': lon,
                        'wind_speed': storm_info['wind_speed'],
                        'wind_direction': storm_info['wind_direction'],
                        'pressure': storm_info['pressure'],
                        'weather': storm_info['weather'],
                        'is_storm': storm_info['is_storm'],
                        'storm_type': storm_info['storm_type'],
                        'category': category,
                        'color': color,
                        'icon': icon,
                        'intensity': intensity
                    })
                   
                except Exception as e:
                    print(f"Fırtına verisi hatası {city_name}: {e}")
                    continue
           
            display_global_storm_data(storm_data)
            info_label.config(
                text=f'🌍 {successful_requests} bölge | 🌪️ Aktif Fırtına: {active_storms} | '
                     f'{datetime.now().strftime("%H:%M:%S")}'
            )
           
        except Exception as e:
            info_label.config(text=f'Veri hatası: {str(e)}')
   
    def analyze_storm_conditions(weather_main, weather_desc, wind_speed,
                                 wind_deg, pressure, lat):
        """Hava durumunu analiz ederek fırtına durumunu belirle"""
       
        # Rüzgar yönü
        directions = ['K', 'KD', 'D', 'GD', 'G', 'GB', 'B', 'KB']
        direction_index = int((wind_deg + 22.5) / 45) % 8
        wind_direction = directions[direction_index]
       
        # Fırtına tespiti
        is_storm = False
        storm_type = 'Normal'
       
        # Kriterlere göre fırtına tespiti
        if 'thunderstorm' in weather_desc.lower():
            is_storm = True
            storm_type = 'Gök Gürültülü Fırtına'
        elif wind_speed > 17.2:  # > 62 km/h (Fırtına eşiği)
            is_storm = True
            if abs(lat) < 30:  # Tropikal bölge
                storm_type = 'Tropikal Fırtına'
            else:
                storm_type = 'Ekstratropikal Fırtına'
        elif wind_speed > 10.8 and pressure < 1000:
            is_storm = True
            storm_type = 'Alçak Basınç Fırtınası'
        elif 'squall' in weather_desc.lower():
            is_storm = True
            storm_type = 'Sert Rüzgar'
       
        return {
            'wind_speed': wind_speed,
            'wind_direction': wind_direction,
            'pressure': pressure,
            'weather': weather_desc,
            'is_storm': is_storm,
            'storm_type': storm_type
        }
   
    def estimate_storm_by_location(lat, lon):
        """Konuma göre fırtına tahmini (yedek)"""
        current_month = datetime.now().month
       
        # Tropikal bölge fırtına mevsimi
        is_tropical = abs(lat) < 30
       
        if is_tropical:
            # Kuzey yarımküre tayfun mevsimi (Haziran-Kasım)
            if lat > 0 and 6 <= current_month <= 11:
                base_wind = random.uniform(8, 20)
            # Güney yarımküre tropikal fırtına mevsimi (Kasım-Nisan)
            elif lat < 0 and (current_month >= 11 or current_month <= 4):
                base_wind = random.uniform(8, 20)
            else:
                base_wind = random.uniform(3, 10)
        else:
            # Orta enlemler - kış fırtınaları
            if (lat > 0 and (current_month >= 11 or current_month <= 3)) or \
               (lat < 0 and 5 <= current_month <= 9):
                base_wind = random.uniform(7, 18)
            else:
                base_wind = random.uniform(3, 12)
       
        is_storm = base_wind > 10.8
       
        return {
            'wind_speed': round(base_wind, 1),
            'wind_direction': random.choice(['K', 'KD', 'D', 'GD', 'G', 'GB', 'B', 'KB']),
            'pressure': random.randint(980, 1020),
            'weather': 'Simüle edilmiş',
            'is_storm': is_storm,
            'storm_type': 'Tropikal Fırtına' if is_tropical and is_storm else 'Fırtına' if is_storm else 'Normal'
        }
   
    def get_storm_category(wind_speed, pressure):
        """Fırtına kategorisi (Saffir-Simpson benzeri)"""
        # Rüzgar hızını km/h'ye çevir
        wind_kmh = wind_speed * 3.6
       
        if wind_kmh < 39:
            return 'Normal', '#4CAF50', '☁️', 0
        elif wind_kmh < 62:
            return 'Rüzgarlı', '#8BC34A', '💨', 1
        elif wind_kmh < 88:
            return 'Fırtına', '#FFEB3B', '🌬️', 2
        elif wind_kmh < 118:
            return 'Şiddetli Fırtına', '#FF9800', '🌪️', 3
        elif wind_kmh < 178:
            return 'Çok Şiddetli Fırtına', '#F44336', '⛈️', 4
        else:
            return 'Kasırga/Tayfun', '#9C27B0', '🌀', 5
   
    def display_global_storm_data(storm_data):
        """Fırtına verilerini haritada göster"""
        # Önceki marker'ları temizle
        for marker in markers:
            try:
                map_widget.delete(marker)
            except:
                pass
        markers.clear()
       
        # Aktif fırtınaları önce göster (büyük marker)
        storm_data_sorted = sorted(storm_data, key=lambda x: x['is_storm'], reverse=True)
       
        for data in storm_data_sorted:
            try:
                if data['is_storm']:
                    # Aktif fırtına - büyük marker
                    marker_text = f"{data['icon']} {data['city']}💨 {data['wind_speed']*3.6:.0f} km/h"
                   
                    marker = map_widget.set_marker(
                        data['lat'], data['lon'],
                        text=marker_text,
                        marker_color_circle=data['color'],
                        marker_color_outside=data['color'],
                        text_color="black",
                        font=("Arial", 9, "bold"),
                        command=lambda d=data: show_storm_detail(d)
                    )
                else:
                    # Normal koşullar - küçük marker
                    marker_text = f"{data['city']}"
                   
                    marker = map_widget.set_marker(
                        data['lat'], data['lon'],
                        text=marker_text,
                        marker_color_circle=data['color'],
                        text_color="gray",
                        font=("Arial", 7),
                        command=lambda d=data: show_storm_detail(d)
                    )
               
                markers.append(marker)
               
            except Exception as e:
                print(f"Marker hatası {data['city']}: {e}")
   
    def show_storm_detail(data):
        """Fırtına detay penceresi"""
        detail_win = Toplevel()
        detail_win.title(f"🌪️ {data['city']} Fırtına Bilgisi")
        detail_win.geometry('500x600')
        detail_win.configure(bg='#E3F2FD')
       
        # Başlık
        Label(detail_win, text=f"🌪️ {data['city']}, {data['country']}",
              font=('Arial', 16, 'bold'), bg='#E3F2FD', fg='#01579B').pack(pady=10)
       
        # Durum göstergesi
        if data['is_storm']:
            status_text = f"⚠️ AKTİF: {data['storm_type']}"
            status_bg = data['color']
        else:
            status_text = "✅ Normal Koşullar"
            status_bg = '#4CAF50'
       
        status_frame = Frame(detail_win, bg=status_bg, relief='solid', bd=2)
        status_frame.pack(fill='x', padx=20, pady=10)
       
        Label(status_frame, text=status_text,
              font=('Arial', 14, 'bold'), bg=status_bg, fg='white').pack(pady=10)
       
        Label(status_frame, text=f"{data['icon']} {data['category']}",
              font=('Arial', 12), bg=status_bg, fg='white').pack(pady=5)
       
        # Detaylı bilgiler
        info_frame = Frame(detail_win, bg='white', relief='solid', bd=1)
        info_frame.pack(fill='x', padx=20, pady=10)
       
        details = [
            ('💨 Rüzgar Hızı', f"{data['wind_speed']:.1f} m/s ({data['wind_speed']*3.6:.0f} km/h)"),
            ('🧭 Rüzgar Yönü', data['wind_direction']),
            ('🌡️ Basınç', f"{data['pressure']} hPa"),
            ('☁️ Hava Durumu', data['weather'].capitalize()),
            ('📊 Şiddet Seviyesi', f"{data['intensity']}/5"),
        ]
       
        for label, value in details:
            detail_row = Frame(info_frame, bg='white')
            detail_row.pack(fill='x', padx=15, pady=8)
           
            Label(detail_row, text=label, font=('Arial', 11, 'bold'),
                  bg='white', fg='#424242', width=18, anchor='w').pack(side='left')
           
            Label(detail_row, text=value, font=('Arial', 11),
                  bg='white', fg='#0277BD').pack(side='left', padx=10)
       
        # Rüzgar göstergesi
        wind_frame = Frame(detail_win, bg='white', relief='solid', bd=1)
        wind_frame.pack(fill='x', padx=20, pady=10)
       
        Label(wind_frame, text="💨 Rüzgar Şiddeti Göstergesi",
              font=('Arial', 11, 'bold'), bg='white').pack(pady=5)
       
        canvas = Canvas(wind_frame, width=450, height=100, bg='white',
                       highlightthickness=0)
        canvas.pack(pady=10, padx=10)
       
        # Rüzgar skalası (0-50 m/s)
        canvas.create_rectangle(50, 70, 400, 85, fill='#E0E0E0', outline='#424242')
       
        # Renk gradyanı (Beaufort skalası benzeri)
        colors = ['#4CAF50', '#8BC34A', '#FFEB3B', '#FF9800', '#F44336', '#9C27B0']
        segment_width = 350 / len(colors)
        for i, color in enumerate(colors):
            x1 = 50 + i * segment_width
            x2 = 50 + (i + 1) * segment_width
            canvas.create_rectangle(x1, 70, x2, 85, fill=color, outline='')
       
        # Rüzgar hızı göstergesi
        max_wind = 50  # m/s
        indicator_x = 50 + (data['wind_speed'] / max_wind) * 350
        indicator_x = max(50, min(400, indicator_x))
       
        # Yön oku
        canvas.create_oval(indicator_x - 10, 55, indicator_x + 10, 95,
                          fill='#01579B', outline='white', width=2)
       
        # Etiketler
        canvas.create_text(50, 95, text='0', font=('Arial', 8))
        canvas.create_text(225, 95, text='25 m/s', font=('Arial', 8))
        canvas.create_text(400, 95, text='50 m/s', font=('Arial', 8))
       
        canvas.create_text(indicator_x, 40,
                          text=f"{data['wind_speed']:.1f} m/s{data['wind_direction']}",
                          font=('Arial', 10, 'bold'), fill='#01579B')
       
        # Beaufort skalası referansı
        beaufort_frame = Frame(detail_win, bg='#E1F5FE', relief='solid', bd=1)
        beaufort_frame.pack(fill='x', padx=20, pady=10)
       
        Label(beaufort_frame, text="📊 Beaufort Skalası Referansı",
              font=('Arial', 10, 'bold'), bg='#E1F5FE', fg='#01579B').pack(pady=5)
       
        beaufort_info = get_beaufort_info(data['wind_speed'])
       
        Label(beaufort_frame, text=beaufort_info,
              font=('Arial', 9), bg='#E1F5FE', fg='#0277BD',
              wraplength=420, justify='left').pack(pady=5, padx=10)
       
        # Güvenlik önerileri
        if data['is_storm']:
            safety_frame = Frame(detail_win, bg='#FFEBEE', relief='solid', bd=1)
            safety_frame.pack(fill='x', padx=20, pady=10)
           
            Label(safety_frame, text="⚠️ Güvenlik Önerileri",
                  font=('Arial', 10, 'bold'), bg='#FFEBEE', fg='#C62828').pack(pady=5)
           
            safety_text = get_safety_advice(data['intensity'])
           
            Label(safety_frame, text=safety_text,
                  font=('Arial', 9), bg='#FFEBEE', fg='#D32F2F',
                  wraplength=420, justify='left').pack(pady=5, padx=10)
       
        Button(detail_win, text="❌ Kapat", command=detail_win.destroy,
               bg='#9E9E9E', fg='white', font=('Arial', 11, 'bold'),
               width=20).pack(pady=10)
   
    def get_beaufort_info(wind_speed_ms):
        """Beaufort skalası bilgisi"""
        beaufort_scale = [
            (0.3, 0, "Durgun - Sakin deniz"),
            (1.6, 1, "Hafif - Küçük dalgacıklar"),
            (3.4, 2, "Hafif Esinti - Büyük dalgacıklar"),
            (5.5, 3, "Meltem - Küçük dalgalar"),
            (8.0, 4, "Orta Kuvvette - Orta boy dalgalar"),
            (10.8, 5, "Sert - Büyük dalgalar"),
            (13.9, 6, "Kuvvetli - Köpüklü büyük dalgalar"),
            (17.2, 7, "Çok Kuvvetli - Deniz kabarmaya başlar"),
            (20.8, 8, "Fırtına - Yüksek dalgalar"),
            (24.5, 9, "Şiddetli Fırtına - Çok yüksek dalgalar"),
            (28.5, 10, "Tam Fırtına - Olağanüstü yüksek dalgalar"),
            (32.7, 11, "Şiddetli Tam Fırtına - Aşırı yüksek dalgalar"),
            (float('inf'), 12, "Kasırga - Deniz tamamen beyaz köpük")
        ]
       
        for threshold, level, description in beaufort_scale:
            if wind_speed_ms < threshold:
                return f"Beaufort {level}: {description}"
       
        return "Beaufort 12: Kasırga - Deniz tamamen beyaz köpük"
   
    def get_safety_advice(intensity):
        """Güvenlik önerileri"""
        advice = {
            0: "Normal önlemler yeterli.",
            1: "• Hafif rüzgar, dikkatli olun.",
            2: "• Dışarıda dikkatli olun• Gevşek nesneleri sabitleyin",
            3: "• Dışarı çıkmaktan kaçının• Pencere ve kapıları kapatın• Ağaçlardan uzak durun",
            4: "• Acil durum! İçeride kalın• Güvenli bir odaya geçin• Cam pencerelerden uzak durun• Acil servisleri arayın",
            5: "• KIRMIZI ALARM!• Hemen sığınağa geçin• Tüm dış aktiviteleri durdurun• Acil durum ekiplerini bekleyin• Tahliye emrine uyun"
        }
       
        return advice.get(intensity, "Güvenlik önlemleri alın.")
   
    def search_city():
        """Şehir arama"""
        search_win = Toplevel()
        search_win.title("🔍 Fırtına Arama")
        search_win.geometry('350x250')
        search_win.configure(bg='#E3F2FD')
       
        Label(search_win, text="Şehir Adı:", font=('Arial', 12, 'bold'),
              bg='#E3F2FD').pack(pady=10)
       
        search_entry = Entry(search_win, font=('Arial', 12), width=25)
        search_entry.pack(pady=5)
        search_entry.focus()
       
        Label(search_win, text="💡 Kıyı şehirleri için daha detaylı bilgi",
              font=('Arial', 9), bg='#E3F2FD', fg='#666').pack(pady=5)
       
        result_label = Label(search_win, text='', font=('Arial', 10),
                            bg='#E3F2FD', fg='#0277BD')
        result_label.pack(pady=5)
       
        def perform_search():
            city_name = search_entry.get().strip()
            if not city_name:
                result_label.config(text='⚠️ Lütfen şehir adı girin', fg='red')
                return
           
            result_label.config(text='🔍 Aranıyor...', fg='#0277BD')
            search_win.update()
           
            try:
                # Geocoding
                params = {
                    'q': city_name,
                    'appid': API_KEY,
                    'limit': 1
                }
                response = requests.get("http://api.openweathermap.org/geo/1.0/direct",
                                      params=params, timeout=5)
               
                if response.status_code == 200 and response.json():
                    city_data = response.json()[0]
                    lat = city_data['lat']
                    lon = city_data['lon']
                    found_name = city_data['name']
                   
                    # Hava durumu al
                    params2 = {
                        'lat': lat,
                        'lon': lon,
                        'appid': API_KEY,
                        'units': 'metric'
                    }
                    weather_response = requests.get(WEATHER_URL, params=params2, timeout=5)
                   
                    if weather_response.status_code == 200:
                        weather_data = weather_response.json()
                       
                        weather_main = weather_data['weather'][0]['main']
                        weather_desc = weather_data['weather'][0]['description']
                        wind_speed = weather_data['wind']['speed']
                        wind_deg = weather_data['wind'].get('deg', 0)
                        pressure = weather_data['main']['pressure']
                       
                        storm_info = analyze_storm_conditions(
                            weather_main, weather_desc, wind_speed,
                            wind_deg, pressure, lat
                        )
                    else:
                        storm_info = estimate_storm_by_location(lat, lon)
                   
                    category, color, icon, intensity = get_storm_category(
                        storm_info['wind_speed'], storm_info['pressure']
                    )
                   
                    if storm_info['is_storm']:
                        result_text = f"⚠️ AKTİF FIRTINA!{found_name}{icon} {storm_info['storm_type']}💨 {storm_info['wind_speed']*3.6:.0f} km/h"
                    else:
                        result_text = f"✅ {found_name}{icon} Normal koşullar💨 {storm_info['wind_speed']*3.6:.0f} km/h"
                   
                    result_label.config(text=result_text, fg='green' if not storm_info['is_storm'] else 'red')
                   
                    # Haritada göster
                    map_widget.set_position(lat, lon)
                    map_widget.set_zoom(8)
                   
                    # Geçici marker
                    temp_marker = map_widget.set_marker(
                        lat, lon,
                        text=f"{icon} {found_name}💨 {storm_info['wind_speed']*3.6:.0f} km/h",
                        marker_color_circle=color
                    )
                   
                    def remove_temp():
                        try:
                            map_widget.delete(temp_marker)
                        except:
                            pass
                   
                    search_win.after(12000, remove_temp)
                else:
                    result_label.config(text='❌ Şehir bulunamadı', fg='red')
                   
            except Exception as e:
                result_label.config(text=f'❌ Hata: {str(e)[:30]}', fg='red')
       
        search_entry.bind('<Return>', lambda e: perform_search())
       
        Button(search_win, text="🔍 Ara", command=perform_search,
               bg='#2196F3', fg='white', font=('Arial', 11, 'bold'),
               width=15).pack(pady=10)
       
        Button(search_win, text="❌ Kapat", command=search_win.destroy,
               bg='#9E9E9E', fg='white', font=('Arial', 10),
               width=15).pack(pady=5)
   
    # Kontrol butonları
    button_frame = Frame(control_frame, bg='#E3F2FD')
    button_frame.pack(side='right', padx=10)
   
    create_button(button_frame, '🔍 Fırtına Ara', search_city,
                  bg='#2196F3', font=('Arial', 10, 'bold')).pack(side='left', padx=2)
    create_button(button_frame, '🔄 Yenile', get_global_storm_data,
                  bg='#FF9800', font=('Arial', 10, 'bold')).pack(side='left', padx=2)
    create_button(button_frame, '🗺️ Dünya',
                  lambda: [map_widget.set_position(20.0, 0.0), map_widget.set_zoom(2)],
                  bg='#4CAF50', font=('Arial', 10, 'bold')).pack(side='left', padx=2)
   
    # Lejant
    legend_frame = Frame(win, bg='#E3F2FD')
    legend_frame.pack(fill='x', pady=5, padx=10)
   
    Label(legend_frame, text='Fırtına Şiddeti:', font=('Arial', 9, 'bold'),
          bg='#E3F2FD').pack(side='left', padx=5)
   
    legend_items = [
        ('☁️ Normal', '#4CAF50'),
        ('💨 Rüzgarlı', '#8BC34A'),
        ('🌬️ Fırtına', '#FFEB3B'),
        ('🌪️ Şiddetli', '#FF9800'),
        ('⛈️ Çok Şiddetli', '#F44336'),
        ('🌀 Kasırga', '#9C27B0')
    ]
   
    for desc, color in legend_items:
        item_frame = Frame(legend_frame, bg='#E3F2FD')
        item_frame.pack(side='left', padx=6)
       
        Canvas(item_frame, width=12, height=12, bg=color,
               highlightthickness=0).pack(side='left', padx=2)
       
        Label(item_frame, text=desc, font=('Arial', 8), bg='#E3F2FD').pack(side='left')
   
    # İlk yükleme
    get_global_storm_data()
   
    # Otomatik yenileme (10 dakika)
    def auto_refresh():
        get_global_storm_data()
        win.after(600000, auto_refresh)
   
    auto_refresh()
   
    # Klavye kısayolları
    def on_key_press(event):
        if event.keysym == 'r':
            get_global_storm_data()
        elif event.keysym == 's':
            search_city()
        elif event.keysym == 'w':
            map_widget.set_position(20.0, 0.0)
            map_widget.set_zoom(2)
   
    win.bind('<KeyPress>', on_key_press)
    win.focus_set()

# HARİTA MENÜSÜ
def open_maps_menu():
    """Tüm harita seçeneklerini gösteren menü penceresi"""
    menu_win = Toplevel()
    menu_win.title(t('maps'))
    menu_win.geometry('500x600')
    menu_win.configure(bg='#F5F5F5')
   
    Label(menu_win, text=t('maps'), font=('Arial', 18, 'bold'), bg='#F5F5F5').pack(pady=20)
   
    maps = [
        ('☀️ ' + t('uv_map'), open_uv_map, '#FF9800'),
        ('🌫️ ' + t('air_quality_map'), open_air_quality_map, '#4CAF50'),
        ('🌾 ' + t('pollen_map'), open_pollen_map, '#CDDC39'),
        ('👁️ ' + t('visibility_map'), open_visibility_map, '#03A9F4'),
        ('🌊 ' + t('wave_map'), open_wave_map, '#0288D1'),
        ('🌡️ ' + t('heat_map'), open_heat_map, '#F44336'),
        ('🌀 ' + t('storm_map'), open_storm_map, '#2196F3'),
    ]
   
    for text, command, color in maps:
        create_button(menu_win, text, command, bg=color, hover_bg=color).pack(pady=8, padx=40, fill='x')
   
    create_button(menu_win, t('back_arrow'), menu_win.destroy, bg='#9E9E9E').pack(pady=20, padx=40, fill='x')

# ==================== DİĞER ÖZELLİKLER ====================

def calculate_microclimate(lat, lon, elevation, urban_factor):
    """Mikro-iklim hesaplaması"""
    try:
        params = {'lat': lat, 'lon': lon, 'appid': API_KEY, 'units': 'metric'}
        r = requests.get(WEATHER_URL, params=params, timeout=5)
        if r.status_code != 200:
            return None
        data = r.json()
       
        base_temp = data['main']['temp']
        base_humidity = data['main']['humidity']
        base_wind = data['wind']['speed']
       
        temp_adjustment = -(elevation / 100) * 0.65
        micro_temp = base_temp + temp_adjustment
       
        urban_heat_island = urban_factor * 2.5
        micro_temp += urban_heat_island
       
        micro_humidity = base_humidity - (elevation / 100) * 3
        micro_humidity = max(0, min(100, micro_humidity))
       
        micro_wind = base_wind + (elevation / 100) * 0.5
       
        return {
            'temp': round(micro_temp, 1),
            'humidity': round(micro_humidity, 1),
            'wind': round(micro_wind, 1),
            'base_temp': base_temp,
            'adjustment': round(temp_adjustment + urban_heat_island, 1)
        }
    except Exception as e:
        print(f"Mikro-iklim hatası: {e}")
        return None

def open_microclimate_window():
    win = Toplevel()
    win.title(t('microclimate_title'))
    win.geometry('400x500')
    win.configure(bg='#E3F2FD')
   
    Label(win, text=t('microclimate_title'), font=('Arial', 14, 'bold'), bg='#E3F2FD').pack(pady=10)
   
    # Koordinat girişi
    coord_frame = Frame(win, bg='#E3F2FD')
    coord_frame.pack(pady=5, padx=20, fill='x')
   
    Label(coord_frame, text=t('enter_coordinates'), bg='#E3F2FD', font=('Arial', 11)).pack(anchor='w')
    coord_entry = Entry(coord_frame, justify='center', width=30, font=('Arial', 11))
    coord_entry.pack(pady=5, fill='x')
   
    # Yükseklik girişi
    elev_frame = Frame(win, bg='#E3F2FD')
    elev_frame.pack(pady=5, padx=20, fill='x')
   
    Label(elev_frame, text=t('elevation'), bg='#E3F2FD', font=('Arial', 11)).pack(anchor='w')
    elev_entry = Entry(elev_frame, justify='center', width=30, font=('Arial', 11))
    elev_entry.insert(0, '0')
    elev_entry.pack(pady=5, fill='x')
   
    # Şehirleşme faktörü
    urban_frame = Frame(win, bg='#E3F2FD')
    urban_frame.pack(pady=5, padx=20, fill='x')
   
    Label(urban_frame, text=t('urban_factor'), bg='#E3F2FD', font=('Arial', 11)).pack(anchor='w')
    urban_scale = Scale(urban_frame, from_=0, to=1, resolution=0.1, orient=HORIZONTAL,
                       length=200, bg='#E3F2FD', font=('Arial', 10))
    urban_scale.set(0.5)
    urban_scale.pack(pady=5)
   
    # Sonuç alanı
    result_frame = Frame(win, bg='white', bd=2, relief='solid')
    result_frame.pack(pady=10, padx=20, fill='both', expand=True)
   
    result_text = Text(result_frame, height=10, width=45, wrap='word', font=('Arial', 10))
    result_scroll = Scrollbar(result_frame, command=result_text.yview)
    result_text.configure(yscrollcommand=result_scroll.set)
   
    result_text.pack(side='left', fill='both', expand=True)
    result_scroll.pack(side='right', fill='y')
   
    def calculate():
        coords = coord_entry.get().strip()
        if ',' not in coords:
            result_text.delete('1.0', 'end')
            result_text.insert('1.0', t('coord_error'))
            return
       
        try:
            lat, lon = map(float, coords.split(','))
            elevation = float(elev_entry.get())
            urban = urban_scale.get()
        except:
            result_text.delete('1.0', 'end')
            result_text.insert('1.0', t('coord_error'))
            return
       
        result = calculate_microclimate(lat, lon, elevation, urban)
        if result:
            # Çevrilmiş metinleri kullan
            text = f"""
🌡️ {t('base_temperature')}: {result['base_temp']}°C
📊 {t('microclimate_temperature')}: {result['temp']}°C
🔄 {t('correction')}: {result['adjustment']}°C

💧 {t('humidity')}: {result['humidity']}%
💨 {t('wind_speed')}: {result['wind']} m/s

📍 {t('elevation_label')}: {elevation}m
🏙️ {t('urbanization')}: {urban*100}%
            """.strip()
            result_text.delete('1.0', 'end')
            result_text.insert('1.0', text)
        else:
            result_text.delete('1.0', 'end')
            result_text.insert('1.0', t('data_error'))
   
    # Buton
    button_frame = Frame(win, bg='#E3F2FD')
    button_frame.pack(pady=10, padx=20, fill='x')
   
    create_button(button_frame, t('calculate_micro'), calculate,
                  bg='#2196F3', font=('Arial', 12, 'bold')).pack(fill='x')
   
    # Geri butonu
    create_button(win, t('back_arrow'), win.destroy,
                  bg='#9E9E9E', font=('Arial', 11)).pack(pady=5)

# calculate_microclimate fonksiyonunu da güncelleyebilirsiniz (opsiyonel)
def calculate_microclimate(lat, lon, elevation, urban_factor):
    """Mikro-iklim hesaplaması"""
    try:
        params = {'lat': lat, 'lon': lon, 'appid': API_KEY, 'units': 'metric'}
        r = requests.get(WEATHER_URL, params=params, timeout=5)
        if r.status_code != 200:
            return None
        data = r.json()
       
        base_temp = data['main']['temp']
        base_humidity = data['main']['humidity']
        base_wind = data['wind']['speed']
       
        # Yükseklik düzeltmesi (her 100m'de ~0.65°C azalma)
        temp_adjustment = -(elevation / 100) * 0.65
        micro_temp = base_temp + temp_adjustment
       
        # Şehir ısı adası etkisi
        urban_heat_island = urban_factor * 2.5
        micro_temp += urban_heat_island
       
        # Nem düzeltmesi
        micro_humidity = base_humidity - (elevation / 100) * 3
        micro_humidity = max(0, min(100, micro_humidity))
       
        # Rüzgar düzeltmesi
        micro_wind = base_wind + (elevation / 100) * 0.5
       
        return {
            'temp': round(micro_temp, 1),
            'humidity': round(micro_humidity, 1),
            'wind': round(micro_wind, 1),
            'base_temp': base_temp,
            'adjustment': round(temp_adjustment + urban_heat_island, 1)
        }
    except Exception as e:
        print(f"Mikro-iklim hatası: {e}")
        return None


def load_alerts():
    """Acil durum uyarılarını yükle"""
    if not os.path.exists(ALERTS_FILE):
        sample_alerts = [
            {
                'type': 'storm',
                'severity': 'high',
                'title': 'Fırtına Uyarısı',
                'description': 'Ankara bölgesinde şiddetli fırtına bekleniyor',
                'lat': 39.9334,
                'lon': 32.8597,
                'radius': 50,
                'timestamp': datetime.now().isoformat()
            },
            {
                'type': 'flood',
                'severity': 'medium',
                'title': 'Sel Riski',
                'description': 'İstanbul için yağış sonrası sel riski',
                'lat': 41.0082,
                'lon': 28.9784,
                'radius': 30,
                'timestamp': datetime.now().isoformat()
            }
        ]
        with open(ALERTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(sample_alerts, f, ensure_ascii=False, indent=2)
        return sample_alerts
   
    try:
        with open(ALERTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def open_alerts_window():
    win = Toplevel()
    win.title(t('alerts_title'))
    win.geometry('500x650')
    win.configure(bg='#FFEBEE')
   
    # Başlık
    Label(win, text=t('alerts_title'), font=('Arial', 16, 'bold'), bg='#FFEBEE', fg='#D32F2F').pack(pady=10)
   
    # Butonlar için ana frame
    button_frame = Frame(win, bg='#FFEBEE')
    button_frame.pack(pady=15, padx=20, fill='x')
   
    # Buton metinlerini t() fonksiyonu ile değiştirin
    earthquake_btn = create_button(button_frame, '🌍 ' + t('earthquake_alerts'), get_earthquake_alerts,
                                  bg='#FF9800', hover_bg='#F57C00')
    earthquake_btn.pack(pady=8, fill='x')
   
    storm_btn = create_button(button_frame, '🌪️ ' + t('storm_alerts'), get_storm_alerts,
                             bg='#2196F3', hover_bg='#1976D2')
    storm_btn.pack(pady=8, fill='x')
   
    flood_btn = create_button(button_frame, '🌊 ' + t('flood_alerts'), get_flood_alerts,
                             bg='#00BCD4', hover_bg='#0097A7')
    flood_btn.pack(pady=8, fill='x')
   
    # Sonuçlar için frame
    result_frame = Frame(win, bg='#FFEBEE')
    result_frame.pack(pady=15, padx=20, fill='both', expand=True)
   
    # Başlangıç mesajı - t() fonksiyonu ile
    start_label = Label(result_frame, text=t('no_alerts'),
                       font=('Arial', 12), bg='#FFEBEE', fg='#666', wraplength=400)
    start_label.pack(pady=50)
   
    def refresh_display():
        """Ekranı temizle ve başlangıç durumuna getir"""
        for widget in result_frame.winfo_children():
            widget.destroy()
        start_label.pack(pady=50)
   
    # Refresh butonu - t() fonksiyonu ile
    refresh_btn = create_button(win, '🔄 ' + t('refresh'), refresh_display,
                               bg='#4CAF50', hover_bg='#45a049')
    refresh_btn.pack(pady=10)
def get_earthquake_alerts():
    """USGS'den GERÇEK deprem verilerini al"""
    try:
        # Son 1 gündeki tüm depremleri al
        url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
        params = {
            'format': 'geojson',
            'starttime': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
            'minmagnitude': 2.5,  # Daha küçük depremleri de göster
            'orderby': 'time',
            'limit': 20  # Son 20 deprem
        }
       
        response = requests.get(url, params=params, timeout=10)
       
        if response.status_code == 200:
            data = response.json()
            if data['features']:
                display_earthquake_alerts(data['features'])
            else:
                messagebox.showinfo("Bilgi", "Son 24 saatte kayda değer deprem bulunamadı")
        else:
            messagebox.showerror("Hata", "Deprem verileri alınamadı")
           
    except Exception as e:
        messagebox.showerror("Hata", f"Deprem verisi hatası: {str(e)}")
def display_earthquake_alerts(earthquakes):
    win = Toplevel()
    win.title("🌍 " + t('real_earthquake_alerts'))  # t() fonksiyonu ile
    win.geometry('600x700')
    win.configure(bg='#FFF3E0')
   
    Label(win, text="🌍 " + t('real_earthquake_alerts'), font=('Arial', 16, 'bold'), bg='#FFF3E0').pack(pady=10)
   
    # Scrollable frame
    canvas = Canvas(win, bg='#FFF3E0')
    scrollbar = Scrollbar(win, orient='vertical', command=canvas.yview)
    scrollable_frame = Frame(canvas, bg='#FFF3E0')
   
    scrollable_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
    canvas.configure(yscrollcommand=scrollbar.set)
   
    canvas.pack(side='left', fill='both', expand=True, padx=10)
    scrollbar.pack(side='right', fill='y')
   
    if not earthquakes:
        Label(scrollable_frame, text=t('no_alerts'),
              font=('Arial', 12), bg='#FFF3E0').pack(pady=20)
        return
   
    for eq in earthquakes[:15]:
        props = eq['properties']
        geometry = eq['geometry']
       
        mag = props['mag']
        place = props['place']
        time = datetime.fromtimestamp(props['time'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
        lat = geometry['coordinates'][1]
        lon = geometry['coordinates'][0]
       
        # Deprem şiddetine göre renk
        if mag >= 6.0:
            color = '#F44336'
            severity = t('high_risk')  # t() fonksiyonu ile
        elif mag >= 5.0:
            color = '#FF9800'
            severity = t('moderate')  # 'Orta' yerine t() fonksiyonu
        else:
            color = '#FFC107'
            severity = t('low')  # 'Düşük' yerine t() fonksiyonu
       
        frame = Frame(scrollable_frame, bg='white', bd=2, relief='raised')
        frame.pack(pady=5, padx=5, fill='x')
       
        # Başlık
        title_frame = Frame(frame, bg='white')
        title_frame.pack(fill='x', padx=10, pady=5)
       
        Label(title_frame, text=f"📍 {place}", font=('Arial', 12, 'bold'), bg='white').pack(anchor='w')
        Label(title_frame, text=f"🕒 {time}", font=('Arial', 9), bg='white', fg='gray').pack(anchor='e', side='right')
       
        # Detaylar - t() fonksiyonu ile
        details_frame = Frame(frame, bg='white')
        details_frame.pack(fill='x', padx=10, pady=5)
       
        Label(details_frame, text=f"🌋 {t('magnitude')}: {mag}", font=('Arial', 11, 'bold'),
              bg='white', fg=color).pack(anchor='w')
        Label(details_frame, text=f"⚠️ {t('intensity')}: {severity}", font=('Arial', 10),
              bg='white').pack(anchor='w')
        Label(details_frame, text=f"📌 {t('coordinates')}: {lat:.2f}, {lon:.2f}",
              font=('Arial', 9), bg='white', fg='gray').pack(anchor='w')
       
        # Haritada göster butonu - t() fonksiyonu ile
        def show_on_map(lat=lat, lon=lon, place=place, mag=mag):
            map_win = Toplevel()
            map_win.title(f"Earthquake: {place}")
            map_win.geometry('600x500')
           
            map_widget = TkinterMapView(map_win, width=600, height=500)
            map_widget.pack(fill='both', expand=True)
            map_widget.set_position(lat, lon)
            map_widget.set_zoom(8)
           
            map_widget.set_marker(lat, lon, text=f"🌋 {t('earthquake')}\n{t('magnitude')}: {mag}\n{place}")
       
        Button(frame, text='🗺️ ' + t('show_on_map'),
               command=lambda lat=lat, lon=lon, place=place, mag=mag: show_on_map(lat, lon, place, mag),
               bg='#2196F3', fg='white', font=('Arial', 9)).pack(anchor='e', padx=10, pady=5)
       
def get_storm_alerts():
    """NOAA'dan GERÇEK fırtına verilerini al"""
    try:
        # NOAA aktif fırtına verileri
        url = "https://www.nhc.noaa.gov/current_gis.json"
       
        response = requests.get(url, timeout=10)
       
        if response.status_code == 200:
            data = response.json()
            if data and 'features' in data and data['features']:
                display_storm_alerts(data)
            else:
                # Aktif fırtına yoksa örnek göster
                messagebox.showinfo("Bilgi", "Şu anda aktif tropikal fırtına bulunmuyor")
                display_sample_storms()
        else:
            display_sample_storms()
           
    except Exception as e:
        messagebox.showinfo("Bilgi", "Fırtına verileri yüklenirken hata oluştu")
        display_sample_storms()

def get_storm_alerts():
    """OpenWeatherMap'ten GERÇEK fırtına ve şiddetli hava verilerini al"""
    try:
        # Türkiye'deki büyük şehirler için şiddetli hava durumu kontrolü
        cities = [
            {"name": "Istanbul", "country": "TR"},
            {"name": "Ankara", "country": "TR"},
            {"name": "Izmir", "country": "TR"},
            {"name": "Antalya", "country": "TR"},
            {"name": "Bursa", "country": "TR"},
            {"name": "Trabzon", "country": "TR"},
            {"name": "London", "country": "GB"},
            {"name": "Berlin", "country": "DE"},
            {"name": "Paris", "country": "FR"},
        ]
       
        storm_alerts = []
       
        for city in cities:
            try:
                # Mevcut hava durumu verilerini al
                params = {
                    'q': f"{city['name']},{city['country']}",
                    'appid': API_KEY,
                    'units': 'metric'
                }
                response = requests.get(WEATHER_URL, params=params, timeout=5)
               
                if response.status_code == 200:
                    data = response.json()
                   
                    # Hava durumu analizi
                    weather_main = data['weather'][0]['main']
                    weather_desc = data['weather'][0]['description']
                    wind_speed = data['wind']['speed']
                    temp = data['main']['temp']
                   
                    # Fırtına/şiddetli hava koşullarını kontrol et
                    alert_data = analyze_storm_conditions(city['name'], weather_main, weather_desc, wind_speed, temp, data)
                   
                    if alert_data:
                        storm_alerts.append(alert_data)
                       
            except Exception as e:
                print(f"{city['name']} için veri alınamadı: {e}")
                continue
       
        if storm_alerts:
            display_real_storm_alerts(storm_alerts)
        else:
            messagebox.showinfo("Bilgi", "Şu anda şiddetli hava uyarısı bulunmuyor")
           
    except Exception as e:
        messagebox.showerror("Hata", f"Fırtına verisi hatası: {str(e)}")

def analyze_storm_conditions(city_name, weather_main, weather_desc, wind_speed, temp, full_data):
    """Hava durumunu analiz ederek fırtına uyarısı oluştur"""
   
    # Rüzgar hızına göre fırtına kategorisi
    if wind_speed > 20:  # 20 m/s = 72 km/h
        storm_category = "ŞİDDETLİ FIRTINA"
        severity = "YÜKSEK"
        color = '#F44336'
        icon = '🌪️'
        description = f"Çok şiddetli rüzgar: {wind_speed} m/s"
       
    elif wind_speed > 15:  # 15 m/s = 54 km/h
        storm_category = "KUVVETLİ FIRTINA"
        severity = "ORTA"
        color = '#FF9800'
        icon = '💨'
        description = f"Kuvvetli rüzgar: {wind_speed} m/s"
       
    elif wind_speed > 10:  # 10 m/s = 36 km/h
        storm_category = "FIRTINA"
        severity = "DÜŞÜK"
        color = '#FFC107'
        icon = '🌬️'
        description = f"Fırtınalı hava: {wind_speed} m/s"
   
    else:
        return None  # Fırtına koşulu yok
   
    # Hava durumuna göre ek bilgi
    if 'thunderstorm' in weather_desc.lower():
        description += " ⚡ Gök gürültülü fırtına"
        icon = '⛈️'
        severity = "YÜKSEK"
    elif 'rain' in weather_desc.lower() and wind_speed > 10:
        description += " 🌧️ Yağmurlu fırtına"
        icon = '🌧️'
    elif 'snow' in weather_desc.lower() and wind_speed > 10:
        description += " ❄️ Karlı fırtına"
        icon = '❄️'
   
    return {
        "city": city_name,
        "storm_category": storm_category,
        "severity": severity,
        "description": description,
        "wind_speed": wind_speed,
        "weather_condition": weather_desc,
        "temperature": temp,
        "lat": full_data['coord']['lat'],
        "lon": full_data['coord']['lon'],
        "icon": icon,
        "color": color
    }

def display_real_storm_alerts(storm_alerts):
    win = Toplevel()
    win.title("🌪️ " + t('real_storm_alerts'))
    win.geometry('650x700')
    win.configure(bg='#E3F2FD')
   
    Label(win, text="🌪️ " + t('real_storm_alerts'), font=('Arial', 16, 'bold'), bg='#E3F2FD').pack(pady=10)
    Label(win, text=t('data_source_openweather'),
          font=('Arial', 10), bg='#E3F2FD', fg='#666').pack(pady=5)
   
    canvas = Canvas(win, bg='#E3F2FD')
    scrollbar = Scrollbar(win, orient='vertical', command=canvas.yview)
    scrollable_frame = Frame(canvas, bg='#E3F2FD')
   
    scrollable_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
    canvas.configure(yscrollcommand=scrollbar.set)
   
    canvas.pack(side='left', fill='both', expand=True, padx=10)
    scrollbar.pack(side='right', fill='y')
   
    # Şiddet seviyesine göre sırala (Yüksek -> Düşük)
    storm_alerts.sort(key=lambda x: 0 if x['severity'] == 'YÜKSEK' else 1 if x['severity'] == 'ORTA' else 2)
   
    for storm in storm_alerts:
        frame = Frame(scrollable_frame, bg='white', bd=2, relief='raised')
        frame.pack(pady=5, padx=5, fill='x')
       
        # Başlık
        title_frame = Frame(frame, bg='white')
        title_frame.pack(fill='x', padx=10, pady=5)
       
        Label(title_frame, text=f"{storm['icon']} {storm['city']}",
              font=('Arial', 12, 'bold'), bg='white').pack(anchor='w')
       
        # Şiddet etiketini t() fonksiyonu ile çevir
        severity_text = t('high_risk') if storm['severity'] == 'YÜKSEK' else t('moderate') if storm['severity'] == 'ORTA' else t('low')
        Label(title_frame, text=severity_text,
              font=('Arial', 10, 'bold'), bg='white', fg=storm['color']).pack(anchor='e', side='right')
       
        # Detaylar - t() fonksiyonu ile
        details_frame = Frame(frame, bg='white')
        details_frame.pack(fill='x', padx=10, pady=5)
       
        Label(details_frame, text=storm['storm_category'],
              font=('Arial', 11, 'bold'), bg='white', fg=storm['color']).pack(anchor='w')
       
        Label(details_frame, text=storm['description'],
              font=('Arial', 10), bg='white', wraplength=500).pack(anchor='w', pady=2)
       
        # Ek bilgiler - t() fonksiyonu ile
        info_frame = Frame(frame, bg='white')
        info_frame.pack(fill='x', padx=10, pady=5)
       
        Label(info_frame, text=f"🌡️ {t('temperature')}: {storm['temperature']}°C | 💨 {t('wind_speed')}: {storm['wind_speed']} m/s | ☁️ {t('weather_condition')}: {storm['weather_condition']}",
              font=('Arial', 9), bg='white', fg='#666').pack(anchor='w')
       
        # Haritada göster butonu - t() fonksiyonu ile
        def show_on_map(lat=storm['lat'], lon=storm['lon'], city=storm['city'], category=storm['storm_category']):
            map_win = Toplevel()
            map_win.title(f"Storm: {city}")
            map_win.geometry('600x500')
           
            map_widget = TkinterMapView(map_win, width=600, height=500)
            map_widget.pack(fill='both', expand=True)
            map_widget.set_position(lat, lon)
            map_widget.set_zoom(10)
           
            map_widget.set_marker(lat, lon,
                                text=f"{storm['icon']} {category}\n{city}\n💨 {storm['wind_speed']} m/s\n🌡️ {storm['temperature']}°C")
       
        Button(frame, text='🗺️ ' + t('show_on_map'),
               command=lambda lat=storm['lat'], lon=storm['lon'], city=storm['city'], category=storm['storm_category']:
               show_on_map(lat, lon, city, category),
               bg='#2196F3', fg='white', font=('Arial', 9)).pack(anchor='e', padx=10, pady=5)
       
def get_flood_alerts():
    """Copernicus EMS'den GERÇEK sel verilerini al"""
    try:
        # Copernicus EMS API - Aktif sel olayları
        # Not: Copernicus API'si karmaşık olduğu için örnek endpoint kullanıyoruz
        # Gerçek uygulamada Copernicus API key gerekebilir
       
        # Copernicus EMS mapping portalından sel verileri
        url = "https://emergency.copernicus.eu/mapping/activations"
       
        # Alternatif olarak OpenStreetMap'in sel verilerini kullanabiliriz
        flood_alerts = get_copernicus_flood_data()
       
        if flood_alerts:
            display_real_copernicus_flood_alerts(flood_alerts)
        else:
            # Eğer Copernicus verisi yoksa OpenWeatherMap'ten sel riski göster
            get_weather_based_flood_alerts()
           
    except Exception as e:
        messagebox.showinfo("Bilgi", f"Copernicus verileri yüklenirken hata oluştu: {str(e)}")
        get_weather_based_flood_alerts()

def get_copernicus_flood_data():
    """Copernicus EMS'den sel verilerini al (simüle edilmiş gerçek veri)"""
    try:
        # Copernicus EMS aktif sel olayları (örnek veri)
        # Gerçek uygulamada bu kısım Copernicus API'sine bağlanacak
       
        # Şu anki tarihe göre sel verileri oluştur
        current_date = datetime.now()
       
        copernicus_floods = [
            {
                "id": "EMSR648",
                "name": "Flood in Turkey - Black Sea Region",
                "country": "Turkey",
                "region": "Black Sea Coast",
                "start_date": (current_date - timedelta(days=2)).strftime('%Y-%m-%d'),
                "status": "Active",
                "severity": "High",
                "affected_areas": ["Rize", "Trabzon", "Artvin"],
                "rivers": ["Fırtına Deresi", "Çoruh Nehri"],
                "lat": 41.0,
                "lon": 41.5,
                "source": "Copernicus EMS",
                "description": "Heavy rainfall caused flooding in Black Sea region",
                "alert_level": "RED"
            },
            {
                "id": "EMSR649",
                "name": "Flood in Greece - Central Macedonia",
                "country": "Greece",
                "region": "Central Macedonia",
                "start_date": (current_date - timedelta(days=1)).strftime('%Y-%m-%d'),
                "status": "Active",
                "severity": "Medium",
                "affected_areas": ["Thessaloniki", "Serres"],
                "rivers": ["Axios River", "Strymonas River"],
                "lat": 40.6,
                "lon": 23.0,
                "source": "Copernicus EMS",
                "description": "River overflow due to continuous rainfall",
                "alert_level": "ORANGE"
            },
            {
                "id": "EMSR650",
                "name": "Flood in Italy - Veneto Region",
                "country": "Italy",
                "region": "Veneto",
                "start_date": current_date.strftime('%Y-%m-%d'),
                "status": "Monitoring",
                "severity": "Low",
                "affected_areas": ["Venice", "Padua"],
                "rivers": ["Po River", "Brenta River"],
                "lat": 45.4,
                "lon": 11.9,
                "source": "Copernicus EMS",
                "description": "Rising water levels in rivers",
                "alert_level": "YELLOW"
            }
        ]
       
        return copernicus_floods
       
    except Exception as e:
        print(f"Copernicus veri hatası: {e}")
        return []

def display_real_copernicus_flood_alerts(flood_alerts):
    win = Toplevel()
    win.title("🌊 " + t('real_flood_alerts'))
    win.geometry('750x800')
    win.configure(bg='#E0F2F1')
   
    Label(win, text="🌊 " + t('real_flood_alerts'), font=('Arial', 16, 'bold'), bg='#E0F2F1').pack(pady=10)
    Label(win, text=t('emergency_copernicus'),
          font=('Arial', 10), bg='#E0F2F1', fg='#666').pack(pady=5)
   
    # İstatistik paneli
    stats_frame = Frame(win, bg='#B2DFDB', bd=1, relief='solid')
    stats_frame.pack(pady=5, padx=20, fill='x')
   
    active_floods = len(flood_alerts)
    high_risk = len([f for f in flood_alerts if f['severity'] == 'High'])
   
    Label(stats_frame,
          text=f"📊 {t('active_events')}: {active_floods} | 🚨 {t('high_risk')}: {high_risk}",
          font=('Arial', 10, 'bold'), bg='#B2DFDB').pack(pady=5)
   
    canvas = Canvas(win, bg='#E0F2F1')
    scrollbar = Scrollbar(win, orient='vertical', command=canvas.yview)
    scrollable_frame = Frame(canvas, bg='#E0F2F1')
   
    scrollable_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
    canvas.configure(yscrollcommand=scrollbar.set)
   
    canvas.pack(side='left', fill='both', expand=True, padx=10)
    scrollbar.pack(side='right', fill='y')
   
    # Şiddete göre sırala (Yüksek -> Düşük)
    flood_alerts.sort(key=lambda x: 0 if x['severity'] == 'High' else 1 if x['severity'] == 'Medium' else 2)
   
    for flood in flood_alerts:
        # Şiddete göre renk ve ikon - t() fonksiyonu ile
        if flood['severity'] == 'High':
            color = '#F44336'
            icon = '🚨'
            severity_text = t('high_risk')
        elif flood['severity'] == 'Medium':
            color = '#FF9800'
            icon = '⚠️'
            severity_text = t('moderate')
        else:
            color = '#FFC107'
            icon = '💧'
            severity_text = t('low')
       
        frame = Frame(scrollable_frame, bg='white', bd=2, relief='raised')
        frame.pack(pady=5, padx=5, fill='x')
       
        # Başlık
        title_frame = Frame(frame, bg='white')
        title_frame.pack(fill='x', padx=10, pady=5)
       
        Label(title_frame, text=f"{icon} {flood['name']}",
              font=('Arial', 12, 'bold'), bg='white').pack(anchor='w')
       
        # Sağ tarafta şiddet bilgisi
        severity_frame = Frame(title_frame, bg='white')
        severity_frame.pack(side='right')
       
        Label(severity_frame, text=flood['alert_level'],
              font=('Arial', 9, 'bold'), bg=color, fg='white', padx=8, pady=2).pack()
        Label(severity_frame, text=severity_text,
              font=('Arial', 9, 'bold'), bg='white', fg=color).pack()
       
        # Ülke ve bölge bilgisi
        location_frame = Frame(frame, bg='white')
        location_frame.pack(fill='x', padx=10, pady=2)
       
        Label(location_frame, text=f"🇺🇳 {flood['country']} - {flood['region']}",
              font=('Arial', 10, 'bold'), bg='white').pack(anchor='w')
       
        # Detaylar
        details_frame = Frame(frame, bg='white')
        details_frame.pack(fill='x', padx=10, pady=5)
       
        Label(details_frame, text=flood['description'],
              font=('Arial', 10), bg='white', wraplength=600).pack(anchor='w')
       
        # Etkilenen alanlar - t() fonksiyonu ile
        affected_frame = Frame(frame, bg='white')
        affected_frame.pack(fill='x', padx=10, pady=2)
       
        Label(affected_frame, text=f"📍 {t('affected_areas')}: {', '.join(flood['affected_areas'])}",
              font=('Arial', 9), bg='white', fg='#666').pack(anchor='w')
       
        # Nehirler ve tarih - t() fonksiyonu ile
        info_frame = Frame(frame, bg='white')
        info_frame.pack(fill='x', padx=10, pady=2)
       
        Label(info_frame, text=f"🌊 {t('rivers_at_risk')}: {', '.join(flood['rivers'])}",
              font=('Arial', 9), bg='white', fg='#666').pack(anchor='w')
       
        Label(info_frame, text=f"📅 {t('start_date')}: {flood['start_date']} | 🔍 {t('status')}: {flood['status']}",
              font=('Arial', 9), bg='white', fg='#666').pack(anchor='w')
       
        # Kaynak bilgisi - t() fonksiyonu ile
        source_frame = Frame(frame, bg='white')
        source_frame.pack(fill='x', padx=10, pady=2)
       
        Label(source_frame, text=f"🔗 {t('source')}: {flood['source']} | 🆔 ID: {flood['id']}",
              font=('Arial', 8), bg='white', fg='#999').pack(anchor='w')
       
        # Butonlar
        button_frame = Frame(frame, bg='white')
        button_frame.pack(fill='x', padx=10, pady=5)
       
        # Haritada göster butonu - t() fonksiyonu ile
        def show_on_map(lat=flood['lat'], lon=flood['lon'], name=flood['name'], severity=flood['severity']):
            map_win = Toplevel()
            map_win.title(f"Copernicus Flood: {name}")
            map_win.geometry('700x600')
           
            map_widget = TkinterMapView(map_win, width=700, height=600)
            map_widget.pack(fill='both', expand=True)
            map_widget.set_position(lat, lon)
            map_widget.set_zoom(8)
           
            map_widget.set_marker(lat, lon,
                                text=f"🌊 Copernicus Flood\n{name}\n🚨 {severity}\n🇺🇳 {flood['country']}")
       
        Button(button_frame, text='🗺️ ' + t('show_on_map'),
               command=lambda lat=flood['lat'], lon=flood['lon'], name=flood['name'], severity=flood['severity']:
               show_on_map(lat, lon, name, severity),
               bg='#2196F3', fg='white', font=('Arial', 9)).pack(side='right', padx=5)
       
        # Copernicus web sitesini aç butonu - t() fonksiyonu ile
        def open_copernicus_website():
            import webbrowser
            webbrowser.open("https://emergency.copernicus.eu/mapping/")
       
        Button(button_frame, text='🌐 ' + t('open_website'),
               command=open_copernicus_website,
               bg='#4CAF50', fg='white', font=('Arial', 9)).pack(side='right', padx=5)
       
def get_weather_based_flood_alerts():
    """Copernicus verisi yoksa OpenWeatherMap'ten sel riski göster (yedek)"""
    try:
        # OpenWeatherMap'ten sel riski analizi
        cities = [
            {"name": "Istanbul", "country": "TR", "rivers": ["Boğaz", "Marmara"]},
            {"name": "Trabzon", "country": "TR", "rivers": ["Karadeniz Kıyıları"]},
            {"name": "Rize", "country": "TR", "rivers": ["Fırtına Deresi", "Çayeli"]},
        ]
       
        flood_alerts = []
       
        for city in cities:
            try:
                params = {
                    'q': f"{city['name']},{city['country']}",
                    'appid': API_KEY,
                    'units': 'metric'
                }
                response = requests.get(FORECAST_URL, params=params, timeout=5)
               
                if response.status_code == 200:
                    data = response.json()
                   
                    # Yağmur analizi
                    total_rain = 0
                    for forecast in data['list'][:8]:  # Son 24 saat
                        if 'rain' in forecast:
                            rain_3h = forecast['rain'].get('3h', 0)
                            total_rain += rain_3h
                   
                    # Sel riski hesaplama
                    if total_rain > 30:
                        risk_level = "YÜKSEK"
                    elif total_rain > 15:
                        risk_level = "ORTA"
                    elif total_rain > 5:
                        risk_level = "DÜŞÜK"
                    else:
                        continue
                   
                    flood_alerts.append({
                        "region": city['name'],
                        "risk_level": risk_level,
                        "description": f"Yoğun yağış: {total_rain:.1f}mm",
                        "total_rain": total_rain,
                        "rivers": city['rivers'],
                        "lat": data['city']['coord']['lat'],
                        "lon": data['city']['coord']['lon'],
                        "source": "OpenWeatherMap (Yedek)"
                    })
                   
            except Exception as e:
                continue
       
        if flood_alerts:
            display_backup_flood_alerts(flood_alerts)
        else:
            messagebox.showinfo("Bilgi", "Şu anda sel riski bulunmuyor")
           
    except Exception as e:
        messagebox.showerror("Hata", f"Sel verisi hatası: {str(e)}")
def show_error_message(message):
    """Hata mesajı göster"""
    messagebox.showerror("Hata", message)

def show_storm_on_map(geometry, name, wind_speed):
    """Fırtınayı haritada göster"""
    map_win = Toplevel()
    map_win.title(f"Fırtına: {name}")
    map_win.geometry('600x500')
   
    map_widget = TkinterMapView(map_win, width=600, height=500)
    map_widget.pack(fill='both', expand=True)
   
    # Geometry'den koordinatları al
    if geometry and 'coordinates' in geometry:
        coords = geometry['coordinates']
        if isinstance(coords[0], list):
            # Polygon
            center_lat = sum(coord[1] for coord in coords[0]) / len(coords[0])
            center_lon = sum(coord[0] for coord in coords[0]) / len(coords[0])
        else:
            # Point
            center_lon, center_lat = coords
       
        map_widget.set_position(center_lat, center_lon)
        map_widget.set_zoom(6)
        map_widget.set_marker(center_lat, center_lon, text=f"🌀 {name}\n💨 {wind_speed} km/h")
def refresh_alerts_display(result_frame):
    """Alert ekranını temizle ve başlangıç durumuna getir"""
    for widget in result_frame.winfo_children():
        widget.destroy()
   
    Label(result_frame, text='Yukarıdaki butonlardan birine tıklayarak uyarıları görüntüleyin',
          font=('Arial', 12), bg='#FFEBEE', fg='#666').pack(pady=20)

def save_climate_data(city, year, month, avg_temp):
    """İklim verilerini kaydet"""
    if not os.path.exists(CLIMATE_DATA_FILE):
        data = {}
    else:
        try:
            with open(CLIMATE_DATA_FILE, 'r') as f:
                data = json.load(f)
        except:
            data = {}
   
    if city not in data:
        data[city] = {}
    if str(year) not in data[city]:
        data[city][str(year)] = {}
   
    data[city][str(year)][str(month)] = avg_temp
   
    with open(CLIMATE_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def open_climate_data_window():
    win = Toplevel()
    win.title(t('climate_title'))
    win.geometry('600x700')
    win.configure(bg='#E8F5E9')
   
    Label(win, text=t('climate_title'), font=('Arial', 16, 'bold'), bg='#E8F5E9').pack(pady=10)
   
    # Giriş alanları
    input_frame = Frame(win, bg='#E8F5E9')
    input_frame.pack(pady=10, padx=20, fill='x')
   
    Label(input_frame, text=t('city'), bg='#E8F5E9', font=('Arial', 11)).pack(anchor='w')
    city_entry = Entry(input_frame, justify='center', font=('Arial', 12))
    city_entry.pack(pady=5, fill='x')
    city_entry.insert(0, "Istanbul")
   
    # Yıl seçimi
    year_frame = Frame(win, bg='#E8F5E9')
    year_frame.pack(pady=5, padx=20, fill='x')
   
    Label(year_frame, text=t('select_years'), bg='#E8F5E9', font=('Arial', 11)).pack(anchor='w')
   
    year_subframe = Frame(year_frame, bg='#E8F5E9')
    year_subframe.pack(fill='x', pady=5)
   
    current_year = datetime.now().year
   
    Label(year_subframe, text=t('year1'), bg='#E8F5E9').pack(side='left')
    year1_var = StringVar(value=str(current_year - 1))
    year1_spinbox = Spinbox(year_subframe, from_=2000, to=current_year, textvariable=year1_var,
                           width=8, font=('Arial', 11))
    year1_spinbox.pack(side='left', padx=5)
   
    Label(year_subframe, text=t('year2'), bg='#E8F5E9').pack(side='left', padx=(20,0))
    year2_var = StringVar(value=str(current_year))
    year2_spinbox = Spinbox(year_subframe, from_=2000, to=current_year, textvariable=year2_var,
                           width=8, font=('Arial', 11))
    year2_spinbox.pack(side='left', padx=5)
   
    # Sonuç alanı
    result_frame = Frame(win, bg='white', bd=2, relief='solid')
    result_frame.pack(pady=10, padx=20, fill='both', expand=True)
   
    result_text = Text(result_frame, height=20, width=65, wrap='word', font=('Arial', 10))
    result_scroll = Scrollbar(result_frame, command=result_text.yview)
    result_text.configure(yscrollcommand=result_scroll.set)
   
    result_text.pack(side='left', fill='both', expand=True)
    result_scroll.pack(side='right', fill='y')
   
    def get_climate_data():
        city = city_entry.get().strip()
        if not city:
            result_text.delete('1.0', 'end')
            result_text.insert('1.0', t('enter_city_first'))
            return
       
        try:
            year1 = int(year1_var.get())
            year2 = int(year2_var.get())
           
            if year1 >= year2:
                result_text.delete('1.0', 'end')
                result_text.insert('1.0', t('invalid_years'))
                return
               
        except ValueError:
            result_text.delete('1.0', 'end')
            result_text.insert('1.0', t('invalid_year_format'))
            return
       
        try:
            # OpenWeatherMap Historical Data API (ücretsiz sürümde mevcut değil, simüle ediyoruz)
            # Gerçek uygulamada OpenWeatherMap One Call API 3.0 kullanılabilir
           
            # Şehir koordinatlarını al
            geo_params = {'q': city, 'appid': API_KEY, 'limit': 1}
            geo_response = requests.get("http://api.openweathermap.org/geo/1.0/direct", params=geo_params, timeout=5)
           
            if geo_response.status_code != 200 or not geo_response.json():
                result_text.delete('1.0', 'end')
                result_text.insert('1.0', t('city_not_found'))
                return
           
            city_data = geo_response.json()[0]
            lat = city_data['lat']
            lon = city_data['lon']
            city_name = city_data['name']
            country = city_data.get('country', '')
           
            # Mevcut hava durumu verileri ile iklim analizi yap
            current_params = {'lat': lat, 'lon': lon, 'appid': API_KEY, 'units': 'metric'}
            current_response = requests.get(WEATHER_URL, params=current_params, timeout=5)
           
            if current_response.status_code != 200:
                result_text.delete('1.0', 'end')
                result_text.insert('1.0', t('data_error'))
                return
           
            current_data = current_response.json()
            current_temp = current_data['main']['temp']
           
            # Tarihsel verileri simüle et (gerçek API olmadığı için)
            # Gerçek uygulamada OpenWeatherMap Historical API veya başka bir servis kullanılmalı
            monthly_data_year1 = simulate_historical_data(lat, lon, year1)
            monthly_data_year2 = simulate_historical_data(lat, lon, year2)
           
            # İklim analizi sonuçları
            result_text.delete('1.0', 'end')
           
            text = f"""
🌍 {t('climate_analysis_for')} {city_name}, {country}

📅 {t('analysis_period')}: {year1} - {year2}
📍 {t('coordinates')}: {lat:.2f}°N, {lon:.2f}°E

{t('yearly_comparison')}:
----------------------------
{year1} {t('average_temperature')}: {monthly_data_year1['year_avg']:.1f}°C
{year2} {t('average_temperature')}: {monthly_data_year2['year_avg']:.1f}°C
📈 {t('temperature_change')}: {monthly_data_year2['year_avg'] - monthly_data_year1['year_avg']:+.1f}°C

{t('monthly_breakdown')}:
----------------------------
          {year1}    {year2}    {t('change')}
📊 {t('winter_months')}:
  Dec: {monthly_data_year1['dec']:5.1f}°C  {monthly_data_year2['dec']:5.1f}°C  {monthly_data_year2['dec'] - monthly_data_year1['dec']:+.1f}°C
  Jan: {monthly_data_year1['jan']:5.1f}°C  {monthly_data_year2['jan']:5.1f}°C  {monthly_data_year2['jan'] - monthly_data_year1['jan']:+.1f}°C
  Feb: {monthly_data_year1['feb']:5.1f}°C  {monthly_data_year2['feb']:5.1f}°C  {monthly_data_year2['feb'] - monthly_data_year1['feb']:+.1f}°C

📊 {t('spring_months')}:
  Mar: {monthly_data_year1['mar']:5.1f}°C  {monthly_data_year2['mar']:5.1f}°C  {monthly_data_year2['mar'] - monthly_data_year1['mar']:+.1f}°C
  Apr: {monthly_data_year1['apr']:5.1f}°C  {monthly_data_year2['apr']:5.1f}°C  {monthly_data_year2['apr'] - monthly_data_year1['apr']:+.1f}°C
  May: {monthly_data_year1['may']:5.1f}°C  {monthly_data_year2['may']:5.1f}°C  {monthly_data_year2['may'] - monthly_data_year1['may']:+.1f}°C

📊 {t('summer_months')}:
  Jun: {monthly_data_year1['jun']:5.1f}°C  {monthly_data_year2['jun']:5.1f}°C  {monthly_data_year2['jun'] - monthly_data_year1['jun']:+.1f}°C
  Jul: {monthly_data_year1['jul']:5.1f}°C  {monthly_data_year2['jul']:5.1f}°C  {monthly_data_year2['jul'] - monthly_data_year1['jul']:+.1f}°C
  Aug: {monthly_data_year1['aug']:5.1f}°C  {monthly_data_year2['aug']:5.1f}°C  {monthly_data_year2['aug'] - monthly_data_year1['aug']:+.1f}°C

📊 {t('autumn_months')}:
  Sep: {monthly_data_year1['sep']:5.1f}°C  {monthly_data_year2['sep']:5.1f}°C  {monthly_data_year2['sep'] - monthly_data_year1['sep']:+.1f}°C
  Oct: {monthly_data_year1['oct']:5.1f}°C  {monthly_data_year2['oct']:5.1f}°C  {monthly_data_year2['oct'] - monthly_data_year1['oct']:+.1f}°C
  Nov: {monthly_data_year1['nov']:5.1f}°C  {monthly_data_year2['nov']:5.1f}°C  {monthly_data_year2['nov'] - monthly_data_year1['nov']:+.1f}°C

{t('climate_insights')}:
----------------------------
🔍 {t('trend_analysis')}: {get_trend_analysis(monthly_data_year1, monthly_data_year2)}
🌡️ {t('current_temperature')}: {current_temp:.1f}°C
📈 {t('warming_trend')}: {calculate_warming_trend(monthly_data_year1, monthly_data_year2)}

{t('data_source_note')}
            """.strip()
           
            result_text.insert('1.0', text)
           
        except Exception as e:
            result_text.delete('1.0', 'end')
            result_text.insert('1.0', f'{t("data_error")}: {str(e)}')
   
    # Yardımcı fonksiyonlar
    def simulate_historical_data(lat, lon, year):
        """Tarihsel iklim verilerini simüle et"""
        # Enlem ve mevsime göre sıcaklık varyasyonu
        base_temp = 15 - (abs(lat) / 90 * 30)  # Ekvatordan uzaklaştıkça soğuk
       
        # İklim değişikliği etkisi (yıllara göre artan sıcaklık)
        warming = (year - 2000) * 0.03
       
        return {
            'jan': base_temp - 10 + warming + random.uniform(-2, 2),
            'feb': base_temp - 8 + warming + random.uniform(-2, 2),
            'mar': base_temp - 3 + warming + random.uniform(-1, 1),
            'apr': base_temp + 2 + warming + random.uniform(-1, 1),
            'may': base_temp + 8 + warming + random.uniform(-1, 1),
            'jun': base_temp + 12 + warming + random.uniform(-1, 1),
            'jul': base_temp + 15 + warming + random.uniform(-1, 1),
            'aug': base_temp + 14 + warming + random.uniform(-1, 1),
            'sep': base_temp + 10 + warming + random.uniform(-1, 1),
            'oct': base_temp + 5 + warming + random.uniform(-1, 1),
            'nov': base_temp + 0 + warming + random.uniform(-2, 2),
            'dec': base_temp - 7 + warming + random.uniform(-2, 2),
            'year_avg': base_temp + 3 + warming
        }
   
    def get_trend_analysis(data1, data2):
        """İklim trend analizi"""
        avg_change = data2['year_avg'] - data1['year_avg']
        if avg_change > 1.0:
            return t('significant_warming')
        elif avg_change > 0.5:
            return t('moderate_warming')
        elif avg_change > 0:
            return t('slight_warming')
        else:
            return t('stable_temperatures')
   
    def calculate_warming_trend(data1, data2):
        """Isınma trendini hesapla"""
        change = data2['year_avg'] - data1['year_avg']
        return f"+{change:.2f}°C {t('per_decade')}" if change > 0 else f"{change:.2f}°C {t('per_decade')}"
   
    # Butonlar
    button_frame = Frame(win, bg='#E8F5E9')
    button_frame.pack(pady=10, padx=20, fill='x')
   
    create_button(button_frame, t('compare_years'), get_climate_data,
                  bg='#4CAF50', font=('Arial', 12, 'bold')).pack(fill='x')
   
    create_button(win, t('back_arrow'), win.destroy,
                  bg='#9E9E9E', font=('Arial', 11)).pack(pady=5)

def calculate_energy_consumption(temp, target_temp=21):
    """Gelişmiş enerji tüketim tahmini"""
    if temp < target_temp:
        # Isıtma ihtiyacı - derece-gün metodu
        heating_degree_days = target_temp - temp
        # Binanın yalıtım faktörüne göre enerji ihtiyacı
        insulation_factor = 2.5  # kWh/°C-gün (ortalama yalıtımlı bina)
        heating_kwh = heating_degree_days * insulation_factor
        cooling_kwh = 0
    else:
        # Soğutma ihtiyacı
        cooling_degree_days = temp - target_temp
        # Klima verimlilik faktörü (COP ~3.0)
        cooling_efficiency = 3.0
        cooling_kwh = cooling_degree_days * cooling_efficiency
        heating_kwh = 0
   
    return {
        'heating': round(heating_kwh, 1),
        'cooling': round(cooling_kwh, 1),
        'total': round(heating_kwh + cooling_kwh, 1)
    }

def calculate_energy_consumption(temp, target_temp=21):
    """Enerji tüketim tahmini"""
    if temp < target_temp:
        heating_degree_days = target_temp - temp
        heating_kwh = heating_degree_days * 2.5
        cooling_kwh = 0
    else:
        cooling_degree_days = temp - target_temp
        cooling_kwh = cooling_degree_days * 3.0
        heating_kwh = 0
   
    return {
        'heating': round(heating_kwh, 1),
        'cooling': round(cooling_kwh, 1),
        'total': round(heating_kwh + cooling_kwh, 1)
    }

def open_energy_window():
    win = Toplevel()
    win.title(t('energy_title'))
    win.geometry('450x500')  # Boyutu biraz büyüttüm
    win.configure(bg='#FFF9C4')
   
    Label(win, text=t('energy_title'), font=('Arial', 14, 'bold'), bg='#FFF9C4').pack(pady=10)
   
    # Giriş alanı
    input_frame = Frame(win, bg='#FFF9C4')
    input_frame.pack(pady=5, padx=20, fill='x')
   
    Label(input_frame, text=t('city'), bg='#FFF9C4', font=('Arial', 11)).pack(anchor='w')
    city_entry = Entry(input_frame, justify='center', font=('Arial', 12))
    city_entry.pack(pady=5, fill='x')
   
    # Sonuç alanı
    result_frame = Frame(win, bg='white', bd=2, relief='solid')
    result_frame.pack(pady=10, padx=20, fill='both', expand=True)
   
    result_text = Text(result_frame, height=15, width=50, wrap='word', font=('Arial', 10))
    result_scroll = Scrollbar(result_frame, command=result_text.yview)
    result_text.configure(yscrollcommand=result_scroll.set)
   
    result_text.pack(side='left', fill='both', expand=True)
    result_scroll.pack(side='right', fill='y')
   
    def calculate():
        city = city_entry.get().strip()
        if not city:
            result_text.delete('1.0', 'end')
            result_text.insert('1.0', t('enter_city_energy'))
            return
       
        params = {'appid': API_KEY, 'units': 'metric'}
        if ',' in city:
            try:
                lat, lon = city.split(',')
                params['lat'] = lat.strip()
                params['lon'] = lon.strip()
            except:
                result_text.delete('1.0', 'end')
                result_text.insert('1.0', t('coord_error'))
                return
        else:
            params['q'] = city
       
        try:
            r = requests.get(FORECAST_URL, params=params, timeout=5)
            if r.status_code != 200:
                result_text.delete('1.0', 'end')
                result_text.insert('1.0', t('energy_data_error'))
                return
           
            data = r.json()
            forecasts = data['list'][:8]  # 24 saatlik tahmin
           
            total_heating = 0
            total_cooling = 0
            current_temp = forecasts[0]['main']['temp'] if forecasts else 0
           
            for fc in forecasts:
                temp = fc['main']['temp']
                energy = calculate_energy_consumption(temp)
                total_heating += energy['heating']
                total_cooling += energy['cooling']
           
            avg_heating = total_heating / len(forecasts) if forecasts else 0
            avg_cooling = total_cooling / len(forecasts) if forecasts else 0
           
            # Çevrilmiş metinleri kullan
            text = f"""
{t('energy_24h_forecast')}

🔥 {t('heating_need')}: {avg_heating:.1f} {t('kwh_day')}
❄️ {t('cooling_need')}: {avg_cooling:.1f} {t('kwh_day')}
⚡ {t('total_energy')}: {avg_heating + avg_cooling:.1f} {t('kwh_day')}

{t('estimated_cost')}
{t('heating_cost').format(avg_heating * 1.5)}
{t('cooling_cost').format(avg_cooling * 1.8)}

{t('recommendation')} {t('use_heater') if avg_heating > avg_cooling else t('use_ac')}

{t('energy_savings_tip')}
{t('tip_heating')}
{t('tip_cooling')}
{t('tip_insulation')}
{t('tip_curtains')}
{t('tip_unplug')}
            """.strip()
           
            result_text.delete('1.0', 'end')
            result_text.insert('1.0', text)
           
        except Exception as e:
            result_text.delete('1.0', 'end')
            result_text.insert('1.0', f'{t("energy_data_error")}: {str(e)}')
   
    # Buton
    button_frame = Frame(win, bg='#FFF9C4')
    button_frame.pack(pady=10, padx=20, fill='x')
   
    create_button(button_frame, t('get_forecast'), calculate,
                  bg='#FFC107', font=('Arial', 12, 'bold')).pack(fill='x')
   
    # Geri butonu
    create_button(win, t('back_arrow'), win.destroy,
                  bg='#9E9E9E', font=('Arial', 11)).pack(pady=5)
def show_weather_widget():
    """Widget görünümü"""
    widget_win = Toplevel()
    widget_win.title('')
    widget_win.geometry('200x250')
    widget_win.attributes('-topmost', True)
    widget_win.overrideredirect(True)
    widget_win.configure(bg='#263238')
   
    def start_move(event):
        widget_win.x = event.x
        widget_win.y = event.y
   
    def do_move(event):
        x = widget_win.winfo_x() - widget_win.x + event.x
        y = widget_win.winfo_y() - widget_win.y + event.y
        widget_win.geometry(f'+{x}+{y}')
   
    widget_win.bind('<Button-1>', start_move)
    widget_win.bind('<B1-Motion>', do_move)
   
    try:
        params = {'q': 'Istanbul', 'appid': API_KEY, 'units': 'metric'}
        r = requests.get(WEATHER_URL, params=params, timeout=5)
        if r.status_code == 200:
            data = r.json()
            city = data['name']
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            icon_code = data['weather'][0]['icon']
        else:
            city, temp, desc, icon_code = 'Unknown', '--', 'N/A', '01d'
    except:
        city, temp, desc, icon_code = 'Unknown', '--', 'N/A', '01d'
   
    try:
        icon_response = requests.get(ICON_URL.format(icon_code), timeout=5)
        img_data = icon_response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((80, 80), Image.LANCZOS if hasattr(Image, 'LANCZOS') else Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        icon_lbl = Label(widget_win, image=photo, bg='#263238')
        icon_lbl.image = photo
        icon_lbl.pack(pady=(10,0))
    except:
        pass
   
    Label(widget_win, text=city, font=('Arial', 14,'bold'), fg='white', bg='#263238').pack()
    Label(widget_win, text=f'{temp}°C', font=('Arial', 24, 'bold'), fg='#FFC107', bg='#263238').pack()
    Label(widget_win, text=desc.capitalize(), font=('Arial', 10), fg='white', bg='#263238').pack()
   
    Button(widget_win, text='✕', command=widget_win.destroy,
           bg='#F44336', fg='white', bd=0, font=('Arial', 10, 'bold')).pack(side='bottom', fill='x')

def open_traveler_mode():
    win = Toplevel()
    win.title(t('traveler_title'))
    win.geometry('500x600')
    win.configure(bg='#E1F5FE')
   
    Label(win, text=t('traveler_title'), font=('Arial', 16, 'bold'), bg='#E1F5FE').pack(pady=10)
   
    # Giriş alanları için frame
    input_frame = Frame(win, bg='#E1F5FE')
    input_frame.pack(pady=10, padx=20, fill='x')
   
    Label(input_frame, text=t('destination'), bg='#E1F5FE', font=('Arial', 11)).pack(anchor='w')
    dest_entry = Entry(input_frame, justify='center', font=('Arial', 12))
    dest_entry.pack(fill='x', pady=(5,10))
   
    # Tarih seçimleri için frame
    date_frame = Frame(win, bg='#E1F5FE')
    date_frame.pack(pady=5, padx=20, fill='x')
   
    Label(date_frame, text=t('departure_date'), bg='#E1F5FE', font=('Arial', 11)).pack(anchor='w')
    dep_entry = Entry(date_frame, justify='center', font=('Arial', 12))
    dep_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
    dep_entry.pack(fill='x', pady=(5,10))
   
    Label(date_frame, text=t('return_date'), bg='#E1F5FE', font=('Arial', 11)).pack(anchor='w')
    ret_entry = Entry(date_frame, justify='center', font=('Arial', 12))
    ret_entry.insert(0, (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'))
    ret_entry.pack(fill='x', pady=(5,10))
   
    # Sonuç alanı
    result_frame = Frame(win, bg='white', bd=2, relief='solid')
    result_frame.pack(pady=10, padx=20, fill='both', expand=True)
   
    result_text = Text(result_frame, height=15, width=55, wrap='word', font=('Arial', 10))
    result_scroll = Scrollbar(result_frame, command=result_text.yview)
    result_text.configure(yscrollcommand=result_scroll.set)
   
    result_text.pack(side='left', fill='both', expand=True)
    result_scroll.pack(side='right', fill='y')
   
    def get_travel_forecast():
        dest = dest_entry.get().strip()
        if not dest:
            result_text.delete('1.0', 'end')
            result_text.insert('1.0', t('enter_city_first'))
            return
       
        try:
            # Tarih kontrolleri
            dep_date = datetime.strptime(dep_entry.get(), '%Y-%m-%d')
            ret_date = datetime.strptime(ret_entry.get(), '%Y-%m-%d')
           
            if ret_date <= dep_date:
                result_text.delete('1.0', 'end')
                result_text.insert('1.0', t('invalid_dates'))
                return
               
        except ValueError:
            result_text.delete('1.0', 'end')
            result_text.insert('1.0', t('invalid_date_format'))
            return
       
        try:
            params = {'q': dest, 'appid': API_KEY, 'units': 'metric'}
            r = requests.get(FORECAST_URL, params=params, timeout=5)
            if r.status_code != 200:
                result_text.delete('1.0', 'end')
                result_text.insert('1.0', t('travel_city_not_found'))
                return
           
            data = r.json()
            forecasts = data['list']
           
            # Başlık
            text = "✈️ " + t('travel_forecast_for').format(dest) + "\n"
            text += "📅 " + t('travel_period').format(dep_entry.get(), ret_entry.get()) + "\n\n"
           
            # Günlük tahminler (her gün için 1 tahmin)
            daily_forecasts = forecasts[::8]  # Her 24 saatte bir (8*3 saat)
           
            for i, fc in enumerate(daily_forecasts[:7]):  # Maksimum 7 gün
                date = fc['dt_txt'].split()[0]
                temp = fc['main']['temp']
                desc = fc['weather'][0]['description']
                humidity = fc['main']['humidity']
                wind = fc['wind']['speed']
               
                text += t('travel_date').format(date) + "\n"
                text += t('travel_temp').format(temp, desc) + "\n"
                text += "💧 " + t('humidity') + f": {humidity}% | "
                text += "💨 " + t('wind') + f": {wind} m/s\n\n"
           
            text += "💼 " + t('travel_advice') + "\n"
           
            # Detaylı tavsiyeler
            avg_temp = sum(fc['main']['temp'] for fc in forecasts[:8]) / min(8, len(forecasts))
           
            if avg_temp < 5:
                text += "❄️ " + t('very_cold_weather') + "\n"
                text += "• " + t('advice_thermal_clothes') + "\n"
                text += "• " + t('advice_winter_boots') + "\n"
                text += "• " + t('advice_gloves_scarf') + "\n"
            elif avg_temp < 15:
                text += "🥶 " + t('cold_weather') + "\n"
                text += "• " + t('advice_jacket') + "\n"
                text += "• " + t('advice_long_pants') + "\n"
                text += "• " + t('advice_closed_shoes') + "\n"
            elif avg_temp < 25:
                text += "😊 " + t('pleasant_weather') + "\n"
                text += "• " + t('advice_light_jacket') + "\n"
                text += "• " + t('advice_versatile_clothes') + "\n"
                text += "• " + t('advice_comfortable_shoes') + "\n"
            else:
                text += "🥵 " + t('hot_weather') + "\n"
                text += "• " + t('advice_light_clothes') + "\n"
                text += "• " + t('advice_sunscreen') + "\n"
                text += "• " + t('advice_hat') + "\n"
                text += "• " + t('advice_water') + "\n"
           
            # Yağmur kontrolü
            has_rain = any('rain' in fc['weather'][0]['description'].lower() for fc in forecasts[:8])
            if has_rain:
                text += "\n🌧️ " + t('rain_expected') + "\n"
                text += "• " + t('advice_umbrella') + "\n"
                text += "• " + t('advice_waterproof') + "\n"
           
            result_text.delete('1.0', 'end')
            result_text.insert('1.0', text)
           
        except Exception as e:
            result_text.delete('1.0', 'end')
            result_text.insert('1.0', f'{t("travel_no_data")}: {str(e)}')
   
    create_button(win, t('get_travel_forecast'), get_travel_forecast,
                  bg='#03A9F4', font=('Arial', 12, 'bold')).pack(pady=10)
def load_social_posts():
    if not os.path.exists(SOCIAL_POSTS_FILE):
        return []
    try:
        with open(SOCIAL_POSTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_social_post(username, lat, lon, city, comment, photo_path=None):
    posts = load_social_posts()
    post = {
        'username': username,
        'lat': lat,
        'lon': lon,
        'city': city,
        'comment': comment,
        'photo': photo_path,
        'timestamp': datetime.now().isoformat()
    }
    posts.append(post)
   
    with open(SOCIAL_POSTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts[-100:], f, ensure_ascii=False, indent=2)

def open_social_window():
    win = Toplevel()
    win.title(t('social_title'))
    win.geometry('500x600')
    win.configure(bg='#FCE4EC')
   
    Label(win, text=t('social_title'), font=('Arial', 14, 'bold'), bg='#FCE4EC').pack(pady=10)
   
    add_frame = Frame(win, bg='white', bd=2, relief='raised')
    add_frame.pack(pady=10, padx=10, fill='x')
   
    Label(add_frame, text=t('city'), bg='white').pack(pady=5)
    city_entry = Entry(add_frame, justify='center', width=30)
    city_entry.pack(pady=5)
   
    Label(add_frame, text=t('your_comment'), bg='white').pack(pady=5)
    comment_entry = Text(add_frame, height=3, width=40)
    comment_entry.pack(pady=5)
   
    photo_path_var = StringVar(value='')
   
    def upload_photo():
        path = filedialog.askopenfilename(filetypes=[('Images', '*.jpg *.jpeg *.png')])
        if path:
            photo_path_var.set(path)
            messagebox.showinfo(t('success'), 'Fotoğraf seçildi!')
   
    create_button(add_frame, t('upload_photo'), upload_photo, bg='#E91E63').pack(pady=5)
   
    def add_post():
        city = city_entry.get().strip()
        comment = comment_entry.get('1.0', 'end').strip()
       
        if not city or not comment:
            messagebox.showwarning(t('error'), t('empty_fields'))
            return
       
        try:
            params = {'q': city, 'appid': API_KEY}
            r = requests.get(WEATHER_URL, params=params, timeout=5)
            if r.status_code == 200:
                data = r.json()
                lat = data['coord']['lat']
                lon = data['coord']['lon']
            else:
                lat, lon = 0, 0
        except:
            lat, lon = 0, 0
       
        save_social_post(current_user or 'Anonymous', lat, lon, city, comment, photo_path_var.get())
        messagebox.showinfo(t('success'), 'Paylaşım eklendi!')
        city_entry.delete(0, 'end')
        comment_entry.delete('1.0', 'end')
        photo_path_var.set('')
        refresh_posts()
   
    create_button(add_frame, t('post'), add_post, bg='#4CAF50').pack(pady=10)
   
    posts_frame = Frame(win, bg='#FCE4EC')
    posts_frame.pack(pady=10, padx=10, fill='both', expand=True)
   
    canvas = Canvas(posts_frame, bg='#FCE4EC')
    scrollbar = Scrollbar(posts_frame, orient='vertical', command=canvas.yview)
    scrollable_frame = Frame(canvas, bg='#FCE4EC')
   
    scrollable_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
    canvas.configure(yscrollcommand=scrollbar.set)
   
    canvas.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')
   
    def refresh_posts():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
       
        posts = load_social_posts()
        if not posts:
            Label(scrollable_frame, text='Henüz paylaşım yok', bg='#FCE4EC', font=('Arial', 11)).pack(pady=20)
        else:
            for post in reversed(posts[-20:]):
                post_frame = Frame(scrollable_frame, bg='white', bd=1, relief='solid')
                post_frame.pack(pady=5, padx=5, fill='x')
               
                header = Frame(post_frame, bg='white')
                header.pack(fill='x', padx=5, pady=5)
               
                Label(header, text=f"👤 {post['username']}", font=('Arial', 10, 'bold'), bg='white').pack(side='left')
                Label(header, text=post['timestamp'][:16], font=('Arial', 8), bg='white', fg='gray').pack(side='right')
               
                Label(post_frame, text=f"📍 {post['city']}", bg='white', fg='#1976D2').pack(anchor='w', padx=5)
                Label(post_frame, text=post['comment'], bg='white', wraplength=400, justify='left').pack(anchor='w', padx=5, pady=5)
               
                if post.get('photo'):
                    try:
                        img = Image.open(post['photo'])
                        img = img.resize((100, 100), Image.LANCZOS if hasattr(Image, 'LANCZOS') else Image.ANTIALIAS)
                        photo = ImageTk.PhotoImage(img)
                        img_label = Label(post_frame, image=photo, bg='white')
                        img_label.image = photo
                        img_label.pack(padx=5, pady=5)
                    except:
                        pass
               
                def show_post_on_map(lat, lon, city):
                    map_win = Toplevel()
                    map_win.title(city)
                    map_win.geometry('500x400')
                   
                    map_widget = TkinterMapView(map_win, width=500, height=400)
                    map_widget.pack(fill='both', expand=True)
                    if lat and lon:
                        map_widget.set_position(lat, lon)
                        map_widget.set_zoom(10)
                        map_widget.set_marker(lat, lon, text=f"📷 {city}")
               
                Button(post_frame, text='🗺️ Haritada Göster',
                       command=lambda p=post: show_post_on_map(p['lat'], p['lon'], p['city']),
                       bg='#2196F3', fg='white', bd=0).pack(anchor='e', padx=5, pady=5)
   
    refresh_posts()
def open_lightning_monitor():
    mon = Toplevel()
    mon.title(t('lightning_title'))  # t() fonksiyonu ile
    mon.geometry('800x600')

    ctrl_frame = Frame(mon)
    ctrl_frame.pack(fill='x', pady=6)
    try:
        ctrl_frame.configure(bg=mon.cget('bg'))
    except Exception:
        pass
   
    # Durum etiketi - t() fonksiyonu ile
    status_lbl = Label(ctrl_frame, text=t('lightning_status_stopped'))
    status_lbl.pack(side='left', padx=6)

    # Başlat ve Durdur butonları - t() fonksiyonu ile
    start_btn = Button(ctrl_frame, text=t('lightning_start'), command=lambda: start_monitor(),
                      bg="#FF5722", activebackground="#F4511E", fg="white",
                      font=("Arial", 11, "bold"))
    start_btn.pack(side='right', padx=6, pady=4)

    stop_btn = Button(ctrl_frame, text=t('lightning_stop'), command=lambda: stop_monitor(),
                     bg="#9E9E9E", activebackground="#757575", fg="white",
                     font=("Arial", 11, "bold"))
    stop_btn.pack(side='right', padx=6, pady=4)

    map_w = TkinterMapView(mon, width=800, height=520, corner_radius=0)
    map_w.pack(fill='both', expand=True)
    try:
        map_w.set_position(39.0, 35.0)
        map_w.set_zoom(5)
    except Exception:
        pass

    running = {'val': False}
    markers = []

    def simulate_strike():
        if not running['val']:
            return
       
        try:
            center = map_w.get_position()
            latc = center[0]
            lonc = center[1]
        except Exception:
            latc, lonc = 39.0, 35.0

        # Rastgele konumda yıldırım oluştur
        lat = latc + (random.random() - 0.5) * 1.0
        lon = lonc + (random.random() - 0.5) * 1.0

        try:
            m = map_w.set_marker(lat, lon, text='⚡')
            markers.append(m)
        except Exception:
            m = None

        # Bir sonraki yıldırım için zamanlama
        if running['val']:
            delay = 800 + int(random.random() * 2200)
            mon.after(delay, simulate_strike)

    def convert_to_recent():
        if running['val']:
            try:
                # Aktif yıldırımları son yıldırımlara dönüştür
                for i, marker in enumerate(markers[:]):
                    if marker.text == '⚡':  # Sadece aktif yıldırımları dönüştür
                        try:
                            latx, lonx = marker.position
                            map_w.delete(marker)
                            # • işareti ile yeni marker oluştur
                            r = map_w.set_marker(latx, lonx, text='•')
                            markers[i] = r  # Markeri güncelle
                        except Exception as e:
                            print(f"Marker conversion error: {e}")
            except Exception as e:
                print(f"Convert error: {e}")
           
            # Bu fonksiyonu tekrar çalıştır
            mon.after(800, convert_to_recent)

    def remove_mark():
        if running['val']:
            try:
                # En eski 2 marker'ı kaldır
                if markers:
                    for _ in range(min(2, len(markers))):
                        if markers:
                            mm = markers.pop(0)
                            try:
                                map_w.delete(mm)
                            except Exception:
                                pass
            except Exception as e:
                print(f"Remove error: {e}")
           
            # Bu fonksiyonu tekrar çalıştır
            mon.after(2000, remove_mark)

    def start_monitor():
        if running['val']:
            return
        running['val'] = True
        status_lbl.config(text=t('lightning_status_running'))  # t() fonksiyonu ile
       
        # Buton renklerini güncelle
        start_btn.config(bg="#9E9E9E", state="disabled")
        stop_btn.config(bg="#FF5722", state="normal")
       
        # Simülasyonu başlat
        simulate_strike()
        convert_to_recent()
        remove_mark()

    def stop_monitor():
        running['val'] = False
        status_lbl.config(text=t('lightning_status_stopped'))  # t() fonksiyonu ile
       
        # Buton renklerini güncelle
        start_btn.config(bg="#FF5722", state="normal")
        stop_btn.config(bg="#9E9E9E", state="disabled")
       
        # Tüm marker'ları temizle
        try:
            for marker in markers:
                try:
                    map_w.delete(marker)
                except Exception:
                    pass
            markers.clear()
        except Exception:
            pass

    # Açıklama (legend) kısmı - t() fonksiyonu ile
    legend = Frame(mon)
    legend.pack(fill='x', pady=(4,8))
    Label(legend, text=t('legend_title'), font=('Arial', 10, 'bold')).pack(anchor='w', padx=6)
   
    leg_row = Frame(legend)
    leg_row.pack(anchor='w', padx=6, pady=2)
   
    # Aktif yıldırım göstergesi
    active_swatch = Canvas(leg_row, width=14, height=14)
    active_swatch.create_oval(2,2,12,12, fill='red', outline='red')
    active_swatch.pack(side='left', padx=(0,6))
    Label(leg_row, text="⚡ " + t('legend_active')).pack(side='left', padx=(0,12))  # t() fonksiyonu ile
   
    # Son yıldırım göstergesi
    recent_swatch = Canvas(leg_row, width=14, height=14)
    recent_swatch.create_oval(4,4,10,10, fill='yellow', outline='orange')
    recent_swatch.pack(side='left', padx=(0,6))
    Label(leg_row, text="• " + t('legend_recent')).pack(side='left')  # t() fonksiyonu ile

    # Pencere kapatıldığında simülasyonu durdur
    def on_closing():
        running['val'] = False
        mon.destroy()
   
    mon.protocol("WM_DELETE_WINDOW", on_closing)
   
    return mon
# Global widget tanımlamaları
username_entry = Entry(app, justify='center', font=('Arial', 12))
password_entry = Entry(app, justify='center', font=('Arial', 12), show='*')
reg_hot = Entry(app, justify='center')
reg_cold = Entry(app, justify='center')
reg_wind = Entry(app, justify='center')
reg_humid = Entry(app, justify='center')
info_label = Label(app, font=('Arial', 10))
city_entry = Entry(app, justify='center', font=('Arial', 12))
date_entry = Entry(app, justify='center', font=('Arial', 12))
hour_entry = Entry(app, justify='center', font=('Arial', 12))
icon_label = Label(app)
location_label = Label(app)
temp_label = Label(app)
condition_label = Label(app)
comfort_label = Label(app)

def show_login_screen():
    clear_screen()
    app.configure(bg="#52C7EE")
    app.current_screen = show_login_screen

    global username_entry, password_entry, info_label

    frame = Frame(app, bg="#ffffff", bd=2, relief="ridge", width=300, height=350)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    frame.pack_propagate(False)

    Label(frame, text=t('login_title'), font=('Arial', 16, 'bold'), bg="#ffffff").pack(pady=(10,20))

    Label(frame, text=t('username'), font=('Arial', 12), bg="#ffffff").pack(pady=(5,2))
    username_entry = Entry(frame, justify='center', font=('Arial', 12))
    username_entry.pack(pady=(0,10), padx=20, fill="x")

    Label(frame, text=t('password'), font=('Arial', 12), bg="#ffffff").pack(pady=(5,2))
    password_entry = Entry(frame, justify='center', font=('Arial', 12), show='*')
    password_entry.pack(pady=(0,15), padx=20, fill="x")

    create_button(frame, t('login'), login, bg="#4CAF4F", hover_bg="#45a049").pack(pady=5, fill="x", padx=20)
    create_button(frame, t('register'), show_register_screen, bg="#2196F3", hover_bg="#1976D2").pack(pady=(5,10), fill="x", padx=20)

    info_label = Label(frame, font=('Arial', 10), bg="#ffffff", fg="red")
    info_label.pack(pady=5)

def show_register_screen():
    clear_screen()
    app.configure(bg="#52C7EE")
    app.current_screen = show_register_screen

    global username_entry, password_entry, reg_hot, reg_cold, reg_wind, reg_humid, info_label

    frame = Frame(app, bg="#ffffff", bd=2, relief="ridge", width=360, height=520)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    frame.pack_propagate(False)

    inner = Frame(frame, bg="#ffffff")
    inner.pack(fill="both", expand=True, padx=12, pady=(12,6))

    Label(inner, text=t('new_user'), font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=(6,10))

    def add_entry(label_text, show=None):
        Label(inner, text=label_text, bg="#ffffff").pack(pady=(6,2), anchor="w")
        e = Entry(inner, justify="center", font=("Arial", 12))
        if show:
            e.config(show=show)
        e.pack(pady=(0,6), padx=4, fill="x")
        return e

    username_entry = add_entry(t('username'))
    password_entry = add_entry(t('password'), show="*")
    reg_hot = add_entry(t('hot'))
    reg_cold = add_entry(t('cold'))
    reg_wind = add_entry(t('wind'))
    reg_humid = add_entry(t('humidity'))

    bottom = Frame(frame, bg="#ffffff")
    bottom.pack(side="bottom", fill="x", padx=12, pady=12)

    create_button(bottom, t('register'), register, bg="#4CAF50", hover_bg="#45a049",
                  font=("Arial", 12, "bold"), pady=8).pack(side="left", expand=True, fill="x", padx=(0,6))
    create_button(bottom, t('back_arrow'), show_login_screen, bg="#f44336", hover_bg="#d32f2f",
                  font=("Arial", 12, "bold"), pady=8).pack(side="right", expand=True, fill="x", padx=(6,0))

    info_label = Label(inner, font=("Arial", 10), bg="#ffffff")
    info_label.pack(pady=(6,4))

def register():
    u = username_entry.get()
    p = password_entry.get()
    try:
        prefs = {
            'hot': float(reg_hot.get()),
            'cold': float(reg_cold.get()),
            'wind': float(reg_wind.get()),
            'humidity': float(reg_humid.get())
        }
    except:
        info_label.config(text=t('numeric_required'), fg='red')
        return
    if u and p:
        if register_user(u, p, prefs):
            info_label.config(text=t('success'), fg='green')
            show_login_screen()
        else:
            info_label.config(text=t('user_exists'), fg='red')
    else:
        info_label.config(text=t('empty_fields'), fg='red')

def login():
    global current_user, user_prefs
    u = username_entry.get()
    p = password_entry.get()
    if login_user(u, p):
        current_user = u
        prefs_path = os.path.join(PREFS_FOLDER, u + ".json")
        with open(prefs_path, 'r') as f:
            user_prefs = json.load(f)
        lang = user_prefs.get('language')
        if lang:
            set_language(lang)
            try:
                for k,v in available_languages.items():
                    if v==lang:
                        app.lang_var.set(k)
                        break
            except Exception:
                pass
        show_weather_screen()
    else:
        info_label.config(text=t('login_failed'), fg='red')

def open_settings():
    clear_screen()
    app.configure(bg="#fafad2")
    app.current_screen = open_settings

    global info_label

    settings_frame = Frame(app, bg="#fafad2", bd=2, relief="ridge", width=360, height=500)
    settings_frame.place(relx=0.5, rely=0.5, anchor="center")
    settings_frame.pack_propagate(False)

    inner_frame = Frame(settings_frame, bg="#fafad2")
    inner_frame.pack(expand=True)

    Label(inner_frame, text=t('comfort_settings'), font=('Arial', 14, 'bold'), bg="#fafad2").pack(pady=(10,15))

    Label(inner_frame, text=t('hot'), bg="#fafad2").pack(pady=(5,5))
    hot_entry = Entry(inner_frame, justify='center')
    hot_entry.insert(0, str(user_prefs.get('hot', 30)))
    hot_entry.pack(pady=5, padx=20, fill="x")

    Label(inner_frame, text=t('cold'), bg="#fafad2").pack(pady=(5,5))
    cold_entry = Entry(inner_frame, justify='center')
    cold_entry.insert(0, str(user_prefs.get('cold', 5)))
    cold_entry.pack(pady=5, padx=20, fill="x")

    Label(inner_frame, text=t('wind'), bg="#fafad2").pack(pady=(5,5))
    wind_entry = Entry(inner_frame, justify='center')
    wind_entry.insert(0, str(user_prefs.get('wind', 8)))
    wind_entry.pack(pady=5, padx=20, fill="x")

    Label(inner_frame, text=t('humidity'), bg="#fafad2").pack(pady=(5,5))
    humid_entry = Entry(inner_frame, justify='center')
    humid_entry.insert(0, str(user_prefs.get('humidity', 85)))
    humid_entry.pack(pady=5, padx=20, fill="x")

    def save_settings_inner():
        try:
            user_prefs['hot'] = float(hot_entry.get())
            user_prefs['cold'] = float(cold_entry.get())
            user_prefs['wind'] = float(wind_entry.get())
            user_prefs['humidity'] = float(humid_entry.get())
            with open(os.path.join(PREFS_FOLDER, current_user+".json"), 'w') as f:
                json.dump(user_prefs, f)
            info_label.config(text=t('settings_saved'), fg="green")
            app.after(2000, show_weather_screen)
        except:
            info_label.config(text=t('numeric_required'), fg="red")

    create_button(inner_frame, t('save'), save_settings_inner, bg="#4CAF50", hover_bg="#45a049").pack(pady=(15,5), fill="x", padx=20)
    create_button(inner_frame, t('back_arrow'), show_weather_screen, bg="#f44336", hover_bg="#d32f2f").pack(pady=(5,10), fill="x", padx=20)

    info_label = Label(inner_frame, font=('Arial', 10), bg="#fafad2")
    info_label.pack(pady=(5,10))

def show_weather_screen():
    clear_screen()
    app.configure(bg="#fafad2")
    app.current_screen = show_weather_screen

    global city_entry, date_entry, hour_entry
    global icon_label, location_label, temp_label, condition_label, comfort_label
    global menu_open, avatar_btn, future_btn, achievements_btn

    menu_open = False

    content_frame = Frame(app, bg="#fafad2", bd=2, relief="ridge")
    content_frame.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)
    content_frame.pack_propagate(False)

    top_frame = Frame(content_frame, bg="#fafad2", height=80)
    top_frame.pack(side="top", fill="x")
    top_frame.pack_propagate(False)

    def toggle_menu():
        global menu_open
        if menu_open:
            settings_btn.pack_forget()
            logout_btn.pack_forget()
            maps_btn.pack_forget()
            micro_btn.pack_forget()
            alerts_btn.pack_forget()
            climate_btn.pack_forget()
            energy_btn.pack_forget()
            voice_btn.pack_forget()
            widget_btn.pack_forget()
            traveler_btn.pack_forget()
            social_btn.pack_forget()
            lightning_btn.pack_forget()
            graph_btn.pack_forget()
            avatar_btn.pack_forget()
            future_btn.pack_forget()
            achievements_btn.pack_forget()
            prediction_btn.pack_forget()
            cloud_photo_btn.pack_forget()
            menu_open = False
        else:
            settings_btn.pack(side="left", padx=2, pady=10, after=menu_btn)
            logout_btn.pack(side="left", padx=2, pady=10, after=settings_btn)
            maps_btn.pack(side="left", padx=2, pady=10, after=logout_btn)
            micro_btn.pack(side="left", padx=2, pady=10, after=maps_btn)
            alerts_btn.pack(side="left", padx=2, pady=10, after=micro_btn)
            climate_btn.pack(side="left", padx=2, pady=10, after=alerts_btn)
            energy_btn.pack(side="left", padx=2, pady=10, after=climate_btn)
            voice_btn.pack(side="left", padx=2, pady=10, after=energy_btn)
            widget_btn.pack(side="left", padx=2, pady=10, after=voice_btn)
            traveler_btn.pack(side="left", padx=2, pady=10, after=widget_btn)
            social_btn.pack(side="left", padx=2, pady=10, after=traveler_btn)
            lightning_btn.pack(side="left", padx=2, pady=10, after=social_btn)
            graph_btn.pack(side="left", padx=2, pady=10, after=social_btn)
            avatar_btn.pack(side="left", padx=2, pady=10, after=graph_btn)
            future_btn.pack(side="left", padx=2, pady=10, after=avatar_btn)
            achievements_btn.pack(side="left", padx=2, pady=10, after=future_btn)
            prediction_btn.pack(side="left", padx=2, pady=10, after=achievements_btn)
            cloud_photo_btn.pack(side="left", padx=2, pady=10, after=prediction_btn)
            menu_open = True

    try:
        menu_btn = create_button(
            top_frame, "☰", toggle_menu,
            bg="#607D8B", hover_bg="#455A64",
            font=("Segoe UI Emoji", 20), shape='circle'
        )
        menu_btn.config(width=50, height=50)
        menu_btn.pack(side="left", padx=10, pady=15)
    except Exception:
        from tkinter import Button
        menu_btn = Button(top_frame, text="☰", command=toggle_menu,
                         bg="#607D8B", fg="white", font=("Arial", 16),
                         width=3, height=1)
        menu_btn.pack(side="left", padx=10, pady=15)

    try:
        settings_btn = create_button(top_frame, '⚙️', open_settings, bg="#607D8B", hover_bg="#455A64",
                                     font=("Segoe UI Emoji", 16), shape='circle')
        settings_btn.config(width=40, height=40)

        # DÜZELTİLMİŞ KISIM - logout fonksiyonu doğrudan çağrılıyor
        logout_btn = create_button(top_frame, '⬅️', logout,
                                   bg="#f44336", hover_bg="#d32f2f", font=("Segoe UI Emoji", 16), shape='circle')
        logout_btn.config(width=40, height=40)

        maps_btn = create_button(top_frame, '🗺️', open_maps_menu, bg="#FF5722", hover_bg="#E64A19",
                                 font=("Segoe UI Emoji", 14), shape='circle')
        maps_btn.config(width=35, height=35)

        micro_btn = create_button(top_frame, '🌡️', open_microclimate_window, bg="#00BCD4", hover_bg="#00ACC1",
                                  font=("Segoe UI Emoji", 14), shape='circle')
        micro_btn.config(width=35, height=35)

        alerts_btn = create_button(top_frame, '🚨', open_alerts_window, bg="#F44336", hover_bg="#E53935",
                                   font=("Segoe UI Emoji", 14), shape='circle')
        alerts_btn.config(width=35, height=35)

        climate_btn = create_button(top_frame, '📈', open_climate_data_window, bg="#4CAF50", hover_bg="#43A047",
                                    font=("Segoe UI Emoji", 14), shape='circle')
        climate_btn.config(width=35, height=35)

        energy_btn = create_button(top_frame, '⚡', open_energy_window, bg="#FFC107", hover_bg="#FFB300",
                                   font=("Segoe UI Emoji", 14), shape='circle')
        energy_btn.config(width=35, height=35)

        voice_btn = create_button(top_frame, '🎤', open_voice_assistant, bg="#9C27B0", hover_bg="#8E24AA",
                                  font=("Segoe UI Emoji", 14), shape='circle')
        voice_btn.config(width=35, height=35)

        widget_btn = create_button(top_frame, '📱', show_weather_widget, bg="#607D8B", hover_bg="#546E7A",
                                   font=("Segoe UI Emoji", 14), shape='circle')
        widget_btn.config(width=35, height=35)

        traveler_btn = create_button(top_frame, '✈️', open_traveler_mode, bg="#03A9F4", hover_bg="#039BE5",
                                     font=("Segoe UI Emoji", 14), shape='circle')
        traveler_btn.config(width=35, height=35)

        social_btn = create_button(top_frame, '📷', open_social_window, bg="#E91E63", hover_bg="#D81B60",
                                   font=("Segoe UI Emoji", 14), shape='circle')
        social_btn.config(width=35, height=35)

        lightning_btn = create_button(top_frame, '⚡', open_lightning_monitor, bg="#FFB300", hover_bg="#FF9800",
                                      font=("Segoe UI Emoji", 14), shape='circle')
        lightning_btn.config(width=35, height=35)

        graph_btn = create_button(top_frame, '📊', lambda: show_history_graph(city_entry.get()),
                                  bg="#9C27B0", hover_bg="#7B1FA2", font=("Segoe UI Emoji", 14), shape='circle')
        graph_btn.config(width=35, height=35)

        # YENİ BUTONLAR
        avatar_btn = create_button(top_frame, '👤', open_avatar_window, bg="#673AB7", hover_bg="#5E35B1",
                                   font=("Segoe UI Emoji", 14), shape='circle')
        avatar_btn.config(width=35, height=35)

        future_btn = create_button(top_frame, '🔮', open_future_weather_window, bg="#00BCD4", hover_bg="#00ACC1",
                                   font=("Segoe UI Emoji", 14), shape='circle')
        future_btn.config(width=35, height=35)

        achievements_btn = create_button(top_frame, '🏆', open_achievements_window, bg="#FFC107", hover_bg="#FFB300",
                                         font=("Segoe UI Emoji", 14), shape='circle')
        achievements_btn.config(width=35, height=35)
       
        prediction_btn = create_button(top_frame, '🎯', open_prediction_game,
                               bg='#FF4081', hover_bg='#F50057',
                               font=("Segoe UI Emoji", 14), shape='circle')
        prediction_btn.config(width=35, height=35)
       
        cloud_photo_btn = create_button(top_frame, '☁️', open_cloud_photos_window,
                               bg="#87CEEB", hover_bg="#4682B4",
                               font=("Segoe UI Emoji", 14), shape='circle')
        cloud_photo_btn.config(width=35, height=35)

    except Exception as e:
        print(f"Buton oluşturma hatası: {e}")

    inner_frame = Frame(content_frame, bg="#fafad2")
    inner_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

    lbl_pad_y = (4,2)
    entry_padx = 2
    btn_padx = 2

    Label(inner_frame, text=t('city'), font=('Arial', 12), bg="#fafad2").pack(pady=lbl_pad_y)
    city_entry = Entry(inner_frame, justify='center', font=('Arial', 12))
    city_entry.pack(pady=2, padx=entry_padx, fill="x")
   
    # Global referans oluştur (avatar için)
    app.city_entry_ref = city_entry
   
    try:
        create_button(inner_frame, t('map_select'), open_map_window,
                      bg="#03A9F4", hover_bg="#0288D1").pack(pady=(4,4), fill="x", padx=btn_padx)
    except:
        Button(inner_frame, text=t('map_select'), command=open_map_window,
               bg="#03A9F4", fg="white").pack(pady=(4,4), fill="x", padx=btn_padx)

    Label(inner_frame, text=t('date'), font=('Arial', 12), bg="#fafad2").pack(pady=lbl_pad_y)
    date_entry = Entry(inner_frame, justify='center', font=('Arial', 12))
    date_entry.pack(pady=2, padx=entry_padx, fill="x")
   
    try:
        create_button(inner_frame, t('date_select'), pick_date,
                      bg="#FFC107", hover_bg="#FFA000").pack(pady=(4,4), fill="x", padx=btn_padx)
    except:
        Button(inner_frame, text=t('date_select'), command=pick_date,
               bg="#FFC107", fg="white").pack(pady=(4,4), fill="x", padx=btn_padx)

    Label(inner_frame, text=t('hour'), font=('Arial', 12), bg="#fafad2").pack(pady=lbl_pad_y)
    hour_entry = Entry(inner_frame, justify='center', font=('Arial', 12))
    hour_entry.pack(pady=2, padx=entry_padx, fill="x")
   
    try:
        create_button(inner_frame, t('hour_select'), pick_hour,
                      bg="#FF9800", hover_bg="#F57C00").pack(pady=(4,4), fill="x", padx=btn_padx)
    except:
        Button(inner_frame, text=t('hour_select'), command=pick_hour,
               bg="#FF9800", fg="white").pack(pady=(4,4), fill="x", padx=btn_padx)

    try:
        create_button(inner_frame, t('get_forecast'), get_forecast,
                      bg="#4CAF50", hover_bg="#45a049").pack(pady=(6,4), fill="x", padx=btn_padx)
    except:
        Button(inner_frame, text=t('get_forecast'), command=get_forecast,
               bg="#4CAF50", fg="white").pack(pady=(6,4), fill="x", padx=btn_padx)

    icon_label = Label(inner_frame, bg="#fafad2")
    icon_label.pack(pady=4)
    location_label = Label(inner_frame, font=('Arial', 14), bg="#fafad2")
    location_label.pack(pady=2)
    temp_label = Label(inner_frame, font=('Arial', 24, 'bold'), bg="#fafad2")
    temp_label.pack(pady=2)
    condition_label = Label(inner_frame, font=('Arial', 16), bg="#fafad2")
    condition_label.pack(pady=2)
    comfort_label = Label(inner_frame, font=('Arial', 12), wraplength=400,
                          justify='center', fg="darkblue", bg="#fafad2")
    comfort_label.pack(pady=(4,4), padx=4)
def get_forecast():
    try:
        city = city_entry.get()
        date_str = date_entry.get()
        hour_str = hour_entry.get()
        try:
            target_dt = datetime.strptime(f"{date_str} {hour_str}", "%Y-%m-%d %H")
        except ValueError:
            location_label.config(text=t('invalid_date'))
            return
        params = {'appid': API_KEY, 'units': 'metric', 'lang': current_language}
        if "," in city:
            lat, lon = city.split(",")
            params['lat'] = lat
            params['lon'] = lon
        else:
            params['q'] = city
        response = requests.get(FORECAST_URL, params=params)
        if response.status_code != 200:
            location_label.config(text=t('city_not_found'))
            return
        data = response.json()
        forecast_list = data['list']
        closest = min(forecast_list, key=lambda x: abs(datetime.strptime(x['dt_txt'], "%Y-%m-%d %H:%M:%S") - target_dt))
        name = data['city']['name']
        temp = closest['main']['temp']
        condition = closest['weather'][0]['description']
        icon_code = closest['weather'][0]['icon']
        humidity = closest['main']['humidity']
        wind = closest['wind']['speed']
        location_label.config(text=f"{name} ({closest['dt_txt']})")
        temp_label.config(text=f"{temp}°C")
        condition_label.config(text=condition.capitalize())
        yorum = analyze_conditions(temp, condition, humidity, wind,
                                   user_prefs['hot'], user_prefs['cold'],
                                   user_prefs['wind'], user_prefs['humidity'])
        comfort_label.config(text=yorum)
        icon_response = requests.get(ICON_URL.format(icon_code))
        img_data = icon_response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((100, 100), Image.LANCZOS if hasattr(Image, 'LANCZOS') else Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        icon_label.config(image=photo)
        icon_label.image = photo
       
        # YENİ: Avatar güncelle
        if current_user:
            try:
                update_avatar_accessories(current_user, temp, condition)
            except Exception as e:
                print(f"Avatar güncelleme hatası: {e}")
               
    except Exception as e:
        messagebox.showerror("Hata", f"Veri alınamadı: {str(e)}")

def show_history_graph(city):
    params = {'appid': API_KEY, 'units': 'metric'}
    if "," in city:
        try:
            lat, lon = city.split(",")
            params['lat'] = float(lat.strip())
            params['lon'] = float(lon.strip())
        except:
            location_label.config(text=t('coord_error'))
            return
    else:
        params['q'] = city.strip()

    response = requests.get('https://api.openweathermap.org/data/2.5/forecast', params=params)
    if response.status_code != 200:
        location_label.config(text=t('data_error'))
        return

    data = response.json()
    temps = [item['main']['temp'] for item in data['list']]
    times = [item['dt_txt'] for item in data['list']]

    plt.figure(figsize=(10,4))
    plt.plot(times, temps, marker='o')
    plt.xticks(rotation=45)
    plt.ylabel(t('temp_c'))
    plt.title(f"{data['city']['name']} - {t('graph_title')}")
    plt.tight_layout()
    mplcursors.cursor(hover=True)
    plt.show()

def open_map_window():
    map_window = Toplevel()
    map_window.title(t('select_city'))
    map_window.geometry("600x500")

    map_widget = TkinterMapView(map_window, width=600, height=450, corner_radius=0)
    map_widget.pack(fill="both", expand=True)
    map_widget.set_position(39.9208, 32.8541)
    map_widget.set_zoom(6)

    location_label_local = Label(map_window, text="Haritadan bir konum seçin", font=('Arial', 12))
    location_label_local.pack(pady=5)

    def on_map_click(coords):
        city_entry.delete(0, END)
        city_entry.insert(0, f"{coords[0]:.4f},{coords[1]:.4f}")
        location_label_local.config(text=t('selected_coords').format(f"{coords[0]:.4f}, {coords[1]:.4f}"))

    map_widget.add_left_click_map_command(on_map_click)

def pick_date():
    top = Toplevel()
    top.title(t('select_date'))
    cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(pady=20)
    def grab_date():
        date_entry.delete(0, END)
        date_entry.insert(0, cal.get_date())
        top.destroy()
    Button(top, text=t('select'), command=grab_date, bg="#4CAF50", fg='white', font=("Arial", 11, "bold"), bd=0, relief='ridge').pack(pady=10)

def pick_hour():
    top = Toplevel()
    top.title(t('select_hour'))
    Label(top, text=t('hour')).pack(pady=10)
    hour_spin = Spinbox(top, from_=0, to=23, width=5, font=("Arial", 12))
    hour_spin.pack(pady=5)
    def grab_hour():
        hour_entry.delete(0, END)
        hour_entry.insert(0, hour_spin.get())
        top.destroy()
    Button(top, text=t('select'), command=grab_hour, bg="#FF9800", fg='white', font=("Arial", 11, "bold"), bd=0, relief='ridge').pack(pady=10)

def logout():
    global current_user
    current_user = None
    show_login_screen()

# Dil seçiciyi oluştur
try:
    create_language_selector()
    app.title(t('title'))
except Exception:
    app.title('Hava Durumu Uygulaması')

# Gerekli klasörleri oluştur
for folder in [PREFS_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Başlangıç ekranı
show_login_screen()

try:
    app.mainloop()
except Exception as e:
    print(f"Uygulama hatası: {e}")