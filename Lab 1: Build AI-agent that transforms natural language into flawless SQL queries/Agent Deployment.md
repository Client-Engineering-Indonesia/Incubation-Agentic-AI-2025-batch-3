# 🤖Membuat AI Agent dengan **watsonx.ai** & **LangGraph**

Pada lab ini, kita akan membuat **Data Analyzer** dengan memanfaatkan *watsonx.AI Agent Lab*. Agent ini akan menganalisis data Customer yang mengakses BTS.

> **Catatan** File‐file yang diperlukan dapat diunduh dari folder “📂 Assets”.

---

# 🧭Tahapan Pembuatan Agent

## _Step 1 — Membuat *Project*_

1. Scroll kebawah lalu buat Project baru di **Watsonx.AI** dengan menekan tombol "+".

![5.Create new Project for agent](https://github.com/Client-Engineering-Indonesia/workshop-telco-tower-ai/blob/main/Lab2-AgenticAI%20in%20watsonxAI/Assets/5.Create%20new%20Project%20for%20agent.png)

2. Menamai dan membuat project baru.

![Creat a  Project](https://github.com/user-attachments/assets/1282049d-f55e-47f6-9ff9-e176dd3e4af8)

---

## 🔗 _Step 2 — Mengasosiasikan watsonx.ai Runtime_

1. Buka Halaman Project dan tekan **Manage**

![6.Press Manage](https://github.com/Client-Engineering-Indonesia/workshop-telco-tower-ai/blob/main/Lab2-AgenticAI%20in%20watsonxAI/Assets/6.Press%20Manage.png)

2. Buka **Services & Integrations → Associate Service**.

![7.Press Service Integration](https://github.com/Client-Engineering-Indonesia/workshop-telco-tower-ai/blob/main/Lab2-AgenticAI%20in%20watsonxAI/Assets/7.Press%20Service%20Integration.png)

3. Pilih **watsonx.ai** lalu kaitkan dengan project.

![9.Instance to associate](https://github.com/user-attachments/assets/3e22c81c-288c-445c-a5c8-6cffb5976012)

---

### 🗂️ _Step 3 — Menambahkan *Asset* Baru_
1. Masuk ke tab **Assets** dan klik **New Asset**.

![10.Make a New Asset](https://github.com/Client-Engineering-Indonesia/workshop-telco-tower-ai/blob/main/Lab2-AgenticAI%20in%20watsonxAI/Assets/10.Make%20a%20new%20Assets.png)

---

### 🧠 _Step 4 — Buat AI Agent_
- Klik **New Asset** di sisi kiri dan pilih **Build an AI Agent to Automate Tasks**.

![Build AI Agent](https://github.com/user-attachments/assets/c6dde849-5455-45a8-a82d-9cd11b135933)

## 📝 _Step 5 - Instruksi ke agent_

1. Masukan text di **Agent instructions** sesuai dengan kebutuhan dan fungsi yang dibutuhkan

```text
You are a helpful assistant that uses tools to answer questions in detail.
When greeted, say "Hi, I am watsonx.ai agent. How can I help you?""
```

2. Kemudian, apabila ada instruction yang lebih spesifik bisa ditambahkan juga ke dalam **Common instructions** dalam pilihan **Advance Configuration** pada pojok kanan atas.

```text
# Notes
- Use markdown syntax for formatting code snippets, links, JSON, tables, images, files.
- Any HTML tags must be wrapped in block quotes, for example ```<html>```.
- When returning code blocks, specify language.
- Sometimes, things don't go as planned. Tools may not provide useful information on the first few tries. You should always try a few different approaches before declaring the problem unsolvable.
- When the tool doesn't give you what you were asking for, you must either use another tool or a different tool input.
- When using search engines, you try different formulations of the query, possibly even in a different language.
- You cannot do complex calculations, computations, or data manipulations without using tools.
- If you need to call a tool to compute something, always call it instead of saying you will call it.

#Main Notes:
1. Always prioritizing the DB2_query tools for the information related to CUSTOMER data or table.
2. use Google Search after if DB2_querry tools cannot give an answer.
```

![Agent Instruction](https://github.com/user-attachments/assets/062cc7ad-4510-4c08-91cc-9f2b0a94d64d)


## 🧰 _Step 6 — Tambahkan Tools untuk Agent_
Di dalam Agent lab watsonx.ai, kita dapat menambahkan tools yang sudah tersedia atau bisa mengkostumisasi tools sebgai berikut:

1. Tools di **Add atool**
  ![Add Tool](https://github.com/user-attachments/assets/31d08bd7-606c-4d93-8eab-47ea54a56f55)

Pada Bagian ini kita cukup menambahkan Google Search sebagai tools yang akan digunakan.

## 🛠️ _Step 7 — Tambahkan Custom Tools untuk Agent_
Pada step ini, kita hanya menggunakan custom tool dikarenakan data yang digunakan merupakan data structured yang harus dikoneksikan ke dalam DB2.
oleh karnea itu kita akan menambahkan custom tool dalam Agent lab watsonx.AI.

Dan untuk workshop kali ini kami telah menyiapkan custom tools sebagai berikut:

## Tools di **Create custom tool**
![Add Tool](https://github.com/user-attachments/assets/74596736-0460-45b7-a394-f7323859826c)

### 1. Tool **db2tool**

- Notes: parameter dibawah dapat langsung di _copy_ dan _paste_ pada tempat seperti gambar diatas.

#### Name: ```DB2_query```
     
#### Tool description:

    ```text
    Query the CUSTOMER table in DB2. Ensure that all queries related to this table are passed through the DB2 tool for execution, make sure to pass all query with this tool.
    ```
    
#### Input JSON Schema

```json
{
"question": {
"title": "question",
"description": "This parameter is an original question asked by the user.",
"type": "string"
}
}
```
    
#### Python code:
    
```python
def db2_init(question):
    import ibm_db, ibm_db_dbi as dbi
    import pandas as pd
    import requests
    import ast

    #============== Token Generator =========================#
    token_url = "https://iam.cloud.ibm.com/identity/token"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    data = {
        'grant_type': 'urn:ibm:params:oauth:grant-type:apikey',
        'apikey': <"API KEY">
    }

    response = requests.post(token_url, headers=headers, data=data, verify=False)
    iam_token = response.json().get('access_token')

    payload_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {iam_token}'
    }

    #============== Step 1: Create Text To SQL ==============#
    texttosql_url = "https://us-south.ml.cloud.ibm.com/ml/v1/deployments/01e168d6-eec9-4e2c-9a1f-2134fde2e8bf/text/generation?version=2021-05-01"
    texttosql_data = {
        "parameters": {
            "prompt_variables": {
                "question": f"'{question}'"
            }
        }
    }

    texttosql_response = requests.post(texttosql_url, headers=payload_headers, json=texttosql_data)
    texttosql_response = texttosql_response.json()['results'][0]['generated_text']
    texttosql_response = ast.literal_eval(texttosql_response)['query']

    #============ Step 2: Get Data from Db2 =====================#
    DB2_HOST = 'b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud'
    DB2_PORT = '31249'
    DB2_USERNAME = 'klq31162'
    DB2_PASSWORD = '<PASS>'
    
    db2_dsn = 'DATABASE={};HOSTNAME={};PORT={};PROTOCOL=TCPIP;UID={uid};PWD={pwd};SECURITY=SSL'.format(
        'bludb',
        DB2_HOST,
        DB2_PORT,
        uid=DB2_USERNAME,
        pwd=DB2_PASSWORD
    )

    db2_connection = dbi.connect(db2_dsn)
    answer_df = pd.read_sql_query(texttosql_response, con=db2_connection)
    json_data = answer_df.to_json(orient='records')
    
    return json_data
```


## ⚙️ _Step 8— Konfigurasi Model & Parameter Agent_

Pada step ini kita dapat meng-konfiguurasi parameter dan dapat memilih untuk menggunakan model yang sesuai dengan kebutuhan kita.

Pada workshop kali ini kita akan menggunakkan settingan default yaitu dengan tidak merubah apapun.

Selanjutnya kita bisa untuk mengkonfigurasikan model dan parameter
![Add Tool](https://github.com/user-attachments/assets/3f3f10d8-d993-4694-a12c-e30b54d5b1d7)

- Konfigurasi model
  ![Add Tool](https://github.com/user-attachments/assets/58bd73b3-0777-4e0d-a376-a83d75bd7541)
  
- Konfigurasi parameter
  ![Add Tool](https://github.com/user-attachments/assets/3f3f10d8-d993-4694-a12c-e30b54d5b1d7)
  <img width="1237" alt="image" src="https://github.com/user-attachments/assets/6e4875be-2be3-410f-bac9-bf31c8268673" />

## 🧪 _Step 9 — Test Agent_
Coba pertanyaan berikut:
### **Natural Langguage to SQL (Data Analyzer) Agent**

- how many customer do we have?
- which provider has the biggest avg GB use?
- show me how much each providers average monthly charge.
- What is the reason Telkomsel charge less than other Providers?

## 👀Step 10 — Lihat Respon Agent

![16. Test the AI Agent with the question](https://github.com/Client-Engineering-Indonesia/workshop-telco-tower-ai/blob/main/Lab2-AgenticAI%20in%20watsonxAI/Assets/16.%20Test%20the%20AI%20Agent%20with%20the%20questions.png)

## 💾 _Step 11 — Simpan Agent_

![Save Agent](https://github.com/user-attachments/assets/3c0363a7-cfdf-481a-b365-9ccc0fb1686e)

## 📤 _Step 12 — Export Agent_
- Simpan agent ke dalam notebook atau file yang bisa diedit untuk modifikasi selanjutnya.

![Export Agent](https://github.com/user-attachments/assets/3b1d61d0-7285-4621-88cf-8144cee6f598)
![Export Agent](https://github.com/user-attachments/assets/9f92307a-8808-449d-8bcd-3fe73d43258e)

---
