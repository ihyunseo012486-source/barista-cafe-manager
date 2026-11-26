import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="바리스타 카페 키오스크", page_icon="☕", layout="centered")

# 1. 카페 메뉴 데이터 (메뉴명: 가격)
MENU = {
    "아메리카노": 5000,
    "카페라떼": 5000,
    "바닐라라떼": 6000,
    "달고나라떼": 6500,
    "레모네이드": 5500
}

# 2. 세션 상태(장바구니) 초기화
# Streamlit은 버튼을 누를 때마다 코드가 재실행되므로, 장바구니 데이터를 유지하기 위해 session_state를 사용합니다.
if "cart" not in st.session_state:
    st.session_state.cart = []

# --- UI 구성 시작 ---
st.title("☕ 바리스타 카페 주문 시스템")
st.write("원하시는 메뉴와 온도를 선택해 장바구니에 담아주세요. (HOT / ICE 동일 가격)")
st.divider()

# 좌우 2단 컬럼으로 화면 분할 (왼쪽: 메뉴 선택 / 오른쪽: 장바구니 및 결제)
col1, col2 = st.columns([1.2, 1])

# [왼쪽 화면] 메뉴 선택 영역
with col1:
    st.subheader("📋 메뉴 선택")
    
    # 메뉴 선택 드롭다운 (메뉴명과 가격 함께 표시)
    selected_menu = st.selectbox(
        "음료를 선택하세요",
        options=list(MENU.keys()),
        format_func=lambda x: f"{x} ({MENU[x]:,}원)"
    )
    
    # 온도 선택 (레모네이드는 ICE만 가능하도록 예외 처리)
    if selected_menu == "레모네이드":
        temp = st.radio("온도 선택", ["ICE"], horizontal=True)
        st.caption("※ 레모네이드는 아이스 전용 음료입니다.")
    else:
        temp = st.radio("온도 선택", ["HOT", "ICE"], horizontal=True)
        
    # 수량 선택
    quantity = st.number_input("수량", min_value=1, max_value=20, value=1, step=1)
    
    # 장바구니 담기 버튼
    if st.button("🛒 장바구니에 담기", use_container_width=True, type="primary"):
        item_price = MENU[selected_menu]
        
        # 동일한 메뉴 + 동일한 온도 옵션이 이미 장바구니에 있는지 확인
        found = False
        for item in st.session_state.cart:
            if item["menu"] == selected_menu and item["temp"] == temp:
                item["quantity"] += quantity
                item["total_price"] += item_price * quantity
                found = True
                break
        
        # 장바구니에 없는 새로운 조합이면 새로 추가
        if not found:
            st.session_state.cart.append({
                "menu": selected_menu,
                "temp": temp,
                "price": item_price,
                "quantity": quantity,
                "total_price": item_price * quantity
            })
        
        st.success(f"[{temp}] {selected_menu} {quantity}잔이 담겼습니다!")

# [오른쪽 화면] 장바구니 및 결제 영역
with col2:
    st.subheader("🧾 주문 내역 (장바구니)")
    
    if not st.session_state.cart:
        st.info("장바구니가 비어 있습니다.")
    else:
        total_amount = 0
        
        # 장바구니 목록 출력
        for idx, item in enumerate(st.session_state.cart):
            st.write(f"**{idx+1}. [{item['temp']}] {item['menu']}**")
            st.write(f"└ {item['price']:,}원 × {item['quantity']}잔 = **{item['total_price']:,}원**")
            total_amount += item["total_price"]
            
        st.divider()
        st.markdown(f"### 총 결제 금액: :blue[{total_amount:,}원]")
        
        # 결제 및 초기화 버튼 배치
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("🗑️ 비우기", use_container_width=True):
                st.session_state.cart = []
                st.rerun()
        with btn_col2:
            if st.button("💳 주문하기", use_container_width=True, type="primary"):
                st.balloons() # 주문 완료 축하 효과
                st.success("주문이 완료되었습니다! 음료가 준비되면 호출해 드리겠습니다.")
                st.session_state.cart = [] # 주문 완료 후 장바구니 비우기
