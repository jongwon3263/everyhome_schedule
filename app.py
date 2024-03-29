import streamlit as st
import pandas as pd
import itertools
from streamlit_gsheets import GSheetsConnection

st.set_page_config(
    page_icon="💕",
    page_title="에브리홈 일정 뷰어",
    layout="wide"
)

st.sidebar.title('고객 휴대폰 번호(하이픈 포함)')
st.sidebar.text('2024매출표에 있는 자료에 한함')
tab1, tab2 = st.tabs(["메시지", "일정"])

phoneNumber = st.sidebar.text_input("phone")
# indexNumber = st.sidebar.text_input("number")


conn = st.connection("gsheets", type=GSheetsConnection)

data = conn.read(worksheet="everyhome2024")

df = pd.DataFrame(data)
df = df.loc[3650:]

# rowSelected = df.loc[(df.phone == phoneNumber) | [indexNumber]]
rowSelected = df.loc[df.phone == phoneNumber]
# rowSelectedIndex = df.loc[indexNumber]

value_list = rowSelected.values.tolist()

value_list = list(itertools.chain(*value_list))

# 키값
district = value_list[0] #지역
address = value_list[1] #주소
product = value_list[2] #상품군
service = value_list[3] #상세 내역
dayStart = value_list[4] #착수
dayEnd = value_list[5] #마감
customerPhone = value_list[6] #연락처
worker = value_list[7] #시공업체
workerPay = int(value_list[8]) 
workerPay = format(workerPay,',') #업체 단가
customerPrice = format(value_list[9], ',') #고객단가
netProfit = format(value_list[10], ',') #순이익
netProfitMargin = value_list[11] #순이익률
customerName = value_list[12] #고객명
downPayment = format(value_list[13], ',') #계약금
balance = format(value_list[14], ',') #잔금
# balance2 = balance.replace(' ', '')
dayContract = value_list[15] #계약일자
checkPoint = value_list[25] #체크

# # 최종 문장
# customerInfo = f"시공 상품: {product}\n\n[고객정보] \n\n고객명: {customerName} \n\n고객 연락처: {customerPhone}"
# workInfo = f"[현장정보]\n\n주소: {address} \n\n상세내역: {service} \n\n업체: {worker} \n\n시공일자: {dayStart} ~ {dayEnd} "
# bill = f"[가격정보]\n\n고객단가: {customerPrice} \n\n업체 단가: {workerPay} \n\n순이익: {netProfit} \n\n\n예약금: {downPayment} \n\n잔금: {balance} "

# 팀장 전달 메시지
messageForWorker = f"[{dayStart}] 실수령 ₩ {workerPay}원 \n > 고객 잔금 ₩ {balance}원 수령해 주시고 마무리해 주시면 감사하겠습니다 :) \n\n{service}\n\n{address}\n{customerPhone} ({customerName} 고객님)"


tab1.text_area("메모",messageForWorker, height=250)
tab1.text_area("메모", height=500)


tab2.dataframe(df.loc[3790:], height=1500)
