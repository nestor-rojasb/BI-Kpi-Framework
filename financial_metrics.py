"""
Sistema de KPI: Financial Performance Metrics

Métricas financieras derivadas de operaciones de compra-venta:
- Análisis de márgenes
- Rentabilidad por categoría/proveedor
- Concentración de proveedores (riesgo)
- Eficiencia en gestión de montos

Aplicable a: Cualquier operación B2B con compra-venta de productos.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple

class FinancialPerformanceKPI:
    """
    Calcula KPIs financieros de operaciones B2B.
    """
    
    def __init__(self, orders_df: pd.DataFrame, order_lines_df: pd.DataFrame = None):
        """
        Inicializa el sistema de KPI financiero.
        
        Args:
            orders_df: DataFrame con órdenes que contenga:
                      - order_id, total_cost, sale_amount, margin, margin_pct
            order_lines_df: DataFrame opcional con líneas de orden para análisis detallado
        """
        self.orders_df = orders_df.copy()
        self.order_lines_df = order_lines_df.copy() if order_lines_df is not None else None
    
    def calculate_margin_metrics(self) -> Dict:
        """
        Calcula métricas de margen global.
        
        Returns:
            Diccionario con métricas de margen
        """
        return {
            'total_cost': self.orders_df['total_cost'].sum(),
            'total_sale': self.orders_df['sale_amount'].sum(),
            'total_margin': self.orders_df['margin'].sum(),
            'avg_margin_pct': self.orders_df['margin_pct'].mean(),
            'median_margin_pct': self.orders_df['margin_pct'].median(),
            'margin_std': self.orders_df['margin_pct'].std(),
            'orders_with_low_margin': len(self.orders_df[self.orders_df['margin_pct'] < 10]),
            'orders_with_high_margin': len(self.orders_df[self.orders_df['margin_pct'] > 20])
        }
    
    def analyze_by_supplier(self, suppliers_df: pd.DataFrame) -> pd.DataFrame:
        """
        Analiza performance financiera por proveedor.
        
        Args:
            suppliers_df: DataFrame con información de proveedores
        
        Returns:
            DataFrame con métricas por proveedor
        """
        supplier_metrics = self.orders_df.groupby('supplier_id').agg({
            'order_id': 'count',
            'total_cost': 'sum',
            'sale_amount': 'sum',
            'margin': 'sum',
            'margin_pct': 'mean'
        }).rename(columns={
            'order_id': 'num_orders',
            'total_cost': 'total_purchases',
            'sale_amount': 'total_sales',
            'margin': 'total_margin',
            'margin_pct': 'avg_margin_pct'
        })
        
        # Calcular participación
        supplier_metrics['pct_purchases'] = (
            supplier_metrics['total_purchases'] / supplier_metrics['total_purchases'].sum() * 100
        )
        
        # Join con info de proveedores
        supplier_metrics = supplier_metrics.join(
            suppliers_df.set_index('supplier_id')[['supplier_name', 'supplier_type', 'rating']], 
            how='left'
        )
        
        return supplier_metrics.round(2).sort_values('total_purchases', ascending=False)
    
    def calculate_concentration_risk(self) -> Dict:
        """
        Calcula riesgo de concentración de proveedores.
        
        Returns:
            Diccionario con métricas de concentración
        """
        supplier_purchases = self.orders_df.groupby('supplier_id')['total_cost'].sum().sort_values(ascending=False)
        total_purchases = supplier_purchases.sum()
        
        # Top 5 proveedores
        top5_pct = (supplier_purchases.head(5).sum() / total_purchases * 100)
        
        # Índice Herfindahl-Hirschman (HHI)
        market_shares = (supplier_purchases / total_purchases * 100) ** 2
        hhi = market_shares.sum()
        
        return {
            'total_suppliers': len(supplier_purchases),
            'top5_concentration_pct': round(top5_pct, 2),
            'hhi_index': round(hhi, 2),
            'risk_level': 'Alto' if hhi > 2500 else 'Moderado' if hhi > 1500 else 'Bajo'
        }
    
    def analyze_by_category(self, skus_df: pd.DataFrame) -> pd.DataFrame:
        """
        Analiza performance por categoría de producto.
        
        Args:
            skus_df: DataFrame con información de SKUs
        
        Returns:
            DataFrame con métricas por categoría
        """
        if self.order_lines_df is None:
            raise ValueError("Se requiere order_lines_df para análisis por categoría")
        
        # Join para obtener categorías
        lines_with_category = self.order_lines_df.merge(
            skus_df[['sku', 'category']], 
            on='sku'
        )
        
        # Agregar info de orden
        lines_with_order = lines_with_category.merge(
            self.orders_df[['order_id', 'margin_pct']], 
            on='order_id'
        )
        
        category_metrics = lines_with_order.groupby('category').agg({
            'order_id': 'nunique',
            'line_total': 'sum',
            'margin_pct': 'mean'
        }).rename(columns={
            'order_id': 'num_orders',
            'line_total': 'total_sales',
            'margin_pct': 'avg_margin_pct'
        })
        
        category_metrics['pct_sales'] = (
            category_metrics['total_sales'] / category_metrics['total_sales'].sum() * 100
        )
        
        return category_metrics.round(2).sort_values('total_sales', ascending=False)
    
    def identify_margin_opportunities(self, threshold: float = 15.0) -> pd.DataFrame:
        """
        Identifica órdenes con oportunidad de mejora en margen.
        
        Args:
            threshold: Margen mínimo esperado (%)
        
        Returns:
            DataFrame con órdenes bajo el threshold
        """
        low_margin = self.orders_df[self.orders_df['margin_pct'] < threshold].copy()
        low_margin['improvement_potential'] = threshold - low_margin['margin_pct']
        low_margin['potential_additional_margin'] = (
            low_margin['total_cost'] * low_margin['improvement_potential'] / 100
        )
        
        return low_margin[
            ['order_id', 'supplier_id', 'total_cost', 'margin_pct', 
             'improvement_potential', 'potential_additional_margin']
        ].sort_values('potential_additional_margin', ascending=False)
    
    def generate_financial_report(self, suppliers_df: pd.DataFrame = None, 
                                 skus_df: pd.DataFrame = None) -> str:
        """
        Genera reporte financiero completo.
        
        Returns:
            String con reporte formateado
        """
        margin_metrics = self.calculate_margin_metrics()
        concentration = self.calculate_concentration_risk()
        
        report = ["="*80]
        report.append("REPORTE DE PERFORMANCE FINANCIERA")
        report.append("="*80)
        report.append("")
        
        report.append("1. MÉTRICAS GLOBALES DE MARGEN")
        report.append("-" * 80)
        report.append(f"Costo total: ${margin_metrics['total_cost']:,.2f}")
        report.append(f"Venta total: ${margin_metrics['total_sale']:,.2f}")
        report.append(f"Margen total: ${margin_metrics['total_margin']:,.2f}")
        report.append(f"Margen promedio: {margin_metrics['avg_margin_pct']:.1f}%")
        report.append(f"Margen mediano: {margin_metrics['median_margin_pct']:.1f}%")
        report.append(f"Desviación estándar: {margin_metrics['margin_std']:.1f}%")
        report.append("")
        
        report.append("2. RIESGO DE CONCENTRACIÓN DE PROVEEDORES")
        report.append("-" * 80)
        report.append(f"Total de proveedores: {concentration['total_suppliers']}")
        report.append(f"Concentración Top 5: {concentration['top5_concentration_pct']:.1f}%")
        report.append(f"Índice HHI: {concentration['hhi_index']:.0f}")
        report.append(f"Nivel de riesgo: {concentration['risk_level']}")
        report.append("")
        
        if concentration['risk_level'] == 'Alto':
            report.append("⚠️  ALERTA: Alta concentración de proveedores - diversificar riesgo")
        
        if suppliers_df is not None:
            report.append("\n3. TOP 10 PROVEEDORES POR VOLUMEN")
            report.append("-" * 80)
            supplier_perf = self.analyze_by_supplier(suppliers_df)
            report.append(supplier_perf.head(10).to_string())
        
        if skus_df is not None and self.order_lines_df is not None:
            report.append("\n\n4. PERFORMANCE POR CATEGORÍA")
            report.append("-" * 80)
            category_perf = self.analyze_by_category(skus_df)
            report.append(category_perf.to_string())
        
        report.append("\n" + "="*80)
        
        return "\n".join(report)


def example_usage():
    """Ejemplo de uso del sistema"""
    # Cargar datos
    orders_df = pd.read_csv('data/synthetic/purchase_orders.csv')
    suppliers_df = pd.read_csv('data/synthetic/suppliers.csv')
    skus_df = pd.read_csv('data/synthetic/skus.csv')
    order_lines_df = pd.read_csv('data/synthetic/order_lines.csv')
    
    # Inicializar sistema
    kpi_system = FinancialPerformanceKPI(orders_df, order_lines_df)
    
    # Generar reporte
    print(kpi_system.generate_financial_report(suppliers_df, skus_df))
    
    # Identificar oportunidades
    print("\n\nOPORTUNIDADES DE MEJORA DE MARGEN:")
    print("-" * 80)
    opportunities = kpi_system.identify_margin_opportunities(threshold=15.0)
    print(opportunities.head(10))


if __name__ == "__main__":
    example_usage()
