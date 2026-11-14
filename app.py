import streamlit as st

from calculations import calculate_split

st.set_page_config(page_title="Tip & Bill Splitter", page_icon="🧾")
st.title("Tip & Bill Splitter")
st.write("Enter the bill, choose a tip, and split the total between friends.")

with st.form("bill_split_form"):
    number_of_people = st.number_input(
        "Number of people",
        min_value=1,
        value=2,
        step=1,
    )
    bill = st.number_input(
        "Bill amount ($)",
        min_value=0.0,
        value=100.0,
        step=1.0,
        format="%.2f",
    )
    tip_percent = st.number_input(
        "Tip percentage (%)",
        min_value=0.0,
        value=15.0,
        step=1.0,
        format="%.2f",
    )
    submitted = st.form_submit_button("Split bill")

if submitted:
    try:
        bill_amount, tip_amount, shares = calculate_split(
            int(number_of_people), bill, tip_percent
        )
    except ValueError as error:
        st.error(str(error))
    else:
        total = bill_amount + tip_amount
        bill_column, tip_column, total_column = st.columns(3)
        bill_column.metric("Bill", f"${bill_amount:,.2f}")
        tip_column.metric("Tip", f"${tip_amount:,.2f}")
        total_column.metric("Total", f"${total:,.2f}")

        st.subheader("Per-person split")
        for amount in sorted(set(shares), reverse=True):
            count = shares.count(amount)
            st.write(f"{count} person(s) pay **${amount:,.2f}**")

        if len(set(shares)) > 1:
            st.caption(
                "A few people pay one cent more so the shares add up exactly to the total."
            )
