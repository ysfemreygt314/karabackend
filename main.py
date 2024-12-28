from flask import Flask, request, jsonify
import gspread
from google.oauth2.service_account import Credentials

# Flask uygulaması
app = Flask(__name__)

# Google Sheets için kimlik doğrulama
scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_id = "15XvkmBA52H0mWExMt0z7VfR4GLOVMVOFmcCVodZA8oI"
sheet = client.open_by_key(sheet_id).sheet1

# Veri eklemek için API
@app.route('/add_data', methods=['POST'])
def add_data():
    try:
        # JSON isteği ile gelen veriyi al
        data = request.get_json()
        ad = data['ad']
        email = data['email']
        sinif = data['sinif']

        # Google Sheets'e veri ekle
        sheet.append_row([ad, email, sinif])

        # Başarı mesajı döndür
        return jsonify({"message": "Veri başarıyla eklendi!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Verileri listelemek için API
@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        # Verileri al
        values_list = sheet.get_all_values()
        return jsonify(values_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Flask uygulamasını çalıştır
if __name__ == '__main__':
    app.run(debug=True)
