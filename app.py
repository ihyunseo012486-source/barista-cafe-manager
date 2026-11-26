import streamlit as st

st.set_page_config(page_title="바리스타 카페 키오스크", page_icon="☕", layout="centered")

# [필수 요소 1: 리스트] 메뉴명, 가격, 온도 옵션을 리스트로 정의
MENU_NAMES = ["아메리카노", "카페라떼", "바닐라라떼", "달고나라떼", "레모네이드"]
MENU_PRICES = [5000, 5000, 6000, 6500, 5500]
TEMP_OPTIONS = ["HOT", "ICE"]

# 장바구니를 저장할 리스트 초기화
if "cart" not in st.session_state:
    st.session_state.cart = []


# [필수 요소 2: 함수] 1) 선택한 메뉴의 가격을 찾아 반환하는 함수
def get_menu_price(selected_name):
    # [필수 요소 3: 반복구문] 메뉴 리스트를 순회하며 인덱스 찾기
    for i in range(len(MENU_NAMES)):
        # [필수 요소 4: 선택구문] 일치하는 메뉴명을 찾으면 해당 인덱스의 가격 반환
        if MENU_NAMES[i] == selected_name:
            return MENU_PRICES[i]
    return 0


# [필수 요소 2: 함수] 2) 장바구니 리스트에 주문을 추가하는 함수
def add_to_cart(cart_list, menu, temp, price, qty):
    is_exist = False
    
    # [필수 요소 3: 반복구문] 장바구니 리스트 안의 기존 주문 내역 확인
    for item in cart_list:
        # [필수 요소 4: 선택구문] 메뉴와 온도가 모두 같으면 수량과 금액만 누적
        if item["menu"] == menu and item["temp"] == temp:
            item["qty"] += qty
            item["subtotal"] += price * qty
            is_exist = True
            break
            
    # [필수 요소 4: 선택구문] 장바구니에 없는 새로운 주문이면 리스트에 새로 추가
    if not is_exist:
        cart_list.append({
            "menu": menu,
            "temp": temp,
            "price": price,
            "qty": qty,
            "subtotal": price * qty
        })


# [필수 요소 2: 함수] 3) 장바구니의 총 결제 금액을 계산하는 함수
def calculate_total(cart_list):
    total = 0
    # [필수 요소 3: 반복구문] 장바구니의 모든 항목 금액을 반복해서 더하기
    for item in cart_list:
        total += item["subtotal"]
    return total


# ================= 화면(UI) 구성 =================
st.title("☕ 바리스타 카페 주문 시스템")
st.write("원하시는 메뉴와 온도(HOT / ICE)를 선택해 주세요. (옵션 추가 금액 없음)")
st.divider()

col1, col2 = st.columns([1.2, 1])

# [왼쪽 화면] 메뉴 선택 및 장바구니 담기
with col1:
    st.subheader("📋 메뉴 선택")
    
    # 메뉴 선택 (함수 get_menu_price를 호출해 가격 함께 표시)
    selected_menu = st.selectbox(
        "음료를 선택하세요",
        options=MENU_NAMES,
        format_func=lambda x: f"{x} ({get_menu_price(x):,}원)"
    )
    
    # [필수 요소 4: 선택구문] 레모네이드는 아이스만 선택 가능하도록 분기 처리
    if selected_menu == "레모네이드":
        selected_temp = st.radio("온도 선택", ["ICE"], horizontal=True)
        st.caption("※ 레모네이드는 ICE 전용 메뉴입니다.")
    else:
        selected_temp = st.radio("온도 선택", TEMP_OPTIONS, horizontal=True)
        
    quantity = st.number_input("수량 선택", min_value=1, max_value=20, value=1, step=1)
    
    if st.button("🛒 장바구니 담기", use_container_width=True, type="primary"):
        price = get_menu_price(selected_menu)
        add_to_cart(st.session_state.cart, selected_menu, selected_temp, price, quantity)
        st.success(f"[{selected_temp}] {selected_menu} {quantity}잔이 담겼습니다!")

# [오른쪽 화면] 주문 내역 확인 및 결제
with col2:
    st.subheader("🧾 주문 내역")
    
    # [필수 요소 4: 선택구문] 장바구니 리스트가 비어있는지 확인
    if len(st.session_state.cart) == 0:
        st.info("장바구니가 비어 있습니다.")
    else:
        # [필수 요소 3: 반복구문] 장바구니 리스트의 주문 항목을 하나씩 화면에 출력
        for idx, item in enumerate(st.session_state.cart):
            st.write(f"**{idx + 1}. [{item['temp']}] {item['menu']}**")
            st.write(f"└ {item['price']:,}원 × {item['qty']}잔 = **{item['subtotal']:,}원**")
            
        st.divider()
        
        # 함수를 호출해 총 결제 금액 계산
        final_price = calculate_total(st.session_state.cart)
        st.markdown(f"### 총 결제 금액: :blue[{final_price:,}원]")
        
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("🗑️ 전체 비우기", use_container_width=True):
                st.session_state.cart = []
                st.rerun()
        with btn_col2:
            if st.button("💳 주문 완료", use_container_width=True, type="primary"):
                st.balloons()
                st.success("주문이 접수되었습니다! 감사합니다.")
                st.session_state.cart = []
