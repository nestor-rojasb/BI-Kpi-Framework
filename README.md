# Business Intelligence KPI Framework

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Sistema modular de KPIs para análisis de operaciones B2B basado en datos de órdenes de compra, productos, proveedores e inventario.

## Propósito

Este framework implementa sistemas de KPIs probados en entornos de producción para medir:
- **Carga laboral** de equipos analíticos considerando complejidad, no solo volumen
- **Performance operacional** con métricas confiables al 100%
- **Eficiencia financiera** en operaciones de compra-venta

## Casos de Uso

- Necesidad de medidores confiables en contextos de inteligencia empresarial
- Análisis de Datos
- Distribuidores mayoristas  
- E-commerce B2B  
- Empresas de suministros industriales  
- Retail corporativo  
- Operaciones de procurement  
- Centros de procesamiento de pedidos  

## KPIs Implementados

### 1. Analyst Workload System
**Problema:** Medir carga de trabajo solo por volumen ignora la complejidad real.

**Solución:** Sistema de ponderación basado en:
- Cantidad de SKUs por transacción
- Categorización automática de complejidad
- Identificación de especialización por analista

**Aplicaciones:**
- Call centers (tickets por complejidad)
- Equipos de soporte técnico
- Analistas financieros
- Equipos de logística

### 2. Operational Processing Monitor (3-KPI System)
**Problema:** Sistemas con muchos KPIs generan dudas sobre confiabilidad de datos.

**Solución:** Solo 3 KPIs con garantía de 100% confiabilidad:
1. **Volumen:** Cantidad procesada
2. **Cumplimiento:** % de lo asignado completado
3. **Calidad:** % sin errores

**Aplicaciones:**
- Cuentas por pagar
- Registro de facturas
- Procesamiento de pedidos
- Back-office operations

### 3. Financial Performance Metrics
**Métricas derivadas:**
- Margen por orden de compra
- Valor promedio de transacción
- Concentración de proveedores
- Eficiencia en gestión de montos

## Inicio Rápido

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/bi-kpi-framework.git
cd bi-kpi-framework

# Instalar dependencias
pip install -r requirements.txt

# Generar datos sintéticos de ejemplo
python data/synthetic/generate_data.py

# Ejecutar análisis de ejemplo
jupyter notebook notebooks/01_analyst_workload.ipynb
```

## Estructura del Proyecto

```
bi-kpi-framework/
│
├── data/
│   ├── schema/              # Definiciones SQL de estructura de datos
│   └── synthetic/           # Generador de datos sintéticos
│
├── src/
│   ├── kpis/               # Implementación de KPIs
│   ├── core/               # Motor de cálculo y validación
│   └── viz/                # Visualizaciones y dashboards
│
├── notebooks/              # Análisis interactivos
├── docs/                   # Metodología y casos de uso
└── examples/               # Ejemplos por industria
```

## Tecnologías

- **Python 3.8+**
- **Pandas** - Manipulación de datos
- **NumPy** - Cálculos numéricos
- **Matplotlib/Plotly** - Visualizaciones
- **Jupyter** - Análisis interactivo

## Principios de Diseño

1. **Confiabilidad sobre Cantidad:** Pocos KPIs 100% confiables > Muchos KPIs dudosos
2. **Contexto sobre Volumen:** Complejidad importa tanto como cantidad
3. **Accionable:** Cada KPI debe impulsar decisiones específicas
4. **Generalizable:** Metodología aplicable a múltiples industrias

## Inspiración

Este framework surge de experiencia real implementando sistemas de KPIs en entornos de producción con transacciones diarias. Los sistemas aquí documentados han demostrado su valor en:
- Justificación de bonos por performance
- Optimización de distribución de carga laboral
- Detección de patrones de especialización
- Identificación de cuellos de botella operacionales

## Licencia

MIT License - Ver [LICENSE](LICENSE) para detalles


---

**Nota:** Los datos de ejemplo son completamente sintéticos. La metodología es aplicable a cualquier organización con operaciones B2B.
