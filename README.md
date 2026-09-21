# FLO Customer Segmentation with RFM Analysis

This project uses RFM analysis to segment FLO’s omnichannel customers based on their purchasing behavior and identify target audiences for marketing campaigns.

## Business Problem

FLO aims to better understand its customers and develop marketing strategies for different customer groups. The analysis focuses on identifying loyal customers, customers at risk of becoming inactive, and potential audiences for category-specific campaigns.

## Dataset

The dataset contains historical shopping information for omnichannel customers whose most recent purchases occurred in 2020–2021.

Key variables include:

- Customer ID
- First and last purchase dates
- Online and offline order counts
- Total spending across online and offline channels
- Shopping channels
- Categories purchased from in the last 12 months

The script expects the dataset at `datasets/flo_data_20k.csv`.

## Methodology

1. Explore the dataset and prepare date fields.
2. Combine online and offline purchases to calculate total orders and spending.
3. Calculate RFM metrics using **June 1, 2021** as the analysis date:
   - **Recency:** Days since the customer's last purchase.
   - **Frequency:** Total number of purchases.
   - **Monetary:** Total customer spending.
4. Assign scores from 1 to 5 using quantile-based groups.
5. Map Recency and Frequency scores to customer segments.
6. Summarize segment characteristics and export campaign target lists.

Monetary scores are included in the RFM score, while segment labels are determined by Recency and Frequency scores.

## Customer Segments

Customers are assigned to ten segments:

- Champions
- Loyal Customers
- Potential Loyalists
- New Customers
- Promising
- Need Attention
- About to Sleep
- At Risk
- Can't Lose
- Hibernating

## Marketing Use Cases

### 1. New Women's Footwear Brand

Identify customers in the **Champions** and **Loyal Customers** segments who purchased from the women's category in the last 12 months.

Output: `yeni_marka_hedef_müşteri_id.csv`

### 2. Men's and Children's Category Promotion

Identify customers in the **Can't Lose**, **Hibernating**, and **New Customers** segments who purchased from the men's or children's categories in the last 12 months.

Output: `indirim_hedef_müşteri_ids.csv`

Both files contain customer IDs for the selected campaign audiences.

## Tools

- Python
- pandas
- datetime

## How to Run

1. Install the required dependency:

   ```bash
   pip install pandas
   ```

2. Place the dataset at `datasets/flo_data_20k.csv`.

3. Run the script from the repository root:

   ```bash
   python flo_rfm.py
   ```

The campaign CSV files are saved in the working directory.

## Reusable RFM Function

The script includes `create_rfm(dataframe)`, which prepares the data and returns a customer-level table containing:

- Customer ID
- Recency, Frequency, and Monetary values
- RF and RFM scores
- Customer segment

## Project Scope

This project demonstrates rule-based customer segmentation and campaign audience selection. Campaign performance and revenue impact are not measured.
