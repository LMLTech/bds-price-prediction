import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Standard academic styling configuration
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['figure.titlesize'] = 14


def _ensure_dir(path):
    if path:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)


# ==============================================================================
# GROUP A — DATASET OVERVIEW
# ==============================================================================

def plot_price_distribution(df, target_col='price_million_vnd', save_path=None, show=False):
    """
    Figure 01: Raw Target Price Distribution.
    Demonstrates strong right-skewness (skewness ~8.16) across real estate market data.
    """
    if df is None or df.empty or target_col not in df.columns:
        print(f"Warning: {target_col} missing or DataFrame empty in plot_price_distribution.")
        return None, None

    data = df[target_col].dropna()
    skewness = data.skew()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data, bins=50, kde=True, color='navy', ax=ax, alpha=0.6)

    ax.set_title(f'Price Distribution — Raw Scale (Skewness = {skewness:.2f})')
    ax.set_xlabel('Price (Million VND)')
    ax.set_ylabel('Number of Properties')
    ax.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    if save_path:
        _ensure_dir(save_path)
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    if not show:
        plt.close(fig)
    return fig, ax


def plot_log_price_distribution(df, target_col='price_million_vnd', save_path=None, show=False):
    """
    Figure 02: Log-Transformed Price Distribution (EDA visualization only).
    Note: The final production model is Multiple Linear Regression evaluated on raw scale.
    """
    if df is None or df.empty or target_col not in df.columns:
        print(f"Warning: {target_col} missing or DataFrame empty in plot_log_price_distribution.")
        return None, None

    data = np.log1p(df[target_col].dropna())
    skewness = data.skew()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data, bins=50, kde=True, color='coral', ax=ax, alpha=0.6)

    ax.set_title(f'Log-Transformed Price Distribution — log1p(Price) (Skewness = {skewness:.2f})')
    ax.set_xlabel('log1p(Price in Million VND)')
    ax.set_ylabel('Number of Properties')
    ax.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    if save_path:
        _ensure_dir(save_path)
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    if not show:
        plt.close(fig)
    return fig, ax


# ==============================================================================
# GROUP B — PROPERTY CHARACTERISTICS
# ==============================================================================

def plot_area_vs_price(df, area_col='area_m2', price_col='price_million_vnd', save_path=None, show=False):
    """
    Figure 03: Relationship between Property Area (m2) and Price (Million VND).
    """
    if df is None or df.empty or area_col not in df.columns or price_col not in df.columns:
        print("Warning: Missing required columns in plot_area_vs_price.")
        return None, None

    sub = df[[area_col, price_col]].dropna()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(sub[area_col], sub[price_col], alpha=0.35, color='teal', s=20, edgecolors='none')

    ax.set_title('Property Area vs Price Scatter Plot')
    ax.set_xlabel('Area (m²)')
    ax.set_ylabel('Price (Million VND)')
    ax.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    if save_path:
        _ensure_dir(save_path)
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    if not show:
        plt.close(fig)
    return fig, ax



def plot_price_by_bedrooms(df, bedrooms_col='bedrooms', price_col='price_million_vnd', max_bedrooms=8, save_path=None, show=False):
    """
    Figure 04: Price Distribution across Bedroom Counts (Boxplot).
    """
    if df is None or df.empty or bedrooms_col not in df.columns or price_col not in df.columns:
        print("Warning: Missing required columns in plot_price_by_bedrooms.")
        return None, None

    sub = df[[bedrooms_col, price_col]].dropna().copy()
    sub = sub[sub[bedrooms_col] <= max_bedrooms]

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=sub, x=bedrooms_col, y=price_col, palette='Blues', ax=ax, showfliers=False)

    ax.set_title('Property Price Distribution by Bedroom Count (Outliers Omitted in View)')
    ax.set_xlabel('Number of Bedrooms')
    ax.set_ylabel('Price (Million VND)')
    ax.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    if save_path:
        _ensure_dir(save_path)
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    if not show:
        plt.close(fig)
    return fig, ax


def plot_price_by_area_bucket(df, area_col='area_m2', price_col='price_million_vnd', save_path=None, show=False):
    """
    Figure 05: Median Price and Sample Count across Size Segments (Area Buckets).
    """
    if df is None or df.empty or area_col not in df.columns or price_col not in df.columns:
        print("Warning: Missing required columns in plot_price_by_area_bucket.")
        return None, None

    sub = df[[area_col, price_col]].dropna().copy()

    bins = [0, 50, 80, 120, 200, np.inf]
    labels = ['<50 m²', '50–80 m²', '80–120 m²', '120–200 m²', '200+ m²']
    sub['area_bucket'] = pd.cut(sub[area_col], bins=bins, labels=labels)

    summary = sub.groupby('area_bucket', observed=False)[price_col].agg(['median', 'count']).reset_index()

    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:blue'
    ax1.set_xlabel('Area Segment (m²)')
    ax1.set_ylabel('Median Price (Million VND)', color=color)
    bars = ax1.bar(summary['area_bucket'], summary['median'], color=color, alpha=0.7, width=0.5)
    ax1.tick_params(axis='y', labelcolor=color)

    for bar in bars:
        height = bar.get_height()
        ax1.annotate(f'{height:,.0f}M',
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Sample Count', color=color)
    ax2.plot(summary['area_bucket'], summary['count'], color=color, marker='o', linewidth=2, linestyle='--')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.grid(False)

    plt.title('Median Price and Property Count by Area Segment')
    plt.tight_layout()
    if save_path:
        _ensure_dir(save_path)
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    if not show:
        plt.close(fig)
    return fig, ax1


# ==============================================================================
# GROUP C — LOCATION
# ==============================================================================

def plot_avg_price_by_district(df, district_col='district', price_col='price_million_vnd', top_n=10, save_path=None, show=False):
    """
    Figure 06: Top N Districts by Average Property Price in Dataset.
    Academic note: Represents average price among properties present in this dataset.
    """
    if df is None or df.empty or district_col not in df.columns or price_col not in df.columns:
        print("Warning: Missing required columns in plot_avg_price_by_district.")
        return None, None

    sub = df[[district_col, price_col]].dropna()
    avg_price = sub.groupby(district_col)[price_col].mean().sort_values(ascending=False).head(top_n).reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(avg_price[district_col][::-1], avg_price[price_col][::-1], color='steelblue', alpha=0.85)

    ax.set_title(f'Top {top_n} Districts by Average Property Price in Dataset')
    ax.set_xlabel('Average Price (Million VND)')
    ax.set_ylabel('District')
    ax.grid(True, linestyle='--', alpha=0.5)

    for bar in bars:
        width = bar.get_width()
        ax.annotate(f'{width:,.0f}M',
                    xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0), textcoords="offset points",
                    ha='left', va='center', fontsize=9)

    plt.tight_layout()
    if save_path:
        _ensure_dir(save_path)
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    if not show:
        plt.close(fig)
    return fig, ax


def plot_median_price_per_m2_by_district(df, district_col='district', area_col='area_m2', price_col='price_million_vnd', top_n=10, save_path=None, show=False):
    """
    Figure 07: Median Price per m² by District (EDA ONLY).
    Academic note: price_per_m2 is derived from target and is strictly excluded from feature engineering.
    """
    if df is None or df.empty or district_col not in df.columns or area_col not in df.columns or price_col not in df.columns:
        print("Warning: Missing required columns in plot_median_price_per_m2_by_district.")
        return None, None

    sub = df[[district_col, area_col, price_col]].dropna().copy()
    sub = sub[sub[area_col] > 0]
    sub['price_per_m2'] = sub[price_col] / sub[area_col]

    med_pm2 = sub.groupby(district_col)['price_per_m2'].median().sort_values(ascending=False).head(top_n).reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(med_pm2[district_col][::-1], med_pm2['price_per_m2'][::-1], color='darkslategrey', alpha=0.85)

    ax.set_title(f'Top {top_n} Districts by Median Price per m² (EDA Only)')
    ax.set_xlabel('Median Price per m² (Million VND / m²)')
    ax.set_ylabel('District')
    ax.grid(True, linestyle='--', alpha=0.5)

    for bar in bars:
        width = bar.get_width()
        ax.annotate(f'{width:,.1f}M/m²',
                    xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0), textcoords="offset points",
                    ha='left', va='center', fontsize=9)

    plt.tight_layout()
    if save_path:
        _ensure_dir(save_path)
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    if not show:
        plt.close(fig)
    return fig, ax


def plot_distance_vs_price(df, distance_col='distance_to_center_km', price_col='price_million_vnd', save_path=None, show=False):
    """
    Figure 08: Distance to CBD vs Price Scatter Plot.
    Academic note: Distance is a geographic spatial proxy based on representative district coordinates.
    """
    if df is None or df.empty or distance_col not in df.columns or price_col not in df.columns:
        print("Warning: Missing required columns in plot_distance_vs_price.")
        return None, None

    sub = df[[distance_col, price_col]].dropna()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(sub[distance_col], sub[price_col], alpha=0.35, color='firebrick', s=20, edgecolors='none')


    ax.set_title('Distance to City Center (CBD Spatial Proxy) vs Price')
    ax.set_xlabel('Distance to Center (km)')
    ax.set_ylabel('Price (Million VND)')
    ax.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    if save_path:
        _ensure_dir(save_path)
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    if not show:
        plt.close(fig)
    return fig, ax


def plot_price_by_distance_bucket(df, distance_col='distance_to_center_km', price_col='price_million_vnd', save_path=None, show=False):
    """
    Figure 09: Median Property Price across Distance Bands.
    """
    if df is None or df.empty or distance_col not in df.columns or price_col not in df.columns:
        print("Warning: Missing required columns in plot_price_by_distance_bucket.")
        return None, None

    sub = df[[distance_col, price_col]].dropna().copy()

    bins = [0, 3, 5, 10, 15, np.inf]
    labels = ['0–3 km', '3–5 km', '5–10 km', '10–15 km', '15+ km']
    sub['dist_bucket'] = pd.cut(sub[distance_col], bins=bins, labels=labels)

    summary = sub.groupby('dist_bucket', observed=False)[price_col].agg(['median', 'count']).reset_index()

    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'purple'
    ax1.set_xlabel('Distance Band to CBD Proxy (km)')
    ax1.set_ylabel('Median Price (Million VND)', color=color)
    bars = ax1.bar(summary['dist_bucket'], summary['median'], color=color, alpha=0.65, width=0.5)
    ax1.tick_params(axis='y', labelcolor=color)

    for bar in bars:
        height = bar.get_height()
        ax1.annotate(f'{height:,.0f}M',
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax2 = ax1.twinx()
    color = 'teal'
    ax2.set_ylabel('Sample Count', color=color)
    ax2.plot(summary['dist_bucket'], summary['count'], color=color, marker='s', linewidth=2, linestyle='--')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.grid(False)

    plt.title('Median Price and Property Count across Distance Bands')
    plt.tight_layout()
    if save_path:
        _ensure_dir(save_path)
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    if not show:
        plt.close(fig)
    return fig, ax1


# ==============================================================================
# GROUP D — MODEL PERFORMANCE
# ==============================================================================

def plot_actual_vs_predicted(y_true, y_pred, title_suffix="Raw Predictions", save_path=None, show=False):
    """
    Figure 10: Actual vs Predicted Price — Final Linear Regression.
    Academic note: Evaluated on Raw Model Predictions (Unclipped Xb + b) with ideal y = x line.
    """
    if y_true is None or y_pred is None or len(y_true) == 0:
        print("Warning: Input arrays empty in plot_actual_vs_predicted.")
        return None, None

    y_t = np.asarray(y_true)
    y_p = np.asarray(y_pred)

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.scatter(y_t, y_p, alpha=0.35, color='royalblue', s=20, edgecolors='none')

    max_val = max(y_t.max(), y_p.max())
    min_val = min(y_t.min(), y_p.min())
    ax.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Ideal Reference Line (y = x)')

    ax.set_title(f'Actual vs Predicted Price — Final Linear Regression ({title_suffix})')
    ax.set_xlabel('Actual Price (Million VND)')
    ax.set_ylabel('Predicted Price (Million VND)')
    ax.legend(loc='upper left')
    ax.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    if save_path:
        _ensure_dir(save_path)
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    if not show:
        plt.close(fig)
    return fig, ax


def plot_residual_distribution(y_true, y_pred, save_path=None, show=False):
    """
    Figure 11: Residual Distribution (Residual = Actual - Predicted).
    """
    if y_true is None or y_pred is None or len(y_true) == 0:
        print("Warning: Input arrays empty in plot_residual_distribution.")
        return None, None

    residuals = np.asarray(y_true) - np.asarray(y_pred)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(residuals, bins=50, kde=True, color='crimson', ax=ax, alpha=0.6)
    ax.axvline(0, color='black', linestyle='--', linewidth=2, label='Zero Error Line')

    ax.set_title('Residual Distribution — Final Linear Regression (Residual = Actual - Predicted)')
    ax.set_xlabel('Residual Error (Million VND)')
    ax.set_ylabel('Frequency')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    if save_path:
        _ensure_dir(save_path)
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    if not show:
        plt.close(fig)
    return fig, ax


def plot_residual_vs_predicted(y_true, y_pred, save_path=None, show=False):
    """
    Figure 12: Residual vs Predicted Plot (Heteroscedasticity & Systematic Error Diagnostics).
    """
    if y_true is None or y_pred is None or len(y_true) == 0:
        print("Warning: Input arrays empty in plot_residual_vs_predicted.")
        return None, None

    y_p = np.asarray(y_pred)
    residuals = np.asarray(y_true) - y_p

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(y_p, residuals, alpha=0.35, color='darkmagenta', s=20, edgecolors='none')
    ax.axhline(0, color='r', linestyle='--', linewidth=2, label='Zero Residual Reference Line')

    ax.set_title('Residual vs Predicted Price — Final Linear Regression')
    ax.set_xlabel('Predicted Price (Million VND)')
    ax.set_ylabel('Residual = Actual - Predicted (Million VND)')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    if save_path:
        _ensure_dir(save_path)
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    if not show:
        plt.close(fig)
    return fig, ax


# ==============================================================================
# GROUP E — ERROR ANALYSIS
# ==============================================================================

def plot_absolute_error_distribution(y_true, y_pred, save_path=None, show=False):
    """
    Figure 13: Absolute Error Distribution (|Actual - Predicted|).
    """
    if y_true is None or y_pred is None or len(y_true) == 0:
        print("Warning: Input arrays empty in plot_absolute_error_distribution.")
        return None, None

    abs_err = np.abs(np.asarray(y_true) - np.asarray(y_pred))

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(abs_err, bins=50, kde=True, color='darkorange', ax=ax, alpha=0.6)

    ax.set_title('Absolute Error Distribution — Final Linear Regression')
    ax.set_xlabel('Absolute Error = |Actual - Predicted| (Million VND)')
    ax.set_ylabel('Frequency')
    ax.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    if save_path:
        _ensure_dir(save_path)
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    if not show:
        plt.close(fig)
    return fig, ax


def plot_error_by_price_range(y_true, y_pred, save_path=None, show=False):
    """
    Figure 14: MAE and RMSE Metrics across Actual Price Ranges.
    """
    if y_true is None or y_pred is None or len(y_true) == 0:
        print("Warning: Input arrays empty in plot_error_by_price_range.")
        return None, None

    y_t = np.asarray(y_true)
    y_p = np.asarray(y_pred)

    bins = [0, 2000, 5000, 10000, 20000, 50000, np.inf]
    labels = ['<2B', '2–5B', '5–10B', '10–20B', '20–50B', '50B+']

    df_err = pd.DataFrame({'Actual': y_t, 'Predicted': y_p})
    df_err['Range'] = pd.cut(df_err['Actual'], bins=bins, labels=labels)

    stats = []
    for label in labels:
        sub = df_err[df_err['Range'] == label]
        if len(sub) > 0:
            mae_val = np.mean(np.abs(sub['Actual'] - sub['Predicted']))
            rmse_val = np.sqrt(np.mean((sub['Actual'] - sub['Predicted'])**2))
            stats.append({'Range': label, 'MAE': mae_val, 'RMSE': rmse_val, 'Count': len(sub)})

    summary = pd.DataFrame(stats)

    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(summary['Range']))
    width = 0.35

    bars1 = ax.bar(x - width / 2, summary['MAE'], width, label='MAE (Million VND)', color='cornflowerblue', alpha=0.85)
    bars2 = ax.bar(x + width / 2, summary['RMSE'], width, label='RMSE (Million VND)', color='indianred', alpha=0.85)

    ax.set_title('Prediction Error (MAE & RMSE) by Actual Price Range')
    ax.set_xlabel('Actual Price Range (VND)')
    ax.set_ylabel('Error Metric (Million VND)')
    ax.set_xticks(x)
    ax.set_xticklabels(summary['Range'])
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)

    for bar in bars1:
        h = bar.get_height()
        ax.annotate(f'{h:,.0f}M', xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    if save_path:
        _ensure_dir(save_path)
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    if not show:
        plt.close(fig)
    return fig, ax


def plot_top_prediction_errors(df_test, y_true, y_pred, top_n=20, save_path=None, show=False):
    """
    Figure 15: Top N Largest Absolute Errors Bar Chart.
    Omits PII (URLs, phone numbers) and focuses purely on property location & size.
    """
    if y_true is None or y_pred is None or len(y_true) == 0:
        print("Warning: Input arrays empty in plot_top_prediction_errors.")
        return None, None

    df_err = df_test.copy() if df_test is not None else pd.DataFrame()
    df_err['Actual'] = np.asarray(y_true)
    df_err['Predicted'] = np.asarray(y_pred)
    df_err['Abs_Error'] = np.abs(df_err['Actual'] - df_err['Predicted'])

    top_err = df_err.sort_values(by='Abs_Error', ascending=False).head(top_n).reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(12, 7))
    y_pos = np.arange(len(top_err))

    bars = ax.barh(y_pos, top_err['Abs_Error'], color='firebrick', alpha=0.85)

    labels = []
    for idx, row in top_err.iterrows():
        dist = row.get('district', 'N/A')
        prov = row.get('province', '')
        area = row.get('area_m2', 'N/A')
        labels.append(f"#{idx+1}: {dist}, {prov} ({area}m²) — Act: {row['Actual']:,.0f}M | Pred: {row['Predicted']:,.0f}M")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels[::-1], fontsize=9)
    ax.invert_yaxis()

    ax.set_title(f'Top {top_n} Largest Prediction Errors (Absolute Error in Million VND)')
    ax.set_xlabel('Absolute Prediction Error |Actual - Predicted| (Million VND)')
    ax.grid(True, linestyle='--', alpha=0.5)

    for bar in bars:
        w = bar.get_width()
        ax.annotate(f'{w:,.0f}M', xy=(w, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0), textcoords="offset points", ha='left', va='center', fontsize=8)

    plt.tight_layout()
    if save_path:
        _ensure_dir(save_path)
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    if not show:
        plt.close(fig)
    return fig, ax
