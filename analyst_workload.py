"""
Sistema de KPI: Carga Laboral de Analistas

Este módulo implementa un sistema de medición de carga laboral que considera
la COMPLEJIDAD de las tareas, no solo el volumen.

Principio clave: Una orden con 100 SKUs requiere mucho más esfuerzo que 
una orden con 1 SKU, pero ambas cuentan como "1 ticket" en sistemas tradicionales.

Metodología:
- Categorización por complejidad basada en número de SKUs
- Ponderación de carga según complejidad
- Identificación de especialización de analistas
- Detección de desbalance de carga

Aplicable a: Call centers, soporte técnico, analistas financieros, logística, etc.
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict

class AnalystWorkloadKPI:
    """
    Calcula KPIs de carga laboral considerando complejidad de tareas.
    """
    
    # Categorías de complejidad según número de SKUs
    COMPLEXITY_CATEGORIES = {
        'Muy Simple': (1, 5),
        'Simple': (6, 20),
        'Moderado': (21, 50),
        'Complejo': (51, float('inf'))
    }
    
    # Pesos de complejidad (tiempo relativo de procesamiento)
    COMPLEXITY_WEIGHTS = {
        'Muy Simple': 1.0,
        'Simple': 2.5,
        'Moderado': 5.0,
        'Complejo': 10.0
    }
    
    def __init__(self, orders_df: pd.DataFrame):
        """
        Inicializa el sistema de KPI.
        
        Args:
            orders_df: DataFrame con órdenes que contenga al menos:
                      - analyst_id: Identificador del analista
                      - num_skus: Cantidad de SKUs en la orden
                      - order_date: Fecha de la orden
        """
        self.orders_df = orders_df.copy()
        self._categorize_complexity()
    
    def _categorize_complexity(self):
        """Categoriza cada orden según su complejidad"""
        def get_complexity(num_skus):
            for category, (min_val, max_val) in self.COMPLEXITY_CATEGORIES.items():
                if min_val <= num_skus <= max_val:
                    return category
            return 'Complejo'
        
        self.orders_df['complexity'] = self.orders_df['num_skus'].apply(get_complexity)
        self.orders_df['complexity_weight'] = self.orders_df['complexity'].map(self.COMPLEXITY_WEIGHTS)
    
    def calculate_workload_by_analyst(self) -> pd.DataFrame:
        """
        Calcula carga de trabajo por analista.
        
        Returns:
            DataFrame con métricas de carga por analista
        """
        workload = self.orders_df.groupby('analyst_id').agg({
            'order_id': 'count',  # Total de tickets
            'num_skus': 'sum',    # Total de SKUs procesados
            'complexity_weight': 'sum'  # Carga ponderada
        }).rename(columns={
            'order_id': 'total_tickets',
            'num_skus': 'total_skus',
            'complexity_weight': 'weighted_workload'
        })
        
        # Agregar distribución por complejidad
        complexity_dist = self.orders_df.groupby(['analyst_id', 'complexity']).size().unstack(fill_value=0)
        workload = workload.join(complexity_dist, how='left')
        
        # Métricas derivadas
        workload['avg_skus_per_ticket'] = workload['total_skus'] / workload['total_tickets']
        workload['avg_complexity_weight'] = workload['weighted_workload'] / workload['total_tickets']
        
        return workload.round(2)
    
    def identify_specialization(self, skus_df: pd.DataFrame, order_lines_df: pd.DataFrame) -> pd.DataFrame:
        """
        Identifica si los analistas tienen especialización por categoría de producto.
        
        Args:
            skus_df: DataFrame con información de SKUs
            order_lines_df: DataFrame con líneas de órdenes
        
        Returns:
            DataFrame con análisis de especialización por analista
        """
        # Join para obtener categorías
        order_lines = order_lines_df.merge(skus_df[['sku', 'category']], on='sku')
        orders_with_category = self.orders_df.merge(
            order_lines.groupby('order_id')['category'].apply(lambda x: x.mode()[0] if len(x) > 0 else 'Sin categoría'),
            left_on='order_id',
            right_index=True
        )
        
        # Distribución de categorías por analista
        category_dist = orders_with_category.groupby(['analyst_id', 'category']).size().unstack(fill_value=0)
        
        # Calcular % de especialización (categoría más frecuente)
        specialization = pd.DataFrame({
            'primary_category': category_dist.idxmax(axis=1),
            'primary_category_pct': (category_dist.max(axis=1) / category_dist.sum(axis=1) * 100).round(1),
            'categories_handled': (category_dist > 0).sum(axis=1)
        })
        
        return specialization
    
    def detect_workload_imbalance(self) -> Dict:
        """
        Detecta desbalance en la distribución de carga.
        
        Returns:
            Diccionario con métricas de desbalance
        """
        workload = self.calculate_workload_by_analyst()
        
        return {
            'max_workload': workload['weighted_workload'].max(),
            'min_workload': workload['weighted_workload'].min(),
            'avg_workload': workload['weighted_workload'].mean(),
            'std_workload': workload['weighted_workload'].std(),
            'imbalance_ratio': workload['weighted_workload'].max() / workload['weighted_workload'].min(),
            'coefficient_variation': (workload['weighted_workload'].std() / workload['weighted_workload'].mean() * 100)
        }
    
    def get_complexity_distribution(self) -> pd.DataFrame:
        """
        Retorna distribución global de complejidad.
        
        Returns:
            DataFrame con distribución de órdenes por complejidad
        """
        dist = self.orders_df.groupby('complexity').agg({
            'order_id': 'count',
            'num_skus': ['mean', 'median', 'max'],
            'complexity_weight': 'sum'
        })
        
        dist.columns = ['count', 'avg_skus', 'median_skus', 'max_skus', 'total_weight']
        dist['pct_orders'] = (dist['count'] / dist['count'].sum() * 100).round(1)
        
        return dist.round(2)
    
    def generate_report(self, analyst_df: pd.DataFrame = None) -> str:
        """
        Genera reporte textual de análisis de carga laboral.
        
        Args:
            analyst_df: DataFrame opcional con nombres de analistas
        
        Returns:
            String con reporte formateado
        """
        workload = self.calculate_workload_by_analyst()
        imbalance = self.detect_workload_imbalance()
        complexity_dist = self.get_complexity_distribution()
        
        report = ["="*80]
        report.append("REPORTE DE CARGA LABORAL - ANALISTAS")
        report.append("="*80)
        report.append("")
        
        report.append("1. DISTRIBUCIÓN GLOBAL DE COMPLEJIDAD")
        report.append("-" * 80)
        report.append(complexity_dist.to_string())
        report.append("")
        
        report.append("2. CARGA POR ANALISTA")
        report.append("-" * 80)
        
        if analyst_df is not None:
            workload = workload.join(analyst_df.set_index('analyst_id')[['analyst_name']], how='left')
        
        report.append(workload.to_string())
        report.append("")
        
        report.append("3. ANÁLISIS DE BALANCE")
        report.append("-" * 80)
        report.append(f"Carga máxima: {imbalance['max_workload']:.2f}")
        report.append(f"Carga mínima: {imbalance['min_workload']:.2f}")
        report.append(f"Carga promedio: {imbalance['avg_workload']:.2f}")
        report.append(f"Ratio desbalance: {imbalance['imbalance_ratio']:.2f}x")
        report.append(f"Coeficiente de variación: {imbalance['coefficient_variation']:.1f}%")
        report.append("")
        
        if imbalance['coefficient_variation'] > 30:
            report.append("⚠️  ALERTA: Desbalance significativo detectado (CV > 30%)")
        else:
            report.append("✓ Distribución de carga relativamente balanceada")
        
        report.append("="*80)
        
        return "\n".join(report)


def example_usage():
    """Ejemplo de uso del sistema"""
    # Cargar datos
    orders_df = pd.read_csv('data/synthetic/purchase_orders.csv')
    analysts_df = pd.read_csv('data/synthetic/analysts.csv')
    skus_df = pd.read_csv('data/synthetic/skus.csv')
    order_lines_df = pd.read_csv('data/synthetic/order_lines.csv')
    
    # Inicializar sistema
    kpi_system = AnalystWorkloadKPI(orders_df)
    
    # Generar análisis
    print(kpi_system.generate_report(analysts_df))
    
    # Análisis de especialización
    print("\nESPECIALIZACIÓN POR ANALISTA:")
    print("-" * 80)
    specialization = kpi_system.identify_specialization(skus_df, order_lines_df)
    print(specialization)


if __name__ == "__main__":
    example_usage()
