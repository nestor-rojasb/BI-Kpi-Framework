#!/usr/bin/env python3
"""
Quick Demo - Business Intelligence KPI Framework

Este script demuestra rápidamente los 3 sistemas de KPI principales.
"""

import pandas as pd
import sys
sys.path.append('.')

from src.kpis.analyst_workload import AnalystWorkloadKPI
from src.kpis.invoice_processing import OperationalProcessingKPI
from src.kpis.financial_metrics import FinancialPerformanceKPI

def main():
    print("="*80)
    print("DEMOSTRACIÓN - BUSINESS INTELLIGENCE KPI FRAMEWORK")
    print("="*80)
    print()
    
    # Cargar datos
    print("Cargando datos sintéticos...")
    orders_df = pd.read_csv('data/synthetic/purchase_orders.csv')
    analysts_df = pd.read_csv('data/synthetic/analysts.csv')
    skus_df = pd.read_csv('data/synthetic/skus.csv')
    order_lines_df = pd.read_csv('data/synthetic/order_lines.csv')
    invoices_df = pd.read_csv('data/synthetic/invoices.csv')
    suppliers_df = pd.read_csv('data/synthetic/suppliers.csv')
    
    print(f"✓ {len(orders_df):,} órdenes de compra")
    print(f"✓ {len(invoices_df):,} facturas")
    print(f"✓ {len(analysts_df)} analistas")
    print()
    
    # Sistema 1: Analyst Workload
    print("\n" + "="*80)
    print("SISTEMA 1: ANALYST WORKLOAD (Carga Laboral)")
    print("="*80)
    workload_system = AnalystWorkloadKPI(orders_df)
    print(workload_system.generate_report(analysts_df))
    
    # Sistema 2: Operational Processing (3-KPI)
    print("\n" + "="*80)
    print("SISTEMA 2: OPERATIONAL PROCESSING MONITOR (3-KPI)")
    print("="*80)
    processing_system = OperationalProcessingKPI(invoices_df)
    print(processing_system.generate_weekly_report(analyst_df=analysts_df))
    
    # Sistema 3: Financial Performance
    print("\n" + "="*80)
    print("SISTEMA 3: FINANCIAL PERFORMANCE METRICS")
    print("="*80)
    financial_system = FinancialPerformanceKPI(orders_df, order_lines_df)
    print(financial_system.generate_financial_report(suppliers_df, skus_df))
    
    print("\n" + "="*80)
    print("DEMOSTRACIÓN COMPLETADA")
    print("="*80)
    print("\nPróximos pasos:")
    print("1. Explora los notebooks en notebooks/")
    print("2. Lee la metodología completa en docs/methodology.md")
    print("3. Adapta los KPIs a tus propios datos")
    print()

if __name__ == "__main__":
    main()
