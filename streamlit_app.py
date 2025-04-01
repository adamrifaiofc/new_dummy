import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Konfigurasi halaman
st.set_page_config(page_title="Financial Dashboard", layout="wide")

# Membuat dummy data
dates = pd.date_range(start='2023-01-01', end='2023-12-01', freq='MS')
revenue = [10000 * (1.05 ** i) for i in range(12)]  # Pendapatan dengan pertumbuhan 5% per bulan
profit_margins = [0.2 + np.random.uniform(-0.05, 0.05) for _ in range(12)]  # Margin laba bervariasi
expenses = [rev * (1 - pm) for rev, pm in zip(revenue, profit_margins)]  # Pengeluaran
salaries = [exp * 0.5 for exp in expenses]  # Gaji: 50% dari pengeluaran
rent = [exp * 0.2 for exp in expenses]  # Sewa: 20% dari pengeluaran
utilities = [exp * 0.1 for exp in expenses]  # Utilitas: 10% dari pengeluaran
marketing = [exp * 0.2 for exp in expenses]  # Pemasaran: 20% dari pengeluaran
total_expenses = [s + r + u + m for s, r, u, m in zip(salaries, rent, utilities, marketing)]
profit = [rev - exp for rev, exp in zip(revenue, total_expenses)]  # Laba
profit_margin = [p / rev for p, rev in zip(profit, revenue)]  # Margin laba

# Membuat DataFrame
df = pd.DataFrame({
    'Date': dates,
    'Revenue': revenue,
    'Salaries': salaries,
    'Rent': rent,
    'Utilities': utilities,
    'Marketing': marketing,
    'Total_Expenses': total_expenses,
    'Profit': profit,
    'Profit_Margin': profit_margin
})

# Judul dashboard
st.title("Financial Dashboard")

# Menampilkan KPI
total_revenue = df['Revenue'].sum()
total_expenses = df['Total_Expenses'].sum()
avg_profit_margin = df['Profit_Margin'].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Total Pendapatan", f"${total_revenue:,.2f}")
col2.metric("Total Pengeluaran", f"${total_expenses:,.2f}")
col3.metric("Rata-rata Margin Laba", f"{avg_profit_margin:.2%}")

# Grafik garis: Pendapatan dan Pengeluaran
fig1 = px.line(df, x='Date', y=['Revenue', 'Total_Expenses'], 
               title='Pendapatan dan Pengeluaran dari Waktu ke Waktu')
st.plotly_chart(fig1, use_container_width=True)

# Grafik batang: Laba bulanan
fig2 = px.bar(df, x='Date', y='Profit', title='Laba Bulanan')
st.plotly_chart(fig2, use_container_width=True)

# Grafik pie: Distribusi pengeluaran
expense_categories = ['Salaries', 'Rent', 'Utilities', 'Marketing']
expense_totals = df[expense_categories].sum()
fig3 = px.pie(values=expense_totals, names=expense_categories, title='Distribusi Pengeluaran')
st.plotly_chart(fig3, use_container_width=True)

# Tabel data (dapat diperluas)
with st.expander("Tampilkan Data Mentah"):
    st.dataframe(df)
