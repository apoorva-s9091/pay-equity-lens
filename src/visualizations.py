"""
visualizations.py
Reusable plotting functions for Pay Equity Lens analysis.
All plots use a consistent dark corporate theme.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import pandas as pd
import numpy as np

# ── Theme ─────────────────────────────────────────────────────────────────────
DARK_BG = "#0f1117"
PANEL_BG = "#1a1d2e"
COLORS = {
    "primary": "#7B5EA7",
    "male": "#54A0E0",
    "female": "#E07B54",
    "positive": "#5EC87B",
    "warning": "#E0C454",
    "danger": "#E07B54",
}

def set_theme():
    """Apply consistent dark theme to all plots."""
    plt.rcParams.update({
        "figure.facecolor": DARK_BG,
        "axes.facecolor": PANEL_BG,
        "axes.labelcolor": "white",
        "xtick.color": "white",
        "ytick.color": "white",
        "text.color": "white",
        "axes.titlecolor": "white",
        "axes.edgecolor": "#333355",
        "grid.color": "#333355",
        "legend.facecolor": PANEL_BG,
        "legend.labelcolor": "white",
    })


def plot_income_distribution(df: pd.DataFrame, save_path: str = None):
    """Histogram of monthly income with mean/median lines."""
    set_theme()
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor(DARK_BG)

    ax.hist(df["MonthlyIncome"], bins=40, color=COLORS["primary"], edgecolor=DARK_BG, alpha=0.9)
    ax.axvline(df["MonthlyIncome"].mean(), color=COLORS["female"], lw=2, linestyle="--",
               label=f"Mean: ${df['MonthlyIncome'].mean():,.0f}")
    ax.axvline(df["MonthlyIncome"].median(), color=COLORS["male"], lw=2, linestyle="--",
               label=f"Median: ${df['MonthlyIncome'].median():,.0f}")
    ax.set_title("Monthly Income Distribution", fontweight="bold", fontsize=14)
    ax.set_xlabel("Monthly Income ($)")
    ax.set_ylabel("Count")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight", facecolor=DARK_BG)
    return fig


def plot_gender_pay_gap(df: pd.DataFrame, save_path: str = None):
    """Bar chart comparing average salary by gender."""
    set_theme()
    fig, ax = plt.subplots(figsize=(6, 5))
    fig.patch.set_facecolor(DARK_BG)

    gender_income = df.groupby("Gender")["MonthlyIncome"].mean()
    gap_pct = ((gender_income["Male"] - gender_income["Female"]) / gender_income["Male"]) * 100

    bars = ax.bar(gender_income.index, gender_income.values,
                  color=[COLORS["female"], COLORS["male"]], edgecolor=DARK_BG, width=0.5)
    for bar, val in zip(bars, gender_income.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 100,
                f"${val:,.0f}", ha="center", color="white", fontweight="bold")

    ax.set_title(f"Average Income by Gender\n(Pay Gap: {gap_pct:.1f}%)", fontweight="bold")
    ax.set_ylabel("Average Monthly Income ($)")
    ax.grid(True, alpha=0.3, axis="y")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight", facecolor=DARK_BG)
    return fig


def plot_department_gap(df: pd.DataFrame, save_path: str = None):
    """Grouped bar chart of pay by department and gender."""
    set_theme()
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor(DARK_BG)

    dept_gender = df.groupby(["Department", "Gender"])["MonthlyIncome"].mean().unstack()
    dept_gender.plot(kind="bar", ax=ax, color=[COLORS["female"], COLORS["male"]],
                     edgecolor=DARK_BG, width=0.7)
    ax.set_title("Average Income by Department & Gender", fontweight="bold")
    ax.set_xlabel("")
    ax.set_ylabel("Avg Monthly Income ($)")
    ax.legend(title="Gender")
    ax.tick_params(axis="x", rotation=15)
    ax.grid(True, alpha=0.3, axis="y")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight", facecolor=DARK_BG)
    return fig


def plot_feature_importance(importances: pd.Series, save_path: str = None):
    """Horizontal bar chart of model feature importances."""
    set_theme()
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor(DARK_BG)

    colors = [COLORS["primary"] if v > importances.mean() else COLORS["male"]
              for v in importances.values]
    ax.barh(importances.index, importances.values, color=colors, edgecolor=DARK_BG)
    ax.set_title("Feature Importance — Salary Predictor\n(Random Forest)", fontweight="bold")
    ax.set_xlabel("Importance Score")
    ax.grid(True, alpha=0.3, axis="x")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight", facecolor=DARK_BG)
    return fig


def plot_underpaid_analysis(df: pd.DataFrame, save_path: str = None):
    """Bar charts showing underpaid % by gender and department."""
    set_theme()
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.patch.set_facecolor(DARK_BG)

    by_gender = df.groupby("Gender")["Underpaid"].mean() * 100
    bars = axes[0].bar(by_gender.index, by_gender.values,
                       color=[COLORS["female"], COLORS["male"]], edgecolor=DARK_BG, width=0.5)
    for bar, val in zip(bars, by_gender.values):
        axes[0].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                     f"{val:.1f}%", ha="center", color="white", fontweight="bold")
    axes[0].set_title("% Underpaid by Gender\n(>$500 below predicted fair salary)", fontweight="bold")
    axes[0].set_ylabel("% Underpaid")
    axes[0].grid(True, alpha=0.3, axis="y")

    by_dept = df.groupby("Department")["Underpaid"].mean() * 100
    dept_colors = [COLORS["primary"], COLORS["positive"], COLORS["warning"]]
    bars2 = axes[1].bar(by_dept.index, by_dept.values, color=dept_colors, edgecolor=DARK_BG, width=0.5)
    for bar, val in zip(bars2, by_dept.values):
        axes[1].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                     f"{val:.1f}%", ha="center", color="white", fontweight="bold")
    axes[1].set_title("% Underpaid by Department", fontweight="bold")
    axes[1].set_ylabel("% Underpaid")
    axes[1].tick_params(axis="x", rotation=10)
    axes[1].grid(True, alpha=0.3, axis="y")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight", facecolor=DARK_BG)
    return fig
