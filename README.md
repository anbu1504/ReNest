# **ReNest**  

## 🚀 Overview  
*ReNest is a web application that allows clothing e-commerce businesses to upload an image of a returned piece of clothing, determine how repairable that clothing item is, and determine what to do with said clothing item. The options of what to do with a returned piece of clothing are resell, donate, or discard. The repairability score (which ranges from 1 to 10) and possible donation centers are determined by Google Gemini (gemini-flash-1.5).*

## 🎯 Problem Statement  
*Retailers struggle to efficiently route returned items to secondary markets, such as resale platforms, liquidation channels, or donation programs. This is an important problem due to this inefficient routing; over 5 billion pounds of waste is generated through returns annually in the U.S. alone, highlighting the negative environmental impact that e-commerce has.*  

## 💡 Solution  
*Our AI-powered system optimizes reverse logistics and resale routings by feeding in the image to Google Gemini with a descriptive prompt to accurately determine how "repairable" a returned piece of clothing is. If the repairability score is between 1 and 4, we advise the e-commerce business to trash the item. If the repairability score is between 5 and 7, we advise the e-commerce business to donate the item. In the donating case, we ask the company to enter the city that their company is based in, and with the help of Google Gemini (with its separate descriptive prompt), we return 5 charities in that city. Otherwise, if the repairability score is above an 8, we advise the e-commerce business to donate that item.*


## 🛠️ Tech Stack  
- **Frontend:** HTML/CSS 
- **Backend:** Python
- **APIs:** Google Gemini API
- **Libraries:** google.generativeai, Flask, os, dotenv

## 📖 How It Works  
1. **User Input:** User uploads an image of a piece of returned clothing
2. **AI Processing:** Google Gemini determines how repairable that piece of clothing is on a scale from 1 to 10.
3. **Reports** Determines whether the item is resealable, donatable, or if it needs to be discarded.
4. **Donation Case AI Processing:** In the case where we can donate a piece of clothing, then we prompt the user to enter their city and use Gemini to produce 5 charities/donation cneters that are in that city.

## 🔧 Installation & Setup  
1. **Clone the repository:**  
   ```bash
   git clone https://github.com/your-username/project-name.git
   cd project-name
   ```  
2. **Install dependencies:**  
   ```bash
   pip install flask google-generativeai python-dotenv
   ```  
3. **Set up environment variables:**  
   - Create a `.env` file and add an API key for Google Gemini (through https://aistudio.google.com/).  
4. **Run the application:**  
   ```bash
   python3.10 app.py

   # NOTE: If the port number does not work (i.e. https:127.0.0.1:xxxx, where xxxx is the port number)
   # then go to line 132 on app.py and specify a port number of your choice:
   # Example:
   # if __name__ == "__main__":
   #   app.run(debug=True, port=xxxx)
   ```  


## 👥 Team  
| Name  
|---|
| Abbirah Athithan | 
| Shivansh Dube | 
| Ashmann Jaain |
| Rishika Jain |
| Anbuselvan Ragunathan |
