from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import time
import json  # JSON modülünü ekleyin

chrome_options = Options()
chrome_options.add_argument("--headless")  # Tarayıcıyı headless modda çalıştırır
chrome_options.add_argument("--no-sandbox")  # Linux tabanlı sistemlerde gerekebilir
chrome_options.add_argument("--disable-dev-shm-usage")  # Bellek kullanımını azaltır

# Tarayıcıyı başlat
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)

# Banka kampanyalar sayfasına git
url = "https://www.bonus.com.tr/kampanyalar/marka/bonus"  # Bu URL'yi değiştirmelisiniz
driver.get(url)

try:
    # Butonu bekle (15 saniyeye kadar)
    wait = WebDriverWait(driver, 15)
    while True:
        # Engelleyici elementi kontrol et ve gizle
        try:
            checkbox_label = driver.find_element(By.XPATH, "//label[@for='hypeStickyCheckbox']")
            driver.execute_script("arguments[0].style.display='none';", checkbox_label)  # Engelleyici elementi gizle
        except:
            pass  # Engelleyici element yoksa hata verme

        # Butonu bul ve tıklanabilir olup olmadığını kontrol et
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='DAHA FAZLA KAMPANYA GÖSTER']")))
        
        # Buton görünürse tıkla
        if button.is_displayed():
            # JavaScript ile butona tıklama
            driver.execute_script("arguments[0].click();", button)
            # Diğer içeriklerin yüklenmesi için biraz bekle
            time.sleep(2)
        else:
            break  # Buton görünmüyorsa döngüden çık

except Exception as e:
    print("Butona tıklarken bir hata oluştu:", e)

# Sayfanın yüklenmesi için bekle
time.sleep(5)

# Kampanyaları bul ve çek
kampanyalar = driver.find_elements(By.CLASS_NAME, "direct")  # HTML sınıf ismini güncelleyin
kampanya_listesi = []  # Kampanya başlıklarını saklamak için bir liste oluşturun

for kampanya in kampanyalar:
    baslik = kampanya.find_element(By.TAG_NAME, "h3").text  # Tüm metni al
    kampanya_listesi.append(baslik)  # Başlığı listeye ekleyin
    print(baslik + "\n")

# Veriyi bir JSON dosyasına yaz
try:
    with open('../kampanyalar.json', 'w', encoding='utf-8') as f:  # Üst klasöre yaz
        json.dump(kampanya_listesi, f, ensure_ascii=False, indent=4)  # JSON formatında yaz
    print("JSON dosyası kaydedildi: ../kampanyalar.json")  # Dosya kaydedildi mesajı
except Exception as e:
    print("JSON dosyasına yazarken bir hata oluştu:", e)  # Hata mesajı

# Tarayıcıyı kapat
driver.quit()
