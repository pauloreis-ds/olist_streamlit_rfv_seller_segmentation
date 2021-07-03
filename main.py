import pandas as pd
import streamlit as st
from olist_utils import graph


def count_classes_observations(series):
    count = pd.concat([series.value_counts(), series.value_counts(normalize=True)*100], axis=1)
    count.columns = ["quantity_of_sellers", "percentage"]
    return count


def space(spaces):
    for space in range(spaces):
        st.markdown("#")


if __name__ == '__main__':
    img = 'https://raw.githubusercontent.com/pauloreis-ds/Paulo-Reis-Data-Science/master/Paulo%20Reis/PRojects.png'
    st.set_page_config(page_title='Seller RFV Segmentation', page_icon=img, layout="centered")

    show_details = st.checkbox("Technical Details")
    if show_details:
        query ='''
        SELECT orders.order_id AS order_id,
               order_approved_at AS order_approved_at,
               order_purchase_timestamp AS purchase_date,
               price AS price,
               order_items.seller_id AS seller_id
        FROM orders LEFT JOIN order_items ON orders.order_id = order_items.order_id
                    LEFT JOIN sellers ON order_items.seller_id = sellers.seller_id;'''
        st.markdown("**Data was queried from PostgreSQL as:**")
        st.text(f"{query}")
        link = "https://github.com/pauloreis-ds/olist/blob/main/business_questions_insights/streamlit_rfv_seller_segmentation_app/streamlit_rfv_seller_segmentation.py"
        st.markdown(f"**and [processed]({link}) in Python Pandas.**")

        st.markdown("**Entity–Relationship Model:**")
        st.image("images/mer.png", width=800)

    sellers_sgmt_abt = pd.read_csv("data/sellers_sgmt_abt.csv")

    st.markdown("## Statistics")
    seller_status_df = count_classes_observations(sellers_sgmt_abt['seller_status'])
    st.dataframe(seller_status_df)

    seller_rank_df = count_classes_observations(sellers_sgmt_abt['value_frequency_segment'])
    st.dataframe(seller_rank_df, width=520)

    space(2)
    sellers_stats = sellers_sgmt_abt.groupby("value_frequency_segment").agg(['mean', 'sum'])[
        ['total_revenue', 'orders_quantity']]
    st.dataframe(sellers_stats)
    sellers_stats = sellers_sgmt_abt.groupby("value_frequency_segment").agg(['mean', 'sum'])[
        ['revenue_per_month', 'orders_per_month']]
    st.dataframe(sellers_stats)

    space(3)
    legend_order = ['ACTIVE', 'INACTIVE', 'NEW SELLER']
    palette = ['#1f77b4', '#c1c0b9', '#2ca02c']
    st.pyplot(graph.scatterplot(data=sellers_sgmt_abt, x='frequency_rank', y='value_rank',
                                hue='seller_status', hue_order=legend_order,
                                x_label="Frequency Rank", y_label="Value Rank",
                                title="Seller Activity Status", palette=palette))
    space(2)
    st.pyplot(graph.scatterplot(data=sellers_sgmt_abt, x='orders_per_month', y='revenue_per_month',
                                hue='seller_status', hue_order=legend_order,
                                x_label="Orders per month", y_label="Revenue per month (BRL)",
                                title="Seller Activity Status", palette=palette, x_lim=[-1, 20], y_lim=[-1, 2000]))

    space(2)
    legend_order = ['SUPER PRODUCTIVE', 'PRODUCTIVE', 'HIGH VALUE', 'HIGH FREQUENCY', 'LOW VALUE LOW FREQUENCY']
    palette = ['#ff7f0e', '#1f77b4', '#2ca02c', '#9467bd', '#d62728']
    st.pyplot(graph.scatterplot(data=sellers_sgmt_abt, x='frequency_rank', y='value_rank',
                                hue='value_frequency_segment', hue_order=legend_order,
                                x_label="Frequency Rank", y_label="Value Rank",
                                title="RFM Seller Segmentation", palette=palette))
    space(2)
    st.pyplot(graph.scatterplot(data=sellers_sgmt_abt, x='orders_per_month', y='revenue_per_month',
                                hue='value_frequency_segment', hue_order=legend_order,
                                x_label="Orders per month", y_label="Revenue per month (BRL)",
                                title="RFM Seller Segmentation", palette=palette, x_lim=[-1, 20], y_lim=[-1, 2000]))

