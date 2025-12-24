"""
Generador de datos sintéticos para el framework de KPIs B2B.

Este script genera datos que replican la estructura de operaciones B2B reales:
- Órdenes de compra (Purchase Orders)
- Catálogo de productos (SKUs)
- Proveedores
- Analistas operacionales
- Registro de facturas

Los datos son completamente sintéticos pero mantienen patrones realistas.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from faker import Faker
import random

fake = Faker(['es_CL'])
np.random.seed(42)
random.seed(42)

# Configuración
NUM_SUPPLIERS = 50
NUM_ANALYSTS = 8
NUM_SKUS = 500
NUM_ORDERS = 2000
DATE_START = datetime(2024, 1, 1)
DATE_END = datetime(2024, 12, 31)

# Categorías de productos (universales B2B)
PRODUCT_CATEGORIES = [
    'Alimentos secos',
    'Alimentos refrigerados', 
    'Bebidas',
    'Productos de limpieza',
    'Suministros de oficina',
    'Equipamiento',
    'Insumos industriales',
    'Tecnología'
]

def generate_suppliers():
    """Genera catálogo de proveedores"""
    suppliers = []
    for i in range(NUM_SUPPLIERS):
        suppliers.append({
            'supplier_id': f'SUP{i+1:04d}',
            'supplier_name': fake.company(),
            'supplier_type': random.choice(['Nacional', 'Internacional']),
            'payment_terms': random.choice([30, 45, 60, 90]),
            'rating': round(random.uniform(3.0, 5.0), 1)
        })
    return pd.DataFrame(suppliers)

def generate_skus():
    """Genera catálogo de productos (SKUs)"""
    skus = []
    for i in range(NUM_SKUS):
        category = random.choice(PRODUCT_CATEGORIES)
        skus.append({
            'sku': f'SKU{i+1:06d}',
            'product_name': fake.catch_phrase(),
            'category': category,
            'unit_cost': round(random.uniform(100, 50000), 2),
            'unit': random.choice(['UN', 'KG', 'LT', 'CJ']),
            'active': random.choice([True, True, True, False])  # 75% activos
        })
    return pd.DataFrame(skus)

def generate_analysts():
    """Genera equipo de analistas operacionales"""
    analysts = []
    for i in range(NUM_ANALYSTS):
        analysts.append({
            'analyst_id': f'AN{i+1:03d}',
            'analyst_name': fake.name(),
            'hire_date': fake.date_between(start_date='-5y', end_date='-6m'),
            'specialization': random.choice(PRODUCT_CATEGORIES) if random.random() > 0.3 else None
        })
    return pd.DataFrame(analysts)

def generate_purchase_orders(skus_df, suppliers_df, analysts_df):
    """Genera órdenes de compra con patrones realistas"""
    orders = []
    order_lines = []
    
    for i in range(NUM_ORDERS):
        order_date = fake.date_time_between(start_date=DATE_START, end_date=DATE_END)
        supplier = suppliers_df.sample(1).iloc[0]
        analyst = analysts_df.sample(1).iloc[0]
        
        # Número de SKUs por orden (sesgo realista hacia órdenes pequeñas)
        num_skus = np.random.choice(
            [1, 2, 3, 5, 8, 15, 25, 50, 100],
            p=[0.15, 0.20, 0.18, 0.15, 0.12, 0.10, 0.05, 0.03, 0.02]
        )
        
        order_id = f'OC{i+1:06d}'
        
        # Si el analista tiene especialización, 70% de sus órdenes son de esa categoría
        if analyst['specialization'] and random.random() < 0.7:
            category_filter = skus_df['category'] == analyst['specialization']
            available_skus = skus_df[category_filter]
        else:
            available_skus = skus_df
        
        selected_skus = available_skus.sample(min(num_skus, len(available_skus)))
        
        total_amount = 0
        for _, sku in selected_skus.iterrows():
            quantity = random.randint(1, 100)
            line_total = sku['unit_cost'] * quantity
            total_amount += line_total
            
            order_lines.append({
                'order_id': order_id,
                'sku': sku['sku'],
                'quantity': quantity,
                'unit_price': sku['unit_cost'],
                'line_total': round(line_total, 2)
            })
        
        # Margen realista (5% a 25%)
        margin_pct = random.uniform(0.05, 0.25)
        sale_amount = total_amount * (1 + margin_pct)
        
        orders.append({
            'order_id': order_id,
            'order_date': order_date,
            'supplier_id': supplier['supplier_id'],
            'analyst_id': analyst['analyst_id'],
            'num_skus': len(selected_skus),
            'total_cost': round(total_amount, 2),
            'sale_amount': round(sale_amount, 2),
            'margin': round(sale_amount - total_amount, 2),
            'margin_pct': round(margin_pct * 100, 2),
            'status': random.choice(['Completed', 'Completed', 'Completed', 'Pending']),
            'delivery_date': order_date + timedelta(days=random.randint(3, 30))
        })
    
    return pd.DataFrame(orders), pd.DataFrame(order_lines)

def generate_invoice_processing(orders_df, analysts_df):
    """Genera datos de procesamiento de facturas (para KPI de facturación)"""
    # Filtrar solo órdenes completadas
    completed_orders = orders_df[orders_df['status'] == 'Completed'].copy()
    
    invoices = []
    for _, order in completed_orders.iterrows():
        # Fecha de factura es 1-5 días después de la orden
        invoice_date = order['order_date'] + timedelta(days=random.randint(1, 5))
        
        # Asignar a un analista de facturación (puede ser diferente al de la orden)
        processor = analysts_df.sample(1).iloc[0]
        
        # Fecha de procesamiento (1-7 días después de recibir factura)
        processing_delay = random.randint(1, 7)
        processed_date = invoice_date + timedelta(days=processing_delay)
        
        # 5% de facturas tienen errores
        has_error = random.random() < 0.05
        
        invoices.append({
            'invoice_id': f'INV{order["order_id"][2:]}',
            'order_id': order['order_id'],
            'invoice_date': invoice_date,
            'assigned_to': processor['analyst_id'],
            'processed_date': processed_date,
            'processing_days': processing_delay,
            'amount': order['sale_amount'],
            'has_error': has_error,
            'error_type': random.choice(['Monto incorrecto', 'Datos faltantes', 'SKU incorrecto']) if has_error else None
        })
    
    return pd.DataFrame(invoices)

def main():
    """Genera todos los datasets y los guarda"""
    print("Generando datos sintéticos...")
    
    # Generar datos maestros
    print("- Proveedores")
    suppliers_df = generate_suppliers()
    suppliers_df.to_csv('data/synthetic/suppliers.csv', index=False)
    
    print("- SKUs")
    skus_df = generate_skus()
    skus_df.to_csv('data/synthetic/skus.csv', index=False)
    
    print("- Analistas")
    analysts_df = generate_analysts()
    analysts_df.to_csv('data/synthetic/analysts.csv', index=False)
    
    # Generar transacciones
    print("- Órdenes de compra")
    orders_df, order_lines_df = generate_purchase_orders(skus_df, suppliers_df, analysts_df)
    orders_df.to_csv('data/synthetic/purchase_orders.csv', index=False)
    order_lines_df.to_csv('data/synthetic/order_lines.csv', index=False)
    
    print("- Facturas")
    invoices_df = generate_invoice_processing(orders_df, analysts_df)
    invoices_df.to_csv('data/synthetic/invoices.csv', index=False)
    
    # Resumen
    print("\n" + "="*60)
    print("DATOS GENERADOS EXITOSAMENTE")
    print("="*60)
    print(f"Proveedores: {len(suppliers_df)}")
    print(f"SKUs: {len(skus_df)}")
    print(f"Analistas: {len(analysts_df)}")
    print(f"Órdenes de compra: {len(orders_df)}")
    print(f"Líneas de orden: {len(order_lines_df)}")
    print(f"Facturas: {len(invoices_df)}")
    print("\nArchivos guardados en: data/synthetic/")
    print("="*60)

if __name__ == "__main__":
    main()
