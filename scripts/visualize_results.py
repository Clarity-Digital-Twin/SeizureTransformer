#!/usr/bin/env python3
"""
Visualize SeizureTransformer evaluation results.
Creates publication-quality figures for the evaluation report.
"""

import json
import pickle
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, auc

# Set publication style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def load_results():
    """Load evaluation results from checkpoint and JSON."""
    # Load checkpoint
    checkpoint_path = Path("evaluation/tusz/checkpoint.pkl")
    with open(checkpoint_path, 'rb') as f:
        checkpoint = pickle.load(f)
    
    # Load summary results
    results_path = Path("evaluation/tusz/results.json")
    with open(results_path, 'r') as f:
        results = json.load(f)
    
    return checkpoint, results

def plot_roc_curve(checkpoint):
    """Plot ROC curve with AUC."""
    # Collect all predictions and labels
    all_preds = []
    all_labels = []
    
    for file_id, result in checkpoint['results'].items():
        if result['predictions'] is not None and result['seizure_events'] is not None:
            preds = result['predictions']
            
            # Create binary labels
            labels = np.zeros(len(preds))
            for start_sec, end_sec in result['seizure_events']:
                start_idx = int(start_sec * 256)
                end_idx = int(end_sec * 256)
                if start_idx < len(labels):
                    labels[start_idx:min(end_idx, len(labels))] = 1
            
            all_preds.extend(preds)
            all_labels.extend(labels)
    
    # Calculate ROC
    fpr, tpr, thresholds = roc_curve(all_labels, all_preds)
    roc_auc = auc(fpr, tpr)
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.plot(fpr, tpr, linewidth=2, label=f'SeizureTransformer (AUC = {roc_auc:.3f})')
    ax.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random (AUC = 0.500)')
    
    # Mark operating point (threshold=0.8)
    idx_08 = np.argmin(np.abs(thresholds - 0.8))
    ax.scatter(fpr[idx_08], tpr[idx_08], s=100, c='red', 
               label=f'Operating Point (θ=0.8)\nSensitivity={tpr[idx_08]:.3f}, FPR={fpr[idx_08]:.3f}')
    
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel('False Positive Rate', fontsize=14)
    ax.set_ylabel('True Positive Rate (Sensitivity)', fontsize=14)
    ax.set_title('ROC Curve - SeizureTransformer on TUSZ v2.0.3', fontsize=16)
    ax.legend(loc="lower right", fontsize=12)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('docs/roc_curve.png', dpi=300, bbox_inches='tight')
    plt.savefig('docs/roc_curve.pdf', bbox_inches='tight')
    print("ROC curve saved to docs/roc_curve.png and .pdf")

def plot_performance_comparison():
    """Create bar chart comparing our results with paper claims."""
    
    metrics = ['AUROC', 'Sensitivity', 'F1 Score']
    paper_values = [0.876, 0.711, 0.675]  # Paper's TUSZ results
    our_values = [0.902, 0.242, 0.312]    # Our TAES results
    
    x = np.arange(len(metrics))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar(x - width/2, paper_values, width, label='Paper (Event-based)', color='#1f77b4')
    bars2 = ax.bar(x + width/2, our_values, width, label='Our Results (TAES)', color='#ff7f0e')
    
    ax.set_xlabel('Metric', fontsize=14)
    ax.set_ylabel('Score', fontsize=14)
    ax.set_title('Performance Comparison: Paper vs Our Evaluation', fontsize=16)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.legend(fontsize=12)
    ax.set_ylim([0, 1.0])
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.3f}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom')
    
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('docs/performance_comparison.png', dpi=300, bbox_inches='tight')
    plt.savefig('docs/performance_comparison.pdf', bbox_inches='tight')
    print("Performance comparison saved to docs/performance_comparison.png and .pdf")

def plot_false_alarm_analysis():
    """Visualize false alarm rates across different thresholds."""
    
    # Data from paper and our evaluation
    datasets = ['Dianalund\n(Competition)', 'TUSZ\n(Our Evaluation)']
    fa_rates = [1, 137.5]  # False alarms per 24 hours
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Bar chart of FA rates
    colors = ['#2ecc71', '#e74c3c']
    bars = ax1.bar(datasets, fa_rates, color=colors, alpha=0.7)
    ax1.set_ylabel('False Alarms per 24 Hours', fontsize=14)
    ax1.set_title('False Alarm Rate Comparison', fontsize=16)
    ax1.set_ylim([0, 150])
    
    # Add value labels
    for bar, rate in zip(bars, fa_rates):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                f'{rate:.1f}', ha='center', fontsize=12, fontweight='bold')
    
    # Add clinical threshold line
    ax1.axhline(y=10, color='red', linestyle='--', linewidth=2, 
                label='Clinical Acceptability Threshold')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Time between false alarms
    times = [24*60/fa for fa in fa_rates]  # Minutes between false alarms
    colors2 = ['#2ecc71', '#e74c3c']
    bars2 = ax2.bar(datasets, times, color=colors2, alpha=0.7)
    ax2.set_ylabel('Minutes Between False Alarms', fontsize=14)
    ax2.set_title('Clinical Impact: Alarm Frequency', fontsize=16)
    ax2.set_ylim([0, 1500])
    
    # Add value labels
    for bar, time in zip(bars2, times):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
                f'{time:.0f} min', ha='center', fontsize=12, fontweight='bold')
    
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.suptitle('False Alarm Analysis: Clinical Deployment Challenge', fontsize=18, y=1.02)
    plt.tight_layout()
    plt.savefig('docs/false_alarm_analysis.png', dpi=300, bbox_inches='tight')
    plt.savefig('docs/false_alarm_analysis.pdf', bbox_inches='tight')
    print("False alarm analysis saved to docs/false_alarm_analysis.png and .pdf")

def plot_prediction_distribution(checkpoint):
    """Plot distribution of prediction probabilities."""
    
    # Collect predictions by class
    seizure_preds = []
    background_preds = []
    
    for file_id, result in checkpoint['results'].items():
        if result['predictions'] is not None and result['seizure_events'] is not None:
            preds = np.array(result['predictions'])
            
            # Create binary labels
            labels = np.zeros(len(preds))
            for start_sec, end_sec in result['seizure_events']:
                start_idx = int(start_sec * 256)
                end_idx = int(end_sec * 256)
                if start_idx < len(labels):
                    labels[start_idx:min(end_idx, len(labels))] = 1
            
            seizure_preds.extend(preds[labels == 1])
            background_preds.extend(preds[labels == 0])
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot histograms
    bins = np.linspace(0, 1, 51)
    ax.hist(background_preds, bins=bins, alpha=0.5, label='Background', 
            color='blue', density=True)
    ax.hist(seizure_preds, bins=bins, alpha=0.5, label='Seizure', 
            color='red', density=True)
    
    # Add threshold line
    ax.axvline(x=0.8, color='black', linestyle='--', linewidth=2, 
               label='Threshold (0.8)')
    
    ax.set_xlabel('Prediction Probability', fontsize=14)
    ax.set_ylabel('Density', fontsize=14)
    ax.set_title('Distribution of Model Predictions by True Class', fontsize=16)
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Add text annotations
    ax.text(0.82, ax.get_ylim()[1]*0.9, 
            f'Seizure samples > 0.8: {np.mean(np.array(seizure_preds) > 0.8):.1%}',
            fontsize=11, bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.5))
    ax.text(0.82, ax.get_ylim()[1]*0.8,
            f'Background samples > 0.8: {np.mean(np.array(background_preds) > 0.8):.1%}',
            fontsize=11, bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('docs/prediction_distribution.png', dpi=300, bbox_inches='tight')
    plt.savefig('docs/prediction_distribution.pdf', bbox_inches='tight')
    print("Prediction distribution saved to docs/prediction_distribution.png and .pdf")

def main():
    """Generate all visualizations."""
    print("Generating visualizations for SeizureTransformer evaluation...")
    
    # Create docs directory if it doesn't exist
    Path("docs").mkdir(exist_ok=True)
    
    # Load results
    checkpoint, results = load_results()
    
    # Generate plots
    plot_roc_curve(checkpoint)
    plot_performance_comparison()
    plot_false_alarm_analysis()
    plot_prediction_distribution(checkpoint)
    
    print("\n✅ All visualizations generated successfully!")
    print("Files saved in docs/ directory")

if __name__ == "__main__":
    main()