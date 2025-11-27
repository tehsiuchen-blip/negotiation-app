import streamlit as st
import openai

# 設定網頁標題
st.set_page_config(page_title="談判戰術分析 MVP", page_icon="🕵️")

# 標題區
st.title("🕵️ 商業談判戰術復盤 MVP")
st.info("這是你的 AI 戰術教練。請輸入 API Key 並上傳錄音檔，開始分析。")

# 側邊欄：設定區
with st.sidebar:
    st.header("🔑 啟動設定")
    # 讓使用者輸入金鑰 (密碼模式顯示)
    user_api_key = st.text_input("請輸入 OpenAI API Key", type="password")
    
    if not user_api_key:
        st.warning("請先輸入 Key 才能使用！")
        st.stop()
    
    # 設定 OpenAI 客戶端
    client = openai.OpenAI(api_key=user_api_key)

# 主畫面：上傳區
uploaded_file = st.file_uploader("請上傳談判錄音檔 (支援 mp3, wav, m4a)", type=['mp3', 'wav', 'm4a'])

if uploaded_file is not None:
    st.audio(uploaded_file)
    
    # 分析按鈕
    if st.button("🚀 開始深度分析"):
        try:
            with st.spinner("AI 正在聆聽並分析... (約需 30-60 秒)"):
                # 1. 語音轉文字 (Whisper)
                transcript = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=uploaded_file
                )
                full_text = transcript.text
                
                # 2. 戰術分析 (GPT-4o)
                system_prompt = """
                你是一個頂尖的商業談判心理學家。請分析這段談判逐字稿，輸出以下報告(繁體中文)：
                1. **關鍵時刻診斷**: 找出對話中最關鍵的轉折點，分析當事人的心理狀態。
                2. **口是心非偵測**: 找出對方說的話與可能的真實意圖不符的地方。
                3. **談判主動權**: 估算雙方的主動權佔比 (例如 60/40)，並說明原因。
                4. **下一步戰術建議**: 針對下一次溝通的具體建議。
                """
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"逐字稿內容：\n{full_text}"}
                    ]
                )
                analysis_result = response.choices[0].message.content

            # 顯示結果
            st.success("分析完成！")
            st.markdown("### 📊 戰術復盤報告")
            st.markdown(analysis_result)
            
            # 顯示原始文字
            with st.expander("查看原始逐字稿"):
                st.write(full_text)
            
        except Exception as e:
            st.error(f"發生錯誤：{str(e)}")
