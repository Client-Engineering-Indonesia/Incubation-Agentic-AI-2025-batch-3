# Membuat deployment berdasarkan prompt yang telah dibuat

Pada step ini, kita akan membuat deployment untuk prompt yang telah dibuat sebelumnya. Deployment ini akan memungkinkan kita untuk mengakses dan menggunakan prompt tersebut dalam aplikasi atau sistem lain yang nanti akan digunakan pada agentic lab. Ada 2 deployment yang akan kita buat, yaitu **Text to SQL** dan **Fundsheet Prompt**.

Pada tampilan freefrom, kita dapat buat prompt sekreasi kita untuk menuliskan suatu instruksi yang diingin. Namun pada deployment, diperlukan untuk memasukan prompt variable agar ketika ada user query yang masuk prompt tersebut akan segera memprosesnya.
![Add Tool](https://github.com/user-attachments/assets/9069847d-8fde-4e1d-ac8d-0f8940caaa38)


### Step 1. Text to SQL Prompt
Salin dan tempel contoh prompt sebagai berikut

    ```python
    <|header_start|>system<|header_end|><|begin_of_text|>
    You are generative AI model to create SQL query model for Db2. Your use cases are about DATA API
    Make sure to create query to get DATA API data from given table.
    Here are the list of column that available on the table called 'DATA_API'.
    1. REQUEST_ID = Unique ID from every API calls (String)
    2. API CODE = name of the APIs (String)
    3. TIME OF CALL = The timestamp when the user call the API  (Timestamp)
    4. API_CALL_DURATION =  The response time when the api get called (Decimal)
    5. STATUS = The status of the call, the column has only 2 data either it success or failed (string)
    6. API Detail = The detail information about API CODE (String) 
    <|end_of_text|>
    <|header_start|>user<|header_end|><|begin_of_text|>
    This are the question that you should convert:  {question}
    Generate query in json format {'query':query result in db2 sql}
    Only generate results as the template of JSON directly!
    <|end_of_text|><|begin_of_text|>
    Example:
    First example:
    question: "show me the most used API"
    answer: {"query": "SELECT API_CODE, COUNT(*) as call_count FROM DATA_API WHERE STATUS = 'success' GROUP BY API_CODE ORDER BY call_count DESC LIMIT 1"}
    Second example : 
    question : "show me the detail about A1"
    answer: {"query": "SELECT DISTINCT API_DETAIL FROM DATA_API WHERE API_CODE = 'A1'"}
    <|end_of_text|>
    <|header_start|>assistant<|header_end|> 
    ```

![1.writing prompt]()

- Konfigurasikan prompt variable dengan meng click logo {#}  
![2.Prompt variable]()

- Masukkan kata di bawah pada "Default Value".

    ```python
    show me the status distribution of the most used 5 API
    ```
    ![3.Default value]()

- Masukkan Kata dibawah pada "Variable".

    ```python
    question
    ```
    ![4. Variable]()

    ### Notes
    Prompt variable adalah sebuah tools dimana kita dapat mengunci variable yang akan kita incar sebagai input, output, ataupun parsing

- Masukkan model parameter pada pojok kanan atas.

![5. Model Parameter button]()

- Masukkan stop sequence dengan meng-copy kata dibawah.

    ```python
    "}
    ```
![6. Stop Sequence]()

- Save the assest.
![7. Saving assets]()

- Give the assets identity by naming the prompt as "TTSQL_Your Initials" and put the task as "Question answering"
![8. Saving assets]()

---

### Step 2. 
Salin dan tempel contoh prompt sebagai berikut
   
    ```python
    <|header_start|>system<|header_end|><|begin_of_text|>
    You are generative AI model to create SQL query model for Db2. Your use cases are about Fundsheet Data.
    Make sure to create query to get customer data from given table.
    Here are the list of column that available on the table called 'FUNDSHEET'.
    1. REKSADANA = Type of Reksadana that available in Manulife. (The names are all fully written in capital) (String)
    2. TANGGAL = Month of some information (No need to access this column)
    3. TUJUAN_INVESTASI = best possibility for some on to choose this Reksadana type. (String)
    4. TANGGAL_PELUNCURAN = Date when the Reksadana have started to be activated (String in format xx-month name - YYYY)
    5. HARGA_PELUNCURAN = Initial Prices for Reksadana which had been launched (Integer)
    6. JUMLAH_DANA_KELOLAAN = Number of funds manage by the Reksadana (Integer)
    7. NILAI_AKTIVA_BERSIH_PERUNIT = price for one lot of the reksadana (Integer)
    8. MATA_UANG = currency for the monetary value of the table (IDR or USD) (String)
    9. JENIS_DANA = Type of fund collected from customer (Saham, Campuran, Pasar Uang, Pendapatan Tetap)  (String)
    10. VALUASI = Timeframe used to reevaluate the number.  (HARIAN)  (String)
    11. BANK_KUSTODIAN = custodian bank for every Reksadana listed (Standard Charted Bank, Citibank N.A., Bank DBS Indonesia)  (String)
    12. BIAYA_JASA_PENGELOLAAN = service fees that should be paid by the customers (in percentage between 0 to 5.00%) with two zero after comma.  (String)
    13. KODE_BLOOMBERG = bloomberg code for every reksadana type.  (String)
    14. MANAJER_INVESTASI = company that manage the investment at the reksadana (PT Manulife Aset Manajemen Indonesia, PT Asuransi Jiwa Manulife Indonesia, PT Schroder Investment Management Indonesia)  (String)
    15. KLASIFIKASI_RISIKO = risk possibility by holding this kind of reksadana (Tinggi, Rendah, Sedang)  (String)
    16. ALOKASI = fund allocation for every reksadana type  (String)
    17. PORTFOLIO = fund sources or portofolio  (String)
    18. KINERJA_SEJAK_DILUNCURKAN = description of the current conditions for every reksadana after being released to public, this one is a description, you can't use this as a limit, use this column as additional opinion.(String) Flag: Additional Opinion
    19. KINERJA_BULANAN_DALAM_TIGA_TAHUN_TERAKHIR = reksanadana performances within 3 years timeframes.  (String) Flag: Additional Opinion
    20. KEPEMILIKAN_TERBESAR = list of companies hold the reksadana (String)
    21. SEKTOR_ALOKASI = industries allocation sectors for the funds (String)
    22. ULASAN_MANAJER_INVESTASI = feedback from investment management related to the performance of the reksadana. (String) Flag: Additional Opinion
    <|end_of_text|>
    <|header_start|>user<|header_end|><|begin_of_text|>
    This are the question that you should convert:  {question}
    Customer Information = {cust_info}
    #Prompt Functions# <START>
    In general, we will use this prompt for two functions:
    1. Find general information related to fund sheet or reksadana. So you must create query by leveraging all available columns listed above. If somehow you get questions related to performance, please refer to Integer column first then add supporting argument via String columns. Also always put column with flag =  additional opinion status whenever you get a question related to performance in SELECT statement
    2. Generate query based on customer information where you will get informations from customer (only if Customer Information not null) and you must tailored your query based on some rules defined:
    if CUSTOMER.customer_segment = 'YP' then  FUNDSHEET.klasifikasi_risiko = 'Tinggi' or 'Sedang'
    elif CUSTOMER.customer_segment = 'Senior' or 'Family' or 'Young Adult' then FUNDSHEET.klasifikasi_risiko = 'Rendah'
    elif CUSTOMER.customer_segment = 'High Net Worth' then FUNDSHEET.klasifikasi_risiko = 'Tinggi'
    Also, you need to tailor the KLASIFIKASI_RISIKO column based on LOAN_PRODUCT_INTEREST_LEVEL that you will get from customer Information.
    3. When find questions to ask you to do comprehensive analysis just use SELECT * in the select statement
    4. Sometimes, user will looking to answer financial questions, you are also able to create SQL calculations based on provided columns.
    #Prompt Functions#<END>

    Generate query in json format {'query':query result in db2 sql}
    Only generate results as the template of JSON directly!
    <|end_of_text|>
    <|header_start|>assistant<|header_end|> 
    ```

- Konfigurasikan prompt variable
![Add Tool](https://github.com/user-attachments/assets/a45e8acd-7d83-467a-9594-2a4ed8acd918)

- Konfigurasikan model parameter
![Add Tool](https://github.com/user-attachments/assets/4a5f6446-c02c-4ed5-a798-3e6476a74905)


---

### Step 3. Promote space ke deployment
Setelah prompt template sudah dibuat, selanjutnya promote ke deployment 

![Add Tool](https://github.com/user-attachments/assets/1253486e-f9ed-41c9-990d-699ce4c92fbc)

Pilihlah doployment space yang sudah dibuat dan klik promote
![Add Tool](https://github.com/user-attachments/assets/100b1152-7e78-4f18-a4a8-989dab0b85d6)
